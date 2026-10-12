import fs from 'node:fs';
import assert from 'node:assert/strict';
const d=JSON.parse(fs.readFileSync(new URL('../data.json',import.meta.url)));
const unique=(xs,key)=>assert.equal(new Set(xs.map(x=>x[key])).size,xs.length,`Duplicate ${key}`);
unique(d.nodes,'id');unique(d.nodes,'name');unique(d.questions,'id');unique(d.roles,'id');
const nodes=new Set(d.nodes.map(n=>n.id)),roles=new Set(d.roles.map(r=>r.id));
for(const n of d.nodes){assert(n.name&&n.modules.length&&n.sources.length);n.roles.forEach(r=>assert(roles.has(r)));n.sources.forEach(s=>assert(d.sources[s]));}
for(const e of d.edges){assert(nodes.has(e.from)&&nodes.has(e.to));assert.notEqual(e.from,e.to);assert(e.type);}
for(const q of d.questions){assert(q.title&&q.cue&&q.nodes.length>=2);q.nodes.forEach(n=>assert(nodes.has(n)));q.roles.forEach(r=>assert(roles.has(r)));assert(d.sources[q.source]);}
for(const r of d.roles)assert(d.questions.some(q=>q.roles.includes(r.id)),`Empty role ${r.id}`);
console.log(`Validated ${d.roles.length} roles / ${d.questions.length} questions / ${d.nodes.length} concepts / ${d.edges.length} relations`);
const window=d.interviewWindow;
assert(window&&window.from<=window.through);
for(const [id,s] of Object.entries(d.sources)){
  assert(/^https:\/\//.test(s.url),`Invalid source URL ${id}`);
  if(s.kind==='公开面经'){
    assert(/^\d{4}-\d{2}-\d{2}$/.test(s.date),`Ambiguous date ${id}`);
    assert(s.date>=window.from&&s.date<=window.through,`Outdated interview ${id}`);
    if(s.endDate)assert(s.endDate>=s.date&&s.endDate<=window.through);
    assert(s.dateType&&s.company&&s.job&&s.notice,`Missing provenance ${id}`);
  }
}
for(const q of d.questions){
  assert(q.references.every(id=>d.sources[id]),`Unknown reference ${q.id}`);
  if(q.origin!=='总览'){
    assert(q.scenario&&q.pitfall&&q.points.length>=2&&q.followups.length>=2,`Incomplete drill ${q.id}`);
    assert(['基础追问','场景分析','手写题','项目深挖'].includes(q.kind));
    if(q.report)assert(d.sources[q.report]?.kind==='公开面经');
    else assert.equal(q.origin,'文档练习');
  }
}
for(const r of d.roles)assert(d.questions.some(q=>q.roles.includes(r.id)&&q.origin!=='总览'),`No specific drills ${r.id}`);
console.log('Recent interview dates, provenance, and drill completeness validated');
assert.equal(d.version,3);
unique(d.chains,'id');
const chainIds=new Set(d.chains.map(c=>c.id));
const questions=new Map(d.questions.map(q=>[q.id,q]));
const stepIdentity=new Map();
for(const c of d.chains){
  assert(c.title&&c.group&&c.reviewed&&c.roles.length&&c.references.length,`Incomplete chain ${c.id}`);
  assert(c.steps.length>=4,`Too short ${c.id}`);
  unique(c.steps,'id');
  c.roles.forEach(r=>assert(roles.has(r),`Unknown role ${r}`));
  c.references.forEach(s=>assert(d.sources[s],`Unknown chain source ${s}`));
  c.related.forEach(id=>assert(chainIds.has(id)&&id!==c.id,`Invalid branch ${c.id} -> ${id}`));
  c.steps.forEach((s,i)=>{
    assert(/^[a-z0-9-]+$/.test(s.id),`Unsafe step ID ${s.id}`);
    assert(s.stage&&(!i||s.why?.length>=8),`Missing transition ${c.id}:${i}`);
    if(s.questionId){assert(questions.has(s.questionId));assert.equal(s.id,s.questionId,`Progress ID mismatch ${s.id}`);}
    else assert(s.title&&s.focus,`Missing authored question ${s.id}`);
    const identity=s.questionId||s.title;
    assert(!stepIdentity.has(s.id)||stepIdentity.get(s.id)===identity,`Conflicting progress ID ${s.id}`);
    stepIdentity.set(s.id,identity);
  });
}
for(const r of d.roles)assert(d.chains.filter(c=>c.roles.includes(r.id)).length>=4,`Insufficient topics ${r.id}`);
console.log(`Validated ${d.chains.length} chains / ${d.chains.reduce((n,c)=>n+c.steps.length,0)} steps / ${stepIdentity.size} unique progress IDs`);
const chainSource=JSON.parse(fs.readFileSync(new URL('../content/chains.json',import.meta.url)));
assert.deepEqual(d.chains,chainSource.chains,'Run python3 scripts/seed.py after editing chains');
for(const [id,source] of Object.entries(chainSource.sources))assert.deepEqual(d.sources[id],source);
