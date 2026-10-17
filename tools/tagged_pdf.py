"""Build and structurally check the single-source, semantically tagged production PDF.
Usage: python tools/tagged_pdf.py REPOSITORY OUTPUT_DIRECTORY
Pinned dependencies are in requirements-build.txt. Machine profile validation is a
separate fail-closed step; semantic tags do not imply independent certification.
"""
from pathlib import Path
from html import escape
from collections import Counter
import sys,json,re,hashlib,logging
import pikepdf,pymupdf,weasyprint
from weasyprint import HTML,Attachment
from weasyprint.urls import URLFetcher
from weasyprint.pdf import tags
ROOT=Path(sys.argv[1]).resolve();OUT=Path(sys.argv[2]).resolve();OUT.mkdir(parents=True,exist_ok=True)
sys.path.insert(0,str(ROOT/'tools'))
from pdf_syntax import source_tokens,token_colour
from fingerprint import publication_fingerprint
book=json.loads((ROOT/'content/chapters.json').read_text());meta=json.loads((ROOT/'content/publication.json').read_text());guide=json.loads((ROOT/'content/reading-guide.json').read_text());inv=json.loads((ROOT/'content/reference-snapshot.json').read_text())['inventories'];register=json.loads((ROOT/'content/api-register.json').read_text())
clean=lambda s:str(s).replace('\u2014',', ').replace('\u2013','-')
def cjk(s):
 return re.sub('[漢かん]+',lambda m:'<span class="cjk">'+m[0]+'</span>',s)
def inline(s):
 return cjk(re.sub(r'`([^`]+)`',r'<code>\1</code>',escape(clean(s))))
def p(s):return '<p>'+inline(s)+'</p>'
def prose(s):
 out=[]
 for block in s.strip().split('\n\n'):
  lines=block.splitlines();match=re.fullmatch(r'(#{2,4}) (.+)',lines[0]) if lines else None
  if match:
   level=len(match[1])+1;out.append(f'<h{level}>'+inline(match[2])+f'</h{level}>');lines=lines[1:]
  if lines and all(x.startswith('- ') for x in lines):out.append('<ul>'+''.join('<li>'+inline(x[2:])+'</li>' for x in lines)+'</ul>')
  elif lines:out.append(p('\n'.join(lines)))
 return ''.join(out)
def link(title,url):return '<a href="'+escape(url,quote=True)+'">'+inline(title)+'</a>'
def code(s,language='html'):
 tokens=source_tokens(s,language=language)
 return '<pre><code>'+''.join('<span style="color:'+token_colour(t)+'">'+cjk(escape(v))+'</span>' for t,v in tokens)+'</code></pre>'
def section(title,id,body):return '<section id="'+id+'"><h2>'+inline(title)+'</h2>'+body+'</section>'
font=lambda f:(ROOT/f).as_uri()
css='''@font-face{font-family:BookCJK;src:url("'''+font('fonts/pdf/CTROTECHCJKSubset.ttf')+'''")}@font-face{font-family:Book;src:url("'''+font('fonts/pdf/DejaVuSans.ttf')+'''")}@font-face{font-family:Book;src:url("'''+font('fonts/pdf/DejaVuSans-Bold.ttf')+'''");font-weight:bold}@font-face{font-family:Display;src:url("'''+font('assets/fonts/InstrumentSerif-Regular.ttf')+'''")}@font-face{font-family:Mono;src:url("'''+font('fonts/pdf/DejaVuSansMono.ttf')+'''")}@page{size:A4;margin:18mm 17mm 20mm;@top-left{content:"CTROTECH / THE HTML PLAYBOOK / PRODUCTION EDITION";font:7pt Book;color:#626c60}@bottom-left{content:"Odejobi Abiola Samuel / CTROTECH / 2026.1";font:7pt Book;color:#626c60}@bottom-right{content:counter(page);font:7pt Book;color:#626c60}}.cjk{font-family:BookCJK}body{font:9.4pt/1.5 Book;color:#25332e}h1{font:70pt/1.04 Display;color:#234d42;bookmark-level:1}h2{font:31pt/1.13 Display;color:#234d42;break-after:avoid;bookmark-level:1}h3{font:22pt/1.2 Display;color:#234d42;break-after:avoid;bookmark-level:none}h4{font:16pt/1.25 Display;color:#234d42;break-after:avoid;bookmark-level:none}h5{font:12pt/1.3 Book;font-weight:bold;break-after:avoid;bookmark-level:none}.api-owner{bookmark-level:2}.cover{break-after:page;padding-top:25mm}.eyebrow{font:8pt/1.5 Book;font-weight:bold;color:#a74125}.notice{border-left:3pt solid #a74125;padding:8pt 12pt;background:#f1f5f0}section{break-before:page}article.chapter{break-before:page}p,li{orphans:3;widows:3;overflow-wrap:anywhere}li{margin-bottom:4pt}a{color:#234d42;text-decoration:underline;overflow-wrap:anywhere}code{font:8.2pt/1.5 Mono}pre{font:8.2pt/1.5 Mono;white-space:pre-wrap;overflow-wrap:anywhere;tab-size:2;background:#f1f5f0;padding:10pt;hyphens:none}pre code,pre span{white-space:pre-wrap;overflow-wrap:anywhere}h1,h2,h3,h4,h5{overflow-wrap:anywhere}table{border-collapse:collapse;width:100%;font-size:8.5pt}th,td{border:1px solid #626c60;text-align:left;vertical-align:top;padding:7pt}caption{font-weight:bold;text-align:left;margin:8pt 0}thead{display:table-header-group}.toc{list-style:none;padding:0}.toc a::after{content:leader('.') target-counter(attr(href),page)}.small{font-size:8pt;color:#626c60}.chapter .part{font-size:8pt;color:#a74125;font-weight:bold}'''
body='<div class="cover"><p class="eyebrow">CTROTECH / FIELD GUIDE 001</p><h1>The HTML<br>Playbook.</h1>'+p('Write pages you can explain.')+p('By '+meta['author'])+p(meta['edition_label'])+'<p class="notice">74 chapters. Seven projects. A source-linked reference. Read the markup, test the result and explain the decision.</p>'+p(meta['copyright_notice'])+p(meta['reuse_license'])+'</div>'
body+=section('Publication details','publication-details',p(meta['title'])+p('Author: '+meta['author'])+p('Publication brand: '+meta['imprint'])+p(meta['copyright_notice'])+p(meta['reuse_license'])+p(meta['preparation_note'])+p(meta['author_bio_policy'])+p('Instrument Serif, DejaVu and Noto CJK font notices, WHATWG, Webref and BCD notices are attached. Original editorial rights do not override upstream rights. This production PDF is generated from the maintained website manuscript and reference data. Semantic tagging and a machine-validation result do not imply independent accessibility certification.'))
read=p(guide['intro'])+'<h3>Choose your route</h3>'
for route in guide['routes']:read+='<h4>'+inline(route['title'])+'</h4>'+p(route['text'])+p('Chapters: '+', '.join(str(n) for n in route['chapters']))
read+='<h3>One useful practice loop</h3><ol>'+''.join('<li><strong>'+inline(x['title'])+'</strong> '+inline(x['text'])+'</li>' for x in guide['practice'])+'</ol>'
for title,key in [('Website, PDF and code','formats'),('Know what a source tells you','sources'),('Scope of this edition','scope'),('Corrections','corrections')]:read+='<h3>'+title+'</h3>'+p(guide[key])
read+='<h3>Edition notes</h3><ul>'+''.join('<li>'+inline(x)+'</li>' for x in guide['edition_notes'])+'</ul>'
body+=section('Start here: a reading guide','reading-guide',read)
rows=[('Publication acceptance','Author accepted this edition on 17 October 2026; reported general-reader feedback is not specialist certification'),('Exhaustive coverage','Member/default/value/algorithm and cross-specification reconciliation remains open'),('Accessibility and security','Automated/native work is not actual OS assistive technology or full independent security assessment'),('Tagged PDF','Semantic tags and machine validation are separate from independent reading-order and actual assistive-technology review')]
table='<table><caption>Production edition: acceptance and review scope</caption><thead><tr><th scope="col">Gate</th><th scope="col">State and limit</th></tr></thead><tbody>'+''.join('<tr><th scope="row">'+inline(a)+'</th><td>'+inline(b)+'</td></tr>' for a,b in rows)+'</tbody></table>'
body+=section('Publication and review scope','candidate-scope',p('Tags, bookmarks, text extraction, links and a validator report are different evidence. No PDF/UA or WCAG certification is asserted merely because a PDF/UA generation target was selected. Tables shown inside source-code examples remain code, not executable document tables. Use the seven supplied projects for their actual rendered tables and forms.')+table)
body+=section('Contents','contents','<ol class="toc">'+''.join('<li>'+link(f'{c["number"]:02}. '+c['title'],'#'+c['id'])+'</li>' for c in book)+'</ol>')
for c in book:
 body+='<article class="chapter" id="'+c['id']+'"><p class="part">'+inline(c['part'])+'</p><h2>'+inline(f'{c["number"]:02}. '+c['title'])+'</h2>'+p(c['dek'])+'<h3>By the end of this chapter</h3><ul>'+''.join('<li>'+inline(g)+'</li>' for g in c['objectives'])+'</ul>'+prose(c['lesson'])+'<h3>The example</h3>'+code(c['code'])+prose(c['explanation'])+'<h3>A mistake to watch for</h3>'+p(c['mistake'])+'<h3>Your turn</h3>'+p(c['question'])+'<h4>Explained answer</h4>'+p(c['answer'])
 if c.get('project_slug'):body+=p('Complete project folder: project-'+c['project_slug']+'.zip in the companion downloads.')
 body+='<h3>Read the source</h3><ul>'+''.join('<li>'+link(s['title'],s['url'])+'</li>' for s in c['sources'])+'</ul></article>'
collections=[('Element reference',['elements','integration_entries']),('Attributes and handlers',['attributes','event_handler_attributes']),('Global attributes and boundaries',['global_attributes','global_attribute_families']),('Input states',['input_states']),('Content categories',['content_categories']),('Obsolete features',['obsolete_elements','obsolete_attributes','obsolete_conforming_conditions']),('API interface routes',['interfaces'])]
for i,(title,keys) in enumerate(collections):
 text=p('Captured index-derived summaries and definition routes, not completed per-feature behavioural documentation or universal browser support.')
 for key in keys:
  for entry in inv[key]:
   text+='<h3>'+inline(entry['name'])+'</h3>';desc=entry.get('description') or entry.get('scope') or entry.get('condition') or entry.get('migration_guidance') or entry.get('inventory_boundary','')
   if desc:text+=p(desc)
   for field,label in [('categories','Categories'),('parents','Parents'),('children','Content'),('attributes','Attributes'),('applicability_summary','Applies to'),('value_summary','Value'),('ownership','Authority'),('state','State'),('data_type','Data'),('control_type','Control'),('elements_summary','Members'),('exceptions_summary','Exceptions')]:
    if entry.get(field):text+=p(label+': '+entry[field])
   url=entry.get('definition_url') or next(iter(entry.get('definition_urls',[])),None) or entry['source_url'];text+=p('Definition route: ')+link('Open the source definition or discovery route',url)
 body+=section(title,'reference-'+str(i),text)
text=p('314 named declarations and 1,574 direct member declarations from captured HTML WebIDL. This is a signature register, not complete behaviour, exception, conversion or inherited cross-specification documentation.')
for rec in register['records']:
 text+='<h3 class="api-owner">'+inline(rec['name'])+'</h3>'+p(rec['type']+(' / inherits '+rec['inheritance'] if rec.get('inheritance') else '')+(' / includes '+', '.join(rec['includes']) if rec['includes'] else ''))
 for declaration in rec['definitions']:text+=code(declaration,'webidl')
 text+=link('Normative owner definition',rec['source_url'])
body+=section('API declaration register','api-declaration-register',text)
body+=section('Keyword, state and event routes','keyword-register',p('437 captured public definition routes, not a complete missing-value/default/applicability table.')+''.join('<h3>'+inline(' / '.join(rec['names']))+'</h3>'+p(rec['type']+' / '+(', '.join(rec['contexts']) or rec['section']))+link('Normative definition',rec['url']) for rec in register['keyword_records']))
body+=section('Glossary','glossary',''.join('<h3>'+inline(term)+'</h3>'+p(value) for term,value in json.loads((ROOT/'content/glossary.json').read_text()).items()))
body+=section('Source and release notes','sources',p('Reference records derive from the WHATWG snapshot dated 14 October 2026. Bounded source retrieval and current audit records have their own dates. An index or link is not complete technical approval. Copyright and source rights remain with their owners.')+'<ul>'+''.join('<li>'+link(s['id'],s['url'])+'</li>' for s in json.loads((ROOT/'content/source-manifest.json').read_text()))+'</ul>'+p('Still open: independent chapter/answer review; exhaustive behaviour, value/default and cross-specification contracts; actual OS assistive-technology and full security assessment; full-book tagged PDF accessibility approval. A repository push is not a production deployment.'))
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>'+escape(meta['title']+': '+meta['edition_label'])+'</title><meta name="author" content="'+escape(meta['author'],quote=True)+'"><style>'+css+'</style></head><body>'+body+'</body></html>'
# Semantic code mapping is explicit, scoped to this builder process and pinned engine.
old_tag=tags._get_pdf_tag
def get_tag(tag):
 return 'Code' if tag=='pre' else 'Span' if tag in ('code','strong','em') else old_tag(tag)
tags._get_pdf_tag=get_tag
from urllib.parse import urlsplit,unquote
class LocalFetcher(URLFetcher):
 def fetch(self,url,headers=None):
  parsed=urlsplit(url)
  if parsed.scheme!='file':raise ValueError('Remote/non-file resource blocked in tagged export: '+url)
  path=Path(unquote(parsed.path)).resolve()
  if not path.is_relative_to(ROOT):raise ValueError('Out-of-root resource blocked: '+str(path))
  return super().fetch(url,headers)
local_fetch=LocalFetcher(allowed_protocols={'file'},fail_on_errors=True)
attachments=[Attachment(filename=str(ROOT/('assets/fonts' if name in ['OFL.txt','DejaVu-COPYRIGHT.txt','Noto-CJK-OFL.txt'] else 'assets')/name),description='Third-party font/source licence and copyright notice') for name in ['OFL.txt','DejaVu-COPYRIGHT.txt','Noto-CJK-OFL.txt','WHATWG-LICENSE.txt','BCD-LICENSE.txt','webref-MIT.txt']]
raw=OUT/'tagged-full.raw.pdf';target=OUT/'ctrotech-html-playbook.pdf'
if '--verify-existing' in sys.argv:
 import shutil
 shutil.copy2(target,raw)
else:HTML(string=html,base_url=str(ROOT),url_fetcher=local_fetch).write_pdf(raw,pdf_variant='pdf/ua-1',attachments=attachments)
# Preserve meaningful semantics while removing orphan margin text from the reading tree.
with pikepdf.open(raw) as pdf:
 root=pdf.Root.StructTreeRoot;seen=set();roles=Counter();headers=Counter();order=[]
 def walk(value,ancestors=()):
  if isinstance(value,pikepdf.Array):
   for v in value:walk(v,ancestors)
  elif isinstance(value,pikepdf.Dictionary) and '/S' in value:
   if value.objgen in seen:return
   seen.add(value.objgen);role=str(value.S);roles[role]+=1
   if role=='/TH':
    scope='/Column' if '/THead' in ancestors else '/Row'
    assert '/THead' in ancestors or '/TBody' in ancestors
    value['/A']=pikepdf.Dictionary(O=pikepdf.Name('/Table'),Scope=pikepdf.Name(scope));headers[scope]+=1
   if '/K' in value:walk(value.K,ancestors+(role,))
 walk(root.K)
 nums=root.ParentTree.Nums;orphan={};pages={page.obj.objgen:i for i,page in enumerate(pdf.pages)}
 for i in range(0,len(nums),2):
  key=int(nums[i]);value=nums[i+1]
  if key<len(pdf.pages) and isinstance(value,pikepdf.Array):
   orphan[key]={j for j,item in enumerate(value) if item is not None and item.objgen not in seen}
   for j in orphan[key]:value[j]=None
 artifacts=0
 for i,page in enumerate(pdf.pages):
  page.obj['/Tabs']=pikepdf.Name('/S');instructions=[]
  for instruction in pikepdf.parse_content_stream(page):
   operands,operator=instruction.operands,instruction.operator
   if str(operator)=='BMC' and operands and str(operands[0])=='/Artifact':artifacts+=1
   if str(operator)=='BDC' and len(operands)>1 and isinstance(operands[1],pikepdf.Dictionary) and '/MCID' in operands[1] and int(operands[1].MCID) in orphan.get(i,set()):
    instruction=pikepdf.ContentStreamInstruction([pikepdf.Name('/Artifact')],pikepdf.Operator('BMC'));artifacts+=1
   instructions.append(instruction)
  page.obj['/Contents']=pdf.make_stream(pikepdf.unparse_content_stream(instructions))
 assert headers==Counter({'/Row':4,'/Column':2}),headers
 pdf.save(target)
raw.unlink()
with pymupdf.open(target) as pdf:
 text='\n'.join(page.get_text(sort=True,clip=pymupdf.Rect(0,48,page.rect.width,page.rect.height-50)) for page in pdf);norm=lambda s:re.sub(r'\s+','',s)
 missing_titles=[c['id'] for c in book if norm(f'{c["number"]:02}. '+c['title']) not in norm(text)]
 missing_code=[c['id'] for c in book if norm(c['code']) not in norm(text)]
 assert not missing_titles,missing_titles
 assert not missing_code,missing_code
 declaration_strings=[value for row in register['records'] for value in row['definitions']]
 assert all(norm(value) in norm(text) for value in declaration_strings),'Captured WebIDL declaration text missing from PDF'
 for c in book:
  for value in [c['dek'],c['explanation'],c['mistake'],c['question'],c['answer']]:assert norm(value.replace('`','').replace('\u2014',', ').replace('\u2013','-')) in norm(text),(c['id'],value[:70])
 bounds=[]
 for i,page in enumerate(pdf):
  for b in page.get_text('blocks'):
   if b[0]<26 or b[2]>page.rect.width-25 or b[1]<10 or b[3]>page.rect.height-10:bounds.append((i+1,list(b[:4]),b[4][:100]))
 assert not bounds,bounds[:8]
 pages=len(pdf);bookmarks=len(pdf.get_toc())
with pikepdf.open(target) as pdf:
 warnings=pdf.check_pdf_syntax();assert not warnings,warnings
 assert pdf.Root.MarkInfo.Marked and str(pdf.Root.Lang)=='en'
 links=[a for page in pdf.pages for a in page.obj.get('/Annots',[]) if a.get('/Subtype')=='/Link'];assert links and all('/StructParent' in a for a in links)
 assert len(pdf.attachments)==6
 result={'date':meta['publication_date'],'result':'PASS_STRUCTURAL_AND_TEXT_CHECKS_ONLY','artifact':target.name,'sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'publication_fingerprint':publication_fingerprint(ROOT),'engine':'WeasyPrint '+weasyprint.__version__,'pages':pages,'bookmarks':bookmarks,'chapters':74,'chapter_code_exact_ignoring_layout_whitespace':74,'chapter_dek_explanation_mistake_question_answer_text_present':74,'reference_collections':len(collections),'captured_declaration_strings_checked':len(declaration_strings),'api_owner_declarations':len(register['records']),'keyword_routes':len(register['keyword_records']),'structure_roles':dict(roles),'header_scopes':dict(headers),'margin_text_sequences_marked_artifact':artifacts,'language':str(pdf.Root.Lang),'link_annotations':len(links),'links_with_structure_parent':len(links),'all_pages_tabs_structure_order':all(str(page.obj.Tabs)=='/S' for page in pdf.pages),'attached_notices':6,'pdf_syntax_warnings':warnings,'pdfua_generation_target':'pdf/ua-1; target is not a validation result','independent_accessibility_approved':False,'os_assistive_technology_reviewed':False,'release_reading_pdf_replaced':True,'limits':['Structure/text/bounds checks do not establish complete reading order or screen-reader behaviour','A PDF/UA generation identifier is not certification','A separate validator and manual checks must be recorded; publication accessibility gate remains open']}
(OUT/'pdf-structure-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
