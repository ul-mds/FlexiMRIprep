#import shutil
import pickle
import os
#import subprocess
#from distutils.command.install import value
#from multiprocessing import Pool, cpu_count
#import csv
#from numpy.distutils.conv_template import header
from pydicom.errors import InvalidDicomError
#from tqdm import tqdm
import argparse
from pydicom import dcmread
#import nighres
#from fcmeans import FCM
#import nibabel as nib
#import numpy as np
import pandas as pd
parser = argparse.ArgumentParser()

#parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
parser.add_argument("-d", "--DICOM_Tags_select", help="The list of DICOM tags to read(set all for reading 'all' tags!)")#, default="Protocol Name,Series Description")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="output_reg")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_brain")
parser.add_argument("-c", "--output_file_name", help="The name of output file(csv file & pkl data file)", default="list_dicom_contain")
#parser.add_argument("-max", "--max_iterations", help="The number of maximum iterations", default=200)
args = parser.parse_args()

#mask_name="/"+args.mask

DICOM_Tags_select=args.DICOM_Tags_select.split(",")
data_input_dir = args.read_dir
data_output_dir = args.write_dir
output_file_name=args.output_file_name
#number_clusters=args.number_clusters



print("\n##### Scan DICOM files(MRI) #####\n")
#def betbyfsl(input_path, output_path, max_iterat=100,number_clusters=3):
#    dst_path_split = os.path.split(os.path.abspath(input_path))
#    file_name = dst_path_split[1]
#    file_name = file_name.replace('.gz', '')
#    file_name = file_name.replace('.nii', '')
#    dicom_files=os.listdir(input_path)
#    for file in dicom_files:
#        try:
#            ds = dcmread(file)
#            for element in ds:
#                print(element)
#        except InvalidDicomError:
#            pass


#    return


#def unwarp_skull_strip(arg, **kwarg):
#    return skull_strip(*arg, **kwarg)


#def skull_strip(input_path, output_path,max_iterat,number_clusters):
#    print("Reading data from DICOM on :", input_path)
#    try:
#        betbyfsl(input_path, output_path, max_iterat,number_clusters)
#    except RuntimeError:
#        print("\tFailed to Read data from DICOM on: ", input_path)
#
#    return
def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


create_folder(data_output_dir)
#csv_list=[]
#csv_header_flag=True

#csv_all_tags_header=[]
csv_all_tags=[]#pd.DataFrame(columns=csv_all_tags_header)
DICOM_Tags_select.append('Series Instance UID')
DICOM_Tags_select_lower=[x.lower() for x in DICOM_Tags_select]
#if DICOM_Tags_select[0]!="all":
#    for item in DICOM_Tags_select:
#        csv_header.append(item)
dst_path_split = os.path.split(os.path.abspath(data_input_dir))
file_name = dst_path_split[1]
file_name = file_name.replace('.gz', '')
file_name = file_name.replace('.nii', '')
for dirpath, dirnames, filenames in os.walk(data_input_dir):
    for file in filenames:
        full_path = os.path.join(dirpath, file)
        try:
            ds = dcmread(full_path)
            #row= {}
            row = []
            #csv_all_tags[""]
            row.append(file)
            #row.append(dirpath)
            row.append(dirpath)
            for user_site in DICOM_Tags_select_lower:
                #row.append(element.value)
                #if csv_header_flag:
                #    csv_all_tags_header.append(element.name)
                #row[element.name.lower()]=element.value
                item_flag=True
                for element in ds:
                    if user_site.lower() == element.name.lower():
                        row.append(element.value)
                        item_flag = False
                        break
                if item_flag:
                    row.append('not_available_tag')

                    #else:
                    #    row.append('not_available_tag')
            #    if DICOM_Tags_select[0] == "all":
            #        if len(csv_header)==2:
            #            csv_header.append(element.name)
            #        row.append(element.value)
            #    else:
            #        if element.name.lower() in DICOM_Tags_select:
            #            row.append(element.value)
            #if len(row)!=len(csv_header):
            #    print("Unable to find all the tags in "+full_path)
            #csv_list.append(row)
            csv_all_tags.append(row)
            #csv_header_flag=False
        except InvalidDicomError:
            pass
header_csv_user=[]
header_csv_user.append('File_name')
header_csv_user.append('Path_dicom_file')
for item in DICOM_Tags_select:
    header_csv_user.append(item)

df_user = pd.DataFrame(csv_all_tags)
#if len(row)==len(csv_header):
df_user.columns = header_csv_user

output = open(data_output_dir+'/'+output_file_name+'.pkl', 'wb')
pickle.dump(df_user, output)
output.close()

df_unique = df_user.drop_duplicates(subset='Series Instance UID', keep='first')
df_unique.to_csv(data_output_dir+"/"+output_file_name+".csv", index_label='Index4accessing')

######################save all tags
"""
keys = set()
for row in csv_all_tags:
    keys.update(row.keys())
with open(data_input_dir+'/output.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=keys,delimiter='\t', extrasaction='ignore')

    writer.writeheader()

    for row in csv_all_tags:
        writer.writerow({key: row.get(key, '') for key in keys})
"""
print("Scan is done")

"""for session in tqdm(os.listdir(data_input_dir)):
    input_path=os.path.join(data_input_dir, session)
    output_path=os.path.join(data_output_dir, session)
    create_folder(output_path)

    data_src_paths=[]
    data_dst_paths=[]
    for modality_item in list_name_modality:
        data_src_paths.append(os.path.join(input_path, modality_item))
        data_dst_paths.append(output_path)
    paras = zip(data_src_paths, data_dst_paths,[max_iterations],[number_clusters])
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_skull_strip, paras)

    pool.map(unwarp_skull_strip, paras)
    if (mask_name != "/non" ):
        shutil.copyfile(input_path+mask_name, output_path+mask_name)"""
