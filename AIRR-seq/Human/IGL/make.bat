python ../../../../digby_backend/make_vdjbase_db.py Human IGL >make.log
cd samples
zip -r ../samples.zip *
cd ..
python ../../../../digby_data/python/commit_sample_file.py
