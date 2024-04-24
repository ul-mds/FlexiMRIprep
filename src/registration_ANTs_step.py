import os
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="Mask.nii.gz")
parser.add_argument("-b", "--base_image", help="Select the modality for Co-Registration", default="FLAIR.nii.gz")
parser.add_argument("-r", "--remove", help="Remove the extra files(only with a very big size!).", default="0")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="input")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_reg")
parser.add_argument("-s", "--shrink_factor", help="The shrink factor is used to reduce the size and complexity of the image. The N4 algorithm uses a multi-scale optimization approach to compute the bias field.", default=1)
args = parser.parse_args()

Mask_name="/"+args.mask
list_name_modality=args.list_modalities.split(",")
data_input_dir = args.read_dir
data_output_dir =args.write_dir
base_image_name="/"+args.base_image
shrinkFactor = args.shrink_factor#1
remove_active=args.remove
class registration_parameters():
    def __init__(self,input_path, base_image_name,output_path,ref_path):
        self.paras = zip([input_path + base_image_name], [output_path + base_image_name],
                [ref_path],[output_path])
        self.pool = Pool(processes=cpu_count())
def remove_file(path_file):
    if remove_active=="1" and os.path.exists(path_file):
       os.remove(path_file)
    else:
       print(path_file+" has a very big size!")

ref_path = os.path.join("./src", "Template", "mni_icbm152_t2_tal_nlin_asym_09c.nii")
print("\n##### Registration #####\n")
def registration(src_path, dst_path, ref_path,save_path_affine,src_path_mask, dst_path_mask,mode="modality",thr=0.9):
    file_name=""
    dis_path_only=""
    fl=False
    for index in range(len(dst_path)-1,-1,-1):
        if dst_path[index]!='/' and fl==False:
       	    file_name=dst_path[index]+file_name
        else:
       	    fl=True
       	    dis_path_only=dst_path[index]+dis_path_only
    dst_path_split=[dis_path_only,file_name]
    file_name=dst_path_split[1]
    file_name=file_name.replace('.gz', '')
    file_name=file_name.replace('.nii', '')
    dst_path1=dst_path_split[0]+file_name
    create_folder(dis_path_only)
    dst_path2=dst_path_split[0]+dst_path_split[1]
    dst_path3=dst_path_split[0]+"InverseWarped_"+dst_path_split[1]
    if(mode=="base_image"):
        command=["antsRegistration","--verbose", "0","--dimensionality", "3","--float", "0", "--collapse-output-transforms", "1", "--output",
        "[",dst_path1,",",dst_path2,",",dst_path3,"]","--interpolation","Linear", "--use-histogram-matching","0", "--winsorize-image-intensities","[","0.005",",","0.995","]",
        "--initial-moving-transform","[",ref_path,",",src_path,",","1","]", "--transform","SyN[ 0.1,3,0 ]","--metric","MI[",
        ref_path,",", src_path,",","1",",","32","]", "--convergence", "[ 500x400x70x30,1e-6,10 ]", "--shrink-factors", "8x4x2x1", "--smoothing-sigmas", "3x2x1x0vox"]
        subprocess.call(command, stdout=open(os.devnull, "r"),
                        stderr=subprocess.STDOUT)
        if(Mask_name == "/non" ):
            remove_file(dst_path1+"1Warp.nii.gz")
            remove_file(dst_path1+"1InverseWarp.nii.gz")
            remove_file(dst_path3)

    if (mode == "mask"):
        command = ["antsApplyTransforms","--dimensionality","3","--input-image-type","0","--input",src_path_mask,"--reference-image", ref_path,
        "--output",  dst_path_mask,"--interpolation","Linear","--output-data-type","float","--transform",dst_path1+"1Warp.nii.gz","--transform",dst_path1+"0GenericAffine.mat","--default-value","0","--float","0"]#,
        subprocess.call(command, stdout=open(os.devnull, "r"),
                        stderr=subprocess.STDOUT)
        remove_file(dst_path1+"1Warp.nii.gz")
        remove_file(dst_path1+"1InverseWarp.nii.gz")
        remove_file(dst_path3)
    return



def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)



def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)


def main(input_path, output_path, reference_path,save_path_affine,src_path_mask, dst_path_mask,mode="modality"):
    print("Applying Registration on: ", input_path)
    try:
        registration(input_path, output_path, reference_path,save_path_affine,src_path_mask, dst_path_mask,mode)
    except RuntimeError:
        print("\tFalied to apply Registration on: ", input_path)

    return



create_folder(data_output_dir)



data_src_paths, data_dst_paths = [], []
for session in tqdm(os.listdir(data_input_dir)):
    input_path=os.path.join(data_input_dir, session)
    output_path=os.path.join(data_output_dir, session)
    paras = zip([input_path + base_image_name], [output_path + base_image_name],
                [ref_path],[output_path],[None],[None] ,["base_image"])
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_main, paras)
    data_input_paths=[]
    data_output_paths=[]
    if(len(list_name_modality)==1 and list_name_modality[0]!=""):
        for modality_item in list_name_modality:
            data_input_paths.append(os.path.join(input_path, modality_item))
            data_output_paths.append(os.path.join(output_path, modality_item))
        paras = zip(data_input_paths, data_output_paths,
                    [output_path + base_image_name] * len(data_input_paths),[None] * len(data_input_paths))
        pool = Pool(processes=cpu_count())
        pool.map(unwarp_main, paras)
    if(Mask_name != "/non" ):
        paras = zip([input_path + base_image_name], [output_path + base_image_name],
                    [output_path + base_image_name] ,[output_path],[input_path+Mask_name], [output_path+Mask_name],["mask"])#dst_path + T1W_name
        pool = Pool(processes=cpu_count())
        pool.map(unwarp_main, paras)

