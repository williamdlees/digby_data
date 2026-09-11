"""Draw the guQTL schema in the style of Genomic/genomic_data_model.png.

    python qtl_db_schema.py <out.png>

Read from db/qtl_model.py, so it cannot drift from the schema. Run from the
digby_backend directory.
"""
import subprocess, sys, os
sys.path.insert(0, os.getcwd())
from sqlalchemy import Integer, Float, Boolean
from db.qtl_model import Base

BG     = '#2f2f2f'   # canvas
FILL   = '#404040'   # table body
HEADBG = '#202020'   # table header
BORDER = '#0064ae'   # table outline and relationship lines
NAME   = '#c4c4c4'   # column names
HEADFG = '#c4c4c4'   # table name
NUM    = '#008fcf'   # 123 marker
STR    = '#865941'   # ABC marker
KEYFG  = '#9bc4b0'   # key columns

# Read from the model: every relationship is a declared ForeignKey, as in
# vdjbase_model.py and genomic_db.py. Dashed where the column is nullable -
# a pointer the builder caches rather than structure the schema requires.
JOINS = []
for _t in Base.metadata.tables.values():
    for _c in _t.columns:
        for _fk in _c.foreign_keys:
            JOINS.append((_t.name, _c.name, _fk.column.table.name,
                          'dashed' if _c.nullable else 'solid'))
KEYS = {(t, c) for t, c, _, _ in JOINS}

ORDER = ['qtl_run', 'qtl_threshold', 'details', 'qtl_subject', 'qtl_asc', 'qtl_variant',
         'qtl_asc_usage', 'qtl_dosage', 'qtl_usage_association',
         'qtl_pairing_association', 'qtl_cell_test', 'qtl_dj_enrichment']

def box(name):
    t = Base.metadata.tables[name]
    rows = [f'<TR><TD BGCOLOR="{HEADBG}" ALIGN="CENTER" CELLPADDING="4">'
            f'<FONT COLOR="{NUM}" POINT-SIZE="9">▤ </FONT>'
            f'<FONT COLOR="{HEADFG}" POINT-SIZE="12"><B>{name}</B></FONT></TD></TR>']
    for col in t.columns:
        key = col.primary_key or (name, col.name) in KEYS
        mark, mcol = (('123', NUM) if isinstance(col.type, (Integer, Float, Boolean))
                      else ('ABC', STR))
        o, c = ('<B>', '</B>') if key else ('', '')
        rows.append(f'<TR><TD ALIGN="LEFT" PORT="{col.name}">'
                    f'<FONT COLOR="{mcol}" POINT-SIZE="7">{mark} </FONT>'
                    f'<FONT COLOR="{KEYFG if key else NAME}" POINT-SIZE="10">'
                    f'{o}{col.name}{c}</FONT></TD></TR>')
    return (f'  "{name}" [label=<<TABLE BORDER="1" CELLBORDER="0" CELLSPACING="0" '
            f'CELLPADDING="2" BGCOLOR="{FILL}" COLOR="{BORDER}">'
            + ''.join(rows) + '</TABLE>>];')

edges = [f'  "{t}":{c} -> "{target}":id [color="{BORDER}", style={style}, '
         f'arrowhead=none, arrowtail=odot, dir=back];'
         for t, c, target, style in JOINS]

dot = f'''digraph guqtl {{
  graph [bgcolor="{BG}", rankdir=LR, splines=spline, nodesep=0.35, ranksep=1.4,
         fontname="Helvetica", pad=0.3];
  node  [shape=plaintext, fontname="Helvetica"];
  edge  [penwidth=1.2];

{chr(10).join(box(n) for n in ORDER if n in Base.metadata.tables)}

{chr(10).join(edges)}
}}
'''
out = sys.argv[1]
dot_path = os.path.splitext(out)[0] + '.dot'
open(dot_path, 'w').write(dot)
subprocess.run(['dot', '-Tpng', '-Gdpi=110', dot_path, '-o', out], check=True)
os.remove(dot_path)
print('wrote', out)
