python ../../../../digby_backend/make_qtl_db.py Human IGH >make.log
cd annotation
zip -r ../annotation.zip *
cd ..
cd dbsnp
zip -r ../dbsnp.zip *
cd ..
zip db.zip db.sqlite3
python ../../../../digby_data/python/commit_sample_file.py --file db.zip
