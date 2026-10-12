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
