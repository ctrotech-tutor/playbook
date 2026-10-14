'use strict';
(() => {
  const body = document.body;
  const base = body.dataset.base || '';
  const readStored = (key, fallback) => { try { return JSON.parse(localStorage.getItem(key)) ?? fallback; } catch { return fallback; } };
  const writeStored = (key, value) => { try { localStorage.setItem(key, JSON.stringify(value)); return true; } catch { return false; } };
  const theme = readStored('ctrotech.html.theme', 'paper');
  if (theme === 'night') body.dataset.theme = 'night';
  const size = readStored('ctrotech.html.size', 19);
  if ([17,19,21].includes(size)) document.documentElement.style.setProperty('--reader-size', size + 'px');
  const announce = text => { const n = document.getElementById('ui-status'); if (n) n.textContent = text; };
  document.querySelectorAll('[data-theme-toggle]').forEach(button => {
    button.textContent = body.dataset.theme === 'night' ? 'Paper theme' : 'Night theme';
    button.addEventListener('click', () => {
      const next = body.dataset.theme === 'night' ? 'paper' : 'night';
      body.dataset.theme = next; writeStored('ctrotech.html.theme', next);
      document.querySelectorAll('[data-theme-toggle]').forEach(b => b.textContent = next === 'night' ? 'Paper theme' : 'Night theme');
    });
  });
  document.querySelectorAll('[data-font-size]').forEach(button => button.addEventListener('click', () => {
    const value = Number(button.dataset.fontSize);document.documentElement.style.setProperty('--reader-size', value + 'px');writeStored('ctrotech.html.size', value);
    announce('Reading text size changed to ' + value + ' pixels.');
  }));
  const done = readStored('ctrotech.html.read', []);
  const completed = new Set(Array.isArray(done) ? done.filter(n => /^CH-\d{2}$/.test(n)) : []);
  const progressText = () => document.querySelectorAll('[data-reading-count]').forEach(n => n.textContent = completed.size + ' / 74 read');
  progressText();
  const mark = document.querySelector('[data-mark-read]');
  const setMark = () => { if (mark) { const value = completed.has(mark.dataset.markRead);mark.setAttribute('aria-pressed', String(value));mark.textContent = value ? 'Marked as read' : 'Mark this chapter as read'; } };
  setMark();
  if (mark) mark.addEventListener('click', () => {
    const id=mark.dataset.markRead; completed.has(id) ? completed.delete(id) : completed.add(id);setMark();progressText();
    const saved = writeStored('ctrotech.html.read', [...completed]);
    announce(saved ? 'Reading progress saved in this browser.' : 'Progress changed for this visit; browser storage is unavailable.');
  });
  document.querySelectorAll('[data-clear-progress]').forEach(b=>b.addEventListener('click',()=>{completed.clear();writeStored('ctrotech.html.read',[]);setMark();progressText();announce('Reading progress cleared.');}));
  const chapters = document.querySelector('[data-chapters-toggle]');
  if (chapters) chapters.addEventListener('click', () => { const nav=document.getElementById('chapter-navigation');const open=chapters.getAttribute('aria-expanded')!=='true';chapters.setAttribute('aria-expanded',String(open));nav.classList.toggle('is-open',open); });
  const track = document.querySelector('.progress-fill');
  if (track) { const update=()=>{const article=document.querySelector('.reader');const start=article.offsetTop;const available=Math.max(1,article.offsetHeight-innerHeight+100);track.style.width=Math.max(0,Math.min(100,(scrollY-start+80)/available*100))+'%';};addEventListener('scroll',update,{passive:true});addEventListener('resize',update);update(); }
  document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
    const text=document.getElementById(button.dataset.copy).textContent;
    try { await navigator.clipboard.writeText(text);button.textContent='Copied';announce('Example copied.'); }
    catch { const sel=getSelection();sel.removeAllRanges();const range=document.createRange();range.selectNodeContents(document.getElementById(button.dataset.copy));sel.addRange(range);button.textContent='Select and copy';announce('The code is selected. Use your copy command.'); }
  }));
  document.querySelectorAll('dialog').forEach(d=>d.addEventListener('keydown',event=>{if(event.key==='Escape'){event.preventDefault();d.close();}}));
  const search=document.getElementById('search-dialog');
  const input=document.getElementById('book-search');
  const results=document.getElementById('search-results');
  if (search && input && results) {
    function renderSearch(){const q=input.value.trim().toLowerCase();const tokens=q.split(/\s+/).filter(Boolean);const entries=(window.BOOK_SEARCH||[]).filter(r=>!tokens.length||tokens.every(t=>(r.title+' '+r.text).toLowerCase().includes(t)));if(q){const rank=r=>r.title.toLowerCase()===q?0:r.title.toLowerCase().startsWith(q)?1:2;entries.sort((a,b)=>rank(a)-rank(b));}results.replaceChildren();for(const item of entries.slice(0,35)){const li=document.createElement('li'),a=document.createElement('a'),small=document.createElement('small');a.href=base+item.path;small.textContent=item.kind;a.append(small,document.createTextNode(item.title));li.append(a);results.append(li);}document.getElementById('search-status').textContent=entries.length+' matches'+(entries.length>35?' · showing 35; add a more specific term':'');}
    const open=()=>{search.showModal();renderSearch();input.focus();};
    document.querySelectorAll('[data-open-search]').forEach(b=>b.addEventListener('click',open));input.addEventListener('input',renderSearch);
    addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();if(!search.open)open();}});
  }
  document.querySelectorAll('[data-close-dialog]').forEach(b=>b.addEventListener('click',()=>document.getElementById(b.dataset.closeDialog).close()));
  const lab=document.getElementById('lab-dialog');
  if (lab) {
    const editor=document.getElementById('lab-code'),frame=document.getElementById('lab-output');
    const run=()=>{const doc=new DOMParser().parseFromString(editor.value,'text/html');const meta=doc.createElement('meta');meta.httpEquiv='Content-Security-Policy';meta.content="default-src 'none'; script-src 'unsafe-inline'; style-src 'unsafe-inline'; img-src data:; connect-src 'none'; form-action 'none'; base-uri 'none'; frame-src 'none'";doc.head.prepend(meta);frame.srcdoc='<!doctype html>'+doc.documentElement.outerHTML;};
    document.querySelectorAll('[data-open-lab]').forEach(b=>b.addEventListener('click',()=>{editor.value=document.getElementById('example-source').value;lab.showModal();run();}));
    document.getElementById('lab-run').addEventListener('click',run);
    document.getElementById('lab-reset').addEventListener('click',()=>{editor.value=document.getElementById('example-source').value;run();});
  }
  const refInput=document.getElementById('reference-search'),refFilter=document.getElementById('reference-filter');
  if(refInput){const cards=[...document.querySelectorAll('[data-reference-entry]')];const update=()=>{const q=refInput.value.trim().toLowerCase(),category=refFilter?.value||'all';let count=0;for(const card of cards){const match=card.dataset.search.includes(q)&&(category==='all'||card.dataset.category===category);card.hidden=!match;if(match)count++;}document.getElementById('reference-count').textContent=count+' entries shown';};refInput.addEventListener('input',update);refFilter?.addEventListener('change',update);update();}
})();
