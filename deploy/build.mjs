import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';
import {fileURLToPath} from 'node:url';
import * as cheerio from 'cheerio';
import {selectSource} from './integrity.mjs';
import {readHostingConfig} from './hosting.mjs';

const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const out=path.join(root,'dist');
await readHostingConfig(root);
const selected=await selectSource(root);
const source=selected.directory;
const meta=JSON.parse(await fs.readFile(path.join(root,'content/publication.json'),'utf8'));
const book=JSON.parse(await fs.readFile(path.join(root,'content/chapters.json'),'utf8'));
const api=JSON.parse(await fs.readFile(path.join(root,'content/api-register.json'),'utf8'));
const mode=process.env.VERCEL_ENV||process.env.DEPLOY_ENV||'development';
const production=mode==='production';
const configured=process.env.SITE_URL||(process.env.VERCEL_PROJECT_PRODUCTION_URL?`https://${process.env.VERCEL_PROJECT_PRODUCTION_URL}`:'');
let origin='';
if(configured){
  const u=new URL(configured);
  if(u.protocol!=='https:'||u.username||u.password||u.search||u.hash||!['','/'].includes(u.pathname)||u.port)throw new Error('SITE_URL must be a bare HTTPS origin, without credentials, path, query, fragment or port.');
  if(production&&process.env.SEO_TEST_MODE!=='1'&&(/(^|\.)(localhost|test|invalid|example)$/.test(u.hostname)||/^\d+(\.\d+){3}$/.test(u.hostname)))throw new Error('A real production hostname is required.');
  origin=u.origin;
}
if(production&&!origin)throw new Error('Missing production domain. Enable Vercel System Environment Variables or set SITE_URL=https://your-actual-domain. No placeholder canonicals will be published.');
const indexable=production&&!!origin;
const hash=x=>createHash('sha256').update(x).digest('hex').slice(0,12);
const escape=x=>String(x).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');
const clean=p=>{p=p.replace(/\\/g,'/');if(!p.startsWith('/'))p='/'+p;if(p==='/index.html')return '/';if(p.endsWith('/index.html'))return p.slice(0,-11)||'/';return p.replace(/\.html$/,'');};
const absolute=p=>origin?origin+p:p;
async function walk(dir){const files=[];for(const d of await fs.readdir(dir,{withFileTypes:true})){const p=path.join(dir,d.name);if(d.isDirectory())files.push(...await walk(p));else if(d.isFile())files.push(p);}return files.sort();}
await fs.rm(out,{recursive:true,force:true});await fs.cp(source,out,{recursive:true});
// Generated operational README is not a public search page.
await fs.rm(path.join(out,'DEPLOY.md'),{force:true});
await fs.rm(path.join(out,'build-inputs.json'),{force:true});
const assetMap=new Map();
const assetDir=path.join(out,'assets');
async function fingerprint(file,bytes){const rel='/'+path.relative(out,file).split(path.sep).join('/');const extension=path.extname(file);const name=file.slice(0,-extension.length)+'.'+hash(bytes)+extension;await fs.writeFile(name,bytes);await fs.rm(file);assetMap.set(rel,'/'+path.relative(out,name).split(path.sep).join('/'));}
for(const file of await walk(assetDir)){if(['site.css','site.js','search.js'].includes(path.basename(file)))continue;await fingerprint(file,await fs.readFile(file));}
let search=await fs.readFile(path.join(assetDir,'search.js'),'utf8');
const entries=JSON.parse(search.replace(/^window\.BOOK_SEARCH\s*=\s*/,'').trim().replace(/;$/,''));
for(const e of entries){const [p,fragment]=e.path.split('#');e.path=clean(p)+(fragment?'#'+fragment:'');}
search='window.BOOK_SEARCH = '+JSON.stringify(entries).replaceAll('<','\\u003c')+';\n';
await fingerprint(path.join(assetDir,'search.js'),Buffer.from(search));
await fingerprint(path.join(assetDir,'site.js'),await fs.readFile(path.join(assetDir,'site.js')));
let css=await fs.readFile(path.join(assetDir,'site.css'),'utf8');
for(const [before,after] of assetMap)css=css.replaceAll(before.replace('/assets/',''),after.replace('/assets/',''));
await fingerprint(path.join(assetDir,'site.css'),Buffer.from(css));
const mapped=p=>assetMap.get(p)||p;
function local(value,file){
 if(!value||/^(?:[a-z][a-z0-9+.-]*:|\/\/|#)/i.test(value))return value;
 const u=new URL(value,'https://local.invalid/'+file);return mapped(clean(u.pathname))+u.search+u.hash;
}
function auxiliary(title,body){return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>${escape(title)} | CTROTECH</title><link rel="stylesheet" href="/assets/site.css"></head><body><a class="skip" href="#main">Skip to main content</a><header class="wrap topinner"><a class="brand" href="/">CTROTECH / HTML Playbook</a><a href="/contents">Read the book</a></header><main id="main" class="wrap"><div class="page-heading"><h1>${escape(title)}</h1></div><div class="reference-body">${body}</div></main><footer class="wrap footbar"><span>© ${meta.copyright_year} ${escape(meta.author)}</span><a href="/">Back to the book</a></footer></body></html>`;}
await fs.writeFile(path.join(out,'404.html'),auxiliary('Page not found','<p>This address does not match a page in the playbook. Check the address or use the contents and reference desk.</p><p><a class="button primary" href="/contents">Open the contents</a> <a href="/reference">Open the reference desk</a></p>'));
await fs.writeFile(path.join(out,'privacy.html'),auxiliary('Privacy and local data','<p>This publication includes no analytics, advertising scripts, account service or tracking pixels. It does not collect applications or messages.</p><h2>Settings saved in your browser</h2><p>When available, local storage retains your theme, text size and marked chapters. These settings are not sent to a publication backend. Clear reading progress on the status page or remove this site’s data in your browser.</p><h2>Editable examples and demonstration forms</h2><p>The editable preview uses a restricted iframe. Parent DOM access and form submissions are blocked; resource loading is restricted. Inline scripts can run inside the preview. Do not paste secrets or run code you do not trust. Complete project forms demonstrate local validation, not a live application service. Use fictional details.</p><h2>Hosting and external links</h2><p>Vercel may process request information to deliver and protect the site. Its infrastructure policies and the owner’s project settings apply. External documentation has its own privacy practices. Adding Vercel Analytics or another service later requires reviewing this notice.</p><p>This describes the supplied implementation, not a jurisdiction-wide legal compliance certification.</p>'));
await fs.writeFile(path.join(out,'accessibility.html'),auxiliary('Accessibility and alternative formats','<p>The HTML edition is the primary reading format. Chapter text, examples, answers and reference registers are available without client-side rendering.</p><h2>Reading controls</h2><ul><li>Use the skip link to reach the main content.</li><li>Open search with its button or Control/Command K; Escape closes dialogs.</li><li>Change text size and theme in the chapter reading controls.</li><li>Scrollable examples and declaration blocks can receive keyboard focus.</li></ul><h2>PDF and exact code</h2><p>The PDF contains selectable text, links and bookmarks, but is not a tagged accessible PDF. Use the HTML edition for its semantic structure, and download exact code instead of copying wrapped PDF lines.</p><h2>Known limits</h2><p>Automated checks and browser tests do not replace assistive-technology testing. Independent accessibility review remains open; no WCAG certification is claimed. The <a href="/reference/status">status page</a> records executed checks and outstanding work.</p>'));

const person=absolute('/author#person'),organization=absolute('/#organization'),website=absolute('/#website'),bookId=absolute('/#book');
const names={'index.html':'The HTML Playbook by '+meta.author,'contents.html':'HTML Playbook contents: 74 chapters','author.html':meta.author+' | Author and publication credits','about.html':'About the HTML Playbook','projects.html':'Seven HTML reference projects','reference/index.html':'HTML reference desk','reference/api-members.html':'HTML API members and declarations','reference/keywords.html':'HTML keywords, states and events','privacy.html':'Privacy and local browser data','accessibility.html':'Accessibility and alternative formats','404.html':'Page not found'};
const descriptions={
 'index.html':'Learn HTML from document structure to forms, browser behavior and multi-page projects. A source-linked playbook by '+meta.author+'.',
 'contents.html':'Browse all 74 HTML chapters, with objectives, source routes, practical examples, exercises and explained answers.',
 'start.html':'Choose your HTML reading path, practise with the examples, understand this edition and report a content correction.',
 'author.html':'Author and publication credits for '+meta.author+' and the CTROTECH HTML Playbook, including copyright, preparation and source notices.',
 'about.html':'How to use the HTML Playbook: its curriculum, references, project files, source-backed approach and current review limits.',
 'projects.html':'Inspect and download seven static HTML reference projects: profile, portfolio, form, article, dashboard, gallery and multi-page capstone.',
 'privacy.html':'How the supplied CTROTECH HTML Playbook uses browser storage, restricted examples and static hosting, without included analytics.',
 'accessibility.html':'Keyboard reading controls, semantic HTML alternatives, exact code downloads and known PDF and accessibility-review limitations.'
};
const sitePages=[];
const sitemapExcluded=file=>file==='404.html'||file==='privacy.html'||file==='accessibility.html'||file==='reference/status.html'||file.startsWith('examples/')||file.startsWith('projects/');
async function enhance(file){
 const p=path.join(out,file);const $=cheerio.load(await fs.readFile(p,'utf8'));
 const route=clean(file);const chapter=book.find(c=>file===`chapters/${String(c.number).padStart(2,'0')}.html`);
 const h1=$('h1').first().text().replace(/\s+/g,' ').trim();
 const originalTitle=$('head > title').first().text().split(' | ')[0].trim();
 const name=names[file]||originalTitle||h1;
 const title=(name.length>85?name.slice(0,82)+'…':name)+(file==='index.html'?' | CTROTECH':' | CTROTECH');
 const bodyText=$('main p').filter((_,el)=>!$(el).hasClass('eyebrow')).first().text().replace(/\s+/g,' ').trim();
 let description=descriptions[file]||chapter?.dek||$('meta[name=description]').attr('content')||bodyText||('Read '+name+' in the CTROTECH HTML Playbook.');
 if(description.includes('A source-linked HTML curriculum and reference from CTROTECH.'))description=bodyText||('Explore '+name+' with captured definitions and source routes in the CTROTECH HTML Playbook.');
 description=description.replace(/\s+/g,' ').trim();if(description.length>180)description=description.slice(0,177).replace(/\s+\S*$/,'')+'…';
 const canIndex=indexable&&!sitemapExcluded(file);
 const robots=canIndex?'index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1':'noindex, follow';
 // Remove stale head metadata before adding a single authoritative set.
 $('head > title,meta[name=description],meta[name=author],meta[name=robots],meta[name=googlebot],meta[property^="og:"],meta[name^="twitter:"],link[rel=canonical],script[type="application/ld+json"]').remove();
 $('head').append($('<title>').text(title));
 function metadata(name,content,property=false){$('head').append($('<meta>').attr(property?'property':'name',name).attr('content',content));}
 metadata('description',description);metadata('author',meta.author);metadata('robots',robots);metadata('googlebot',robots);
 metadata('application-name','CTROTECH HTML Playbook');metadata('generator','CTROTECH static publication builder');
 metadata('DC.title',name);metadata('DC.creator',meta.author);metadata('DC.publisher',meta.imprint);metadata('DC.language','en');metadata('DC.rights',meta.copyright_notice);
 metadata('og:type',chapter?'article':'website',true);metadata('og:title',name,true);metadata('og:description',description,true);metadata('og:site_name','CTROTECH HTML Playbook',true);
 metadata('twitter:card','summary_large_image');metadata('twitter:title',name);metadata('twitter:description',description);
 const image=mapped('/assets/og-cover.jpg');
 if(origin){
  $('head').append($('<link>').attr('rel','canonical').attr('href',absolute(route)));
  metadata('DC.identifier',absolute(route));metadata('og:url',absolute(route),true);metadata('og:image',absolute(image),true);metadata('og:image:secure_url',absolute(image),true);metadata('og:image:type','image/jpeg',true);metadata('og:image:width','1200',true);metadata('og:image:height','630',true);metadata('og:image:alt','The HTML Playbook by '+meta.author+', CTROTECH',true);metadata('twitter:image',absolute(image));metadata('twitter:image:alt','CTROTECH HTML Playbook cover');
 }
 if(chapter){metadata('article:author',absolute('/author'),true);metadata('article:published_time',meta.publication_date+'T00:00:00+01:00',true);metadata('article:modified_time',meta.publication_date+'T00:00:00+01:00',true);metadata('article:section',chapter.part.split(' / ').at(-1),true);}
 if(indexable){for(const [env,key] of [['GOOGLE_SITE_VERIFICATION','google-site-verification'],['BING_SITE_VERIFICATION','msvalidate.01'],['YANDEX_SITE_VERIFICATION','yandex-verification'],['PINTEREST_SITE_VERIFICATION','p:domain_verify']])if(process.env[env])metadata(key,process.env[env]);}
 // Never invent profile handles, publisher accounts, ratings, ISBNs or translations.
 if(origin&&!sitemapExcluded(file)){
  const graph=[{'@type':'Person','@id':person,name:meta.author,url:absolute('/author')},{'@type':'Organization','@id':organization,name:meta.imprint,url:absolute('/'),logo:{'@type':'ImageObject',url:absolute(mapped('/assets/icon-512.png')),width:512,height:512}},{'@type':'WebSite','@id':website,name:'CTROTECH HTML Playbook',url:absolute('/'),inLanguage:'en',publisher:{'@id':organization}},{'@type':'Book','@id':bookId,name:meta.title,author:{'@id':person},publisher:{'@id':organization},inLanguage:'en',bookEdition:meta.edition_label,datePublished:meta.publication_date,dateModified:meta.publication_date,isAccessibleForFree:true,url:absolute('/'),image:absolute(image),bookFormat:'https://schema.org/EBook',description:'A source-linked HTML curriculum and reference. '+meta.technical_release_status,encoding:{'@type':'MediaObject',contentUrl:absolute('/downloads/ctrotech-html-playbook.pdf'),encodingFormat:'application/pdf'}}];
  graph.push({'@type':chapter?'TechArticle':file==='author.html'?'ProfilePage':'WebPage','@id':absolute(route)+'#page',url:absolute(route),name,headline:name,description,inLanguage:'en',isPartOf:{'@id':chapter?bookId:website},author:{'@id':person},publisher:{'@id':organization},datePublished:meta.publication_date,dateModified:meta.publication_date,...(chapter?{learningResourceType:'Tutorial',position:chapter.number}:{})});
  const crumbs=[{name:'The HTML Playbook',item:absolute('/')}];
  if(file.startsWith('chapters/'))crumbs.push({name:'Contents',item:absolute('/contents')});
  else if(file.startsWith('reference/')){crumbs.push({name:'Reference',item:absolute('/reference')});if(file.startsWith('reference/api/'))crumbs.push({name:'API declarations',item:absolute('/reference/api-members')});}
  if(route!=='/'&&route!=='/reference')crumbs.push({name,item:absolute(route)});
  if(crumbs.length>1)graph.push({'@type':'BreadcrumbList',itemListElement:crumbs.map((r,i)=>({'@type':'ListItem',position:i+1,...r}))});
  $('head').append('<script type="application/ld+json">'+JSON.stringify({'@context':'https://schema.org','@graph':graph}).replaceAll('<','\\u003c')+'</script>');
 }
 $('head').append('<link rel="manifest" href="/site.webmanifest"><link rel="apple-touch-icon" sizes="180x180" href="'+mapped('/assets/apple-touch-icon.png')+'"><link rel="icon" type="image/png" sizes="32x32" href="'+mapped('/assets/favicon-32.png')+'"><link rel="alternate" type="application/atom+xml" title="Playbook release notes" href="/feed.xml">');
 if(!file.startsWith('examples/')&&!file.startsWith('projects/'))$('head').append('<link rel="preload" as="font" type="font/ttf" crossorigin="anonymous" href="'+mapped('/assets/fonts/InstrumentSerif-Regular.ttf')+'">');
 if(chapter)$('head').append('<link rel="alternate" type="text/markdown" title="Chapter Markdown" href="/markdown/chapter-'+String(chapter.number).padStart(2,'0')+'.md">');
 $('[href],[src],[poster],[action]').each((_,el)=>{for(const attr of ['href','src','poster','action']){const value=$(el).attr(attr);if(value!==undefined)$(el).attr(attr,local(value,file));}});
 $('body').attr('data-base','');$('code,pre').attr('translate','no');
 if(!file.startsWith('examples/')&&!file.startsWith('projects/'))$('footer').first().append('<nav class="delivery-links" aria-label="Publication information"><a href="/site-map">Site map</a><a href="/privacy">Privacy</a><a href="/accessibility">Accessibility</a><a href="/llms.txt">Text index</a></nav>');
 // A source example may intentionally have no h1. Do not rewrite its teaching body.
 await fs.writeFile(p,$.html());
 const record={file,path:route,title,description,indexable:canIndex,chapter:chapter?.number||null};sitePages.push(record);return record;
}
for(const p of await walk(out))if(p.endsWith('.html'))await enhance(path.relative(out,p).split(path.sep).join('/'));
const mapLinks=sitePages.filter(p=>!sitemapExcluded(p.file)).sort((a,b)=>a.path.localeCompare(b.path));
await fs.writeFile(path.join(out,'site-map.html'),auxiliary('Site map','<p>Browse the readable pages in this edition. Demonstration documents, raw downloads and internal review evidence are not search landing pages.</p><ul>'+mapLinks.map(p=>'<li><a href="'+p.path+'">'+escape(p.title.replace(' | CTROTECH',''))+'</a></li>').join('')+'</ul>'));
await enhance('site-map.html');
const indexed=sitePages.filter(p=>p.indexable).sort((a,b)=>a.path.localeCompare(b.path));
await fs.writeFile(path.join(out,'sitemap.xml'),'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+indexed.map(p=>'<url><loc>'+escape(absolute(p.path))+'</loc><lastmod>'+meta.publication_date+'</lastmod></url>').join('')+'</urlset>\n');
const group=(agent,allow)=>'User-agent: '+agent+'\n'+(allow?'Allow: /\n':'Disallow: /\n');
let robots=group('*',indexable);
if(indexable){robots+='\n# Search discovery is allowed. This is not a blanket copyright or training grant.\n';for(const bot of ['OAI-SearchBot','Claude-SearchBot'])robots+='\n'+group(bot,true);for(const bot of ['GPTBot','ClaudeBot','Google-Extended','CCBot'])robots+='\n'+group(bot,false);robots+='\nSitemap: '+absolute('/sitemap.xml')+'\n';}
await fs.writeFile(path.join(out,'robots.txt'),robots);
await fs.writeFile(path.join(out,'site.webmanifest'),JSON.stringify({id:'/',name:'CTROTECH HTML Playbook',short_name:'HTML Playbook',lang:'en',description:'Source-linked HTML chapters, examples and references.',start_url:'/',scope:'/',display:'standalone',background_color:'#faf8f1',theme_color:'#234d42',icons:[{src:mapped('/assets/icon-192.png'),sizes:'192x192',type:'image/png',purpose:'any'},{src:mapped('/assets/icon-512.png'),sizes:'512x512',type:'image/png',purpose:'any maskable'}]},null,2)+'\n');
const markdownDir=path.join(out,'markdown');await fs.mkdir(markdownDir,{recursive:true});
const chapterDocs=[];
for(const c of book){const n=String(c.number).padStart(2,'0');const fence='`'.repeat(Math.max(3,...[...c.code.matchAll(/`+/g)].map(m=>m[0].length+1)));const md=`# ${c.number}. ${c.title}\n\n${c.dek}\n\nAuthor: ${meta.author}\nCanonical: ${absolute('/chapters/'+n)}\nEdition: ${meta.edition_label}\nStatus: technical and independent review remain open.\n\n## Objectives\n\n${c.objectives.map(s=>'- '+s).join('\n')}\n\n${c.lesson}\n\n## Example\n\n${fence}html\n${c.code}\n${fence}\n\n${c.explanation}\n\n## Common mistake\n\n${c.mistake}\n\n## Exercise\n\n${c.question}\n\n## Explained answer\n\n${c.answer}\n\n## Sources\n\n${c.sources.map(s=>'- ['+s.title+']('+s.url+')').join('\n')}\n\n${meta.copyright_notice}\n${meta.reuse_license}\n`;
 await fs.writeFile(path.join(markdownDir,'chapter-'+n+'.md'),md);chapterDocs.push({c,n,md});}
const textIndex=`# CTROTECH HTML Playbook\n\n> A source-linked HTML curriculum, reference and project collection by ${meta.author}.\n\nEdition: ${meta.edition_label}. Captured/review position: ${meta.publication_date}. ${meta.technical_release_status}.\n\nThis is a plain-text discovery index, not a universal crawler protocol, ranking guarantee or copyright/training license. Browser implementation support and independent review must not be inferred from a declaration or a checker pass.\n\n## Start here\n\n- [Book](${absolute('/')})\n- [Reading guide and edition notes](${absolute('/start')})\n- [Contents](${absolute('/contents')})\n- [Author and rights](${absolute('/author')})\n- [Reference desk](${absolute('/reference')})\n- [API declaration register](${absolute('/reference/api-members')})\n- [Keywords, states and events](${absolute('/reference/keywords')})\n- [Machine-readable API register](${absolute('/data/api-register.json')})\n- [Review evidence and limitations](${absolute('/reference/status')})\n- [Sitemap](${absolute('/sitemap.xml')})\n- [Full chapter text](${absolute('/llms-full.txt')})\n- [PDF](${absolute('/downloads/ctrotech-html-playbook.pdf')})\n\n## Chapters\n\n${chapterDocs.map(({c,n})=>'- ['+c.number+'. '+c.title+']('+absolute('/markdown/chapter-'+n+'.md')+')').join('\n')}\n\n## Rights\n\n${meta.copyright_notice}\n${meta.reuse_license}\nSearch retrieval permissions and training permissions are separate. robots.txt expresses the supplied crawler preferences; it is not access control.\n`;
await fs.writeFile(path.join(out,'llms.txt'),textIndex);
await fs.writeFile(path.join(out,'llms-full.txt'),textIndex+'\n'+chapterDocs.map(x=>x.md).join('\n\n')+'\n## API declaration index\n\n'+api.records.map(r=>'### '+r.name+'\n\n'+r.definitions.join('\n\n')+'\n\nSource: '+r.source_url).join('\n\n'));
if(origin)await fs.writeFile(path.join(out,'feed.xml'),'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><id>'+escape(absolute('/'))+'</id><title>CTROTECH HTML Playbook releases</title><link href="'+escape(absolute('/feed.xml'))+'" rel="self"/><link href="'+escape(absolute('/'))+'"/><updated>'+meta.publication_date+'T00:00:00+01:00</updated><author><name>'+escape(meta.author)+'</name></author><entry><id>'+escape(absolute('/#edition-'+meta.edition))+'</id><title>'+escape(meta.edition_label)+'</title><updated>'+meta.publication_date+'T00:00:00+01:00</updated><link href="'+escape(absolute('/'))+'"/><summary>HTML chapters, exact examples, declaration registers and a matching PDF. Technical review limitations are documented.</summary></entry></feed>');
else await fs.writeFile(path.join(out,'feed.xml'),'<?xml version="1.0" encoding="utf-8"?><feed xmlns="http://www.w3.org/2005/Atom"><id>urn:ctrotech:html-playbook:local</id><title>Local preview, not a published feed</title><updated>'+meta.publication_date+'T00:00:00+01:00</updated></feed>');
if(process.env.INDEXNOW_KEY){if(!/^[A-Za-z0-9-]{8,128}$/.test(process.env.INDEXNOW_KEY))throw new Error('Invalid INDEXNOW_KEY format.');await fs.writeFile(path.join(out,process.env.INDEXNOW_KEY+'.txt'),process.env.INDEXNOW_KEY);}
const report={mode,origin:origin||null,indexable,html_documents:sitePages.length,indexable_pages:indexed.length,markdown_chapters:chapterDocs.length,hashed_assets:assetMap.size,edition:meta.edition,created_from:'precompiled site/ plus canonical content metadata; no live source fetches during deployment',limitations:'No search ranking, rich-result eligibility, AI citation, universal compatibility or independent content approval is guaranteed.'};
await fs.mkdir(path.join(root,'tests'),{recursive:true});await fs.writeFile(path.join(root,'tests/seo-build.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify(report,null,2));
