import fs from 'node:fs/promises';
import path from 'node:path';
import {createHash} from 'node:crypto';

export const manifestVersion = 2;
export const hashPolicy = 'sha256-json-whitespace-v1';

// Preserve every JSON string and token. Ignore only insignificant JSON
// whitespace outside strings. Do not ignore dependency, content or code edits.
export function inputBytes(name, bytes) {
  const data = Buffer.from(bytes);
  if (path.extname(name).toLowerCase() !== '.json') return data;
  const text = data.toString('utf8');
  JSON.parse(text); // Reject invalid JSON before any normalization.
  return Buffer.from(text.replace(/"(?:\\.|[^"\\])*"|[ \t\r\n]+/g,
    token => token.startsWith('"') ? token : ''), 'utf8');
}

export function inputDigest(name, bytes) {
  return createHash('sha256').update(inputBytes(name, bytes)).digest('hex');
}

export async function verifyInputs(root, manifest) {
  if (manifest.format_version !== manifestVersion || manifest.hash_policy !== hashPolicy) {
    throw new Error('Unsupported build-input manifest. Rebuild with python3 tools/build.py before deployment. Do not edit manifest hashes by hand.');
  }
  if (!manifest.files || typeof manifest.files !== 'object' || Array.isArray(manifest.files)) {
    throw new Error('Invalid build-input manifest: files must be an object.');
  }
  const base = path.resolve(root);
  const changed = [];
  for (const [name, expected] of Object.entries(manifest.files)) {
    const file = path.resolve(base, name);
    if (!file.startsWith(base + path.sep) || !/^[a-f0-9]{64}$/.test(expected)) {
      throw new Error('Invalid build-input manifest entry: ' + name);
    }
    try {
      const actual = inputDigest(name, await fs.readFile(file));
      if (actual !== expected) changed.push(name);
    } catch (error) {
      if (error.code === 'ENOENT') changed.push(name + ' (missing)');
      else throw new Error('Cannot validate ' + name + ': ' + error.message, {cause: error});
    }
  }
  if (changed.length) {
    throw new Error('Precompiled site is stale: ' + changed.join(', ') + '. Formatting-only JSON whitespace is allowed; actual content, dependency and build-code edits require python3 tools/build.py (add --pdf for manuscript/PDF changes). Do not disable this check or replace hashes by hand.');
  }
}


// A git pull can update tracked site/ while leaving ignored build/site stale.
// Use only a candidate whose complete protected-input manifest is current.
export async function selectSource(root) {
  const failures=[];
  for (const name of ['build/site','site']) {
    const candidate=path.join(root,name);
    try {
      const captured=JSON.parse(await fs.readFile(path.join(candidate,'build-inputs.json'),'utf8'));
      await verifyInputs(root,captured);
      return {directory:candidate, skipped:failures};
    } catch (error) {
      failures.push({directory:name, reason:error.message});
    }
  }
  throw new Error('No current precompiled book snapshot. '+failures.map(x=>x.directory+': '+x.reason).join(' | '));
}
