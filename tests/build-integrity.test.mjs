import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {spawnSync} from 'node:child_process';
import {inputDigest, verifyInputs, manifestVersion, hashPolicy} from '../deploy/integrity.mjs';

const manifest = files => ({format_version:manifestVersion, hash_policy:hashPolicy, files});
const json = '{"scripts":{"build":"node deploy/build.mjs"},"dependencies":{"cheerio":"1.2.0"},"text":"keep  two spaces; \\"quoted\\" and \\\\ path"}';

test('JSON indentation, blank lines, trailing whitespace and Windows line endings are harmless', () => {
  const source = JSON.stringify(JSON.parse(json), null, 2) + '\n';
  const variants = [json, source, source.replaceAll('\n','\r\n'), source+'\n\n \t'];
  for (const value of variants) assert.equal(inputDigest('package-lock.json',Buffer.from(value)),inputDigest('package-lock.json',Buffer.from(json)));
});

test('whitespace inside JSON strings is protected', () => {
  assert.notEqual(inputDigest('content/chapters.json',Buffer.from('{"code":"a  b"}')),inputDigest('content/chapters.json',Buffer.from('{"code":"a b"}')));
  assert.notEqual(inputDigest('content/chapters.json',Buffer.from('{"code":"a\\nb"}')),inputDigest('content/chapters.json',Buffer.from('{"code":"a\\r\\nb"}')));
});

test('dependency versions and added dependencies are protected', () => {
  const original = inputDigest('package.json',Buffer.from(json));
  assert.notEqual(original,inputDigest('package.json',Buffer.from(json.replace('1.2.0','99.0.0'))));
  const changed=JSON.parse(json);changed.dependencies.injected='1.0.0';
  assert.notEqual(original,inputDigest('package.json',Buffer.from(JSON.stringify(changed))));
});

test('non-JSON source and binary assets remain byte-exact', () => {
  for (const name of ['assets/site.js','tools/build.py','fonts/book.ttf']) assert.notEqual(inputDigest(name,Buffer.from('a\n')),inputDigest(name,Buffer.from('a\r\n')));
});

test('invalid JSON is rejected rather than repaired by normalization', () => {
  assert.throws(()=>inputDigest('package.json',Buffer.from('{"ok":tr ue}')),SyntaxError);
});

test('Python and Node use the same normalization, including every retained input', async (t) => {
  const root=path.resolve(import.meta.dirname,'..');
  const program='import sys,json;from pathlib import Path;sys.path.insert(0,"tools");from fingerprint import input_digest,input_paths;print(json.dumps({p.relative_to(Path.cwd()).as_posix():input_digest(p) for p in input_paths(Path.cwd())}))';
  const python=spawnSync(process.env.PYTHON_BINARY || (process.platform==='win32'?'python':'python3'),['-c',program],{cwd:root,encoding:'utf8'});
  if (python.error?.code==='ENOENT') return t.skip('Python is optional for Node-only deployment; cross-language parity requires it'); // Deployment itself is Node-only; CI has Python.
  assert.equal(python.status,0,python.stderr);
  for (const [name,digest] of Object.entries(JSON.parse(python.stdout))) assert.equal(inputDigest(name,await fs.readFile(path.join(root,name))),digest,name);
});

test('guard accepts harmless formatting, reports all stale inputs and rejects missing files', async () => {
  const root=await fs.mkdtemp(path.join(os.tmpdir(),'ctrobook-integrity-'));
  try {
    const a='{"x":"same  text"}';const b='{"version":"1.0.0"}';
    await fs.writeFile(path.join(root,'a.json'),'\r\n{\r\n "x": "same  text"\r\n}\r\n\r\n');
    await fs.writeFile(path.join(root,'b.json'),b);
    const captured=manifest({'a.json':inputDigest('a.json',Buffer.from(a)),'b.json':inputDigest('b.json',Buffer.from(b))});
    await verifyInputs(root,captured);
    await fs.writeFile(path.join(root,'a.json'),'{"x":"changed"}');await fs.unlink(path.join(root,'b.json'));
    await assert.rejects(verifyInputs(root,captured),error=>error.message.includes('a.json')&&error.message.includes('b.json (missing)'));
  } finally {await fs.rm(root,{recursive:true,force:true});}
});

test('old manifests and out-of-root paths fail closed', async () => {
  await assert.rejects(verifyInputs(process.cwd(),{files:{}}),/Unsupported build-input manifest/);
  await assert.rejects(verifyInputs(process.cwd(),manifest({'../outside.json':'a'.repeat(64)})),/Invalid build-input manifest entry/);
});
