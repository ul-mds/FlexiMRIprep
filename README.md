# FlexiMRIprep
An automatic pipeline for preprocessing brain MRIs


ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS=8
export ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS
python main.py -s "422256" -m "non" -lm "" -i "/mnt/mds-storage/mabedi/OASIS3_76new/input" -o "/mnt/mds-storage/mabedi/OASIS3_76new/output" -s2 r:1
