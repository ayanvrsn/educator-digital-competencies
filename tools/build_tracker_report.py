"""Build the tracker evidence PDF from the same image selection as the main report."""
from pathlib import Path
import os,json,argparse
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A3,landscape
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from xml.sax.saxutils import escape

R=Path(__file__).resolve().parents[1]
S=R/'project-management/screenshots'
FONT=Path(os.environ.get('DIPLOMA_TIMES_FONT_DIR','/System/Library/Fonts/Supplemental'))
pdfmetrics.registerFont(TTFont('TNR',str(FONT/'Times New Roman.ttf')))
pdfmetrics.registerFont(TTFont('TNRB',str(FONT/'Times New Roman Bold.ttf')))
style=ParagraphStyle('note',fontName='TNR',fontSize=12,leading=16)
head=ParagraphStyle('title',fontName='TNRB',fontSize=16,leading=21)

def build(path):
 items=json.loads((S/'selected-evidence.json').read_text())
 c=canvas.Canvas(str(path),pagesize=landscape(A3))
 c.setTitle('YouTrack task evidence - Ayan Abilbek');c.setAuthor('Ayan Abilbek')
 for i,item in enumerate(items,1):
  W,H=A3 if item['template']=='shottall' else landscape(A3)
  c.setPageSize((W,H));L,Rt,T,B=30*mm,15*mm,20*mm,20*mm;available=W-L-Rt
  p=Paragraph(escape(item['title']),head);_,h=p.wrap(available,100);p.drawOn(c,L,H-T-h)
  c.setFont('TNR',12);c.drawString(L,H-T-h-19,item['source'])
  c.setFont('TNR',10);c.drawString(L,H-T-h-35,item['url']);c.linkURL(item['url'],(L,H-T-h-39,W-Rt,H-T-h-24),relative=0)
  note=Paragraph(escape(item['note']),style);_,nh=note.wrap(available,70);note.drawOn(c,L,B+21)
  top=H-T-h-49;bottom=B+nh+35;iw,ih=Image.open(S/item['file']).size;scale=min(available/iw,(top-bottom)/ih)
  c.drawImage(str(S/item['file']),L+(available-iw*scale)/2,bottom+(top-bottom-ih*scale)/2,width=iw*scale,height=ih*scale)
  c.setFont('TNR',11);c.drawString(L,B,'First-submission tracker evidence. Ayan Abilbek. 23 October 2026.')
  c.setFont('TNR',12);c.drawCentredString(W/2,10*mm,str(i));c.showPage()
 c.save();print(f'Tracker evidence: {len(items)} pages.')

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=R/'docs/YouTrack_Task_Screenshots.pdf');args=parser.parse_args();build(args.output)
