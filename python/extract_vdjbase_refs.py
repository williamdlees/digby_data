# Extract reference files for nominated species

import argparse
import simple_bio_seq as simple
import os


parser = argparse.ArgumentParser(description='Extract reference files for nominated species')
parser.add_argument('species_name', help='species name for IMGT file, e.g. Homo sapiens, Macaca mulatta')
args = parser.parse_args()

os.system('wget -O imgt_gapped.fasta http://www.imgt.org/download/GENE-DB/IMGTGENEDB-ReferenceSequences.fasta-nt-WithGaps-F+ORF+inframeP')

segs = ['IGHV', 'IGHD', 'IGHJ']
refs = simple.read_imgt_fasta('imgt_gapped.fasta', [args.species_name], segs)

for seg in segs:
    simple.write_fasta(refs[args.species_name][seg], '%s_%s_gapped.fasta' % (args.species_name.replace(' ', '_'), seg))
	
os.system('rm imgt_gapped.fasta')

