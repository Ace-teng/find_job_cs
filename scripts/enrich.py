"""Merge reviewed, specific interview drills without changing existing progress IDs."""
import hashlib
import json
from pathlib import Path

def enrich(data):
    content=json.loads(Path('content/drills.json').read_text())
    data['sources'].update(content['sources'])
    data['interviewWindow']=content['interviewWindow']
    lookup={n['name']:n for n in data['nodes']}
    edgekeys={(e['from'],e['to'],e['type']) for e in data['edges']}
    for q in data['questions']:
        q['kind']='概念总览';q['origin']='总览';q['references']=[q['source']]
    for item in content['questions']:
        q={k:v for k,v in item.items() if k not in ['concepts','relations']}
        q['nodes']=[]
        q['origin']='面经改编' if q.get('report') else '文档练习'
        for name in item['concepts']:
            if name not in lookup:
                n={'id':'c-'+hashlib.sha1(name.encode()).hexdigest()[:12],'name':name,'roles':[],'modules':[],'sources':[]}
                lookup[name]=n;data['nodes'].append(n)
            n=lookup[name];q['nodes'].append(n['id'])
            for key,vals in [('roles',q['roles']),('modules',[q['module']]),('sources',q['references'])]:
                n[key]=list(dict.fromkeys(n[key]+vals))
        q['source']=q['references'][0]
        q['cue']='；'.join(q['points'])
        data['questions'].append(q)
        rels=[(a,b,'追问') for a,b in zip(item['concepts'],item['concepts'][1:])]+item.get('relations',[])
        for a,b,t in rels:
            x,y=lookup[a]['id'],lookup[b]['id']
            if (x,y,t) not in edgekeys:
                data['edges'].append({'from':x,'to':y,'type':t});edgekeys.add((x,y,t))
    chains=json.loads(Path('content/chains.json').read_text())
    data['sources'].update(chains['sources'])
    data['chains']=chains['chains']
    data['version']=3
    return data
