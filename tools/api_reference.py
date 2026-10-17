"""Render the captured declaration register without claiming behavior-level review."""
import json,re
from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from html import escape as esc
from behavior_reference import render_behavior,units,markdown

def slug(name):return re.sub(r'[^a-z0-9]+','-',name.lower()).strip('-')
def build_api(root,write,shell):
    data=json.loads((root/'content/api-register.json').read_text())
    records=data['records'];known={r['name'] for r in records}
    note='<p class="review-note">Extracted declaration reference, captured 14 October 2026. Signatures identify declared shapes, not complete behavior or browser support. Follow the normative definition for conversions, defaults, errors, security restrictions and side effects. An owner route is not claimed to be a matched member definition.</p>'
    index='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow"><a href="index.html">Reference desk</a></p><h1>API members and declarations</h1><p>314 named declarations, 1,574 direct member declarations and 73 mixin inclusions from the captured HTML WebIDL. Partial declarations are consolidated by name; inherited and mixed-in members are linked, not silently duplicated.</p></div>'+note+'<div class="reference-controls"><label>Find a declaration<input id="reference-search" type="search" placeholder="Window, HTMLInputElement, Canvas…"></label></div><p id="reference-count" role="status" class="small-note">314 entries</p><div class="reference-grid">'
    for r in records:
        name=r['name'];url='api/'+slug(name)+'.html'
        index+=f'<article class="ref-card" data-reference-entry data-category="all" data-search="{esc((name+" "+r["type"]+" "+" ".join(m["name"] for m in r["members"])).lower(),quote=True)}"><h2><a href="{url}">{esc(name)}</a></h2><p>{esc(r["type"])}. {len(r["members"])} direct member declarations.</p></article>'
        body=f'<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow"><a href="../api-members.html">API declaration register</a></p><h1>{esc(name)}</h1><p>{esc(r["type"])} from the captured HTML Standard WebIDL.</p></div><div class="reference-body">'+note
        if r.get('inheritance'):
            parent=r['inheritance'];target=slug(parent)+'.html'
            body+='<p>Inherits from '+(f'<a href="{target}"><code>{esc(parent)}</code></a>' if parent in known else f'<code>{esc(parent)}</code> (defined outside this captured owner register)')+'. Inherited members remain documented on their declaring interface.</p>'
        if r['includes']:body+='<h2>Included mixins</h2><ul>'+''.join('<li>'+(f'<a href="{slug(n)}.html">{esc(n)}</a>' if n in known else esc(n))+'</li>' for n in r['includes'])+'</ul>'
        if r.get('values') is not None:body+='<h2>Enumeration values</h2><ul>'+''.join('<li><code>'+esc(json.dumps(v,ensure_ascii=False))+'</code></li>' for v in r['values'])+'</ul><p>These are WebIDL enumeration strings, not a blanket list of HTML attribute keywords. Invalid values follow the consuming algorithm.</p>'
        body+='<h2>Declared shape</h2><pre class="idl-source codebox" tabindex="0" role="region" aria-label="Scrollable WebIDL declaration"><code>'+highlight('\n\n'.join(r['definitions']),get_lexer_by_name('webidl',ensurenl=False,stripnl=False),HtmlFormatter(nowrap=True)).removesuffix('\n')+'</code></pre><p><a href="'+esc(r['source_url'],quote=True)+'">Read the normative owner definition</a></p>'
        if r['members']:
            body+='<h2>Direct members</h2><p>Overloads remain separate rows. Read-only describes the WebIDL declaration. Extended attributes such as PutForwards and Replaceable can affect assignment; read-only does not promise an immutable returned object.</p><div class="reference-table"><table><caption>Declared members of '+esc(name)+'</caption><thead><tr><th scope="col">Declaration</th><th scope="col">Kind</th><th scope="col">Definition</th></tr></thead><tbody>'
            for i,m in enumerate(r['members']):
                body+=f'<tr id="member-{i+1}"><th scope="row"><code>{esc(m["signature"])}</code></th><td>{esc(m["kind"])}'+(' / read-only' if m['readonly'] else '')+'</td><td><a href="'+esc(m['definition_url'],quote=True)+'">'+esc(m['definition_match'])+'</a></td></tr>'
            body+='</tbody></table></div>'
        def behavior_code(source,language):
            return '<pre class="codebox" tabindex="0" role="region" aria-label="Scrollable '+esc(language,quote=True)+' example"><code>'+highlight(source,get_lexer_by_name(language,ensurenl=False,stripnl=False),HtmlFormatter(nowrap=True)).removesuffix('\n')+'</code></pre>'
        def behavior_inline(text):
            return re.sub(r'`([^`]+)`',r'<code>\1</code>',esc(str(text)))
        body+=render_behavior(root,name,behavior_inline,behavior_code)
        body+='<h2>Check behavior before using it</h2><p>Exposed globals, secure-context requirements, overload resolution and conversions can change which operation is available or chosen. A signature alone does not list every exception or permission rule. Check the linked algorithm and current implementation evidence.</p></div></main>'
        write('reference/api/'+slug(name)+'.html',shell(name+' API reference',body,base='../../',description=f'Inspect {name}: captured WebIDL declarations, direct member signatures, inheritance, mixins and normative definition links.'))
    index+='</div><div class="reference-body"><h2>Snapshot and scope</h2><p>Derived from the HTML Standard through W3C Webref. Extraction is not independent technical review. The <a href="../data/api-register.json">machine-readable register</a> includes source URLs, hashes, match labels and capture date. <a href="keywords.html">Look up attribute keywords, input states and events</a>.</p><p><a href="https://whatwg.org/ipr-policy#copyright-license-grant">WHATWG source terms</a>; <a href="../assets/webref-MIT.txt">Webref extraction software notice</a>.</p></div></main>'
    write('reference/api-members.html',shell('API members and declarations',index,base='../',description='Search 314 named HTML WebIDL declarations and inspect 1,574 direct member declarations with normative definition routes.'))
    keywords='<main id="main" class="wrap"><div class="page-heading"><p class="eyebrow"><a href="index.html">Reference desk</a></p><h1>Keywords, states and events</h1><p>437 public definition records from the captured HTML Standard, grouped by their actual definition type. This is a definition-route register, not a complete missing-value, invalid-value or applicability table.</p></div>'+note+'<div class="reference-controls"><label>Find a definition<input id="reference-search" type="search" placeholder="crossorigin, checkbox, change…"></label><label>Definition type<select id="reference-filter"><option value="all">All definitions</option>'+''.join(f'<option value="{k}">{k}</option>' for k in ['attr-value','element-state','enum-value','event'])+'</select></label></div><p id="reference-count" role="status" class="small-note">437 entries</p><div class="reference-grid">'
    for definition_index,d in enumerate(data['keyword_records'],1):
        search=' '.join(d['names']+d['contexts']+[d['section']]).lower()
        keywords+=f'<article class="ref-card" id="{esc(d["id"],quote=True)}-{definition_index}" data-reference-entry data-category="{d["type"]}" data-search="{esc(search,quote=True)}"><h2>{esc(" / ".join(d["names"]))}</h2><span class="badge">{d["type"]}</span><p>Contexts: {esc(", ".join(d["contexts"]) or "See definition")}</p><p>{esc(d["section"])}</p><a href="{esc(d["url"],quote=True)}">Normative definition</a></article>'
    write('reference/keywords.html',shell('Keywords, states and events',keywords+'</div></main>',base='../',description='Find captured HTML attribute keywords, input states, enumeration values and event definition routes by context and name.'))
    write('data/api-register.json',json.dumps(data,ensure_ascii=False,separators=(',',':'))+'\n')

    write('data/api-behavior.json',json.dumps({'schema_version':1,'units':units(root)},ensure_ascii=False,separators=(',',':'))+'\n')
    for unit in units(root):write('markdown/'+unit['id']+'.md',markdown(unit))
