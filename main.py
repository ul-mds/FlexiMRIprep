import os
import argparse
import subprocess
parser = argparse.ArgumentParser()
class all_step():
    def __init__(self,p_dir,regis_fsl_para,regis_ants_para,sk_str_par,bi_cor_n4_par,mask,l_modality,modality_make_mask_Co_Regist):
        self.data_dir=p_dir
        self.registration_fsl_parameters=regis_fsl_para
        self.registration_ants_parameters=regis_ants_para
        self.skull_stripping_parameters=sk_str_par
        self.bias_correction_n4_parameters=bi_cor_n4_par
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
        parameters=["python", "./src/bias_correction_n4_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        print(parameters)
        user_parameters=self.bias_correction_n4_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def registration_fsl(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python", "./src/registration_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.registration_fsl_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    def registration_ANTs(self,path_input,path_output):
        list_all_modality=self.list_name_modality[0]
        for index in range(1,len(self.list_name_modality)):
            list_all_modality=list_all_modality+","+self.list_name_modality[index]
        parameters =["python", "./src/registration_ANTs_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.registration_ants_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
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
        parameters =["python", "./src/skull_stripping_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality,"-b",self.first_modality_make_mask_Co_Registration]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
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

        parameters =["python", "./src/multiply_Images_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
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
        parameters =["python", "./src/fuzzy_cmeans_segmentation_step.py","-i",path_input,"-o",path_output,"-m",self.mask_name,"-lm",list_all_modality_]
        user_parameters=self.skull_stripping_parameters
        if user_parameters!="":
            user_parameters=user_parameters.split(",")
        for item in user_parameters:
            pr=item.split(":")
            parameters.append("-"+pr[0])
            parameters.append(pr[1])
        subprocess.run(parameters)
    options = {
            1 : registration_fsl,
            2:registration_ANTs,
            3 : skull_stripping,
            4 : bias_correction_n4,
            5: multiplying,
            6:fuzzy_cmeans_segmentation,
    }

parser.add_argument("-m", "--mask", help="name of the mask file(.nii.gz)", default="Mask.nii.gz")
parser.add_argument("-b", "--base_image", help="The first modality for making skull mask and Co-Registration", default="FLAIR.nii.gz")
parser.add_argument("-lm", "--list_modalities", help="The list of modalities", default="T1W.nii.gz,T1WKS.nii.gz,T2W.nii.gz")

parser.add_argument("-i", "--read_dir", help="ّInput path of the patient directory", default="input")
parser.add_argument("-o", "--write_dir", help="Output path of the patient directory", default="output")
parser.add_argument("-s1", "--registration_FSL_step", help="change the parameters for registration step(for example '-s:1')", default="")
parser.add_argument("-s2", "--registration_ANTS_step", help="change the parameters for registration step(for example '-s:1')", default="")
parser.add_argument("-s3", "--skull_stripping", help="change the parameters for skull stripping(for example '-s:1')", default="")
parser.add_argument("-s4", "--bias_correction_n4_step", help="change the parameters for bias correction(for example '-f:0.4')", default="")
parser.add_argument("-s5", "--Multiplying_step", help="Multiplying Images(for example '-d:3')", default="")
parser.add_argument("-s6", "--fuzzy_cmeans_segmentation_step", help="fuzzy-cmeans segmentation MRI files(for example '-d:3')", default="")
parser.add_argument("-p", "--parent_dir", help="The path of the main directory", default=os.path.join(os.getcwd(), "data"))
parser.add_argument("-s", "--steps", help="choose the order of the pipeline(1.Registraion(FSL), 2.Registraion(ANNTs) 3.skull striping 4.Bias correction-N4 )", default="4134")
args = parser.parse_args()
order_step = args.steps
data_dir =args.parent_dir
data_input_dir = args.read_dir
data_output_dir = args.write_dir

registration_FSL_par=args.registration_FSL_step
registration_ANTS_par=args.registration_ANTS_step
skull_stripping_par=args.skull_stripping
bias_correction_n4_par=args.bias_correction_n4_step

mask_name=args.mask
first_modality_make_mask_Co_Registration=args.base_image
list_name_modality=args.list_modalities.split(",")
pipilne=all_step(data_dir,registration_FSL_par,registration_ANTS_par,skull_stripping_par,bias_correction_n4_par,mask_name,list_name_modality,first_modality_make_mask_Co_Registration)
input_dir_pipline=[data_input_dir]
for step in range(0, len(order_step)-1):
    input_dir_pipline.append(data_output_dir+"/"+"step"+str(step))
input_dir_pipline.append(data_output_dir)
for step in range(0, len(order_step)):
    pipilne.options[int(order_step[step])](pipilne,input_dir_pipline[step],input_dir_pipline[step+1])

print("done")
