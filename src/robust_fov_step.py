import shutil
import os
import subprocess
from multiprocessing import Pool, cpu_count
from tqdm import tqdm
import argparse

parser = argparse.ArgumentParser()

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="mask.nii.gz")
parser.add_argument("-d", "--dimension", help="The number of dimension (kept for compatibility)", default="3")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="FLAIR.nii.gz")
parser.add_argument("-i", "--read_dir", help="Input path of the patient directory", default="output_reg")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output_robustfov")
parser.add_argument(
    "--robustfov_bin",
    help="Path/name of FSL robustfov binary (must be in PATH if only name is given)",
    default="robustfov",
)
args = parser.parse_args()

mask_name = "/" + args.mask
list_name_modality = args.list_modalities.split(",")
data_input_dir = args.read_dir
data_output_dir = args.write_dir
dimension = args.dimension  # kept for compatibility with your template
robustfov_bin = args.robustfov_bin

print("\n##### Applying Robust FOV (FSL robustfov) #####\n")


def run_robustfov(input_path, output_path, robustfov_bin):
    """
    Applies FSL robustfov to crop the FOV.
    Command: robustfov -i <input> -r <output>
    """
    command = [robustfov_bin, "-i", input_path, "-r", output_path]
    print(command)
    subprocess.run(command, check=True)
    return


def unwarp_robustfov(arg, **kwarg):
    return robust_fov(*arg, **kwarg)


def robust_fov(input_path, output_path, robustfov_bin, di="3"):
    # 'di' kept to preserve your call signature; not used by robustfov
    print("Applying Robust FOV on :", input_path)
    try:
        run_robustfov(input_path, output_path, robustfov_bin)
    except subprocess.CalledProcessError:
        print("\tFailed to apply Robust FOV on: ", input_path)
    except FileNotFoundError:
        print("\trobustfov not found. Provide --robustfov_bin or ensure FSL is in PATH.")
    return


def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)


create_folder(data_output_dir)

sessions = [
    name
    for name in os.listdir(data_input_dir)
    if os.path.isdir(os.path.join(data_input_dir, name))
]

for session in tqdm(sessions):
    input_path = os.path.join(data_input_dir, session)
    output_path = os.path.join(data_output_dir, session)
    create_folder(output_path)

    data_src_paths = []
    data_dst_paths = []

    for modality_item in list_name_modality:
        modality_item = modality_item.strip()
        print("******" + modality_item)
        data_src_paths.append(os.path.join(input_path, modality_item))
        data_dst_paths.append(os.path.join(output_path, modality_item))

    # Keep the same "paras" structure style you use
    # Each tuple must match robust_fov signature: (input_path, output_path, robustfov_bin, di)
    paras = zip(data_src_paths, data_dst_paths, [robustfov_bin] * len(data_src_paths), ["3"] * len(data_src_paths))

    pool = Pool(processes=cpu_count())
    pool.map(unwarp_robustfov, paras)
    pool.close()
    pool.join()

    if mask_name != "/non":
        src_mask = input_path + mask_name
        dst_mask = output_path + mask_name
        if os.path.isfile(src_mask):
            shutil.copyfile(src_mask, dst_mask)
        else:
            print("\tMask not found, skipped:", src_mask)
