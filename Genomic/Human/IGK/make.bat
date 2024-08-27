rm -rf samples/*
python ../../../../digby_backend/make_genomic_db.py Human IGK
cd samples
wsl ../make_bam
rm ../samples.z*
7z a ../samples.zip *
cd ..
python ../../../../digby_data/python/commit_sample_file.py