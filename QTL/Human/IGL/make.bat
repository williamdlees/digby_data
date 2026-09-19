python ../../../../digby_backend/make_qtl_db.py Human IGL >make.log
cd annotation
zip -r ../annotation.zip *
cd ..
zip db.zip db.sqlite3
python ../../../../digby_data/python/commit_sample_file.py --file db.zip
