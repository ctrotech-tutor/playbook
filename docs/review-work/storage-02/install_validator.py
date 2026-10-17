"""Restore a signature-verified local validator using the official unattended installer."""
from pathlib import Path
import urllib.request,hashlib,subprocess,zipfile,json,sys
R=Path.cwd();P=R/'.cache/validator-install';P.mkdir(parents=True,exist_ok=True);out=R/'.cache/verapdf';gpg=P/'gnupg';gpg.mkdir(exist_ok=True);gpg.chmod(0o700)
rows=[]
for name,url in [('verapdf-installer.zip','https://software.verapdf.org/releases/verapdf-installer.zip'),('verapdf-installer.zip.asc','https://software.verapdf.org/releases/verapdf-installer.zip.asc'),('KEY','https://software.verapdf.org/keys/KEY')]:
 data=urllib.request.urlopen(url,timeout=60).read();(P/name).write_bytes(data);rows.append({'url':url,'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()})
subprocess.run(['gpg','--homedir',str(gpg),'--import',str(P/'KEY')],check=True,capture_output=True)
keys=subprocess.check_output(['gpg','--homedir',str(gpg),'--with-colons','--fingerprint'],text=True)
assert '13DD102B4DD69354D12DE5A83184863278B17FE7' in keys
run=subprocess.run(['gpg','--homedir',str(gpg),'--status-fd','1','--verify',str(P/'verapdf-installer.zip.asc'),str(P/'verapdf-installer.zip')],capture_output=True,text=True,check=True)
assert 'VALIDSIG 13DD102B4DD69354D12DE5A83184863278B17FE7' in run.stdout
with zipfile.ZipFile(P/'verapdf-installer.zip') as z:
 for n in z.namelist():assert (P/n).resolve().is_relative_to(P)
 z.extractall(P)
jar=next(P.rglob('verapdf-izpack-installer-*.jar'))
xml='<AutomatedInstallation langpack="eng"><com.izforge.izpack.panels.htmlhello.HTMLHelloPanel id="welcome"/><com.izforge.izpack.panels.target.TargetPanel id="install_dir"><installpath>'+str(out)+'</installpath></com.izforge.izpack.panels.target.TargetPanel><com.izforge.izpack.panels.packs.PacksPanel id="sdk_pack_select"><pack index="0" name="veraPDF GUI" selected="false"/><pack index="1" name="veraPDF CLI" selected="true"/><pack index="2" name="veraPDF Documentation" selected="false"/><pack index="3" name="veraPDF Sample Plugins" selected="false"/></com.izforge.izpack.panels.packs.PacksPanel><com.izforge.izpack.panels.install.InstallPanel id="install"/><com.izforge.izpack.panels.finish.FinishPanel id="finish"/></AutomatedInstallation>'
(P/'auto.xml').write_text(xml);subprocess.run(['java','-jar',str(jar),str(P/'auto.xml')],check=True)
version=subprocess.check_output([str(out/'verapdf'),'--version'],text=True);print(version)
(R/'docs/review-work/storage-02/validator-installation.json').write_text(json.dumps({'date':'2026-10-17','official_instructions':'https://docs.verapdf.org/install/','key_fingerprint':'13DD102B4DD69354D12DE5A83184863278B17FE7','signature_verified':True,'version':version.strip(),'downloads':rows},indent=2)+'\n')
