"""Render authored behaviour teaching from one maintained JSON source.
The HTML and tagged-PDF builders supply their own safe inline/code renderers.
"""
from pathlib import Path
from html import escape
import json,re

def units(root):
    data=json.loads((Path(root)/'content/api-behavior.json').read_text())
    assert data['schema_version']==1
    return data['units']

def anchor(unit,member):
    return unit['id']+'-'+re.sub('[^a-z0-9]+','-',member['name'].lower()).strip('-')

def render_unit(unit,inline,code,level=2):
    assert 2<=level<=4
    def heading(title,depth=0,id=None):
        tag='h'+str(level+depth)
        return '<'+tag+((' id="'+escape(id,quote=True)+'"') if id else '')+'>'+inline(title)+'</'+tag+'>'
    def p(text):return '<p>'+inline(text)+'</p>'
    def sources(urls):
        return '<p class="small-note">Sources: '+', '.join('<a href="'+escape(url,quote=True)+'">'+inline(url)+'</a>' for url in dict.fromkeys(urls))+'</p>'
    out='<section class="behavior-unit" id="'+escape(unit['id'],quote=True)+'">'+heading(unit['title'])+p('Technical review: '+unit['review_date']+'. '+unit['review_method'])+p(unit['introduction'])
    for title,key in [('Objectives','objectives'),('Prerequisites','prerequisites')]:
        out+=heading(title,1)+'<ul>'+''.join('<li>'+inline(x)+'</li>' for x in unit[key])+'</ul>'
    out+=heading('Terms',1)+'<dl>'+''.join('<dt>'+inline(k)+'</dt><dd>'+inline(v)+'</dd>' for k,v in unit['terms'].items())+'</dl>'
    for s in unit['shared_sections']:out+=heading(s['title'],1)+p(s['text'])+sources(s['sources'])
    fields=[('Inputs and conversions','inputs_and_conversions'),('Return value and defaults','returns_and_defaults'),('Errors and restrictions','errors_and_restrictions'),('Effects and ordering','effects_and_ordering')]
    for m in unit['members']:
        out+=heading(m['name'],1,anchor(unit,m))+p('`'+m['signature']+'`')+p(m['meaning'])
        for title,key in fields[:2]:out+=heading(title,2)+p(m[key])
        out+=heading('Algorithm and branches',2)+'<ol>'+''.join('<li>'+inline(s)+'</li>' for s in m['algorithm'])+'</ol>'
        for title,key in fields[2:]:out+=heading(title,2)+p(m[key])
        out+=code(m['code'],m['code_language'])+p(m['explanation'])+sources(m['sources'])
    e=unit['exercise'];out+=heading('Exercise',1)+p(e['question'])+heading('Explained answer',2)+p(e['answer'])
    out+=code(e['html'],'html')+code(e['code'],'javascript')+code(e['usage_code'],'javascript')+p(e['implementation_notes'])
    out+=heading('Compatibility and continuing assessment',1)+p(unit['compatibility'])+heading('Still open',1)+'<ul>'+''.join('<li>'+inline(s)+'</li>' for s in unit['still_open'])+'</ul></section>'
    return out

def render_behavior(root,owner,inline,code,level=2):
    return ''.join(render_unit(u,inline,code,level) for u in units(root) if u['owner']==owner)

def markdown(unit):
    # This is an export of the maintained data, not a separately authored manuscript.
    from bs4 import BeautifulSoup
    html=render_unit(unit,lambda s:escape(str(s)),lambda s,language:'<pre data-language="'+language+'">'+escape(s)+'</pre>')
    soup=BeautifulSoup(html,'html.parser')
    for a in soup.select('a'):a.replace_with('<'+a['href']+'>')
    for h in soup.select('h2,h3,h4'):h.replace_with('\n'+'#'*(int(h.name[1])-1)+' '+h.get_text()+'\n')
    for pre in soup.select('pre'):pre.replace_with('\n```'+pre['data-language']+'\n'+pre.get_text()+'\n```\n')
    for dt in soup.select('dt'):dt.insert_before('\n- **');dt.insert_after('**: ')
    for dd in soup.select('dd'):dd.insert_after('\n')
    for ol in soup.select('ol'):
        for i,li in enumerate(ol.find_all('li',recursive=False),1):li.insert_before('\n'+str(i)+'. ')
    for ul in soup.select('ul'):
        for li in ul.find_all('li',recursive=False):li.insert_before('\n- ')
    for p in soup.select('p,dl,ul,ol'):p.insert_after('\n\n')
    return soup.get_text()+'\n'
