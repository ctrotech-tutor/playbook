#!/usr/bin/env python3
"""Check source-preserving highlighting, readable token colours and PDF page splits.
These checks are not an accessibility certification or an answer-key review.
"""
from pathlib import Path
import json,re,tempfile,zipfile,hashlib
import pymupdf
from bs4 import BeautifulSoup
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate
from pdf_syntax import SyntaxCodeBlock,source_tokens,TOKEN_PALETTE

ROOT=Path(__file__).resolve().parents[1]
def flat(text):return re.sub(r'\s+','',text)
def code_text(document):
    return ''.join(span['text'] for page in document for block in page.get_text('dict')['blocks'] if 'lines' in block for line in block['lines'] for span in line['spans'] if ('Mono' in span['font'] or 'BookCJK' in span['font']) and any(abs(span['size']-size)<.01 for size in (8.2,8.5)))
def luminance(value):
    rgb=[int(value[i:i+2],16)/255 for i in (1,3,5)]
    channels=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in rgb]
    return sum(x*w for x,w in zip(channels,[.2126,.7152,.0722]))
def contrast(a,b):
    high,low=sorted([luminance(a),luminance(b)],reverse=True)
    return (high+.05)/(low+.05)
def check():
    book=json.loads((ROOT/'content/chapters.json').read_text())
    meta=json.loads((ROOT/'content/publication.json').read_text())
    for filename,record in json.loads((ROOT/'content/pdf-font-provenance.json').read_text())['files'].items():
        assert hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()==record['sha256'],('PDF font provenance',filename)
    for name,file in [('Mono','DejaVuSansMono.ttf'),('Body','DejaVuSans.ttf')]:
        pdfmetrics.registerFont(TTFont(name,str(ROOT/'fonts/pdf'/file)))
    document=pymupdf.open(ROOT/'deliverables/ctrotech-html-playbook.pdf')
    printed=flat(code_text(document))
    assert document.metadata['author']==meta['author']
    for filename in ['OFL.txt','DejaVu-COPYRIGHT.txt','Noto-CJK-OFL.txt','WHATWG-LICENSE.txt','BCD-LICENSE.txt','webref-MIT.txt']:
        expected=(ROOT/'assets/fonts'/filename) if filename in ['OFL.txt','DejaVu-COPYRIGHT.txt','Noto-CJK-OFL.txt'] else (ROOT/'assets'/filename)
        assert document.embfile_get(filename)==expected.read_bytes()
    assert meta['author'] in document.get_xml_metadata()
    assert document.xref_get_key(document.pdf_catalog(),'Lang')[1]=='en'
    assert meta['author'] in document[0].get_text() and meta['author'] in document[1].get_text()
    assert meta['copyright_notice'] in re.sub(r'\s+',' ',document[1].get_text())
    for c in book:
        source=c['code']
        assert ''.join(value for _,value in source_tokens(source))==source,c['id']
        flow=SyntaxCodeBlock(source);flow.wrap(499,738)
        assert ''.join(value for row in flow.rows for _,value in row)==source.expandtabs(2).replace('\n',''),c['id']
        assert flat(source) in printed,('PDF source characters',c['id'])
        page=BeautifulSoup((ROOT/'build/site/chapters'/f'{c["number"]:02}.html').read_text(),'html5lib')
        assert page.select_one('#chapter-code').get_text()==source,('Website source characters',c['id'])
        raw=ROOT/'build/site/code'/f'{c["number"]:02}.html.txt'
        assert raw.read_bytes()==source.encode('utf-8'),('Raw source download',c['id'])
    register=json.loads((ROOT/'content/api-register.json').read_text())
    declarations=0
    for owner in register['records']:
        for declaration in owner['definitions']:
            assert ''.join(v for _,v in source_tokens(declaration,'webidl'))==declaration
            assert flat(declaration) in printed,('PDF WebIDL characters',owner['name'])
            declarations+=1
    with zipfile.ZipFile(ROOT/'build/site/downloads/code-examples.zip') as archive:
        assert archive.testzip() is None
        for c in book:assert archive.read(f'example-{c["number"]:02}.html')==c['code'].encode('utf-8')
    palette={**{str(k):v for k,v in TOKEN_PALETTE.items()},'label':'#4d6156'}
    ratios={name:round(contrast(value,'#f1f5f0'),2) for name,value in palette.items()}
    assert min(ratios.values())>=4.5,ratios
    # Exercise both very long lines and a block that must cross several pages.
    synthetic='<pre data-long="'+'x'*250+'">\n'+'\n'.join(f'<!-- split line {n:03} -->' for n in range(180))+'\n</pre>'
    (ROOT/'.cache').mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(dir=ROOT/'.cache') as temporary:
        path=Path(temporary)/'split.pdf'
        SimpleDocTemplate(str(path),pagesize=(595,842),leftMargin=48,rightMargin=48,topMargin=52,bottomMargin=52).build([SyntaxCodeBlock(synthetic,label='HTML / layout regression')])
        split=pymupdf.open(path);split_pages=len(split)
        assert split_pages>=3
        assert flat(code_text(split))==flat(synthetic),'Multi-page highlighting lost or reordered source characters.'
        for page in split:
            for block in page.get_text('blocks'):assert block[0]>=40 and block[2]<=555 and block[1]>=40 and block[3]<=805
        split.close()
    colours={span['color'] for page in document for b in page.get_text('dict')['blocks'] if 'lines' in b for line in b['lines'] for span in line['spans'] if 'Mono' in span['font']}
    assert len(colours)>=6
    document.close()
    return {'result':'PASS','author':meta['author'],'pdf_font_notices_attached':True,'examples_checked':len(book),'webidl_declarations_checked':declarations,'website_source_exact':True,'raw_source_files_and_zip_exact':True,'token_stream_and_prepared_rows_preserve_source':True,'pdf_non_whitespace_code_characters_present':True,'pdf_code_text_colours':len(colours),'pdf_token_contrast_ratios':ratios,'minimum_pdf_token_contrast':min(ratios.values()),'synthetic_multi_page_regression_pages':split_pages,'copying_note':'PDF line wraps can change physical line breaks. Raw source downloads preserve exact UTF-8 bytes. Numerical contrast and text checks do not establish WCAG conformance or tagged-PDF accessibility.'}
if __name__=='__main__':print(json.dumps(check(),indent=2))
