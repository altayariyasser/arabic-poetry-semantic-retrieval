"""Recalculate the saved provisional pooled metrics without loading a model."""
import json,math
from pathlib import Path
E=Path(__file__).resolve().parents[1]/'evaluation'
saved=json.loads((E/'metrics.json').read_text(encoding='utf-8'))
rankings=json.loads((E/'rankings.json').read_text(encoding='utf-8'))
judgments=sum([json.loads((E/n).read_text(encoding='utf-8')) for n in ['ai_judgments.json','supplement_judgments.json']],[])
queries=[q['query_id'] for q in saved['results'][0]['queries']]
results=[]
for method in rankings[queries[0]]:
    per=[]
    for q in queries:
        grades={r['pair_id']:r['grade'] for r in judgments if r['query_id']==q}
        order=rankings[q][method];positive={i for i,g in grades.items() if g>=3}
        assert all(i in grades for i in order)
        r={}
        for k in [1,5,10]:
            found=sum(i in positive for i in order[:k])
            r[f'recall@{k}']=found/len(positive);r[f'hit@{k}']=float(found>0)
        r['mrr@10']=next((1/(i+1) for i,p in enumerate(order) if p in positive),0.)
        dcg=lambda a:sum((2**v-1)/math.log2(i+2) for i,v in enumerate(a))
        r['ndcg@10']=dcg([grades[i] for i in order])/dcg(sorted(grades.values(),reverse=True)[:10])
        per.append(r)
    results.append({'method':method,**{k:sum(r[k] for r in per)/len(per) for k in per[0]}})
for r,expected in zip(results,saved['results']):
    assert r['method']==expected['method']
    assert all(abs(r[k]-expected[k])<1e-12 for k in r if k!='method')
print(json.dumps({'scope':'Three answerable AI-authored/AI-judged development queries; finite depth-ten pooling, no generalization claim.','results':results},indent=2))
