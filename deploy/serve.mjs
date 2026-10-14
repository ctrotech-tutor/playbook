// Local static route/header preview. Vercel serves the production output itself.
import http from 'node:http';
import https from 'node:https';
import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const directory=path.join(root,'dist');
const config=JSON.parse(await fs.readFile(path.join(root,'vercel.json'),'utf8'));
const port=Number(process.env.PORT||3000);
const host=process.env.HOST||'0.0.0.0';
const mime={'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.json':'application/json; charset=utf-8','.webmanifest':'application/manifest+json','.xml':'application/xml; charset=utf-8','.txt':'text/plain; charset=utf-8','.md':'text/markdown; charset=utf-8','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.ico':'image/x-icon','.ttf':'font/ttf','.pdf':'application/pdf','.zip':'application/zip'};
const clean=p=>p==='/index.html'?'/':p.endsWith('/index.html')?p.slice(0,-11):p.replace(/\.html$/,'');
async function exists(p){try{return (await fs.stat(p)).isFile();}catch{return false;}}
function applies(source,p){if(source==='/(.*)')return true;const star=source.indexOf('/:path*');if(star>=0)return p.startsWith(source.slice(0,star)+'/');return source===p;}
const handler=async(req,res)=>{
 try{
  const u=new URL(req.url,'http://local.invalid');const pathname=decodeURIComponent(u.pathname);
  if(!['GET','HEAD'].includes(req.method)){res.writeHead(405,{'Allow':'GET, HEAD'});return res.end();}
  for(const rule of config.headers||[])if(applies(rule.source,pathname))for(const h of rule.headers)res.setHeader(h.key,h.value);
  if(process.env.ALLOW_PREVIEW_EMBED==='1'){res.removeHeader('X-Frame-Options');res.setHeader('Content-Security-Policy',String(res.getHeader('Content-Security-Policy')||'').replace("; frame-ancestors 'none'",''));}
  const redirect=config.redirects.find(r=>r.source===pathname);
  if(redirect){res.writeHead(308,{'Location':redirect.destination+u.search});return res.end();}
  if(pathname.endsWith('.html')){res.writeHead(308,{'Location':clean(pathname)+u.search});return res.end();}
  if(pathname!=='/'&&pathname.endsWith('/')){res.writeHead(308,{'Location':pathname.slice(0,-1)+u.search});return res.end();}
  const candidate=path.resolve(directory,'.'+pathname);
  if(!candidate.startsWith(directory+path.sep)&&candidate!==directory){res.writeHead(403);return res.end();}
  let file=candidate,status=200;
  if(!await exists(file)){
   if(await exists(candidate+'.html'))file=candidate+'.html';
   else if(await exists(path.join(candidate,'index.html')))file=path.join(candidate,'index.html');
   else{file=path.join(directory,'404.html');status=404;}
  }
  if(pathname==='/404')status=404;
  const data=await fs.readFile(file);res.statusCode=status;res.setHeader('Content-Type',mime[path.extname(file)]||'application/octet-stream');res.setHeader('Content-Length',data.length);
  if(req.method==='HEAD')return res.end();res.end(data);
 }catch(error){res.writeHead(500,{'Content-Type':'text/plain; charset=utf-8'});res.end('Local preview failed. Build the site first.');console.error(error.message);}
};
const server=process.env.LOCAL_TLS_CERT&&process.env.LOCAL_TLS_KEY?https.createServer({cert:await fs.readFile(process.env.LOCAL_TLS_CERT),key:await fs.readFile(process.env.LOCAL_TLS_KEY)},handler):http.createServer(handler);
server.listen(port,host,()=>console.log('CTROTECH website listening on '+host+':'+server.address().port+(process.env.ALLOW_PREVIEW_EMBED==='1'?' (preview embedding exception enabled)':'')));
