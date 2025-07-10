rm samples*.zip 
rm -rf samples/*
call gunzip *.gz
python ../../../../digby_backend/make_genomic_db.py Human IGHC
cd samples
wsl ../make_bam
rm ../samples.z*
7z a ../samples.zip *
cd ..
python ../../../../digby_data/python/commit_sample_file.py
gzip *.csv
