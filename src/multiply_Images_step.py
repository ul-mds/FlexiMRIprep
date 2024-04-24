import shutil
import os
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
parser.add_argument("-d", "--dimension", help="The number of dimension", default="3")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="output_reg")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_brain")
args = parser.parse_args()

mask_name="/"+args.mask
list_name_modality=args.list_modalities.split(",")
data_input_dir = args.read_dir
data_output_dir = args.write_dir
dimension = args.dimension
ref_path = os.path.join("./src", "Template", "mni_icbm152_wm_tal_nlin_asym_09c.nii")

print("\n##### Multiplying Images #####\n")
def betbyfsl(input_path, output_path,ref_path, di="0.5",mask_gen="make"):
    command = ["MultiplyImages",di, input_path, ref_path, output_path]
    print(command)
    subprocess.call(command)
    return


def unwarp_skull_strip(arg, **kwarg):
    return skull_strip(*arg, **kwarg)


def skull_strip(input_path, output_path,ref_path, di="3"):
    print("Applying Multiplying Images on :", input_path)
    try:
        betbyfsl(input_path, output_path,ref_path, di)
    except RuntimeError:
        print("\tFailed to apply Multiplying Images on: ", input_path)

    return
def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


create_folder(data_output_dir)


for session in tqdm(os.listdir(data_input_dir)):
    input_path=os.path.join(data_input_dir, session)
    output_path=os.path.join(data_output_dir, session)
    create_folder(output_path)

    data_src_paths=[]
    data_dst_paths=[]
    for modality_item in list_name_modality:
        print("******"+modality_item)
        data_src_paths.append(os.path.join(input_path, modality_item))
        data_dst_paths.append(os.path.join(output_path, modality_item))
    paras = zip(data_src_paths, data_dst_paths,[ref_path],[dimension])
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_skull_strip, paras)

    if (mask_name != "/non" ):
        shutil.copyfile(input_path+mask_name, output_path+mask_name)
