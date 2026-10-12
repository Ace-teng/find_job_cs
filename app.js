'use strict';
const $ = id => document.getElementById(id);
const esc = s => String(s ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const KEY = 'internship-atlas-v1';
let D, Q, N, role = 'frontend', topic = '', query = '', company = '', filter = 'all', practice = false, revealed = 1;
let saved = { questions: {}, theme: 'light' };
try {
  const v = JSON.parse(localStorage.getItem(KEY));
  if (v && v.questions && typeof v.questions === 'object' && !Array.isArray(v.questions)) saved = { questions: v.questions, theme: v.theme === 'dark' ? 'dark' : 'light' };
} catch { /* Storage is optional; export remains available. */ }
function state(id) { const s = saved.questions[id]; return { status: ['todo','weak','done'].includes(s?.status) ? s.status : 'todo', star: s?.star === true }; }
function toast(message) { $('toast').textContent = message; $('toast').classList.add('visible'); clearTimeout(toast.timer); toast.timer = setTimeout(() => $('toast').classList.remove('visible'), 2800); }
function persist() { try { localStorage.setItem(KEY, JSON.stringify(saved)); } catch { toast('浏览器无法保存，请导出进度备份'); } }
function theme() { document.body.classList.toggle('dark', saved.theme === 'dark'); $('theme').textContent = saved.theme === 'dark' ? '浅色' : '深色'; }
theme();
function steps(c) { return c.steps.map(s => ({ ...s, title: s.title || Q[s.questionId]?.title, q: Q[s.questionId] })); }
function roleChains() { return D.chains.filter(c => c.roles.includes(role)); }
function textFor(s) { return [s.title, s.q?.scenario, ...(s.q?.nodes || []).map(n => N[n].name)].join(' ').toLowerCase(); }
function searched(s) { return !!query.trim() && textFor(s).includes(query.trim().toLowerCase()); }
function matches(c) {
  const ss = steps(c), term = query.trim().toLowerCase();
  return (!term || [c.title,c.group].join(' ').toLowerCase().includes(term) || ss.some(searched))
    && (!company || ss.some(s => s.q?.report && D.sources[s.q.report].company === company))
    && (filter === 'all' || (filter === 'done' ? ss.every(s => state(s.id).status === 'done') : ss.some(s => filter === 'star' ? state(s.id).star : state(s.id).status === filter)));
}
function actionHTML(s) {
  const v = state(s.id);
  return `<div class="step-actions"><select data-status="${s.id}" aria-label="第 ${s.number} 问掌握程度">${[['todo','待复习'],['weak','不熟'],['done','已掌握']].map(([id,label]) => `<option value="${id}" ${id === v.status ? 'selected' : ''}>${label}</option>`).join('')}</select><button data-star="${s.id}" aria-label="${v.star ? '取消收藏' : '收藏'}第 ${s.number} 问" aria-pressed="${v.star}">${v.star ? '★ 已收藏' : '☆ 收藏'}</button><button data-link="${s.id}" aria-label="复制第 ${s.number} 问链接">↗</button></div>`;
}
function sourceLink(id) {
  const s = D.sources[id]; if (!s) return '';
  return `<li><a href="${esc(s.url)}" target="_blank" rel="noopener">${esc(s.name)} ↗</a><small>${esc(s.kind || '技术参考')}${s.version ? ' · '+esc(s.version) : ''}${s.verified ? ' · 核验 '+s.verified : ''}</small></li>`;
}
function reportHTML(q) {
  if (!q?.report) return '';
  const r = D.sources[q.report];
  return `<div class="evidence"><a href="${esc(r.url)}" target="_blank" rel="noopener">${esc(r.company)} · ${r.date.slice(0,4)} 面经主题 ↗</a><span>${esc(r.dateType)} ${r.date}${r.endDate ? ' — '+r.endDate : ''} · ${esc(r.job)}</span><p>${esc(r.notice)} 该问经编辑改写。</p></div>`;
}
function answerHTML(s, c) {
  const q = s.q;
  return `<details class="answer"><summary>回答抓手与参考 <span>按需展开</span></summary><div class="answer-body">${q?.scenario ? `<p class="scenario">场景：${esc(q.scenario)}</p>` : ''}${q?.points ? `<ul>${q.points.map(p => `<li>${esc(p)}</li>`).join('')}</ul>` : `<p>${esc(s.focus || q?.cue || '')}</p>`}${q?.pitfall ? `<p class="pitfall">易错点：${esc(q.pitfall)}</p>` : ''}${q?.nodes ? `<p class="concepts">关联概念：${q.nodes.map(n => esc(N[n].name)).join(' · ')}</p>` : ''}${reportHTML(q)}<ul class="sources">${(q?.references || c.references).map(sourceLink).join('')}</ul></div></details>`;
}
function renderSummary() {
  const ids = [...new Set(roleChains().flatMap(c => c.steps.map(s => s.id)))];
  const done = ids.filter(id => state(id).status === 'done').length;
  const weak = ids.filter(id => state(id).status === 'weak').length;
  $('progress-label').textContent = `${done} / ${ids.length} 问已掌握`;
  $('stats').textContent = `${roleChains().length} 条话题链 · ${weak} 问不熟`;
  $('progress').style.width = (ids.length ? done / ids.length * 100 : 0)+'%';
}
function renderDirectory() {
  const list = roleChains().filter(matches);
  $('results-count').textContent = `${list.length} 条`;
  const groups = [...new Set(list.map(c => c.group))];
  $('topics').innerHTML = groups.map(g => `<section class="topic-group"><h2>${esc(g)}</h2>${list.filter(c => c.group === g).map(c => {
    const done = c.steps.filter(s => state(s.id).status === 'done').length;
    return `<button class="topic-link ${topic === c.id ? 'active' : ''}" data-topic="${c.id}" ${topic === c.id ? 'aria-current="true"' : ''}><span>${esc(c.title)}</span><small>${c.steps.length} 问 <span>${done === c.steps.length ? '✓ 已掌握' : done+' 已掌握'}</span></small></button>`;
  }).join('')}</section>`).join('') || '<p class="empty">没有匹配的话题。试试清空搜索或筛选。</p>';
  renderSummary();
  return list;
}
function renderChain() {
  const c = D.chains.find(c => c.id === topic && c.roles.includes(role));
  if (!c) { $('chain').innerHTML = '<div class="empty"><h2>没有匹配的追问链</h2><p>换个关键词，或重置筛选继续复习。</p><button data-reset>重置筛选</button></div>'; return; }
  const ss = steps(c), shown = practice ? ss.slice(0, revealed) : ss;
  const done = ss.filter(s => state(s.id).status === 'done').length;
  $('chain').innerHTML = `<div class="chain-heading"><div class="eyebrow">03 / 沿着问题往下走</div><h2>${esc(c.title)}</h2><p class="chain-meta">${ss.length} 问 · <span id="chain-progress">${done} 已掌握</span> · 核验 ${c.reviewed}</p><div class="chain-tools"><button id="practice" aria-pressed="${practice}">${practice ? '查看整条链' : '开始逐问自测'}</button><span>${practice ? '先口述，再揭开下一问' : '默认只看问题，答案按需展开'}</span></div><p class="editor-note">追问顺序为编辑整理；带公司标签的单问附近期面经出处。</p>${query ? '<p class="search-note">已保留上下文；命中的问题会单独标记。</p>' : ''}</div><ol class="question-chain">${shown.map((s,i) => {
    s.number = i+1;
    return `<li class="step ${searched(s) ? 'matched' : ''}" id="step-${s.id}">${i ? `<div class="bridge"><span aria-hidden="true">↓</span><p>${esc(s.why)}</p></div>` : ''}<div class="step-content"><span class="step-number" aria-hidden="true">${String(i+1).padStart(2,'0')}</span><div class="step-main"><div class="step-kicker">${esc(s.stage)}${searched(s) ? '<b>搜索命中</b>' : ''}${s.q?.report ? `<a href="${esc(D.sources[s.q.report].url)}" target="_blank" rel="noopener">${esc(D.sources[s.q.report].company)} ${D.sources[s.q.report].date.slice(0,4)} · 面经改编 ↗</a>` : '<span>编辑追问</span>'}</div><h3>${esc(s.title)}</h3>${s.q?.code ? `<pre><code>${esc(s.q.code)}</code></pre>` : ''}${actionHTML(s)}${answerHTML(s,c)}</div></div></li>`;
  }).join('')}</ol>${practice && revealed < ss.length ? `<button class="next-question" id="next">继续下一问 <span>${revealed} / ${ss.length} →</span></button>` : `<div class="chain-end"><span>✓</span><div><b>这条链走完了</b><p>能顺着讲清楚每一问，再用自己的项目串一次。</p></div></div>`}<section class="branches"><h3>面试官也可能转向</h3>${c.related.map(id => D.chains.find(x => x.id === id && x.roles.includes(role))).filter(Boolean).map(x => `<button data-topic="${x.id}">${esc(x.title)} <span>→</span></button>`).join('') || '<p>回到话题目录，继续准备其他方向。</p>'}</section><details class="topic-sources"><summary>话题来源与更新说明</summary><p>新增问句和衔接为编辑组织，不代表某家公司实际完整提问顺序。技术参考支持相关语义；公开面经仅支持明确标注的主题。你补充的新资料可通过仓库内容文件持续更新。</p><ul class="sources">${c.references.map(sourceLink).join('')}</ul></details>`;
}
function setTopic(id, navigate = true) {
  const c = D.chains.find(c => c.id === id && c.roles.includes(role)); if (!c) return;
  topic = c.id; practice = false; revealed = 1; renderDirectory(); renderChain();
  if (navigate) { history.pushState(null,'',`#${role}/topic/${topic}`); $('chain').focus({preventScroll:true}); $('chain').scrollIntoView({block:'start'}); }
}
function resetFilters() { query=''; company=''; filter='all'; $('search').value=''; $('company').value=''; $('filter').value='all'; }
function selectRole(id) {
  role = D.roles.some(r => r.id === id) ? id : 'frontend'; resetFilters();
  const r = D.roles.find(r => r.id === role);
  $('crumb').textContent = r.name; $('role-title').textContent = r.name+' · 面试追问链';
  $('roles').innerHTML = D.roles.map(r => `<a class="role-link ${r.id === role ? 'active' : ''}" href="#${r.id}" ${r.id === role ? 'aria-current="page"' : ''}><span>${esc(r.number)}</span>${esc(r.name)}</a>`).join('');
  const reports = roleChains().flatMap(c => steps(c)).filter(s => s.q?.report).map(s => D.sources[s.q.report].company);
  $('company').innerHTML = '<option value="">全部面经来源</option>'+[...new Set(reports)].map(c => `<option>${esc(c)}</option>`).join('');
}
function applyFilters() {
  const list = roleChains().filter(matches);
  if (!list.some(c => c.id === topic)) { topic=list[0]?.id || ''; practice=false; revealed=1; }
  renderDirectory(); renderChain(); history.replaceState(null,'',`#${role}${topic ? '/topic/'+topic : ''}`);
}
function route() {
  const [r, type, id, stepId] = location.hash.slice(1).split('/'); selectRole(r);
  const preferred = {frontend:'js-async',java:'java-thread',go:'go-runtime',python:'python-async',fullstack:'http',ai:'rag-flow',ml:'ml-eval',test:'test-cases',ops:'linux',cpp:'cpp-ownership'};
  let c = type === 'topic' ? roleChains().find(c => c.id === id) : null;
  if (type === 'question') c = roleChains().find(c => c.steps.some(s => s.questionId === id));
  c ||= roleChains().find(c => c.id === preferred[role]) || roleChains()[0];
  if (c) setTopic(c.id, false);
  const target = type === 'question' ? id : stepId;
  if (target) requestAnimationFrame(() => document.getElementById('step-'+target)?.scrollIntoView({block:'center'}));
  if (type === 'question' && Q[id] && !c?.steps.some(s => s.questionId === id)) {
    const q = Q[id]; $('legacy-body').innerHTML = `<p>保留的旧题链接 · 原复习进度仍有效</p><h2>${esc(q.title)}</h2>${actionHTML({id:q.id,number:1})}${answerHTML({q}, {references:q.references})}`; $('legacy').showModal();
  }
}
document.addEventListener('click', async e => {
  const b = e.target.closest('button'); if (!b || !D) return;
  if (b.dataset.topic) setTopic(b.dataset.topic);
  if (b.hasAttribute('data-reset')) { resetFilters(); applyFilters(); }
  if (b.dataset.star) {
    const id=b.dataset.star; saved.questions[id]={...state(id),star:!state(id).star}; persist();
    b.textContent=state(id).star?'★ 已收藏':'☆ 收藏'; b.setAttribute('aria-pressed',state(id).star); b.setAttribute('aria-label',b.getAttribute('aria-label').replace(/^(取消收藏|收藏)/,state(id).star?'取消收藏':'收藏')); renderDirectory();
  }
  if (b.dataset.link) {
    const url=new URL(location.href); url.hash=`${role}/topic/${topic}/${b.dataset.link}`;
    try { await navigator.clipboard.writeText(url.href); toast('这一问的链接已复制'); } catch { history.replaceState(null,'',url); toast('已定位到这一问，可复制地址栏链接'); }
  }
  if (b.id === 'practice') { practice=!practice; revealed=1; renderChain(); }
  if (b.id === 'next') { revealed++; renderChain(); document.querySelector('.step:last-child')?.scrollIntoView({block:'center'}); }
});
document.addEventListener('change', e => {
  const id=e.target.dataset.status; if (!id) return;
  saved.questions[id]={...state(id),status:e.target.value}; persist(); renderDirectory();
  const c=D.chains.find(c=>c.id===topic); if(c && $('chain-progress')) $('chain-progress').textContent=c.steps.filter(s=>state(s.id).status==='done').length+' 已掌握';
});
$('search').addEventListener('input',e=>{if(!D)return;query=e.target.value;applyFilters();});
$('company').onchange=e=>{if(!D)return;company=e.target.value;applyFilters();};
$('filter').onchange=e=>{if(!D)return;filter=e.target.value;applyFilters();};
$('theme').onclick=()=>{saved.theme=saved.theme==='dark'?'light':'dark';theme();persist();};
$('close').onclick=()=>$('legacy').close();
document.querySelector('.skip').onclick=e=>{e.preventDefault();$('chain').focus();$('chain').scrollIntoView({block:'start'});};
document.querySelector('.import-label').onkeydown=e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();$('import').click();}};
document.addEventListener('keydown',e=>{if(e.key==='/'&&!['INPUT','SELECT','TEXTAREA'].includes(document.activeElement.tagName)&&!$('legacy').open){e.preventDefault();$('search').focus();}});
$('export').onclick=()=>{
  const url=URL.createObjectURL(new Blob([JSON.stringify({format:KEY,...saved},null,2)],{type:'application/json'}));
  const a=document.createElement('a'); a.href=url;a.download='面试地图-复习进度.json';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);toast('进度已导出');
};
$('import').onchange=async e=>{
  try {
    if(!D)throw Error();const file=e.target.files[0];if(!file)return;if(file.size>2e6)throw Error();
    const v=JSON.parse(await file.text());if(v.format!==KEY||!v.questions||typeof v.questions!=='object'||Array.isArray(v.questions))throw Error();
    const ids=new Set([...D.questions.map(q=>q.id),...D.chains.flatMap(c=>c.steps.map(s=>s.id))]);
    for(const [id,s] of Object.entries(v.questions)) if(ids.has(id)&&s&&['todo','weak','done'].includes(s.status)&&typeof s.star==='boolean')saved.questions[id]={status:s.status,star:s.star};
    persist();renderDirectory();renderChain();toast('已合并进度，旧版导出文件也支持');
  } catch {toast('文件格式不正确，请使用本站导出的 JSON');}e.target.value='';
};
fetch('./data.json?v=3').then(r=>{if(!r.ok)throw Error();return r.json();}).then(data=>{
  if(!data.chains?.length)throw Error();D=data;Q=Object.fromEntries(D.questions.map(q=>[q.id,q]));N=Object.fromEntries(D.nodes.map(n=>[n.id,n]));route();window.addEventListener('hashchange',route);
}).catch(()=>{$('chain').innerHTML='<p class="empty">内容加载失败，请刷新。若本地预览，请通过 HTTP 服务打开。</p>';$('stats').textContent='加载失败';});
