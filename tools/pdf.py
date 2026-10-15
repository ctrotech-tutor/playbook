"""Single-source PDF reading export with selectable text, links, contents and bookmarks.
Not represented as a tagged accessible PDF.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import json,re,shutil
import pymupdf
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether,CondPageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pdf_syntax import SyntaxCodeBlock, source_tokens, token_colour


def build_pdf(root,site,book,inv):
    meta=json.loads((root/'content/publication.json').read_text())
    guide=json.loads((root/'content/reading-guide.json').read_text())
    fonts=root/'fonts/pdf'
    for name,file in [('Body','DejaVuSans.ttf'),('BodyBold','DejaVuSans-Bold.ttf'),('Mono','DejaVuSansMono.ttf')]:pdfmetrics.registerFont(TTFont(name,str(fonts/file)))
    pdfmetrics.registerFont(TTFont('Display',str(root/'assets/fonts/InstrumentSerif-Regular.ttf')))
    pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
    ink=colors.HexColor('#25332e');green=colors.HexColor('#234d42');muted=colors.HexColor('#626c60');orange=colors.HexColor('#a74125');line=colors.HexColor('#d9dccf')
    body=ParagraphStyle('body',fontName='Body',fontSize=9.4,leading=14,textColor=ink,spaceAfter=8)
    h1=ParagraphStyle('bookH1',fontName='Display',fontSize=34,leading=37,textColor=ink,spaceAfter=16,keepWithNext=True)
    h2=ParagraphStyle('bookH2',fontName='Display',fontSize=23,leading=27,textColor=green,spaceBefore=17,spaceAfter=9,keepWithNext=True)
    small=ParagraphStyle('small',parent=body,fontSize=8,leading=12,textColor=muted,spaceAfter=5)
    label=ParagraphStyle('label',parent=small,fontName='BodyBold',fontSize=8,textColor=orange,spaceBefore=10,spaceAfter=9)
    guideLabel=ParagraphStyle('guideLabel',parent=label,keepWithNext=True)
    cover=ParagraphStyle('cover',fontName='Display',fontSize=76,leading=77,textColor=green,spaceAfter=28)
    def clean(s):return str(s).replace('\u2014',', ').replace('\u2013','-')
    def text(s):
        out=[]
        for part in re.split(r'(`[^`]+`|</?[A-Za-z][^<>]*>)',clean(s)):
            is_code=part.startswith('`') or (part.startswith('<') and part.endswith('>'))
            if is_code:
                raw=part[1:-1] if part.startswith('`') else part
                out.append(''.join('<font name="Mono" size="8.5" color="'+token_colour(token)+'">'+escape(value)+'</font>' for token,value in source_tokens(raw)))
            else:out.append(escape(part))
        return ''.join(out)
    class BookDoc(BaseDocTemplate):
        def afterFlowable(self,f):
            if isinstance(f,Paragraph) and getattr(f,'bookmark',None):
                key=f.bookmark;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(f.getPlainText(),key,getattr(f,'outline_level',0),False)
                if not getattr(f,'outline_only',False):self.notify('TOCEntry',(0,f.getPlainText(),self.page,key))
    target=root/'deliverables/ctrotech-html-playbook.pdf';target.parent.mkdir(exist_ok=True)
    doc=BookDoc(str(target),pagesize=(595.28,841.89),leftMargin=48,rightMargin=48,topMargin=52,bottomMargin=52,title=meta['title']+': '+meta['edition_label'],author=meta['author'],subject='HTML curriculum and reference by '+meta['author'])
    def frame(canvas,document):
        canvas.saveState();canvas.setCreator('CTROTECH publication builder');canvas.setKeywords('HTML, CTROTECH, '+meta['author']);canvas.setFillColor(muted);canvas.setFont('Body',7)
        canvas.drawString(48,818,meta['imprint']+' / THE HTML PLAYBOOK / '+meta['edition_label'].upper())
        canvas.setStrokeColor(line);canvas.line(48,40,547,40);canvas.drawString(48,26,meta['author']+' · '+meta['imprint']+' · '+meta['edition']);canvas.drawRightString(547,26,str(document.page));canvas.restoreState()
    doc.addPageTemplates(PageTemplate(id='book',frames=[Frame(48,52,499,738,id='normal',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],onPage=frame))
    flow=[]
    flow+=[Spacer(1,80),Paragraph('FIELD GUIDE 001',label),Paragraph('The HTML<br/>Playbook.',cover),Paragraph('Write pages you can explain.',h2),Paragraph('A source-linked curriculum, reference and project collection for practical HTML authoring.',body),Spacer(1,16),Paragraph('By '+text(meta['author']),ParagraphStyle('authorCredit',fontName='Display',fontSize=24,leading=28,textColor=green)),Spacer(1,24),Paragraph(meta['edition_label'].upper()+' / 14 OCTOBER 2026',label),Paragraph('74 chapters · 74 explained exercises · 7 static projects',body),Paragraph('Published reading curriculum and captured reference. It is not a completed whole-Standard behavioral reference. Independent technical, answer-key, accessibility and security reviews remain open. The PDF has text, links and bookmarks; it is not claimed to be a tagged accessible PDF.',small),PageBreak()]
    credit_heading=Paragraph('Publication details',h1);credit_heading.bookmark='publication-details'
    flow += [credit_heading,Paragraph(meta['title'],h2),Paragraph('<b>Author:</b> '+text(meta['author']),body),Paragraph('<b>Publication brand:</b> '+text(meta['imprint']),body),Paragraph('<b>Edition:</b> '+text(meta['edition_label'])+' / 14 October 2026',body),Spacer(1,15),Paragraph(text(meta['copyright_notice']),body),Paragraph(text(meta['reuse_license']),small),Paragraph('Source and third-party credits',h2),Paragraph('Reference summaries are derived from the captured WHATWG HTML indexes and definition pages. MDN, W3C/WAI, OWASP and other cited authorities retain their own terms. Copyright © WHATWG (Apple, Google, Mozilla, Microsoft). Extracted source summaries and declarations are arranged and linked for this book; no endorsement is implied. The WHATWG source license notice is attached to this PDF. Instrument Serif is supplied under the SIL Open Font License. The PDF also embeds DejaVu fonts. Both font notices are attached to this PDF and included with the companion files.',body),Paragraph('Preparation and review',h2),Paragraph(text(meta['preparation_note']),body),Paragraph('The author has approved the visual direction and confirmed the public site works. Publication does not close the remaining behavioral/value inventories, independent technical and answer-key reviews, accessibility/security checks or accessible-PDF workflow.',body),PageBreak()]
    flow+=[Paragraph('How to use this book',h1),Paragraph('Read the chapters in order if you are starting with HTML. Use the reference when you need a definition route. Attempt each exercise before reading the explanation. Inspect the seven complete project folders to compare document structure and implementation limits.',body),Paragraph('The website and this PDF use the same chapter data. Use the companion source files for exact, unwrapped code. Syntax colours distinguish tags, attributes, strings, keywords and comments. Colours do not change the source or prove its correctness. Long lines wrap to fit the PDF; download the exact source when copying a complete example. External-media filenames in examples are illustrative unless the project includes the actual local asset. The site sandbox blocks requests and submissions deliberately.',body),Paragraph('A feature in a standard is not necessarily available in every browser. Index summaries are not full normative definitions. A checker pass does not establish accessibility or security. The review-status page and source package record actual check scope and remaining work.',body),Paragraph('Editorial note',h2),Paragraph('Prepared with AI assistance for CTROTECH. Author credit and preparation details are recorded on the publication-details page. The source package records executed checks and open reviews separately; neither visual polish nor a successful build closes technical review.',body),PageBreak()]
    guide_heading=Paragraph('Start here: a reading guide',h1);guide_heading.bookmark='reading-guide'
    flow += [guide_heading,Paragraph(text(guide['intro']),body),Paragraph('Choose your route',h2)]
    for route in guide['routes']:
        flow += [Paragraph(text(route['title']),guideLabel),Paragraph(text(route['text']),body)]
        if route['chapters']:flow.append(Paragraph(' · '.join('<link href="#'+book[n-1]['id']+'" color="#234d42">'+text(f'{n:02}. '+book[n-1]['title'])+'</link>' for n in route['chapters']),small))
    flow.append(Paragraph('One useful practice loop',h2))
    for step in guide['practice']:flow += [Paragraph(text(step['title']),guideLabel),Paragraph(text(step['text']),body)]
    for title,key in [('Website, PDF and code','formats'),('Know what a source tells you','sources'),('Scope of this edition','scope'),('Help correct the book','corrections')]:flow += [Paragraph(title,h2),Paragraph(text(guide[key]),body)]
    flow.append(Paragraph('<link href="'+escape(meta['corrections_url'],{chr(34):'&quot;'})+'" color="#234d42">Report a content correction on GitHub</link>',body))
    flow.append(Paragraph('October 2026 edition notes',h2))
    for note in guide['edition_notes']:flow.append(Paragraph(text(note),body))
    flow += [PageBreak(),Paragraph('Contents',h1)]
    toc=TableOfContents();toc.levelStyles=[ParagraphStyle('toc',fontName='Body',fontSize=9,leading=14,leftIndent=0,firstLineIndent=0,spaceBefore=3,textColor=ink)];flow +=[toc,PageBreak()]
    def heading(title,key):
        p=Paragraph(text(title),h1);p.bookmark=key;flow.append(p)
    def paras(s):
        for p in s.split('\n\n'):
            if p.startswith('## '):
                lines=p.split('\n',1);flow.append(Paragraph(text(lines[0][3:]),h2))
                if len(lines)>1:flow.append(Paragraph(text(lines[1]),body))
            elif p.strip():flow.append(Paragraph(text(p),body))
    for c in book:
        flow.append(CondPageBreak(390))
        flow.append(Paragraph(text(c['part']),label));heading(f'{c["number"]:02}. {c["title"]}',c['id']);flow.append(Paragraph(text(c['dek']),body))
        flow.append(Paragraph('By the end of this chapter',label))
        for g in c['objectives']:flow.append(Paragraph('• '+text(g),small))
        flow.append(Spacer(1,15));paras(c['lesson']);flow.append(Paragraph('The example',h2))
        flow.append(SyntaxCodeBlock(c['code'],label=('HTML + JavaScript' if '<script' in c['code'].lower() else 'HTML')+' / example '+f'{c["number"]:02}'))
        paras(c['explanation'])
        flow.append(Paragraph('A mistake to watch for',label));flow.append(Paragraph(text(c['mistake']),body))
        flow.append(Paragraph('Your turn',h2));flow.append(Paragraph(text(c['question']),body));flow.append(Paragraph('Explained answer',label));flow.append(Paragraph(text(c['answer']),body))
        if c.get('project_slug'):flow.append(Paragraph('Complete project folder: project-'+c['project_slug']+'.zip in the companion downloads.',small))
        flow.append(Paragraph('Read the source',label))
        for src in c['sources']:flow.append(Paragraph(f'<link href="{escape(src["url"], {chr(34):"&quot;"})}" color="#234d42">{text(src["title"])}</link>',small))
        flow.append(Spacer(1,25))
    flow.append(PageBreak())
    refname=ParagraphStyle('refname',fontName='Display',fontSize=17,leading=20,textColor=green,spaceBefore=12,spaceAfter=7,keepWithNext=True)
    collections=[('Element reference',['elements','integration_entries']),('Attributes and handlers',['attributes','event_handler_attributes']),('Global attributes and boundaries',['global_attributes','global_attribute_families']),('Input states',['input_states']),('Content categories',['content_categories']),('Obsolete features',['obsolete_elements','obsolete_attributes','obsolete_conforming_conditions']),('API interface routes',['interfaces'])]
    for index,(title,keys) in enumerate(collections):
        heading(title,'reference-'+str(index));flow.append(Paragraph('Index-derived summaries from the captured foundation snapshot. Read the full definition for restrictions, defaults and exceptions. Standard presence does not imply universal implementation. API member-level completeness is still open.',small))
        for key in keys:
            for entry in inv[key]:
                flow.append(Paragraph(text(entry['name']),refname));desc=entry.get('description') or entry.get('scope') or entry.get('condition') or entry.get('migration_guidance') or entry.get('inventory_boundary','')
                if desc:flow.append(Paragraph(text(desc),body))
                for field,labeltext in [('categories','Categories'),('parents','Parents'),('children','Content'),('attributes','Attributes'),('applicability_summary','Applies to'),('value_summary','Value'),('ownership','Authority'),('state','State'),('data_type','Data'),('control_type','Control'),('elements_summary','Members'),('exceptions_summary','Exceptions')]:
                    if entry.get(field):flow.append(Paragraph('<b>'+labeltext+':</b> '+text(entry[field]),small))
                url=entry.get('definition_url') or next(iter(entry.get('definition_urls',[])),None) or entry['source_url']
                flow.append(Paragraph('<link href="'+escape(url,{chr(34):'&quot;'})+'" color="#234d42">Open the source definition or discovery route</link>',small))
        flow.append(PageBreak())
    register=json.loads((root/'content/api-register.json').read_text())
    heading('API declaration register','api-declaration-register')
    flow.append(Paragraph('314 named declarations and 1,574 direct member declarations, extracted from the captured HTML WebIDL through W3C Webref. Partial declarations are consolidated. Inherited and mixed-in members remain on their declaring owner. This is a signature register, not completed behavioral documentation. The website supplies direct member links, match labels and searchable owner pages.',body))
    for record in register['records']:
        p=Paragraph(text(record['name']),refname);p.bookmark='api-'+re.sub(r'[^a-z0-9]+','-',record['name'].lower()).strip('-');p.outline_level=1;p.outline_only=True;flow.append(p)
        flow.append(Paragraph(text(record['type'])+(' / inherits '+text(record['inheritance']) if record.get('inheritance') else '')+(' / includes '+text(', '.join(record['includes'])) if record['includes'] else ''),small))
        for declaration in record['definitions']:flow.append(SyntaxCodeBlock(declaration,label='WebIDL / '+record['name'],language='webidl'))
        flow.append(Paragraph('<link href="'+escape(record['source_url'],{chr(34):'&quot;'})+'" color="#234d42">Normative owner definition</link>',small))
    flow.append(PageBreak());heading('Keyword, state and event routes','keyword-register')
    flow.append(Paragraph('437 captured public definition records. These routes distinguish HTML attribute keywords, input states, WebIDL enumeration values and events. They do not form a complete missing-value, invalid-value or conditional applicability table.',body))
    for record in register['keyword_records']:
        flow.append(Paragraph(text(' / '.join(record['names'])),refname));flow.append(Paragraph(text(record['type']+' / '+(', '.join(record['contexts']) or record['section'])),small))
        flow.append(Paragraph('<link href="'+escape(record['url'],{chr(34):'&quot;'})+'" color="#234d42">Normative definition</link>',small))
    flow.append(PageBreak())
    heading('Glossary','glossary')
    for term,definition in json.loads((root/'content/glossary.json').read_text()).items():flow.append(Paragraph(text(term),h2));flow.append(Paragraph(text(definition),body))
    flow.append(PageBreak());heading('Source and release notes','sources')
    flow.append(Paragraph('Reference summaries derive from the WHATWG HTML source snapshot dated 14 October 2026. See https://whatwg.org/ipr-policy#copyright-license-grant for source terms. MDN prose and Browser Compatibility Data have separate roles and licenses. Instrument Serif is included under the SIL Open Font License. The supplied source and font notices retain upstream terms. The original editorial copyright notice does not override upstream rights.',body))
    for src in json.loads((root/'content/source-manifest.json').read_text()):flow.append(Paragraph('<link href="'+escape(src['url'],{chr(34):'&quot;'})+'" color="#234d42">'+text(src['id'])+'</link>',body))
    flow.append(Paragraph('Still open',h2));flow.append(Paragraph('Independent chapter and answer review; expanded API behavior, cross-specification reconciliation and complete value/default inventories; assistive-technology review; full security review; tagged-PDF accessibility workflow. Executed browser and deployment-package checks are recorded separately. The public site is https://ctrobook.vercel.app/. The author confirmed successful delivery on 14 October 2026. Later repository updates require their own deployment; hosting success is not content approval.',body))
    doc.multiBuild(flow)
    # Keep standalone PDF distribution accompanied by its embedded-font notices.
    with pymupdf.open(target) as document:
        document.xref_set_key(document.pdf_catalog(),'Lang','(en)')
        xmp='<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"><rdf:Description rdf:about="" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:xmp="http://ns.adobe.com/xap/1.0/">'
        for field,value in [('title',meta['title']+': '+meta['edition_label']),('description',meta['preparation_note']),('rights',meta['copyright_notice'])]:xmp+='<dc:'+field+'><rdf:Alt><rdf:li xml:lang="x-default">'+escape(value)+'</rdf:li></rdf:Alt></dc:'+field+'>'
        xmp+='<dc:creator><rdf:Seq><rdf:li>'+escape(meta['author'])+'</rdf:li></rdf:Seq></dc:creator><dc:publisher><rdf:Bag><rdf:li>'+escape(meta['imprint'])+'</rdf:li></rdf:Bag></dc:publisher><dc:language><rdf:Bag><rdf:li>en</rdf:li></rdf:Bag></dc:language><xmp:CreatorTool>CTROTECH publication builder</xmp:CreatorTool></rdf:Description></rdf:RDF></x:xmpmeta>'
        document.set_xml_metadata(xmp)
        for filename in ['OFL.txt','DejaVu-COPYRIGHT.txt','WHATWG-LICENSE.txt','BCD-LICENSE.txt','webref-MIT.txt']:
            document.embfile_add(filename,((root/'assets/fonts'/filename) if filename in ['OFL.txt','DejaVu-COPYRIGHT.txt'] else (root/'assets'/filename)).read_bytes(),filename=filename,desc='Third-party font license and copyright notice')
        temporary=target.with_name('.with-font-notices.pdf')
        document.save(temporary,garbage=4,deflate=True)
    temporary.replace(target)
    shutil.copy2(target,site/'downloads'/target.name)
    print('PDF reading export:',target)
