// Optional post-deployment submission. No requests are sent without --submit.
import fs from 'node:fs/promises';
const raw=await fs.readFile(new URL('../dist/sitemap.xml',import.meta.url),'utf8');
const urls=[...raw.matchAll(/<loc>([^<]+)<\/loc>/g)].map(m=>m[1].replaceAll('&amp;','&'));
if(!urls.length)throw new Error('Build a production sitemap with the real SITE_URL before submission.');
const host=new URL(urls[0]).host,key=process.env.INDEXNOW_KEY;
if(!key||!/^[A-Za-z0-9-]{8,128}$/.test(key))throw new Error('Set the same INDEXNOW_KEY used by the production build.');
const body={host,key,keyLocation:`https://${host}/${key}.txt`,urlList:urls};
if(!process.argv.includes('--submit')){console.log(JSON.stringify({dryRun:true,host,urls:urls.length,keyLocation:body.keyLocation,note:'No network request sent. After public deployment and key-file verification, add --submit.'},null,2));}
else{
 const proof=await fetch(body.keyLocation);if(!proof.ok||(await proof.text()).trim()!==key)throw new Error('Public IndexNow key file did not verify. No submission sent.');
 const response=await fetch('https://api.indexnow.org/indexnow',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(body)});
 console.log('IndexNow response:',response.status);if(!response.ok)throw new Error(await response.text());
 console.log('Accepted for processing. This does not guarantee indexing or submit the site to every search engine.');
}
