import shutil
import os
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import SimpleITK as sitk
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="Mask.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz,FLAIR.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="input")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_bias_field_corr(N4)")
parser.add_argument("-s", "--shrink_factor", help="The shrink factor is used to reduce the size and complexity of the image. The N4 algorithm uses a multi-scale optimization approach to compute the bias field.", default="1")
args = parser.parse_args()

Mask_name="/"+args.mask#"/mask.nii.gz"
list_name_modality=args.list_modalities.split(",")
data_read_dir = args.read_dir
data_write_dir = args.write_dir
shrinkFactor =int(args.shrink_factor)#1

print("\n##### Inhomogeneity Correction(N4) #####\n")

class N4ITK_parameters():
    def __init__(self,r_paths, w_paths):
        self.paras = zip(r_paths, w_paths)
        self.pool = Pool(processes=cpu_count())

def N4ITK(input_path, output_path):
    try:
        raw_img_sitk = sitk.ReadImage(input_path, sitk.sitkFloat32)
        transformed = sitk.RescaleIntensity(raw_img_sitk, 0, 255)
        transformed = sitk.LiThreshold(transformed, 0, 1)
        head_mask = transformed

        inputImage = raw_img_sitk

        inputImage = sitk.Shrink(raw_img_sitk, [shrinkFactor] * inputImage.GetDimension())
        maskImage = sitk.Shrink(head_mask, [shrinkFactor] * inputImage.GetDimension())

        bias_corrector = sitk.N4BiasFieldCorrectionImageFilter()

        corrected = bias_corrector.Execute(inputImage, maskImage)

        log_bias_field = bias_corrector.GetLogBiasFieldAsImage(raw_img_sitk)
        corrected_image_full_resolution = raw_img_sitk / sitk.Exp(log_bias_field)

        sitk.WriteImage(corrected_image_full_resolution, output_path)

    except RuntimeError:
        return "\tFailed to apply N4 on: ", input_path
    return None

def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def unwarp_N4ITK(arg, **kwarg):
    return N4ITK(*arg, **kwarg)


create_folder(data_write_dir)



for session in tqdm(os.listdir(data_read_dir)):
    read_path=os.path.join(data_read_dir, session)
    write_path=os.path.join(data_write_dir, session)
    create_folder(write_path)

    data_read_paths=[]
    data_write_paths=[]
    for modality_item in list_name_modality:
        data_read_paths.append(os.path.join(read_path, modality_item))
        data_write_paths.append(os.path.join(write_path, modality_item))

    myN4ITK=N4ITK_parameters(data_read_paths, data_write_paths)
    print("")
    for modality_item in list_name_modality:
        print("Applying N4 on: ", modality_item)
    output_exep=myN4ITK.pool.map(unwarp_N4ITK, myN4ITK.paras)
    for item in output_exep:
        if item!= None:
            print(item)
    if (Mask_name != "/non" ):
        shutil.copyfile(read_path+Mask_name, write_path+Mask_name)

