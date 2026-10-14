import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import * as cheerio from 'cheerio';

const root=path.resolve(import.meta.dirname,'..');
const dist=path.join(root,'dist');
const report=JSON.parse(await fs.readFile(path.join(root,'tests/seo-build.json'),'utf8'));
const meta=JSON.parse(await fs.readFile(path.join(root,'content/publication.json'),'utf8'));
async function htmlFiles(dir) {
  const out=[];
  for(const entry of await fs.readdir(dir,{withFileTypes:true})) {
    const file=path.join(dir,entry.name);
    if(entry.isDirectory())out.push(...await htmlFiles(file));
    else if(entry.name.endsWith('.html'))out.push(file);
  }
  return out;
}

test('every generated HTML document has valid author, title and mode-dependent metadata',async()=>{
  const files=await htmlFiles(dist);assert.equal(files.length,report.html_documents);assert.ok(files.length>=497);
  let indexed=0;
  for(const file of files) {
    const $=cheerio.load(await fs.readFile(file,'utf8'));
    const name=path.relative(dist,file);
    assert.equal($('html').attr('lang'),'en',name);
    assert.equal($('head > title').length,1,name);
    assert.ok($('head > title').text().trim(),name);
    assert.equal($('meta[name=author]').attr('content'),meta.author,name);
    if(report.origin)assert.ok($('link[rel=canonical]').attr('href')?.startsWith(report.origin+'/'),name);
    else assert.equal($('link[rel=canonical]').length,0,name);
    const robots=$('meta[name=robots]').attr('content');assert.ok(robots,name);
    if(!robots.includes('noindex'))indexed++;
    if(!report.indexable)assert.ok(robots.includes('noindex'),name);
  }
  assert.equal(indexed,report.indexable_pages);
});

test('sitemap and crawler policy agree with production versus preview/local mode',async()=>{
  const sitemap=await fs.readFile(path.join(dist,'sitemap.xml'),'utf8');
  const robots=await fs.readFile(path.join(dist,'robots.txt'),'utf8');
  const count=(sitemap.match(/<loc>/g)||[]).length;
  assert.equal(count,report.indexable_pages);
  if(report.indexable) {
    assert.ok(robots.includes('Sitemap: '+report.origin+'/sitemap.xml'));
    assert.ok(robots.includes('User-agent: OAI-SearchBot\nAllow: /'));
    assert.ok(robots.includes('User-agent: GPTBot\nDisallow: /'));
  } else assert.ok(robots.includes('Disallow: /'));
});

test('output includes discovery files and PDF, but not source manifests or credentials',async()=>{
  for(const name of ['404.html','llms.txt','llms-full.txt','site.webmanifest','feed.xml','downloads/ctrotech-html-playbook.pdf'])assert.ok((await fs.stat(path.join(dist,name))).isFile(),name);
  for(const name of ['build-inputs.json','.env','.vercel','package.json','node_modules','tools'])await assert.rejects(fs.access(path.join(dist,name)),{code:'ENOENT'});
});
