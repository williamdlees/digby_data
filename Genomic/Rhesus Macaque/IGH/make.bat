rm samples/*
python ..\..\..\..\digby_backend\make_genomic_db.py "Rhesus Macaque" IGH
cd samples
wsl ../../../make_bam
7z a -tzip ..\samples.zip *
cd ..