import fs from 'node:fs/promises';
import path from 'node:path';

// Hosting settings are not inputs to the Python-rendered book snapshot.
// Validate the small routing/output contract independently, without pinning
// optional Vercel metadata, ordering, redirects or headers to an old hash.
export function validateHostingConfig(config) {
  const fail = message => { throw new Error('Invalid hosting configuration: '+message+' This is a deployment setting, not a stale manuscript.'); };
  if (!config || typeof config !== 'object' || Array.isArray(config)) fail('vercel.json must contain an object.');
  const output=typeof config.outputDirectory==='string' ? path.posix.normalize(config.outputDirectory).replace(/\/$/,'') : '';
  if (output !== 'dist') fail('outputDirectory must be "dist" for this compiler.');
  if (config.cleanUrls !== true) fail('cleanUrls must be true because generated links omit .html.');
  if (config.trailingSlash !== false) fail('trailingSlash must be false to match generated canonical routes.');
  if (config.framework != null) fail('use the static Other preset (framework null or omitted), not an application framework.');
  for (const name of ['headers','redirects','rewrites']) {
    if (config[name] !== undefined && !Array.isArray(config[name])) fail(name+' must be an array when supplied.');
  }
  return config;
}

export async function readHostingConfig(root) {
  let config;
  try { config = JSON.parse(await fs.readFile(path.join(root,'vercel.json'),'utf8')); }
  catch (error) { throw new Error('Cannot read hosting configuration vercel.json: '+error.message, {cause:error}); }
  return validateHostingConfig(config);
}
