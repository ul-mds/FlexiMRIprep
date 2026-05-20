import shutil
import os
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse
#import nighres
from fcmeans import FCM
import nibabel as nib
import numpy as np
parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")
parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="output_reg")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_brain")
parser.add_argument("-c", "--number_clusters", help="The number of clusters", default=3)
parser.add_argument("-max", "--max_iterations", help="The number of maximum iterations", default=200)
args = parser.parse_args()

mask_name="/"+args.mask

list_name_modality=args.list_modalities.split(",")
data_input_dir = args.read_dir
data_output_dir = args.write_dir
max_iterations=args.max_iterations
number_clusters=args.number_clusters



print("\n##### fuzzy-cmeans segmentation #####\n")
def betbyfcmeans(input_path, output_path, max_iterat=100,number_clusters=3):
    dst_path_split = os.path.split(os.path.abspath(input_path))
    file_name = dst_path_split[1]
    file_name = file_name.replace('.gz', '')
    file_name = file_name.replace('.nii', '')

    #nighres.segmentation.fuzzy_cmeans(input_path,
    #                                  save_data=True,
    #                                  output_dir=output_path,
    #                                  file_name=file_name, max_iterations=max_iterat, overwrite=False, clusters=number_clusters)
    mri_brain = nib.load(input_path)
    MRI_brain = mri_brain.get_fdata()

    MRI_brain_flat = MRI_brain.reshape(-1)
    non_zero_mask = MRI_brain_flat > 0
    MRI_brain_non_zero = MRI_brain_flat[non_zero_mask].reshape(-1, 1)  # Make it a 2D array with shape (n_samples, 1)
    fcm = FCM(n_clusters=number_clusters, max_iter=max_iterat)
    fcm.fit(MRI_brain_non_zero)
    memberships_non_zero = fcm.u
    memberships = np.zeros((MRI_brain_flat.size, fcm.n_clusters))
    memberships[non_zero_mask] = memberships_non_zero
    memberships_reshaped = memberships.reshape(MRI_brain.shape + (fcm.n_clusters,))
    for i in range(fcm.n_clusters):
        membership_map = memberships_reshaped[..., i]
        membership_img = nib.Nifti1Image(membership_map, mri_brain.affine)
        nib.save(membership_img, output_path+'/'+ file_name+f'rfcm-mem-cluster{i + 1}.nii.gz')

    cluster_indices = np.argmax(memberships, axis=1)
    cluster_assignments = np.zeros(MRI_brain_flat.size)
    cluster_assignments[non_zero_mask] = cluster_indices[
                                             non_zero_mask] + 1  # Adding 1 to shift values from (0,1,2) to (1,2,3)
    cluster_assignments_reshaped = cluster_assignments.reshape(MRI_brain.shape)
    cluster_assignments_img = nib.Nifti1Image(cluster_assignments_reshaped, mri_brain.affine)
    nib.save(cluster_assignments_img, output_path+'/'+ file_name+ 'rfcm-cluster-assignments.nii.gz')
    return


def unwarp_fuzzy_cmeans(arg, **kwarg):
    return fuzzy_cmeans(*arg, **kwarg)


def fuzzy_cmeans(input_path, output_path,max_iterat,number_clusters):
    print("Applying fuzzy-cmeans segmentation on :", input_path)
    try:
        betbyfcmeans(input_path, output_path, max_iterat,number_clusters)
    except RuntimeError:
        print("\tFailed to apply fuzzy-cmeans segmentation on: ", input_path)

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
        data_src_paths.append(os.path.join(input_path, modality_item))
        data_dst_paths.append(output_path)
    paras = zip(data_src_paths, data_dst_paths,[max_iterations],[number_clusters])
    pool = Pool(processes=cpu_count())
    pool.map(unwarp_fuzzy_cmeans, paras)

    pool.map(unwarp_fuzzy_cmeans, paras)
    if (mask_name != "/non" ):
        shutil.copyfile(input_path+mask_name, output_path+mask_name)
