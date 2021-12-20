# rename geno to genotype
import os


for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
    for filename in filenames:
        if 'geno.tsv' in filename:
            os.rename(os.path.join(dirpath, filename), os.path.join(dirpath, filename.replace('geno', 'genotype')))
