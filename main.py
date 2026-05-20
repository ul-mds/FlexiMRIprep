import os
import argparse
import subprocess
parser = argparse.ArgumentParser()
class all_step():
    def __init__(self,p_dir,regis_fsl_para,regis_ants_para,sk_str_par,bi_cor_n4_par,fu_cm_se_par,sc_di_par,con_dic2nii_par,rigid_ants_para,affine_ants_para,robust_fov_par,mask,l_modality,modality_make_mask_Co_Regist):
        self.data_dir=p_dir
        self.registration_fsl_parameters=regis_fsl_para
        self.registration_ants_parameters=regis_ants_para
        self.rigid_ants_parameters=rigid_ants_para
        self.affine_ants_parameters = affine_ants_para
        self.skull_stripping_parameters=sk_str_par
        self.bias_correction_n4_parameters=bi_cor_n4_par
        self.fuzzy_cmeans_segmentation_par=fu_cm_se_par
        self.convert_dicom2nifti_parameters=con_dic2nii_par
        self.scan_dicom_par=sc_di_par
        self.robust_fov_parameters = robust_fov_par
        self.mask_name=mask
        self.list_name_modality=l_modality
        self.first_modality_make_mask_Co_Registration=modality_make_mask_Co_Regist
    def bias_correction_n4(self,path_input,path_output):
        if self.list_name_modality[0]!= "":
            list_name_modality=self.list_name_modality
        else:
            list_name_modality=[]
        if not(self.first_modality_make_mask_Co_Registration in list_name_modality):
            list_name_modality.append(self.first_modality_make_mask_Co_Registration)
        list_all_modality_=list_name_modality[0]
        for index in range(1,len(list_name_modality)):
            list_all_modality_ =list_all_modality_+","+self.list_name_modality[index]#"-p",self.data_dir,
        parameters=["python3", "./src/bias_correction_n4_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        print(parameters)
        user_parameters=self.bias_correction_n4_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def registration_fsl(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python3", "./src/registration_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.registration_fsl_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def registration_ANTs(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python3", "./src/registration_ANTs_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.registration_ants_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        print(user_parameters)
        subprocess.run(parameters)
    def rigid_ANTs(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python3", "./src/rigid_ANTs.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.rigid_ants_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        print(user_parameters)
        subprocess.run(parameters)
    def affine_ANTs(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python3", "./src/affine_ANTs.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.affine_ants_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        print(user_parameters)
        subprocess.run(parameters)
    def skull_stripping(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python3", "./src/skull_stripping_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def multiplying(self,path_input,path_output):
        if self.list_name_modality[0]!= "":
            list_name_modality=self.list_name_modality
        else:
            list_name_modality=[]
        if not(self.first_modality_make_mask_Co_Registration in list_name_modality):
            list_name_modality.append(self.first_modality_make_mask_Co_Registration)
        list_all_modality_ =list_name_modality[0]
        for index in range(1,len(list_name_modality)):
            list_all_modality_ =list_all_modality_+","+self.list_name_modality[index]

        parameters =["python3", "./src/multiply_Images_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def fuzzy_cmeans_segmentation(self,path_input,path_output):
        if self.list_name_modality[0]!= "":
            list_name_modality=self.list_name_modality
        else:
            list_name_modality=[]
        if not(self.first_modality_make_mask_Co_Registration in list_name_modality):
            list_name_modality.append(self.first_modality_make_mask_Co_Registration)
        list_all_modality_=list_name_modality[0]
        for index in range(1,len(list_name_modality)):
            list_all_modality_ =list_all_modality_+","+self.list_name_modality[index]
        parameters =["python3", "./src/fuzzy_cmeans_segmentation_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        user_parameters=self.fuzzy_cmeans_segmentation_par
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)

    def scan_dicom_files(self,path_input,path_output):
        parameters =["python3", "./src/scan_dicom.py","-i",path_input,"-o",path_output]
        user_parameters=self.scan_dicom_par
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
        
    def robust_fov(self,path_input,path_output):
        if self.list_name_modality[0]!= "":
            list_name_modality=self.list_name_modality
        else:
            list_name_modality=[]
        if not(self.first_modality_make_mask_Co_Registration in list_name_modality):
            list_name_modality.append(self.first_modality_make_mask_Co_Registration)
        list_all_modality_ =list_name_modality[0]
        for index in range(1,len(list_name_modality)):
            list_all_modality_ =list_all_modality_+","+self.list_name_modality[index]

        parameters =["python3", "./src/robust_fov_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
        
    def convert_dicom2nifti(self,path_input,path_output):
        parameters =["python3", "./src/convert_dicom2nifti.py","-i",path_input,"-o",path_output]
        user_parameters=self.convert_dicom2nifti_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split("+")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    options = {
            1 : registration_fsl,
            2 : registration_ANTs,
            3 : skull_stripping,
            4 : bias_correction_n4,
            5 : multiplying,
            6 : fuzzy_cmeans_segmentation,
            7 : scan_dicom_files,
            8 : convert_dicom2nifti,
            9 : rigid_ANTs,
            10 : affine_ANTs,
            11 : robust_fov
    }
def dir_name(step):
    if step == 1:
        return "registration_fsl"
    elif step == 2:
        return "registration_ANTs"
    elif step == 3:
        return "skull_stripping"
    elif step == 4:
        return "bias_correction_n4"
    elif step == 5:
        return "multiplying"
    elif step == 6:
        return "fuzzy_cmeans_segmentation"
    elif step == 7:
        return "scan_dicom_files"
    elif step == 8:
        return "convert_dicom2nifti"
    elif step == 9:
        return "rigid_ANTs"
    elif step == 10:
        return "affine_ANTs"
    elif step == 11:
        return "robust_fov"   
    else:
        return "Somethings_wrong_in_the_step_name"
def convert_steps_to_list(s):
    result = []
    for char in s:
        if char.isdigit():
            result.append(int(char))
        elif char.isalpha():
            result.append(ord(char.upper()) - ord('A') + 10)
    return result
parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="Mask.nii.gz")
parser.add_argument("-b", "--base_image", help="The first modality for making skull mask and Co-Registration", default="FLAIR.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")

parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="input")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output")
parser.add_argument("-s1", "--registration_FSL_step", help="change the parameters for registration step(for example '-s:1+-p1:mypath')", default="")
parser.add_argument("-s2", "--registration_ANTS_step", help="change the parameters for registration step(for example '-s:1')", default="")
parser.add_argument("-s3", "--skull_stripping", help="change the parameters for skull stripping(for example '-s:1')", default="")
parser.add_argument("-s4", "--bias_correction_n4_step", help="change the parameters for bias correction(for example '-f:0.4')", default="")
parser.add_argument("-s5", "--Multiplying_step", help="Multiplying Images(for example '-d:3')", default="")
parser.add_argument("-s6", "--fuzzy_cmeans_segmentation_step", help="fuzzy-cmeans segmentation MRI files(for example '-d:3')", default="")
parser.add_argument("-s7", "--scan_dicom_step", help="scan dicom files(for example '-d:3')", default="-d:Protocol Name,Series Description")
parser.add_argument("-s8", "--convert_dicom2nifti_step", help="convert dicom files to nifti files(for example '-d:3')", default="-f:%p_%i_%x_%t_%s")
parser.add_argument("-s9", "--rigid_ANTS_step", help="change the parameters for rigid step(for example '-s:1')", default="")
parser.add_argument("-sa", "--affine_ANTS_step", help="change the parameters for affine step(for example '-s:1')", default="")
parser.add_argument("-sb", "--robust_fov_step",help="Apply Robust FOV cropping using FSL robustfov",default="")
parser.add_argument("-p", "--parent_dir", help="The path of the main directory", default=os.path.join(os.getcwd(), "data"))
parser.add_argument("-s", "--steps", help="choose the order of the pipeline(1.Registraion(FSL), 2.Registraion(ANNTs) 3.skull striping 4.Bias correction-N4 )", default="4134")
#parser.add_argument("-f", "--file_csv_scan", help="The path of the csv_scan", default=os.path.join(os.getcwd(), "data"))
args = parser.parse_args()
order_step = args.steps
data_dir =args.parent_dir
data_input_dir = args.read_dir
data_output_dir = args.write_dir

robust_fov_par = args.robust_fov_step
registration_FSL_par=args.registration_FSL_step
registration_ANTS_par=args.registration_ANTS_step
rigid_ANTS_par=args.rigid_ANTS_step
affine_ANTS_par=args.affine_ANTS_step
skull_stripping_par=args.skull_stripping
bias_correction_n4_par=args.bias_correction_n4_step
fuzzy_cmeans_segmentation_par=args.fuzzy_cmeans_segmentation_step
scan_dicom_par=args.scan_dicom_step
convert_dicom2nifti_par=args.convert_dicom2nifti_step
mask_name=args.mask
first_modality_make_mask_Co_Registration=args.base_image
list_name_modality=args.list_modalities.split("+")
pipilne=all_step(data_dir,registration_FSL_par,registration_ANTS_par,skull_stripping_par,bias_correction_n4_par,fuzzy_cmeans_segmentation_par,scan_dicom_par,convert_dicom2nifti_par,rigid_ANTS_par,affine_ANTS_par,robust_fov_par,mask_name,list_name_modality,first_modality_make_mask_Co_Registration)
input_dir_pipline=[data_input_dir]
order_step=convert_steps_to_list(order_step)
for step in range(0, len(order_step)-1):
    input_dir_pipline.append(data_output_dir+"/"+dir_name(int(order_step[step]))+"_step"+str(step))
input_dir_pipline.append(data_output_dir+"/"+dir_name(int(order_step[len(order_step)-1]))+"_finish")
for step in range(0, len(order_step)):
    pipilne.options[int(order_step[step])](pipilne,input_dir_pipline[step],input_dir_pipline[step+1])

print("done")
