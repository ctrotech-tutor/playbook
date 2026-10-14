"""Build bundled typographic social/identity assets using licensed local fonts."""
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.colors import HexColor
import pymupdf,json
R=Path(__file__).resolve().parents[1];A=R/'assets';C=R/'.cache';C.mkdir(exist_ok=True)
m=json.loads((R/'content/publication.json').read_text())
for name,file in [('BrandDisplay',R/'assets/fonts/InstrumentSerif-Regular.ttf'),('BrandBold',R/'fonts/pdf/DejaVuSans-Bold.ttf'),('BrandBody',R/'fonts/pdf/DejaVuSans.ttf')]:pdfmetrics.registerFont(TTFont(name,str(file)))
p=C/'social-source.pdf';c=canvas.Canvas(str(p),pagesize=(1200,630));c.setFillColor(HexColor('#faf8f1'));c.rect(0,0,1200,630,fill=1,stroke=0)
c.setFillColor(HexColor('#234d42'));c.rect(860,0,340,630,fill=1,stroke=0);c.setFont('BrandBold',14);c.drawString(64,565,'CTROTECH / FIELD GUIDE 001')
c.setFont('BrandDisplay',110);c.drawString(60,397,'The HTML');c.drawString(60,281,'Playbook.')
c.setFont('BrandBody',25);c.drawString(65,207,'Write pages you can explain.');c.setFont('BrandBold',18);c.drawString(65,100,m['author']);c.setFont('BrandBody',13);c.drawString(65,65,'Chapters. Source-linked references. Code to inspect.')
c.setFillColor(HexColor('#faf8f1'));c.setFont('BrandDisplay',108);c.drawCentredString(1030,315,'HTML');c.setFont('BrandBody',12);c.drawCentredString(1030,270,'LEARN / LOOK UP / BUILD');c.save()
with pymupdf.open(p) as d:(A/'og-cover.jpg').write_bytes(d[0].get_pixmap(alpha=False).tobytes('jpg',jpg_quality=92))
for size in [32,180,192,512]:
 p=C/f'identity-{size}.pdf';c=canvas.Canvas(str(p),pagesize=(size,size));c.setFillColor(HexColor('#234d42'));c.rect(0,0,size,size,fill=1,stroke=0);c.setFillColor(HexColor('#faf8f1'));c.setFont('BrandBold',size*.46);c.drawCentredString(size/2,size*.33,'CT');c.save()
 name={32:'favicon-32.png',180:'apple-touch-icon.png',192:'icon-192.png',512:'icon-512.png'}[size]
 with pymupdf.open(p) as d:d[0].get_pixmap(alpha=False).save(A/name)
print('Created social cover and four identity icons.')
