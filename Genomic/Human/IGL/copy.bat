cp db.sqlite3 ../../../../digby_backend/static/study_data/Genomic/db/Human/IGL/.
cp db_description.txt ../../../../digby_backend/static/study_data/Genomic/db/Human/IGL/.
rm -rf ../../../../digby_backend/static/study_data/Genomic/samples/Human/IGL/samples/*
cp -r samples/* ../../../../digby_backend/static/study_data/Genomic/samples/Human/IGL/.

