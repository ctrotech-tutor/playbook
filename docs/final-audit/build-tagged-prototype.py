"""Four-page semantic export experiment, NOT the replacement release PDF.
Usage: python3 build-tagged-prototype.py /path/to/extracted/playbook
Requires WeasyPrint 70.0, pikepdf 10.5.1 and the publication build requirements.
"""
from pathlib import Path
from html import escape
import sys,json,hashlib,re,collections
import pikepdf
from weasyprint import HTML,Attachment,__version__
ROOT=Path(sys.argv[1]).resolve();OUT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'tools'));from pdf_syntax import source_tokens,token_colour
book=json.loads((ROOT/'content/chapters.json').read_text());meta=json.loads((ROOT/'content/publication.json').read_text())
def p(s):return '<p>'+escape(s)+'</p>'
def code(s):return '<pre><code>'+''.join('<span style="color:'+token_colour(t)+'">'+escape(v)+'</span>' for t,v in source_tokens(s))+'</code></pre>'
font=lambda f:(ROOT/f).as_uri()
css='''@page{size:A4;margin:19mm;@bottom-left{content:"WORKFLOW PROTOTYPE / NOT THE RELEASE PDF";font:8pt Book;color:#626c60}}@font-face{font-family:Book;src:url("'''+font('fonts/pdf/DejaVuSans.ttf')+'''")}@font-face{font-family:Display;src:url("'''+font('assets/fonts/InstrumentSerif-Regular.ttf')+'''")}@font-face{font-family:Mono;src:url("'''+font('fonts/pdf/DejaVuSansMono.ttf')+'''")}body{font:10.5pt/1.5 Book;color:#25332e}h1{font:35pt/1.1 Display;color:#234d42}h2{font:24pt/1.2 Display;color:#234d42}h3{font:17pt/1.2 Display;color:#234d42}pre{font:9pt/1.5 Mono;background:#f1f5f0;padding:12pt;white-space:pre-wrap}a{color:#234d42;text-decoration:underline}section.page{break-after:page}section.page:last-child{break-after:auto}table{border-collapse:collapse;width:100%}th,td{border:1px solid #626c60;padding:9pt;text-align:left}caption{text-align:left;margin-bottom:8pt}'''
body='<section class="page"><h1>The HTML Playbook</h1><h2>Tagged-export workflow prototype</h2>'+p('By '+meta['author']+' / '+meta['imprint'])+p('This four-page experiment tests semantic export features. It is not the release PDF and is not claimed to conform to PDF/UA or WCAG.')+'<ul><li>Heading hierarchy and paragraphs</li><li>Selectable coloured code</li><li>A linked source and a structured table</li><li>Language metadata and attached third-party notices</li></ul>'+p(meta['copyright_notice'])+p(meta['reuse_license'])+p(meta['preparation_note'])+'</section>'
for n in [1,9]:
 c=book[n-1];body+='<section class="page"><h2>'+escape(f'{n:02}. '+c['title'])+'</h2>'+p(c['explanation'])+code(c['code'])+'<h3>Check your understanding</h3>'+p(c['question'])+p(c['answer'].replace('`',''))+'<p><a href="'+escape(c['sources'][0]['url'],quote=True)+'">Read the chapter source</a></p></section>'
body+='<section class="page"><h2>Table and navigation fixture</h2><table><caption>Publication example types</caption><thead><tr><th scope="col">Example</th><th scope="col">Purpose</th></tr></thead><tbody><tr><th scope="row">Chapter 01</th><td>Document meaning and navigation</td></tr><tr><th scope="row">Chapter 09</th><td>Literal source text and character references</td></tr></tbody></table><h3>What remains unverified</h3>'+p('Tag presence alone does not prove correct reading order, code pronunciation, table-header associations or keyboard behavior in a PDF reader. A full-book export, a PDF/UA validator and assistive-technology checks are still required.')+'<p><a href="https://www.w3.org/WAI/WCAG22/Techniques/pdf/PDF3">WAI guidance on PDF reading and tab order</a></p></section>'
html='<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The HTML Playbook: tagged-export workflow prototype</title><meta name="author" content="'+escape(meta['author'],quote=True)+'"><style>'+css+'</style></head><body>'+body+'</body></html>'
attachments=[Attachment(filename=str(ROOT/'assets/fonts'/name),description='Font license and copyright notice') for name in ['OFL.txt','DejaVu-COPYRIGHT.txt']]+[Attachment(filename=str(ROOT/'assets'/name),description='Third-party source notice') for name in ['WHATWG-LICENSE.txt','BCD-LICENSE.txt','webref-MIT.txt']]
target=OUT/'tagged-workflow-prototype.pdf';HTML(string=html,base_url=str(ROOT)).write_pdf(target,pdf_variant='pdf/ua-1',attachments=attachments)
with pikepdf.open(target) as doc:
 counts=collections.Counter();seen=set();headers=[]
 def walk(value):
  if isinstance(value,pikepdf.Array):
   for x in value:walk(x)
  elif isinstance(value,pikepdf.Dictionary):
   key=value.objgen
   if key!=(0,0):
    if key in seen:return
    seen.add(key)
   if '/S' in value:counts[str(value['/S'])]+=1
   if value.get('/S')=='/TH':headers.append(str(value.get('/A')))
   if '/K' in value:walk(value['/K'])
 walk(doc.Root.StructTreeRoot)
 assert len(doc.pages)==4
 assert doc.Root.MarkInfo.Marked and counts['/H1'] and counts['/H2'] and counts['/Table'] and counts['/Link']
 record={'date':'2026-10-15','engine':'WeasyPrint '+__version__,'artifact':'tagged-workflow-prototype.pdf','sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'pages':len(doc.pages),'pdf_version':doc.pdf_version,'language':str(doc.Root.get('/Lang')),'marked_flag':bool(doc.Root.MarkInfo.Marked),'structure_tree_present':True,'structure_roles':dict(counts),'xmp_pdfua_identifier_present':b'pdfuaid' in doc.Root.Metadata.read_bytes(),'table_header_attribute_dictionaries':headers,'table_header_scope_mapping_verified':False,'attached_notices':len(doc.attachments),'links_with_struct_parent':sum('/StructParent' in a for page in doc.pages for a in page.obj.get('/Annots',[]) if a.get('/Subtype')=='/Link'),'checks':'Structural object inspection only. The PDF/UA generation option is not a validation result.','independent_accessibility_approval':False,'full_book_export':False,'release_pdf_replaced':False}
(OUT/'tagged-prototype-checks.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
