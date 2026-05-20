# FlexiMRIprep

This pipeline provides a versatile framework for applying preprocessing methods to MRI images. With this pipeline, you can easily apply various stages of preprocessing to a large number of MRI images.

## Table of Contents

- [Hardware Requirements](#hardware-requirements)
- [Installation](#installation)
- [Usage](#usage)
- [File Structure](#file-structure)
- [License](#license)

## Hardware Requirements

This pipeline does not require a graphics card or CUDA!

## Installation

- Docker installed
- No local Python environment required (everything runs inside containers)

## Usage

To use the preprocessing pipeline, run the `main.py` script with the appropriate options:

```bash
usage: main.py [-h] [-m MASK] [-b BASE_IMAGE] [-lm LIST_MODALITIES]
               [-i READ_DIR] [-o WRITE_DIR] [-s1 REGISTRATION_FSL_STEP] 
               [-s2 REGISTRATION_ANTS_STEP] [-s3 SKULL_STRIPPING] 
               [-s4 BIAS_CORRECTION_N4_STEP] [-s5 MULTIPLYING_STEP] 
               [-s6 FUZZY_CMEANS_SEGMENTATION_STEP] [-s7 SCAN_DICOM_STEP] 
               [-s8 CONVERT_DICOM2NIFTI_STEP] [-s9 RIGID_ANTS_STEP] [-sa AFFINE_ANTS_STEP]
               [-sb ROBUST_FOV_STEP] [-p PARENT_DIR] [-s STEPS]

options:
  -h, --help            show this help message and exit
  -m MASK, --mask MASK  name of the mask file(.nii.gz)
  -b BASE_IMAGE, --base_image BASE_IMAGE
                        The first modality for making skull mask and Co-Registration
  -lm LIST_MODALITIES, --list_modalities LIST_MODALITIES
                        The list of modalities
  -i READ_DIR, --read_dir READ_DIR
                        ّInput path of the patient directory
  -o WRITE_DIR, --write_dir WRITE_DIR
                        Output path of the patient directory
  -s1 REGISTRATION_FSL_STEP, --registration_FSL_step REGISTRATION_FSL_STEP
                        change the parameters for registration step(for example '-s:1+-p1:mypath')
  -s2 REGISTRATION_ANTS_STEP, --registration_ANTS_step REGISTRATION_ANTS_STEP
                        change the parameters for registration step(for example '-s:1')
  -s3 SKULL_STRIPPING, --skull_stripping SKULL_STRIPPING
                        change the parameters for skull stripping(for example '-s:1')
  -s4 BIAS_CORRECTION_N4_STEP, --bias_correction_n4_step BIAS_CORRECTION_N4_STEP
                        change the parameters for bias correction(for example '-f:0.4')
  -s5 MULTIPLYING_STEP, --Multiplying_step MULTIPLYING_STEP
                        Multiplying Images(for example '-d:3')
  -s6 FUZZY_CMEANS_SEGMENTATION_STEP, --fuzzy_cmeans_segmentation_step FUZZY_CMEANS_SEGMENTATION_STEP
                        fuzzy-cmeans segmentation MRI files(for example '-d:3')
  -s7 SCAN_DICOM_STEP, --scan_dicom_step SCAN_DICOM_STEP
                        scan dicom files(for example '-d:3')
  -s8 CONVERT_DICOM2NIFTI_STEP, --convert_dicom2nifti_step CONVERT_DICOM2NIFTI_STEP
                        convert dicom files to nifti files(for example '-d:3')
  -s9 RIGID_ANTS_STEP, --rigid_ANTS_step RIGID_ANTS_STEP
                        change the parameters for rigid step(for example '-s:1')
  -sa AFFINE_ANTS_STEP, --affine_ANTS_step AFFINE_ANTS_STEP
                        change the parameters for affine step(for example '-s:1')
  -sb ROBUST_FOV_STEP, --robust_fov_step ROBUST_FOV_STEP
                        Apply Robust FOV cropping using FSL robustfov
  -p PARENT_DIR, --parent_dir PARENT_DIR
                        The path of the main directory
  -s STEPS, --steps STEPS
                        choose the order of the pipeline(1.Registraion(FSL), 2.Registraion(ANNTs) 3.skull striping 4.Bias correction-N4 )

```


An example of using this pipeline:

```bash
docker build  -t fleximriprep .
```
Build only once — you do not need to rebuild the image each time you run the pipeline.

```bash
docker run --interactive --tty --volume=/home/mds/Documents/temp/test/data:/data fleximriprep main.py -s "7" -m "non" -lm "" -i "./data/input_dicom" -o "./data/output_dicom_scan"  -s7 "d:Protocol Name,Series Description"
```
Note: Before proceeding to the next step, open the generated list_dicom_contain.csv file and remove any rows you do not want to process — only the remaining rows will be included in the next step.

For example, to process only 3D_FLAIR files, keep only the corresponding rows and delete the rest:

| Index | File_name | Path_dicom_file | Protocol Name | Series Description | Series Instance UID |
|:------|:----------|:----------------|:--------------|:-------------------|:--------------------|
| 0 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | not_available_tag | mdbrain Lesion Report | 1.2.xxx.xxx.xxx |
| 2 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | T1 MPR Rage sag | T1 MPR Rage sag | 1.2.xxx.xxx.xxx |
| 172 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | 3D_FLAIR | 3D_FLAIR | 1.2.xxx.xxx.xxx |
| 174 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | MPR Rage cor | MPR Rage cor | 1.2.xxx.xxx.xxx |
| 241 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | not_available_tag | mdbrain Lesion Segmentation | 1.2.xxx.xxx.xxx |
| 577 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | MPR Rage tra KM | MPR Rage tra KM | 1.2.xxx.xxx.xxx |
| 637 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | MPR FLAIR 3D tra | MPR FLAIR 3D tra | 1.2.xxx.xxx.xxx |
| 695 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | DWI og | DWI og | 1.2.xxx.xxx.xxx |
| 740 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | DWI og | DWI og | 1.2.xxx.xxx.xxx |
| 785 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | not_available_tag | mdbrain Longitudinal Lesion Segmentation | 1.2.xxx.xxx.xxx |
| 1121 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | not_available_tag | mdbrain Lesion Report | 1.2.xxx.xxx.xxx |
| 1123 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | 3D_FLAIR | 3D_FLAIR | 1.2.xxx.xxx.xxx |

↓ After editing:

| Index | File_name | Path_dicom_file | Protocol Name | Series Description | Series Instance UID |
|:------|:----------|:----------------|:--------------|:-------------------|:--------------------|
| 172 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | 3D_FLAIR | 3D_FLAIR | 1.2.xxx.xxx.xxx |
| 1123 | XXXXXXXX | /data/MRI/input_dicom/XXXX/XXXX/XXXX | 3D_FLAIR | 3D_FLAIR | 1.2.xxx.xxx.xxx |

```bash
docker run --interactive --tty --volume=/home/mds/Documents/temp/test/data:/data fleximriprep main.py -s "8a9422256" -m "non" -lm "" -i "./data/MRI/input_dicom3" -o "./data/MRI/output" -s2 r:1 -s8 pcs:./data/MRI/output_dicom_scan/scan_dicom_files_finish
```

## File Structure

The following is an example of the directory structure for input files, output files, and logs:

```
data/
├──input_dicom/
│   ├── 1XXXX/
│   │    ├── XXXX
│   │    │    ├── XXXX
│   │    │    └── .../
│   │    └── .../
│   ├── 2XXXX/
│   │    ├── XXXX
│   │    │    ├── XXXX
│   │    │    └── .../
│   │    └── .../
│   └── .../
├──output_dicom_scan/
│   └── scan_dicom_files_finish
│        ├── list_dicom_contain.csv
│        └── list_dicom_contain.pkl
└──output/
    ├── convert_dicom2nifti_step0
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR.json
    │   │   └── FLAIR.nii.gz
    │   └── .../
    ├── affine_ANTs_step1
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR0GenericAffine.mat
    │   │   ├── FLAIR.nii.gz
    │   │   └── InverseWarped_FLAIR.nii.gz
    │   └── .../
    ├── rigid_ANTs_step2
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR0GenericAffine.mat
    │   │   ├── FLAIR.nii.gz
    │   │   └── InverseWarped_FLAIR.nii.gz
    │   └── .../
    ├── bias_correction_n4_step3
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   └── FLAIR.nii.gz
    │   └── .../
    ├── registration_ANTs_step4
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR.nii.gz
    │   │   └── jacobian.nii.gz
    │   └── .../
    ├── registration_ANTs_step5
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR.nii.gz
    │   │   └── jacobian.nii.gz
    │   └── .../
    ├── registration_ANTs_step6
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   ├── FLAIR.nii.gz
    │   │   └── jacobian.nii.gz
    │   └── .../
    ├── multiplying_step7
    │   ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
    │   │   └── FLAIR.nii.gz
    │   └── .../
    └── fuzzy_cmeans_segmentation_finish
        ├── 3D_FLAIR_xxxxxxxxxx_xxxxxxxxx_xxxxxxxxxxxxxx_xxxxxx
        │   ├── FLAIRrfcm-cluster-assignments.nii.gz
        │   ├── FLAIRrfcm-mem-cluster1.nii.gz
        │   ├── FLAIRrfcm-mem-cluster2.nii.gz
        │   └── FLAIRrfcm-mem-cluster3.nii.gz
        └── .../
logs
 └── pipeline_20XXXXXX_XXXXXX.log
```


## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.
