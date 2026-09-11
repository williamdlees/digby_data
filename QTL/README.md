# guQTL data

Gene-usage QTL results: which variants in a locus change how much each gene is
used. Built the same way as `AIRR-seq` and `Genomic` — run `make.bat` in a locus
directory, then `copy.bat` to install.

One database per locus, holding every study built there. A scan is computed
within one cohort and never pooled across cohorts, so each study is a `qtl_run`
row and `run_id` scopes the tables that hang off it. `qtl_data_model.png` is the
schema, generated from `db/qtl_model.py` by `../python/qtl_data_model.py`.

## A locus directory

    Human/IGH/
      human_igh_qtl.yml          which studies to build, and where each one is
      P28_PRJNA555323.json       the run manifest for study P28
      make.bat  copy.bat
      db.sqlite3  make.log  db_description.txt     built here, not committed
      annotation/                BED release the scan was run against
      dbsnp/                     GRCh38 to IGH position map (IGH only)
      studies/P28/               the run output, below

| File | Purpose |
|---|---|
| `human_<locus>_qtl.yml` | Names each study, its run directory and its manifest. Adding a study is a line here. |
| `P28_PRJNA555323.json` | What the run wrote: the column and row count of every file (checked at build time), the significance thresholds, and the annotation release. |
| `annotation/` | The immune receptor genomics BED release. Fixes every gene and feature call, so it has to be the release the scan used — `RELEASE.txt` states it. |
| `dbsnp/` | GRCh38 to IGH locus-relative position map, for reporting rs identifiers. IGH only, chr14. |

## `studies/<project>/`

| File | Purpose | Loci |
|---|---|---|
| `usage_associations_<locus>.tsv.gz` | One row per variant and gene cluster: effect, p-value, whether it is significant, whether it is a lead, and the power columns. | all |
| `genotypes.matrix` | Variant by subject, one call per cell. Drives the per-genotype plots. | all |
| `variant_features.tsv` | The gene and feature each variant falls in. | all |
| `asc_usage.tsv.gz` | Usage per subject per cluster: the phenotype the scan modelled. | all |
| `pairing.tsv.gz` | Whether a variant shifts D–J pairing, per anchor gene and direction. | IGH |
| `cell_tests.tsv.gz` | The same test per individual D–J pair. | IGH |
| `dj_enrichment.tsv.gz` | Observed D–J pairing per subject: what the pairing panel draws. | IGH |

IGK and IGL have no pairing scan, so they carry four files rather than seven.

## Building

    cd Human/IGH
    make.bat          # python ../../../../digby_backend/make_qtl_db.py Human IGH
    copy.bat          # installs db.sqlite3, annotation/ and dbsnp/

`db.sqlite3` is not committed. IGH's is 191MB, over GitHub's 100MB file limit,
and everything needed to rebuild it is here, so run `make.bat` after cloning.
This is the one way this dataset differs from `AIRR-seq` and `Genomic`, whose
databases are committed because their sample data lives in S3 rather than in the
repository.

The build refuses to run if a file's columns or row count differ from what the
manifest declares, so a renamed column upstream stops the build rather than
quietly filling a table with nulls.

Rebuilding one study replaces only that study's rows; the others are left alone.

## Provenance

Each database records, in `qtl_run.config`, the run it came from, the annotation
release and the files it read. The annotation release must match the installed
`annotation/RELEASE.txt` or every feature call moves silently.
