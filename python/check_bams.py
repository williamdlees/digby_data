# Check that annotations in genomic directories match BAM contents
# Run from samples/Genomic
# Must be run under linux, requires pysam

import glob
import os
import csv
import pysam


sample_count = 0
errors = False

for bamfile in glob.glob('**/*.bam', recursive=True):
    annot_file = bamfile.replace('.bam', '.csv')

    if not os.path.exists(annot_file):
        print(f"Annotation file {annot_file} not found")
        continue

    with open(annot_file) as f:
        recs = {}
        annot_reader = list(csv.DictReader(f))
        annot_contigs = [x['contig'] for x in annot_reader]

        samfile = pysam.AlignmentFile(bamfile, "rb")
        samfile_contigs = [x.query_name for x in samfile.fetch()]

        # print("\n\nAnnots")
        # print(list(set(annot_contigs)))

        if set(annot_contigs) - set(samfile_contigs):
            print(f"Annotations in {annot_file} not found in {bamfile}")
            print("Samfile")
            print(list(set(samfile_contigs)))
            errors = True

        #annot_haps = set([x['haplotype'] for x in annot_reader])
        #if len(annot_haps) < 3:
        #    print(f"Annotation file {annot_file} has less than 3 haplotypes")
        #    continue
        
        sample_count += 1

if not errors:
    print(f'{sample_count} samples checked. Contigs in BAM files match those in the annotation file in all cases.')
else:
    print(f'{sample_count} samples checked. Mismatches found.')
