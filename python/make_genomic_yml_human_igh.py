# Make yml descriptor file for samples described in VDJbase - Genomics

import argparse
import csv
import yaml

parser = argparse.ArgumentParser(description='Make yml descriptor file for samples described in VDJbase - Genomics')
parser.add_argument('infile', help='input file (eval_genes.txt)')
parser.add_argument('metadata', help='metadata file (supplementary table.csv)')
parser.add_argument('outfile', help='output file (yml)')
parser.add_argument('study_details', help='study details file (csv)')
args = parser.parse_args()

def read_csv(infile):
    with open(infile, 'r') as fi:
        return list(csv.DictReader(fi))


def toint(x):
    ret = None
    try:
        ret = int(x)
    except:
        pass
    return ret


def tofloat(x):
    ret = None
    try:
        ret = float(x)
    except:
        pass
    return ret


def tosex(x):
    ret = 'not recorded'
    try:
        x = x.upper()
        if x[0] == 'F':
            ret = 'female'
        elif x[0] == 'M':
            ret = 'male'
    except:
        pass
    return ret


gene_recs = read_csv(args.infile)
raw_metadata = read_csv(args.metadata)

metadata = {v['Sample']: v for v in raw_metadata}

study_details = {}
with open(args.study_details, 'r') as fi:
    reader = csv.DictReader(fi)
    for row in reader:
        study_details[row['Id']] = row


defs = {}       # this will hold the structure to turn in to yml

# Add reference sets

defs['Reference_sets'] = [
    'Homo_sapiens_IGHV_gapped.fasta',
    'Homo_sapiens_IGHD.fasta',
    'Homo_sapiens_IGHJ.fasta'
]

# Add reference assembly

defs['Reference_assemblies'] = {}
defs['Reference_assemblies']['Human_IGH'] = {
    'sequence_file': 'igh.fasta',
    'sense': '-',
    'name': 'igh',
    'reference': '',
    'chromosome': 14,
    'start': 0,
    'end': 0,
    'locations': [
        'GENE.bed',
        'HEPTAMER.bed',
        'NONAMER.bed',
        'SPACER.bed',
        'EXON_1.bed',
        'EXON_2.bed',
        'INTRON.bed',
        'UTR.bed',
    ]
}
defs['Reference_set_version'] = 'IMGT:Homo sapiens:2022-04-03'

# Add studies

studies = ['PRJNA555323']
defs['Studies'] = {}
study_num = 25
processed_subjects = []

for study in studies:
    study_name = f'P{study_num}'
    defs['Studies'][study_name] = {}
    study_num += 1

    for field in study_details[study].keys():
        defs['Studies'][study_name][field] = study_details[study][field]
    defs['Studies'][study_name]['Subjects'] = {}

    subject_num = 1
    subjects = sorted(list(set([x['sample_name'] for x in gene_recs])))

    for subject in subjects:
        subject_name = subject

        if subject_name in metadata:
            processed_subjects.append(subject_name)
            rec = metadata[subject_name]
            defs['Studies'][study_name]['Subjects'][f'{study_name}_I{subject_num}'] = {
                'Name_in_study': subject_name,
                'Age': toint(rec['Age']),
                'Sex': tosex(rec['Sex']),
                'Annotation_file': args.infile,
                'Annotation_method': 'IGenotyper',
                'Annotation_format': 'IGenotyper',
                'Annotation_reference': 'https://www.frontiersin.org/article/10.3389/fimmu.2020.02136',
                'Reference_assembly': 'igh',
                'Grouped Ethnicity': rec['Grouped ethnicity'],
                'Self-reported Ethnicity': rec['Self-reported ethnicity'],
                'Sequencing_platform': rec['Pacific BioScience platform'],
                'IGH_coverage': tofloat(rec['PacBio IGH HiFi sequencing coverage']),
                'Assemblies': {}

            }
        else:
            defs['Studies'][study_name]['Subjects'][f'{study_name}_I{subject_num}'] = {
                'Name_in_study': subject_name,
                'Age': '',
                'Sex': '',
                'Annotation_file': args.infile,
                'Annotation_method': 'IGenotyper',
                'Annotation_format': 'IGenotyper',
                'Annotation_reference': 'https://www.frontiersin.org/article/10.3389/fimmu.2020.02136',
                'Reference_assembly': 'chr22',
                'Grouped Ethnicity': None,
                'Self-reported Ethnicity': None,
                'Sequencing_platform': None,
                'IGH_coverage': None,
                'Assemblies': {}

            }
            print(f"WARNING: subject {subject_name} has a BAM file but is not included in the study metadata")
        subject_num += 1

unprocessed_subjects = list(set(list(metadata.keys())) - set(processed_subjects))
unprocessed_subjects = ', '.join([s for s in unprocessed_subjects if s])

print(f"WARNING: The following subjects were included in the study metadata but do not have corresponding BAM files: {unprocessed_subjects}")

with open(args.outfile, 'w') as fo:
    yaml.dump(defs, fo)
