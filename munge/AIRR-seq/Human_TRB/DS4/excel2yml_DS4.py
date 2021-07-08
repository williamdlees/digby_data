#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 24 11:03:08 2021

@author: aviv
"""
import yaml
import pandas as pd
import datetime
import numpy as np
import io
import os

def int_or_blank(n):
	try:
		return int(n)
	except:
		return ''


def make_bool(s):
	if len(s) < 1:
		return True
	else:
		return True if (s[0] == 'T' or s[0] == 't') else False


def sex(s):
	if len(s) < 1:
		return s
	return 'M' if s[0] == 'M' or s[0] == 'm' else 'F'


dataset_path = ""
excel_file = dataset_path + "DS4.xls"

project_sheet = pd.read_excel(excel_file, sheet_name="Studies")
project_sheet = project_sheet.replace(np.nan, '', regex=True)
subject_sheet = pd.read_excel(excel_file, sheet_name="Subjects")
subject_sheet = subject_sheet.replace(np.nan, '', regex=True)
seq_sheet = pd.read_excel(excel_file, sheet_name="Sequence Protocol")
seq_sheet = seq_sheet.replace(np.nan, '', regex=True)
tissue_sheet = pd.read_excel(excel_file, sheet_name="Tissue Processing")
tissue_sheet = tissue_sheet.replace(np.nan, '', regex=True)
geno_sheet = pd.read_excel(excel_file, sheet_name="Genotype Detections")
geno_sheet = geno_sheet.replace(np.nan, '', regex=True)
sample_sheet = pd.read_excel(excel_file, sheet_name="Samples")
sample_sheet = sample_sheet.replace(np.nan, '', regex=True)

project_list = {
	'DS4': 'P20',
}


for i in range(len(project_sheet.index)):
	project = project_sheet["Project"][i]
	project_dict = {project: {}}

	project_dict[project]["Accession id"] = project_sheet["Accession id"][i]
	project_dict[project]["Accession reference"] = project_sheet["Accession reference"][i]
	project_dict[project]["Contact"] = project_sheet["Contact"][i]
	project_dict[project]["Institute"] = project_sheet["Institute"][i]
	project_dict[project]["Number of Samples"] = int(project_sheet["Number of Samples"][i])
	project_dict[project]["Number of Subjects"] = int(project_sheet["Number of Subjects"][i])
	project_dict[project]["Project"] = project
	project_dict[project]["Reference"] = project_sheet["Refernce"][i]
	project_dict[project]["Researcher"] = project_sheet["Researcher"][i]


	project_dict[project]["Genotype Detections"] = {}
	for i in range(len(geno_sheet.index)):
		geno_det = geno_sheet["Pipeline name"][i]
		project_dict[project]["Genotype Detections"][geno_det] = {}
		project_dict[project]["Genotype Detections"][geno_det]["Name"] = geno_det
		project_dict[project]["Genotype Detections"][geno_det]["Repertoire or Germline"] = geno_sheet["Repertoire\Germline"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Pre-processing"] = geno_sheet["Pre-processing"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Aligner Tool"] = geno_sheet["Aligner tool"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Aligner Version"] = geno_sheet["Aligner version"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Alignment reference v"] = geno_sheet["Alignment reference v"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Alignment reference d"] = geno_sheet["Alignment reference d"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Alignment reference j"] = geno_sheet["Alignment reference j"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Genotyper Tool"] = geno_sheet["Genotyper tool"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Genotyper Version"] = geno_sheet["Genotyper version"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Haplotyper Tool"] = geno_sheet["Haplotyper Tool"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Haplotyper Version"] = geno_sheet["Haplotyper version"][i]
		project_dict[project]["Genotype Detections"][geno_det]["Single Assignment"] = make_bool(geno_sheet["single alignment (True\False)"][i])
		project_dict[project]["Genotype Detections"][geno_det]["Germline Reference"] = ""


	project_dict[project]["Samples"] = {}
	for i in range(len(sample_sheet.index)):
		sample = sample_sheet["Name"][i]
		if project in sample:
			project_dict[project]["Samples"][sample] = {}
			project_dict[project]["Samples"][sample]["Name"] = sample
			project_dict[project]["Samples"][sample]["Sequence Protocol Name"] = sample_sheet["Sequence Protocol"][i]
			project_dict[project]["Samples"][sample]["Tissue Processing Name"] = sample_sheet["Tissue Processing"][i]
			project_dict[project]["Samples"][sample]["Subject Name"] = sample_sheet["Subject"][i]
			project_dict[project]["Samples"][sample]["Chain"] = 'TRB'
			project_dict[project]["Samples"][sample]["Reads"] = int(sample_sheet["Row_reads"][i])
			project_dict[project]["Samples"][sample]["Genotype Detection Name"] = sample_sheet["Genotype detection"][i]
			project_dict[project]["Samples"][sample]["Sample Group"] = str(sample_sheet["Sample group"][i])
			project_dict[project]["Samples"][sample]["Date"] = datetime.date.today()


	project_dict[project]["Sequence Protocol"] = {}
	for i in range(len(seq_sheet.index)):
		seq_name = seq_sheet["Name"][i]
		if project in seq_name:
			project_dict[project]["Sequence Protocol"][seq_name] = {}
			project_dict[project]["Sequence Protocol"][seq_name]["Name"] = seq_name
			project_dict[project]["Sequence Protocol"][seq_name]["Sequencing_platform"] = seq_sheet["Sequencing_platform"][i]
			project_dict[project]["Sequence Protocol"][seq_name]["Sequencing_length"] = seq_sheet["Sequencing_length"][i]
			project_dict[project]["Sequence Protocol"][seq_name]["UMI"] = make_bool(seq_sheet["UMI (TRUE/FALSE)"][i])
			project_dict[project]["Sequence Protocol"][seq_name]["Helix"] = seq_sheet["Helix"][i]
			project_dict[project]["Sequence Protocol"][seq_name]["Primer 5 location"] = seq_sheet["Primers 5 location"][i]
			project_dict[project]["Sequence Protocol"][seq_name]["Primer 3 location"] = seq_sheet["Primers 3 location"][i]


	project_dict[project]["Subjects"] = {}
	for i in range(len(subject_sheet.index)):
		subject = subject_sheet["Name"][i]
		if project in subject:
			project_dict[project]["Subjects"][subject] = {}
			project_dict[project]["Subjects"][subject]["Name"] = subject
			project_dict[project]["Subjects"][subject]["Original name"] = subject_sheet["Old name"][i]
			project_dict[project]["Subjects"][subject]["Sex"] = sex(subject_sheet["Sex"][i])
			project_dict[project]["Subjects"][subject]["Age"] = int_or_blank(subject_sheet["Age"][i])
			project_dict[project]["Subjects"][subject]["Ethnic"] = subject_sheet["Ethnic"][i]
			project_dict[project]["Subjects"][subject]["Country"] = subject_sheet["Country"][i]
			project_dict[project]["Subjects"][subject]["Health Status"] = subject_sheet["Health Status"][i]
			project_dict[project]["Subjects"][subject]["Cohort"] = subject_sheet["Cohort"][i]



	project_dict[project]["Tissue Processing"] = {}
	for i in range(len(tissue_sheet.index)):
		tissue = tissue_sheet["Name"][i]
		if project in tissue:
			project_dict[project]["Tissue Processing"][tissue] = {}
			project_dict[project]["Tissue Processing"][tissue]["Name"] = tissue
			project_dict[project]["Tissue Processing"][tissue]["Species"] = 'Human'
			project_dict[project]["Tissue Processing"][tissue]["Tissue"] = tissue_sheet["Tissue"][i]
			project_dict[project]["Tissue Processing"][tissue]["Cell Type"] = 'T cell'
			project_dict[project]["Tissue Processing"][tissue]["Sub Cell Type"] = tissue_sheet["Sub Cell Type"][i]
			project_dict[project]["Tissue Processing"][tissue]["Isotype"] = tissue_sheet["Isotype"][i]


	yamlio = io.StringIO()
	yaml.dump(project_dict, yamlio)
	s = yamlio.getvalue()
	s = s.replace(project, project_list[project])
	with open(project_list[project] + '.yml', 'w') as outfile:
		outfile.write(s)

for file in os.listdir('genotypes'):
	file = os.path.join('genotypes', file)
	if os.path.isfile(file):
		for k, v in project_list.items():
			if k in file:
				os.rename(file, file.replace(k, v))
				break

for file in os.listdir('haplotypes'):
	file = os.path.join('haplotypes', file)
	if os.path.isfile(file):
		for k, v in project_list.items():
			if k in file:
				os.rename(file, file.replace(k, v))
				break

