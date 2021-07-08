# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pandas as pd
import numpy as np
from itertools import compress
import os
import re
import shutil


dataset_path = "/home/aviv/T cell/DS4/"
old_geno_path = dataset_path + "genotypes_filtered/"
old_haplo_path = dataset_path + "haplotypes/"
excel_file = dataset_path + "DS4.xls"
geno_suffix = "_TCR_geno.tab"

geno_files = os.listdir(old_geno_path)
haplo_files = os.listdir(old_haplo_path)

new_geno_path = dataset_path + "genotypes/"
new_haplo_path = dataset_path + "new_hapotypes/"

if not os.path.isdir(new_geno_path):
    os.mkdir(new_geno_path)


if not os.path.isdir(new_haplo_path):
    os.mkdir(new_haplo_path)

subject_sheet = pd.read_excel(excel_file, sheet_name="Subjects")
for i in range(len(subject_sheet.index)):
    new_name = subject_sheet["Name"][i]
    old_name = subject_sheet["Old name"][i]
    
    subject_file_inds = [bool(re.search(str("^" + old_name), geno_file)) for geno_file in geno_files]
    subject_files = list(compress(geno_files, subject_file_inds))
    
    subject_file_inds = [not bool(re.search(str(old_name + "[0-9]"), geno_file)) for geno_file in subject_files]
    subject_files = list(compress(subject_files, subject_file_inds))
    
    if len(subject_files) == 0:
        print(old_name)


    for subj_file in subject_files:
        old_suffix = ""
        if str(old_name + "T") in subj_file:
            old_suffix = "T"

        if len(subject_files) == 1:
            new_samp_name = new_name + "_S1"
        
        else:
            if not bool(re.search(str(old_name + "[a-z]"), subj_file)):
                new_samp_name = new_name + "_S" + str(len(subject_files))
            elif str(old_name + "a") in subj_file:
                new_samp_name = new_name + "_S1"
                old_suffix = "a"
            elif str(old_name + "b") in subj_file:
                new_samp_name = new_name + "_S2"
                old_suffix = "b"
            elif str(old_name + "c") in subj_file:
                new_samp_name = new_name + "_S3"
                old_suffix = "c"
            elif str(old_name + "d") in subj_file:
                new_samp_name = new_name + "_S4"
                old_suffix = "d"
        
        new_subj_file = subj_file.replace(str(old_name + old_suffix), new_samp_name)

        shutil.copy(old_geno_path + subj_file, new_geno_path + new_subj_file)

    subject_file_inds = [bool(re.search(str("^" + old_name), haplo_file)) for haplo_file in haplo_files]
    subject_files = list(compress(haplo_files, subject_file_inds))
    
    subject_file_inds = [not bool(re.search(str(old_name + "[0-9]"), haplo_file)) for haplo_file  in subject_files]
    subject_files = list(compress(subject_files, subject_file_inds))

    unique_samples = [haplo.split("_haplo")[0] for haplo in subject_files]
    unique_samples = list(set(unique_samples))
    for subj_file in subject_files:
        old_suffix = ""
        if str(old_name + "T") in subj_file:
            old_suffix = "T"
		
        if not bool(re.search(str(old_name + "[a-z]"), subj_file)):
            new_samp_name = new_name + "_S" + str(len(unique_samples))
        elif str(old_name + "a") in subj_file:
            new_samp_name = new_name + "_S1"
            old_suffix = "a"
        elif str(old_name + "b") in subj_file:
            new_samp_name = new_name + "_S2"
            old_suffix = "b"
        elif str(old_name + "c") in subj_file:
            new_samp_name = new_name + "_S3"
            old_suffix = "c"
        elif str(old_name + "d") in subj_file:
            new_samp_name = new_name + "_S4"
            old_suffix = "d"
        
        new_subj_file = subj_file.replace(str(old_name + old_suffix), new_samp_name)

        shutil.copy(old_haplo_path + subj_file, new_haplo_path + new_subj_file)






