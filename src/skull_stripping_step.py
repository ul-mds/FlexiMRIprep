import shutil
import os
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
parser.add_argument("-b", "--base_image", help="The first modality for making skull mask", default="FLAIR.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="output_reg")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_brain")
args = parser.parse_args()

mask_name="/"+args.mask
first_modality_make_mask=args.base_image
list_name_modality=args.list_modalities.split(",")
data_input_dir = args.read_dir
data_output_dir = args.write_dir


print("\n##### Skull Stripping #####\n")
def betbyfsl(input_path, output_path, frac="0.5",mask_gen="make"):
    if mask_gen=="make":
        command = ["bet", input_path, output_path, "-R", "-f", frac, "-g", "0","-m"]
    else:
        command = ["fslmaths", input_path,"-mul",mask_gen, output_path,]
    subprocess.call(command)
    return


def unwarp_skull_strip(arg, **kwarg):
    return skull_strip(*arg, **kwarg)


def skull_strip(input_path, output_path,mask_gen, frac="0.4"):
    print("Applying Skull stripping on :", input_path)
    try:
        betbyfsl(input_path, output_path, frac,mask_gen)
    except RuntimeError:
        print("\tFailed to apply Skull stripping on: ", input_path)

    return
def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


create_folder(data_output_dir)


for session in tqdm(os.listdir(data_input_dir)):
    input_path=os.path.join(data_input_dir, session)
    output_path=os.path.join(data_output_dir, session)
    create_folder(output_path)

    data_input_path=[]
    data_output_path=[]
    if(first_modality_make_mask!= None):
        data_input_path.append(os.path.join(input_path, first_modality_make_mask))
        data_output_path.append(os.path.join(output_path, first_modality_make_mask))
        paras = zip(data_input_path, data_output_path,["make"])
        pool = Pool(processes=cpu_count())
        pool.map(unwarp_skull_strip, paras)

    data_src_paths=[]
    data_dst_paths=[]
    for modality_item in list_name_modality:
        data_src_paths.append(os.path.join(input_path, modality_item))
        data_dst_paths.append(os.path.join(output_path, modality_item))
    if data_output_path!=[]:
        paras = zip(data_src_paths, data_dst_paths,[os.path.splitext(os.path.splitext(data_output_path[0])[0])[0]+"_mask.nii.gz"]* len(data_dst_paths))
    else:
        paras = zip(data_src_paths, data_dst_paths, ["make"]* len(data_dst_paths))
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_skull_strip, paras)
    if (mask_name != "/non" ):
        shutil.copyfile(input_path+mask_name, output_path+mask_name)
