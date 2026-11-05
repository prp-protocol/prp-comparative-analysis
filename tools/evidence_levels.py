"""Reviewed evidence annotations, orthogonal to capability verdicts."""
import hashlib
import json
from pathlib import Path

CELL_CSS='''
.matrix td{position:relative;vertical-align:top}
.matrix td a.cell-evidence-link{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;box-sizing:border-box;min-height:0;padding:0}
.matrix .cell-verdict{display:block;font-weight:600;line-height:1.35}
.matrix .cell-evidence-level{position:absolute;left:0;right:0;bottom:0;
display:block;margin:0;padding:8px 3px;box-sizing:border-box;font-size:10px;font-weight:400;line-height:1.2;
color:#354c55;background:#e4e1ef;border-radius:0 0 5px 5px;white-space:normal;overflow-wrap:normal}
.matrix td:has(.evidence-aligned){vertical-align:middle}
.matrix td:has(.evidence-aligned) a.cell-evidence-link{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;min-height:0;padding:0}
.matrix .cell-evidence-level.evidence-aligned{display:none}
@media print{.matrix td a.cell-evidence-link{min-height:0;padding:0}
.matrix .cell-evidence-level{font-size:6px;bottom:4px;left:2px;right:2px}}
'''

LEVELS = {
 'assumed': {'label': 'Assumed', 'definition': 'Plausible inference from architecture; premises and limits must be explicit.'},
 'reported': {'label': 'Reported', 'definition': 'Explicit attributable statement, without enough inspected documentation to independently establish the mechanism or finding.'},
 'documented': {'label': 'Documented', 'definition': 'Identifiable specification or source code supports the decision within the selected scope.'},
 'demonstrated': {'label': 'Demonstrated', 'definition': 'Reproducible execution evidence supports the decision within the stated test scope.'},
}
POLICY = {'version': 1, 'levels': LEVELS,
 'unclassified': 'Temporary annotation state, not a fifth evidence level and not equivalent to Pending.',
 'interpretation': 'Evidence basis, not protocol maturity or a quality ranking. No automatic verdict changes. A demonstration may support Yes or No; partial coverage must be disclosed. Authorship and independence are separate from the level.'}
POLICY['display_rule']='Hide the evidence band and center the verdict for demonstrated Yes, or reported/documented/demonstrated No. Other bands remain distinct, including Pending. The accessible link label and cell detail retain the evidence level, scope and qualifications.'

def aligned(status, level):
 return (status=='Y' and level=='demonstrated') or (status=='N' and level in ('reported','documented','demonstrated'))

def fingerprint(data, ident):
 fid, sid = ident.split('-')
 payload = {'resolution': data['resolutions'][ident],
            'criterion': next(r[:2]+r[3:] for r in data['rows'] if r[0] == fid),
            'profile': next(c for c in data['columns'] if c[0] == sid)}
 return hashlib.sha256(json.dumps(payload, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

def annotate(data):
 reviews=json.loads((Path(__file__).parent/'evidence-reviews.json').read_text())
 data['evidence_policy']=POLICY
 for cell in data['cells']:
  ident=cell['feature']+'-'+cell['stack'];review=reviews.get(ident)
  if review and review['basis_sha256']==fingerprint(data,ident):
   assert review['level'] in LEVELS
   cell['evidence']=review.copy()
  else:
   cell['evidence']={'level':'unclassified','scope':'Not yet classified.' if not review else 'Underlying decision, criterion or profile changed; classification requires review.'}
 return data

def label(evidence):
 return LEVELS.get(evidence['level'], {'label':'Unclassified'})['label']

def detail_html(evidence):
 from html import escape
 out='<h2>Evidence level</h2><p><strong>'+escape(label(evidence))+'</strong></p>'
 for name,key in [('Scope','scope'),('Basis','basis'),('Attribution','attribution'),('Coverage','coverage'),('Reviewed','reviewed_at')]:
  if evidence.get(key):out+='<p><strong>'+name+':</strong> '+escape(evidence[key])+'</p>'
 return out
