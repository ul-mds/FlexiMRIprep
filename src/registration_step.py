import os
import subprocess
#import matplotlib.pyplot as plt
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="Mask.nii.gz")
parser.add_argument("-b", "--base_image", help="Select the modality for Co-Registration", default="FLAIR.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="input")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_reg")
#parser.add_argument("-p", "--parent_dir", help="The path of the main directory", default=os.path.join(os.getcwd(), "data"))
parser.add_argument("-s", "--shrink_factor", help="The shrink factor is used to reduce the size and complexity of the image. The N4 algorithm uses a multi-scale optimization approach to compute the bias field.", default=1)
args = parser.parse_args()

Mask_name="/"+args.mask#"/mask.nii.gz"
list_name_modality=args.list_modalities.split(",")#["T1W.nii.gz","T1WKS.nii.gz","T2W.nii.gz","FLAIR.nii.gz"]
#parent_dir =args.parent_dir #os.getcwd()#os.path.dirname(os.getcwd())
#data_dir =args.parent_dir# os.path.join(parent_dir, "data")
data_input_dir = args.read_dir#os.path.join(data_dir,args.read_dir)# "output_brain")
data_output_dir =args.write_dir#os.path.join(data_dir,args.write_dir) #"output_bias_field_corr(N4)")
base_image_name="/"+args.base_image
shrinkFactor = args.shrink_factor#1

class registration_parameters():
    def __init__(self,input_path, base_image_name,output_path,ref_path):
        self.paras = zip([input_path + base_image_name], [output_path + base_image_name],
                [ref_path],[output_path])
        self.pool = Pool(processes=cpu_count())
#from fsl.data.image import Image
#base_image_name="/FLAIR.nii.gz"
#Mask_name="/mask.nii.gz"
#list_name_modality=["T1W.nii.gz","T1WKS.nii.gz","T2W.nii.gz"]
#parent_dir =os.getcwd()# os.path.dirname(os.getcwd())
#data_dir = os.path.join(parent_dir, "data")
#data_input_dir = os.path.join(data_dir, "input")
#data_output_dir = os.path.join(data_dir, "output_reg")


ref_path = os.path.join("./src", "Template", "icbm_avg_152_t1_tal_lin.nii.gz")

print("\n##### Registration #####\n")
def registration(src_path, dst_path, ref_path,save_path_affine,mode="modality",thr=0.9):
    if(mode=="modality"):
        if save_path_affine!=None:
            command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
                   "-bins", "256", "-cost", "corratio", "-searchrx", "-180", "180",
                   "-searchry", "-180", "180", "-searchrz", "-180", "180",
                    #"-dof", "12",
                   "-datatype", "float","-omat",save_path_affine+"/image2MNI_affine.mat"]
            #command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
            #       "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
            #       "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
            #       "-interp", "spline","-datatype", "float","-omat",save_path_affine+"/image2MNI_affine.mat"]
        else:
            command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
                       "-bins", "256", "-cost", "corratio", "-searchrx", "-180", "180",
                       "-searchry", "-180", "180", "-searchrz", "-180", "180",
                        #"-dof", "12",
                       "-datatype", "float"]
            #command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,
            #           "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
            #           "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
            #           "-interp", "spline", "-datatype", "float"]
    if (mode == "mask"):
        command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path,"-applyxfm","-init",save_path_affine+"/image2MNI_affine.mat"]#,
        #command = ["flirt", "-in", src_path, "-ref", ref_path, "-out", dst_path]
        subprocess.call(command, stdout=open(os.devnull, "r"),
                        stderr=subprocess.STDOUT)
        command = ["fslmaths", dst_path, "-thr", str(thr), "-bin", dst_path]  # ,
        #           "-bins", "256", "-cost", "corratio", "-searchrx", "0", "0",
        #           "-searchry", "0", "0", "-searchrz", "0", "0", "-dof", "12",
        #           "-interp", "spline"]
        #flirt -in standard_mask -ref highres -applyxfm -init standard2highres.mat -out highres_mask
    subprocess.call(command, stdout=open(os.devnull, "r"),
                    stderr=subprocess.STDOUT)
    return



def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)



def unwarp_main(arg, **kwarg):
    return main(*arg, **kwarg)


def main(input_path, output_path, reference_path,save_path_affine,mode="modality"):
    print("Applying Registration on: ", input_path)
    try:
        command = ["fslreorient2std", input_path, output_path]
        subprocess.call(command)
        registration(input_path, output_path, reference_path,save_path_affine,mode)
    except RuntimeError:
        print("\tFalied to apply Registration on: ", input_path)

    return



create_folder(data_output_dir)



data_src_paths, data_dst_paths = [], []
for session in tqdm([ name for name in os.listdir(data_input_dir) if os.path.isdir(os.path.join(data_input_dir, name)) ]):
    input_path=os.path.join(data_input_dir, session)
    output_path=os.path.join(data_output_dir, session)
    create_folder(output_path)
    paras = zip([input_path + base_image_name], [output_path + base_image_name],
                [ref_path],[output_path] )
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_main, paras)
    data_input_paths=[]
    data_output_paths=[]
    for modality_item in list_name_modality:
        data_input_paths.append(os.path.join(input_path, modality_item))
        data_output_paths.append(os.path.join(output_path, modality_item))
    paras = zip(data_input_paths, data_output_paths,
                [output_path + base_image_name] * len(data_input_paths),[None] * len(data_input_paths))
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_main, paras)
    if(Mask_name != "/non" ):
        paras = zip([input_path+Mask_name], [output_path+Mask_name],
                    [output_path + base_image_name] ,[output_path],["mask"])#dst_path + T1W_name
        pool = Pool(processes=cpu_count())
        pool.map(unwarp_main, paras)
