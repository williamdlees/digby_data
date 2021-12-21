#
# Put all the sequences we have in a simple ascending order
# oddballs get thrown to the end

import simple_bio_seq as simple


def gene_number(name):
    key = 9999
    if '*' in name:
        name = name.split('*')[0]

    name = name[4:]
    if '-' in name:
        name = name.split('-')[1]

    dupe = False
    if name[-1] == 'D':
        name = name[:-1]
        dupe = True

    if name.isdigit():
        key = int(name) * 10
        if dupe:
            key += 5

    return key


fasta_proto = 'Macaca_fascicularis_IGH%s.fasta'
chains = ['V', 'D', 'J']

gene_order = []

for chain in chains:
    names = []

    for name in simple.read_fasta(fasta_proto % chain).keys():
        if '*' in name:
            name = name.split('*')[0]

        if name not in names:
            names.append(name)

    names.sort(key=gene_number)
    gene_order.extend(names)


with open('gene_order.py', 'w') as fo:
    for order in ['LOCUS', 'ALPHA']:
        fo.write('%s_ORDER = [\n' % order)
        for name in gene_order:
            fo.write('"%s",\n' % name)
        fo.write(']\n')

    fo.write('PSEUDO_GENES = []\n')

