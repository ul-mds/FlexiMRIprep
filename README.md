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

Instructions on how to set up the development environment.

This pipeline is fully tested in Python 3.10. To use this pipeline, it is recommended to install using the `install.sh` script. If you use the installation file, there is no need to change the default Python version. The desired Python version is installed locally.

```bash
chmod +x install.sh
./install.sh
source .venv/bin/activate
```

At this stage, you need to install the following tools. If it is not possible to access them through the terminal, please add their paths in the environment file.

- [ANTS](https://andysbrainbook.readthedocs.io/en/latest/ANTs/ANTs_Overview.html)
- [Nighres](https://nighres.readthedocs.io/en/latest/installation.html)

### Template Downloads

Please download the following files and extract them into the `Template` folder.

1. Download the file `mni_icbm152_lin_nifti.zip` from [this link](http://packages.bic.mni.mcgill.ca/mni-models/icbm152/mni_icbm152_lin_nifti.zip) and extract it into the `Template` folder. For more information, visit [this page](https://www.mcgill.ca/bic/software/tools-data-analysis/anatomical-mri/atlases/icbm152lin).

2. Download the file `mni_icbm152_nlin_asym_09c_nifti.zip` from [this link](http://www.bic.mni.mcgill.ca/~vfonov/icbm/2009/mni_icbm152_nlin_asym_09c_nifti.zip) and extract it into the `Template` folder. For more information, visit [this page](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009).

### Note

In some cases, it may be necessary to reinstall the `SimpleITK` package at the final step. Use the following command to reinstall:

```bash
python3 -m pip install SimpleITK==2.1.1.2 # pip install SimpleITK==2.1.1.2
```
## Usage

To use the preprocessing pipeline, run the `main.py` script with the appropriate options:

```bash
usage: main.py [-h] [-m MASK] [-b BASE_IMAGE] [-lm LIST_MODALITIES]
               [-i READ_DIR] [-o WRITE_DIR] [-s1 REGISTRATION_FSL_STEP]
               [-s2 REGISTRATION_ANTS_STEP] [-s3 SKULL_STRIPPING]
               [-s4 BIAS_CORRECTION_N4_STEP] [-s5 MULTIPLYING_STEP]
               [-s6 FUZZY_CMEANS_SEGMENTATION_STEP] [-p PARENT_DIR] [-s STEPS]

options:
  -h, --help            show this help message and exit
  -m MASK, --mask MASK  name of the mask file (.nii.gz)
  -b BASE_IMAGE, --base_image BASE_IMAGE
                        The first modality for making skull mask and Co-Registration
  -lm LIST_MODALITIES, --list_modalities LIST_MODALITIES
                        The list of modalities
  -i READ_DIR, --read_dir READ_DIR
                        Input path of the patient directory
  -o WRITE_DIR, --write_dir WRITE_DIR
                        Output path of the patient directory
  -s1 REGISTRATION_FSL_STEP, --registration_FSL_step REGISTRATION_FSL_STEP
                        Change the parameters for registration step (e.g., '-s:1')
  -s2 REGISTRATION_ANTS_STEP, --registration_ANTS_step REGISTRATION_ANTS_STEP
                        Change the parameters for registration step (e.g., '-s:1')
  -s3 SKULL_STRIPPING, --skull_stripping SKULL_STRIPPING
                        Change the parameters for skull stripping (e.g., '-s:1')
  -s4 BIAS_CORRECTION_N4_STEP, --bias_correction_n4_step BIAS_CORRECTION_N4_STEP
                        Change the parameters for bias correction (e.g., '-f:0.4')
  -s5 MULTIPLYING_STEP, --Multiplying_step MULTIPLYING_STEP
                        Multiplying images (e.g., '-d:3')
  -s6 FUZZY_CMEANS_SEGMENTATION_STEP, --fuzzy_cmeans_segmentation_step FUZZY_CMEANS_SEGMENTATION_STEP
                        Fuzzy-cmeans segmentation of MRI files (e.g., '-d:3')
  -p PARENT_DIR, --parent_dir PARENT_DIR
                        The path of the main directory
  -s STEPS, --steps STEPS
                        Choose the order of the pipeline (1. Registration (FSL), 2. Registration (ANTs), 3. Skull stripping, 4. Bias correction-N4)
```

If you want the calculations to be distributed across the processor to increase speed, use these commands:

```bash
ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS
```

An example of using this pipeline:

```bash
python main.py -s "422256" -m "non" -lm "" -i "input" -o "output" -s2 r:1
```

## File Structure

The following is an example of the directory structure for the input files, output files, and pipeline scripts:

```
MRI-Preprocessing-Pipeline/
├── input/
│   ├── patient1/
│   │   └── FLAIR.nii.gz
│   ├── patient2/
│   │   └── FLAIR.nii.gz
│   └── .../
├── output/
│   ├── patient1/
│   │   └── FLAIR.nii.gz
│   ├── patient2/
│   │   └── FLAIR.nii.gz
│   └── .../
├── src/
│   ├── bias_correction_n4_step.py
│   ├── fuzzy_cmeans_segmentation_step.py
│   ├── multiply_Images_step.py
│   ├── registration_ANTs_step.py
│   ├── registration_step.py
│   ├── skull_stripping_step.py
│   └── Template
│       ├── mni_icbm152_wm_tal_nlin_asym_09c.nii
│       ├── mni_icbm152_t2_tal_nlin_asym_09c.nii
│       ├── icbm_avg_152_t1_tal_lin.nii.gz
│       └── ...
├── install.sh
├── main.py
├── README.md
├── requirements.txt
└── LICENSE.md
```


## License

This project is licensed under the GPL-3.0 license - see the [LICENSE](LICENSE) file for details.
