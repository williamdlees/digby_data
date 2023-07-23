# Create a file of identified genes from a set of assemblies
import argparse
import os
import sys
from collections import namedtuple

import read_bed
import pysam
import receptor_utils.simple_bio_seq as simple
from pathlib import Path

from cigar import Cigar

output_headers = [
    'sample_name',
    'haplotype',
    'gene',
    'allele',
]

v_coord_map = {
    'allele_sequence': 'GENE',
    'V-HEPTAMER': 'HEPTAMER',
    'V-SPACER': 'SPACER',
    'V-NONAMER': 'NONAMER',
    'V-EXON2': 'EXON_2',
    'V-INTRON': 'INTRON',
    'L-PART1': 'EXON_1',
    'V-REGION': 'V-REGION',
    'L-PART2': 'L-PART2',
    'V-UTR': 'UTR',
}

utr_loci = ['IGH']

d_coord_map = {
    'allele_sequence': 'GENE',
    'D-3_HEPTAMER': '3_HEPTAMER',
    'D-3_SPACER': '3_SPACER',
    'D-3_NONAMER': '3_NONAMER',
    'D-REGION': 'EXON_1',
    'D-5_HEPTAMER': '5_HEPTAMER',
    'D-5_SPACER': '5_SPACER',
    'D-5_NONAMER': '5_NONAMER',
}

j_coord_map = {
    'allele_sequence': 'GENE',
    'J-HEPTAMER': 'HEPTAMER',
    'J-SPACER': 'SPACER',
    'J-NONAMER': 'NONAMER',
    'J-REGION': 'EXON_1',
}


def missing_fields(row, fields):
    for field in fields:
        if field not in row or not row[field] or len(row[field]) < 2:
            return True
    return False


def verbose_print(verbose_str, verbose):
    if verbose:
        print(verbose_str)


Contig = namedtuple('Contig', 'header, annotations, haplotype')


class CigarState:
    def __init__(self):
        self.count = 0
        self.state = 'M'
        self.next_pos = 0
        self.string = ''
        self.processed_seq_len = 0
        self.this_seg = ''
        self.processed_segs = []

    def process_cigar(self, op, c):
        if self.state != op:
            if self.count > 0:
                self.string += f"{self.count}{self.state}"
                self.processed_seq_len += self.count
                self.processed_segs.append((len(self.this_seg), self.this_seg))
            self.count = 1
            self.this_seg = c if op != 'D' else ''
            self.state = op
        else:
            if op != 'D':
                self.this_seg += c
            self.count += 1
        if op != 'I':
            self.next_pos += 1

    def finalise_cigar(self):
        if self.count > 0:
            self.string += f"{self.count}{self.state}"
            self.processed_seq_len += self.count
            self.processed_segs.append((len(self.this_seg), self.this_seg))
        return self.string


# Fetch all contigs from the BAM file that cover the specified range
def fetch_contigs(samfile, chrom, start, end, annotation_ranges, verbose):
    contigs = []

    for read in samfile.fetch(chrom, start, end):
        if read.is_secondary:
            verbose_print(f"{read.qname}: secondary alignment", verbose)
            continue
        if read.is_supplementary:
            verbose_print(f"{read.qname}: supplementary read", verbose)
            continue
        if read.is_unmapped:
            verbose_print(f"{read.qname}: unmapped read", verbose)
            continue
        if read.reference_start > start:
            verbose_print(f"{read.qname} start: {read.reference_start} end {read.reference_end} read.ref_start > required start", verbose)
            continue
        if read.reference_end < end:
            verbose_print(f"{read.qname} start: {read.reference_start} end {read.reference_end} read.ref_end < required end", verbose)
            continue

        q_start = -1
        q_end = None
        leading_dels = 0

        for query, ref in read.get_aligned_pairs():
            if ref and ref == start:    # q_start is where we want to take our query sequence from...
                q_start = query         # but if it is None at this point, the first base is a deletion
            if q_start is None and query is not None and ref is not None and ref > start:   # in which case, we set q_start to the first base that isn't deleted...
                q_start = query
            if ref is not None and q_start is None:                     # and in the meantime count the leading deletions
                leading_dels += 1
            if query is not None:
                q_end = query

            if ref and ref >= end:
                break

        name = read.query_name

        #if verbose:
        #    breakpoint()

        haplotype = None
        for el in name.split('_'):
            if 'h=' in el:
                haplotype = el.replace('h=', '')

        if haplotype is None or haplotype not in ['0', '1', '2']:
            verbose_print(f"{read.qname}: unrecognisable haplotype", verbose)
            haplotype = '0'

        seq = read.query_sequence[q_start:q_end]

        if len(seq) < 2:
            verbose_print(f"{read.qname}: no useful alignment with ref 1", verbose)
            continue

        # assign to annotation fields, handling indels
        annotations = {annot: '' for _, _, annot in annotation_ranges}

        cigar_states = {annot: CigarState() for _, _, annot in annotation_ranges}
        ap = read.get_aligned_pairs()

        if ap is None or (ap[0][1] is not None and ap[0][1] >= end):
            verbose_print(f"{read.qname}: no useful alignment with ref", verbose)
            continue    # no useful alignment

        def add_to_annots(pos, c, op):
            for r in annotation_ranges:
                if pos >= r[0] and pos <= r[1]:
                    annotations[r[2]] += c
                    cigar = cigar_states[r[2]]
                    cigar.process_cigar(op, c)

        def finalise_cigars():
            for r in annotation_ranges:
                cigar = cigar_states[r[2]]
                annotations[r[2] + '_CIGAR'] = cigar.finalise_cigar()
                cig = Cigar(annotations[r[2] + '_CIGAR'])
                if cig.__len__() != len(annotations[r[2]]):
                    print(f'Error in cigar string length for annotation {r[2]}')
                    breakpoint()

        q_current = q_start
        seq_current = 0
        annot_pos = 1   # 1-based index of gene sequence relative to ref
        start_encountered = False
        wanted_length = end - start

        def process_cigar(op, cigar_state):
            if cigar_state[1] != op:
                if cigar_state[0] > 0:
                    cigar_state[2] += f"{cigar_state[0]}{cigar_state[1]}"
                cigar_state[0] = 1
                cigar_state[1] = op
            else:
                cigar_state[0] += 1

        for _ in range(leading_dels):
            add_to_annots(annot_pos, '', 'D')
            annot_pos += 1

        for i in range(len(ap)):
            if start_encountered and (ap[i][0] is None or seq_current >= len(seq)):  # deletion relative to franken (including a trailing deletion)
                add_to_annots(annot_pos, '', 'D')
                annot_pos += 1
            elif ap[i][1] is None and ap[i][0] is not None and start_encountered:  # insertion relative to franken
                add_to_annots(annot_pos, seq[seq_current], 'I')
                seq_current += 1
                q_current += 1
            elif ap[i][0] and ap[i][0] == q_current:    # aligned relative to franken
                start_encountered = True
                add_to_annots(annot_pos, seq[seq_current], 'M')
                seq_current += 1
                q_current += 1
                annot_pos += 1

            if annot_pos > wanted_length:
                break

        finalise_cigars()
        verbose_print(f"{read.qname}: h={haplotype} {seq}", verbose)
        new_contig = Contig(name, annotations, haplotype)

        dupe = False
        for contig in contigs:
            if contig.annotations['allele_sequence'] == new_contig.annotations['allele_sequence'] and contig.haplotype == new_contig.haplotype:
                dupe = True
                break

        if not dupe:
            contigs.append(new_contig)

    # remove hap 0 contigs if we have some that are hap 1 or hap 2

    non_zero_seen = False

    for contig in contigs:
        if contig.haplotype != '0':
            non_zero_seen = True
            break

    if non_zero_seen:
        for i in range(len(contigs)-1, -1, -1):
            if contigs[i].haplotype == '0':
                del contigs[i]

    if verbose:
        print("Contigs added to analysis (excluding duplicates:")
        for contig in contigs:
            if 'v-exon2' in contig.annotations:
                print(f"{contig.header} {contig.haplotype} exon_2: {contig.annotations['v-exon2']}")

    return contigs




def process_rows(label, refname, coord_map, samfile, sample_name, beds, debug_gene):
    rows = []

    # if the sample name contains a .1 or .2 suffix, assume that the file contains genes from haplotype 1 or 2:
    # remove the suffix, and force the haplotype designation

    forced_haplotype = None
    if sample_name[-2:] == '.1':
        forced_haplotype = '1'
        sample_name = sample_name[:-2]
    elif sample_name[-2:] == '.2':
        forced_haplotype = '2'
        sample_name = sample_name[:-2]

    for gene in beds[refname].keys():
        if label in gene:
            annotation_ranges = []
            seq_start = beds[refname][gene]['GENE']['start']
            seq_end = beds[refname][gene]['GENE']['end']
            for annot_key, b_name in coord_map.items():
                annotation_ranges.append((beds[refname][gene][b_name]['start'] - seq_start + 1, beds[refname][gene][b_name]['end'] - seq_start, annot_key))         # 1-based ranges

            if gene == debug_gene:
                print(f"Processing {gene} for {sample_name}. Required range {seq_start} - {seq_end}")

            contigs = fetch_contigs(samfile, refname, seq_start, seq_end, annotation_ranges, gene == debug_gene)

            # TODO - consider trying to fetch a contig for the coding region, if we can't get the whole gene
            
            for contig in contigs:
                row = {
                    'sample_name': sample_name,
                    'haplotype': forced_haplotype if forced_haplotype else contig.haplotype,
                    'gene': gene,
                    'allele': '',
                }
                for k, v in contig.annotations.items():
                    row[k] = v
                rows.append(row)

            # get contigs just covering the V-exon for comparison
            '''if label == 'HV':
                start =  beds['igh'][gene]['exon_2']['start']
                end = beds['igh'][gene]['exon_1']['end']
                exons = fetch_contigs(samfile, 'igh', seq_start, seq_end, [(1, 1 + end - start, 'allele_sequence')], gene == debug_gene)
                if len(contigs) != len(exons):
                    print(f"{gene}: full length {len(contigs)} exon only {len(exons)}") 
                    '''
    return rows


def process_sample(locus, refname, sample_file, sample_name, beds, ref_seq, debug_gene):
    samfile = pysam.AlignmentFile(sample_file)
    rows = []
    rows.extend(process_rows(locus + 'V', refname, v_coord_map, samfile, sample_name, beds, debug_gene))

    if locus in ['IGH', 'TRB', 'TRD']:
        rows.extend(process_rows(locus + 'D', refname, d_coord_map, samfile, sample_name, beds, debug_gene))

    rows.extend(process_rows(locus + 'J', refname, j_coord_map, samfile, sample_name, beds, debug_gene))

    for row in rows:
        for el in output_headers:
            if el not in row:
                row[el] = ''

    return rows


def main():
    parser = argparse.ArgumentParser(description='Extract VDJ gene fields from BAM file(s)')
    parser.add_argument('locus', help='locus (e.g. IGH, IGL)')
    parser.add_argument('refname', help='reference assembly name in SAM files (e.g. chr22)')
    parser.add_argument('sense', help='sense of the genes in the reference sequence: - is 5 to 3, + is 3 to 5')
    parser.add_argument('bed_dir', help='pathname to a directory holding one or more BED files containing the field co-ordinates')
    parser.add_argument('ref_seq', help='pathname to a FASTA file holding the reference sequence (in the same orientation as the BED files use it)')
    parser.add_argument('outfile', help='output file that will contain all the VDJ gene field data (csv)')
    parser.add_argument('--bam_dir', help='pathname to a directory holding one or more BAM files (specify one or other of bam_dir, bam_dirs, bam_file)')
    parser.add_argument('--bam_dirs', help='pathname to a directory holding subdirectories including one or more BAM files (specify one or other of bam_dir, bam_dirs, bam_file)')
    parser.add_argument('--bam_file', help='pathname to a BAM file (specify one or other of bam_dir, bam_dirs, bam_file)')
    parser.add_argument('--debug_gene', help='print debug output on the processing of this gene')
    args = parser.parse_args()

    locus = args.locus
    refname = args.refname
    sense = args.sense

    if not args.bam_dir and not args.bam_dirs and not args.bam_file:
        print('Please specify either bam_dir or bam_file')
        sys.exit(1)
    if args.bam_dir and args.bam_file:
        print('Please specify either bam_dir or bam_file, not both')
        sys.exit(1)

    # fudge for missing UTRs

    if locus not in utr_loci:
        del v_coord_map['V-UTR']

    for coord_map in [v_coord_map, d_coord_map, j_coord_map]:
        for el in coord_map.keys():
            if el not in output_headers:
                output_headers.append(el)
                output_headers.append(el + '_CIGAR')

    if locus not in utr_loci:
        output_headers.append('V-UTR')
        output_headers.append('V-UTR' + '_CIGAR')

    ref_seq = simple.read_single_fasta(args.ref_seq)
    beds = read_bed.read_beds(refname, sense, args.bed_dir, ref_seq)
    rows = []

    if args.bam_dir:
        pathlist = Path(args.bam_dir).glob('*.bam')
        for path in pathlist:
            sample_file = str(path)
            if '.bai' not in sample_file:
                sample_name = os.path.basename(sample_file).replace('.bam', '').replace('_IGL_contig', '')
                print(sample_name)
                rows.extend(process_sample(locus, refname, sample_file, sample_name, beds, ref_seq, args.debug_gene))
    elif args.bam_dirs:
        proj_path = Path(args.bam_dirs)
        for item in proj_path.iterdir():
            if item.is_dir():
                project = item.name
                pathlist = Path(item).glob('*.bam')
                for path in pathlist:
                    sample_file = str(path)
                    if '.bai' not in sample_file:
                        sample_name = project + '-' + os.path.basename(sample_file).replace('.bam', '').split('_')[0]
                        #sample_name = os.path.basename(sample_file).replace('.bam', '').split('_')[0]
                        print(sample_name)
                        rows.extend(process_sample(locus, refname, sample_file, sample_name, beds, ref_seq, args.debug_gene))

    else:
        sample_file = args.bam_file
        sample_name = os.path.basename(sample_file).replace('_assembly_to_franken.bam', '')
        rows.extend(process_sample(locus, refname, sample_file, sample_name, beds, ref_seq, args.debug_gene))


    simple.write_csv(args.outfile, rows)

if __name__ == '__main__':
    main()

