import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import {spawnSync} from 'node:child_process';
import {validateHostingConfig} from '../deploy/hosting.mjs';
import {selectSource,inputDigest,manifestVersion,hashPolicy} from '../deploy/integrity.mjs';

const root=path.resolve(import.meta.dirname,'..');
const base={framework:null,outputDirectory:'dist',cleanUrls:true,trailingSlash:false};
const manifest=data=>({format_version:manifestVersion,hash_policy:hashPolicy,files:{'data.json':inputDigest('data.json',Buffer.from(data))}});

test('hosting metadata, property order, regions and redirects are not manuscript changes',()=>{
  assert.doesNotThrow(()=>validateHostingConfig({...base,regions:['iad1'],headers:[],redirects:[{source:'/start',destination:'/contents',permanent:true}]}));
  assert.doesNotThrow(()=>validateHostingConfig(Object.fromEntries(Object.entries(base).reverse())));
  assert.doesNotThrow(()=>validateHostingConfig({...base,outputDirectory:'./dist/'}));
});

test('incompatible output and routing settings fail with hosting-specific guidance',()=>{
  for(const patch of [{outputDirectory:'other'},{cleanUrls:false},{trailingSlash:true},{framework:'nextjs'},{headers:{}}])assert.throws(()=>validateHostingConfig({...base,...patch}),/Invalid hosting configuration/);
  assert.throws(()=>validateHostingConfig(null),/Invalid hosting configuration/);
});

test('an ignored stale local snapshot cannot shadow the current tracked snapshot',async()=>{
  const dir=await fs.mkdtemp(path.join(os.tmpdir(),'ctrobook-sources-'));
  try{
    await fs.mkdir(path.join(dir,'build/site'),{recursive:true});await fs.mkdir(path.join(dir,'site'));
    await fs.writeFile(path.join(dir,'data.json'),'{"value":"current"}');
    await fs.writeFile(path.join(dir,'build/site/build-inputs.json'),JSON.stringify(manifest('{"value":"old"}')));
    await fs.writeFile(path.join(dir,'site/build-inputs.json'),JSON.stringify(manifest('{"value":"current"}')));
    const chosen=await selectSource(dir);assert.equal(chosen.directory,path.join(dir,'site'));assert.equal(chosen.skipped.length,1);
  }finally{await fs.rm(dir,{recursive:true,force:true});}
});

test('all stale candidates still reject a real content edit',async()=>{
  const dir=await fs.mkdtemp(path.join(os.tmpdir(),'ctrobook-stale-'));
  try{
    await fs.mkdir(path.join(dir,'site'));await fs.writeFile(path.join(dir,'data.json'),'{"value":"changed"}');
    await fs.writeFile(path.join(dir,'site/build-inputs.json'),JSON.stringify(manifest('{"value":"old"}')));
    await assert.rejects(selectSource(dir),/Precompiled site is stale: data.json/);
  }finally{await fs.rm(dir,{recursive:true,force:true});}
});

test('the snapshot manifest excludes hosting config but protects book data and dependencies',async()=>{
  const selected=await selectSource(root);const captured=JSON.parse(await fs.readFile(path.join(selected.directory,'build-inputs.json'),'utf8'));
  assert.ok(!Object.hasOwn(captured.files,'vercel.json'));
  for(const key of ['content/chapters.json','content/publication.json','package.json','package-lock.json'])assert.ok(Object.hasOwn(captured.files,key),key);
});

test('actual compiler accepts changed hosting config and stale local cache, but rejects manuscript edits',async()=>{
  await fs.mkdir(path.join(root,'.cache'),{recursive:true});
  const dir=await fs.mkdtemp(path.join(root,'.cache','hosting-fixture-'));
  try{
    for(const name of ['content','assets','fonts','deploy','tools'])await fs.cp(path.join(root,name),path.join(dir,name),{recursive:true});
    for(const name of ['package.json','package-lock.json','requirements-build.txt','requirements-verify.txt','vercel.json'])await fs.copyFile(path.join(root,name),path.join(dir,name));
    await fs.mkdir(path.join(dir,'tests'));await fs.copyFile(path.join(root,'tests/nu-download-provenance.json'),path.join(dir,'tests/nu-download-provenance.json'));
    const source=await selectSource(root);await fs.cp(source.directory,path.join(dir,'site'),{recursive:true});
    const config=JSON.parse(await fs.readFile(path.join(dir,'vercel.json'),'utf8'));
    config.regions=['iad1'];config.redirects.push({source:'/hosting-regression',destination:'/contents',permanent:true});
    await fs.writeFile(path.join(dir,'vercel.json'),JSON.stringify(Object.fromEntries(Object.entries(config).reverse()),null,4)+'\r\n\r\n');
    const run=()=>spawnSync(process.execPath,['deploy/build.mjs'],{cwd:dir,env:process.env,encoding:'utf8',timeout:90000});
    let result=run();assert.equal(result.status,0,result.stdout+result.stderr);
    const first=JSON.parse(await fs.readFile(path.join(dir,'tests/seo-build.json'),'utf8'));assert.equal(first.html_documents,497);
    await fs.mkdir(path.join(dir,'build/site'),{recursive:true});const stale=JSON.parse(await fs.readFile(path.join(dir,'site/build-inputs.json'),'utf8'));
    stale.files['content/chapters.json']='0'.repeat(64);await fs.writeFile(path.join(dir,'build/site/build-inputs.json'),JSON.stringify(stale));
    result=run();assert.equal(result.status,0,result.stdout+result.stderr);
    const chapter=path.join(dir,'content/chapters.json');const book=JSON.parse(await fs.readFile(chapter,'utf8'));book[0].title+=' changed';await fs.writeFile(chapter,JSON.stringify(book));
    result=run();assert.notEqual(result.status,0);assert.match(result.stderr,/content\/chapters.json/);
  }finally{await fs.rm(dir,{recursive:true,force:true});}
});
