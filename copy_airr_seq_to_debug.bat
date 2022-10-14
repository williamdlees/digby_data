cp AIRR-seq/Human/IGH/db.sqlite3 ../digby_backend/static/study_data/VDJbase/db/Human/IGH/db.sqlite3
cp AIRR-seq/Human/IGH/db_description.txt ../digby_backend/static/study_data/VDJbase/db/Human/IGH/db_description.txt
rm -rf ../digby_backend/static/study_data/VDJbase/samples/Human/IGH/*
unzip -q AIRR-seq/Human/IGH/samples.zip -d ../digby_backend/static/study_data/VDJbase/samples/Human/IGH
cp AIRR-seq/Human/IGK/db.sqlite3 ../digby_backend/static/study_data/VDJbase/db/Human/IGK/db.sqlite3
cp AIRR-seq/Human/IGK/db_description.txt ../digby_backend/static/study_data/VDJbase/db/Human/IGK/db_description.txt
rm -rf ../digby_backend/static/study_data/VDJbase/samples/Human/IGK/*
unzip -q AIRR-seq/Human/IGK/samples.zip -d ../digby_backend/static/study_data/VDJbase/samples/Human/IGK
cp AIRR-seq/Human/IGL/db.sqlite3 ../digby_backend/static/study_data/VDJbase/db/Human/IGL/db.sqlite3
cp AIRR-seq/Human/IGL/db_description.txt ../digby_backend/static/study_data/VDJbase/db/Human/IGL/db_description.txt
rm -rf ../digby_backend/static/study_data/VDJbase/samples/Human/IGL/*
unzip -q AIRR-seq/Human/IGK/samples.zip -d ../digby_backend/static/study_data/VDJbase/samples/Human/IGL
cp AIRR-seq/Human/TRB/db.sqlite3 ../digby_backend/static/study_data/VDJbase/db/Human/TRB/db.sqlite3
cp AIRR-seq/Human/TRB/db_description.txt ../digby_backend/static/study_data/VDJbase/db/Human/TRB/db_description.txt
rm -rf ../digby_backend/static/study_data/VDJbase/samples/Human/TRB/*
unzip -q AIRR-seq/Human/TRB/samples.zip -d ../digby_backend/static/study_data/VDJbase/samples/Human/TRB

cp "AIRR-seq/Crab-eating Macaque/IGH/db.sqlite3" "../digby_backend/static/study_data/VDJbase/db/Crab-eating Macaque/IGH/db.sqlite3"
cp "AIRR-seq/Crab-eating Macaque/IGH/db_description.txt" "../digby_backend/static/study_data/VDJbase/db/Crab-eating Macaque/IGH/db_description.txt"
rm -rf "../digby_backend/static/study_data/VDJbase/samples/Crab-eating Macaque/IGH"
mkdir "../digby_backend/static/study_data/VDJbase/samples/Crab-eating Macaque/IGH"
unzip -q "AIRR-seq/Crab-eating Macaque/IGH/samples.zip" -d "../digby_backend/static/study_data/VDJbase/samples/Crab-eating Macaque/IGH"
cp "AIRR-seq/Rhesus Macaque/IGH/db.sqlite3" "../digby_backend/static/study_data/VDJbase/db/Rhesus Macaque/IGH/db.sqlite3"
cp "AIRR-seq/Rhesus Macaque/IGH/db_description.txt" "../digby_backend/static/study_data/VDJbase/db/Rhesus Macaque/IGH/db_description.txt"
rm -rf "../digby_backend/static/study_data/VDJbase/samples/Rhesus Macaque/IGH"
mkdir "../digby_backend/static/study_data/VDJbase/samples/Rhesus Macaque/IGH"
unzip -q "AIRR-seq/Rhesus Macaque/IGH/samples.zip" -d "../digby_backend/static/study_data/VDJbase/samples/Rhesus Macaque/IGH"
