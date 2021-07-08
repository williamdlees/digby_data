# update airr datasets in digby_backend
# run this from digby_data top-level directory
# assumes digby_backend is at ../digby_backend

import argparse
import os
from os.path import basename, isdir, join


parser = argparse.ArgumentParser(description='Update airr datasets in digby backend')
parser.add_argument('species', help='species name')
parser.add_argument('dataset', help='dataset (or all, for all datasets of that species)')
args = parser.parse_args()
import shutil

if basename(os.getcwd()) != 'digby_data':
    print('Please run from ./digby_data')
    quit()

if not isdir('../digby_backend'):
    print('digby_backend must be at ,,/digby_backend')
    quit()

species_path = join('AIRR-seq', args.species)
db_data_path = '../digby_backend/static/study_data/VDJbase'

if not isdir(species_path):
    print('No AIRR-seq data found for species %s' % args.species)
    quit()

if args.dataset == 'all':
    datasets = [d for d in os.listdir(species_path) if isdir(os.path.join(species_path, d)) and d != '.' and d != '..']
else:
    datasets = [args.dataset]

for dataset in datasets:
    print('Updating %s' % dataset)
    dataset_path = join(species_path, dataset)

    # set up the empty directories in digby_data

    dd_path = {}
    for pt in ['db', 'samples']:
        pp = join(db_data_path, pt)
        if not isdir(pp):
            os.mkdir(pp)
        pp = join(pp, args.species)
        if not isdir(pp):
            os.mkdir(pp)
        pp = join(pp, dataset)
        if isdir(pp):
            shutil.rmtree(pp)
        os.mkdir(pp)
        dd_path[pt] = pp

    # Copy database and description to static and to digby_backend root

    for f in ['db.sqlite3', 'db_description.txt']:
        shutil.copy2(join(dataset_path, f), join(dd_path['db'], f))
        shutil.copy2(join(dataset_path, f), join('../digby_backend', f.replace('db', '%s_%s_db' % (args.species, dataset))))

    # Zip data to digby_backend root

    zipname = '../digby_backend/%s_%s_samples' % (args.species, dataset)
    shutil.make_archive(zipname, 'zip', root_dir=join(dataset_path, 'samples'), base_dir='./')

    # Unzip data to samples directory

    shutil.unpack_archive(zipname + '.zip', dd_path['samples'])


