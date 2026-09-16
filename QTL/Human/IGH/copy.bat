mkdir -p ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/annotation
mkdir -p ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/dbsnp
cp db.sqlite3 ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/.
cp db_description.txt ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/.
cp -r annotation/* ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/annotation/.
cp -r dbsnp/* ../../../../digby_backend/static/study_data/QTL/db/Human/IGH/dbsnp/.
