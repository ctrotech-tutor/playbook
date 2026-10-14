import fs from 'node:fs';
import {parse,write} from 'webidl2';
import {createHash} from 'node:crypto';
if(!process.argv.includes('--refresh'))throw new Error('Explicit --refresh required. This retrieves current upstream data; review changes before release.');
fs.mkdirSync('.cache/reference-upstream',{recursive:true});
for(const [name,url] of [['html.idl','https://raw.githubusercontent.com/w3c/webref/main/ed/idl/html.idl'],['html.json','https://raw.githubusercontent.com/w3c/webref/main/ed/dfns/html.json']]){const response=await fetch(url);if(!response.ok)throw new Error('Source retrieval failed: '+response.status);fs.writeFileSync('.cache/reference-upstream/'+name,Buffer.from(await response.arrayBuffer()));}
fs.copyFileSync('.cache/reference-upstream/html.idl','content/upstream/html.idl');
const raw=fs.readFileSync('content/upstream/html.idl','utf8'),ast=parse(raw);
const source=JSON.parse(fs.readFileSync('.cache/reference-upstream/html.json','utf8'));
const dfns=source.dfns.filter(d=>d.access==='public');
const typeMap={attribute:'attribute',operation:'method',constructor:'constructor',const:'const',field:'dict-member'};
const trim=n=>n.replace(/\(.*$/s,'').trim();
const owners=new Map();
for(const a of ast){if(a.type==='includes')continue; const o=owners.get(a.name)||{name:a.name,type:a.type,inheritance:a.inheritance||null,definitions:[],members:[],includes:[],source_url:null};
const own=dfns.find(d=>['interface','dictionary','enum','callback','typedef'].includes(d.type)&&d.linkingText.some(n=>n===a.name));
const inScope=dfns.find(d=>d.for.includes(a.name));
o.source_url=own?.href||inScope?.heading?.href||source.spec.url;
o.definitions.push(write([a]).trim());
for(const m of a.members||[]){const t=typeMap[m.type]||m.type;const candidates=dfns.filter(d=>d.type===t&&d.for.includes(a.name)&&d.linkingText.some(n=>trim(n)===(m.name||'constructor'))); const d=candidates[0];o.members.push({name:m.name||m.special||m.type,kind:m.type,readonly:!!m.readonly,signature:write([m]).trim(),definition_url:d?.href||o.source_url,definition_match:d?'member':'owner route',source_heading:d?.heading?.title||null});}
if(a.type==='enum')o.values=a.values.map(v=>v.value);
owners.set(a.name,o);}
for(const a of ast.filter(a=>a.type==='includes'))if(owners.has(a.target))owners.get(a.target).includes.push(a.includes);
const records=[...owners.values()].sort((a,b)=>a.name.localeCompare(b.name));
const keyword=dfns.filter(d=>['attr-value','element-state','enum-value','event'].includes(d.type)).map(d=>({id:d.id,type:d.type,names:d.linkingText,contexts:d.for,url:d.href,section:d.heading?.title||''}));
const sha=x=>createHash('sha256').update(x).digest('hex');
const output={captured_date:new Date().toISOString().slice(0,10),upstream_spec:source.spec,extraction_source:'https://github.com/w3c/webref',idl_source_url:'https://raw.githubusercontent.com/w3c/webref/main/ed/idl/html.idl',definitions_source_url:'https://raw.githubusercontent.com/w3c/webref/main/ed/dfns/html.json',idl_sha256:sha(raw),definitions_sha256:sha(fs.readFileSync('.cache/reference-upstream/html.json')),parser:'webidl2 '+JSON.parse(fs.readFileSync('node_modules/webidl2/package.json')).version,scope:'Captured HTML WebIDL declarations and public definition routes. This is not reviewed behavioral documentation, universal implementation support or a complete cross-specification API reference.',stats:{declaration_owners:records.length,members:records.reduce((n,o)=>n+o.members.length,0),exact_member_routes:records.flatMap(o=>o.members).filter(m=>m.definition_match==='member').length,keyword_event_state_records:keyword.length,includes:ast.filter(a=>a.type==='includes').length},records,keyword_records:keyword};
fs.writeFileSync('content/api-register.json',JSON.stringify(output,null,2)+'\n');console.log(output.stats);
