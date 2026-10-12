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
