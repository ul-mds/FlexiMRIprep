#import shutil
import pickle
import os, shutil
import subprocess
#from distutils.command.install import value
#from multiprocessing import Pool, cpu_count
#import csv
#from numpy.distutils.conv_template import header
#from pydicom.errors import InvalidDicomError
#from tqdm import tqdm
import argparse
#from pydicom import dcmread
#import nighres
#from fcmeans import FCM
#import nibabel as nib
#import numpy as np
import pandas as pd
parser = argparse.ArgumentParser()

#parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
#parser.add_argument("-dts", "--DICOM_Tags_select", help="The list of DICOM tags to read(set all for reading 'all' tags!)", default="Protocol Name,Series Description")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="output")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output")
parser.add_argument("-c", "--input_file_name", help="The name of output file(csv file & pkl data file)", default="list_dicom_contain")
parser.add_argument("-f", "--file_name_nifti", help="filename (%a=antenna (coil) name, %b=basename, %c=comments, %d=description, %e=echo number,"+
                                                    " %f=folder name, %g=accession number, %i=ID of patient, %j=seriesInstanceUID,%k=studyInstanceUID, %m=manufacturer,"+
                                                    " %n=name of patient, %o=mediaObjectInstanceUID, %p=protocol, %r=instance number, %s=series number, %t=time, %u=acquisition "+
                                                    "number,%v=vendor, %x=study ID; %z=sequence name; default '%p_%i_%x_%t_%s')", default="%p_%i_%x_%t_%s")
parser.add_argument("-b", "--base_image", help="Select the modality for Co-Registration", default="FLAIR.nii.gz")
parser.add_argument("-pcs", "--path_csv_scan", help="The path of the csv file", default="generated")

args = parser.parse_args()

data_input_dir = args.read_dir
data_output_dir = args.write_dir
input_file_name = args.input_file_name
file_name_nifti = args.file_name_nifti
base_image_name = args.base_image
path_csv_scan=args.path_csv_scan
def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def create_temp_dir(path):
    if not os.path.isdir(path):
        os.makedirs(path)
    else:
        shutil.rmtree(path)
        os.makedirs(path)

def remove_temp_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)

def make_dir_rename_files(files,file_name,source_dir):
    for file in files:
        if file.endswith('.nii.gz'):
            base_name = file[:-7]
            new_folder = os.path.join(source_dir, base_name)
            os.makedirs(new_folder, exist_ok=True)
            mri_file_path = os.path.join(source_dir, file)
            new_mri_file_path = os.path.join(new_folder, file_name)
            shutil.move(mri_file_path, new_mri_file_path)
            json_file_name = base_name + '.json'
            json_file_path = os.path.join(source_dir, json_file_name)
            if os.path.exists(json_file_path):
                new_json_file_path = os.path.join(new_folder, 'FLAIR.json')
                shutil.move(json_file_path, new_json_file_path)

def run_convert(file_name_nifti,data_output_dir,path_dicom):
    run_subprocess = subprocess.getstatusoutput(
        'dcm2niix -f ' + file_name_nifti + ' -o ' + data_output_dir + ' -9 -z  y ' + path_dicom)
    if run_subprocess[0] == 0:
        print(run_subprocess[1])
    else:
        print('Failed to apply Converting DICOM format to NIFTI file on: {}'.format(run_subprocess[1]))

if path_csv_scan=="generated":
    with open(data_input_dir + '/' + input_file_name + '.pkl', 'rb') as f:
        data_pkl = pickle.load(f)

    df_user_selected = pd.read_csv(data_input_dir + "/" + input_file_name + ".csv")
else:
    with open(path_csv_scan + '/' + input_file_name + '.pkl', 'rb') as f:
        data_pkl = pickle.load(f)

    df_user_selected = pd.read_csv(path_csv_scan + "/" + input_file_name + ".csv")
create_folder(data_output_dir)
while len(df_user_selected) > 0:
    path_dicom = df_user_selected['Path_dicom_file'][0]
    file_name_dicom = df_user_selected['File_name'][0]
    S_I_UID = df_user_selected['Series Instance UID'][0]
    list_same_path = [0]
    for index in range(1, len(df_user_selected['Path_dicom_file'])):
        if df_user_selected['Path_dicom_file'][index] == path_dicom:
            list_same_path.append(index)
    full_list_S_I_UID = data_pkl.loc[data_pkl['Series Instance UID'] == S_I_UID]
    for index in range(1, len(list_same_path)):
        full_list_S_I_UID_add = data_pkl.loc[
            data_pkl['Series Instance UID'] == df_user_selected['Series Instance UID'][list_same_path[index]]]
        full_list_S_I_UID = pd.concat([full_list_S_I_UID, full_list_S_I_UID_add])

    full_list_dir = data_pkl.loc[data_pkl['Path_dicom_file'] == path_dicom]
    # full_list_files = data_pkl.loc[data_pkl['Path_dicom_file'] == path_dicom]

    if len(full_list_S_I_UID) == len(full_list_dir):
       # run_subprocess = subprocess.getstatusoutput(
       #     'dcm2niix -f ' + file_name_nifti + ' -o ' + data_output_dir + ' -9 -z  y ' + path_dicom)
        run_convert(file_name_nifti, data_output_dir, path_dicom)
        #if run_subprocess[0] == 0:
        #    print(run_subprocess[1])
        #else:
        #    print('Failed to apply Registration on: {}'.format(run_subprocess[1]))
    else:
        create_temp_dir(data_output_dir + '/temp')
        full_list_S_I_UID = full_list_S_I_UID.reset_index(drop=True)
        for index in range(len(full_list_S_I_UID)):
            shutil.copyfile(full_list_S_I_UID['Path_dicom_file'][index] + "/" + full_list_S_I_UID['File_name'][index],
                            data_output_dir + '/temp/' + full_list_S_I_UID['File_name'][index])
        run_convert(file_name_nifti, data_output_dir, data_output_dir + '/temp')
        remove_temp_dir(data_output_dir + '/temp')

    df_user_selected = df_user_selected.drop(list_same_path)
    df_user_selected = df_user_selected.reset_index(drop=True)
files = os.listdir(data_output_dir)
make_dir_rename_files(files, base_image_name, data_output_dir)

print("Scan is done")
