from pathlib import Path
import sys,json,html,shutil,re,os
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.enums import TA_LEFT,TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,KeepTogether,Image,CondPageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing,Rect,String,Line,Ellipse,Circle,Polygon
from reportlab.graphics import renderPDF,renderSVG
from reportlab.platypus.tableofcontents import TableOfContents
from report_content import TITLE,sections,refs,requirements,nfr,tests

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs'; REPO=ROOT
FONT=Path(os.environ.get('DIPLOMA_FONT_DIR','/usr/share/fonts/truetype/dejavu'))
if not (FONT/'DejaVuSerif.ttf').exists():
    raise SystemExit('Set DIPLOMA_FONT_DIR to a directory containing the DejaVu Serif and Sans regular/bold TTF fonts.')
for name,file in [('Body','DejaVuSerif.ttf'),('BodyBold','DejaVuSerif-Bold.ttf'),('Sans','DejaVuSans.ttf'),('SansBold','DejaVuSans-Bold.ttf')]:pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='Body',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
INK=colors.HexColor('#172332'); MUTED=colors.HexColor('#536271'); BLUE=colors.HexColor('#275C69'); LIGHT=colors.HexColor('#EDF3F4'); BORDER=colors.HexColor('#CFD7DC')

def text(d,x,y,t,size=11,font='Sans',color=INK,anchor='middle'):
    for i,line in enumerate(t.split('\n')):d.add(String(x,y-i*size*1.4,line,fontName=font,fontSize=size,fillColor=color,textAnchor=anchor))
def box(d,x,y,w,h,t,fill=LIGHT,size=11):
    d.add(Rect(x,y,w,h,rx=5,ry=5,fillColor=fill,strokeColor=BORDER));text(d,x+w/2,y+h/2+size*len(t.split('\n'))*.48,t,size,color=colors.white if fill==BLUE else INK)
def arrow(d,x1,y1,x2,y2,label=None,dashed=False):
    import math
    line=Line(x1,y1,x2,y2,strokeColor=MUTED,strokeWidth=1.2)
    if dashed:line.strokeDashArray=[4,3]
    d.add(line);a=math.atan2(y2-y1,x2-x1);q=7
    d.add(Polygon([x2,y2,x2-q*__import__('math').cos(a-.45),y2-q*__import__('math').sin(a-.45),x2-q*__import__('math').cos(a+.45),y2-q*__import__('math').sin(a+.45)],fillColor=MUTED,strokeColor=MUTED))
    if label:text(d,(x1+x2)/2,(y1+y2)/2+8,label,8)
def actor(d,x,y,label):
    d.add(Circle(x,y+22,9,fillColor=colors.white,strokeColor=INK));d.add(Line(x,y+13,x,y-18,strokeColor=INK));d.add(Line(x-16,y+3,x+16,y+3,strokeColor=INK));d.add(Line(x,y-18,x-14,y-35,strokeColor=INK));d.add(Line(x,y-18,x+14,y-35,strokeColor=INK));text(d,x,y-54,label,10)
def make_diagrams():
    figs={}
    d=Drawing(650,330)
    box(d,225,90,210,140,'Educator learning\nweb application\n\nAssessment, modules,\npractice and progress',size=12)
    box(d,5,125,140,70,'School educator')
    box(d,505,125,140,70,'Administrator /\ncontent reviewer')
    arrow(d,145,177,225,177,'answers / work');arrow(d,225,142,145,142,'feedback')
    arrow(d,505,177,435,177,'content / review');arrow(d,435,142,505,142,'submissions')
    text(d,325,35,'Browser access over HTTPS; no pupil accounts or mandatory external platform.',10)
    figs['context']=d
    d=Drawing(650,530);d.add(Rect(145,10,360,500,fillColor=colors.white,strokeColor=BORDER));text(d,325,485,'Educator learning application',12,'SansBold')
    actor(d,55,330,'Teacher');actor(d,590,150,'Administrator')
    cases=[('UC1 Sign in / sign out',450),('UC2 Complete assessment',400),('UC3 View recommendation',350),('UC4 Study and submit practice',300),('UC5 View progress and feedback',250),('UC6 Manage own data',200),('UC7 Publish module version',150),('UC8 Review submission',100),('UC9 Export consented pilot data',50)]
    for label,y in cases:
        d.add(Ellipse(325,y,155,19,fillColor=LIGHT,strokeColor=BORDER));text(d,325,y-3,label,10)
    for i in range(6):d.add(Line(75,315,170,cases[i][1],strokeColor=MUTED,strokeWidth=.7))
    for i in [0,6,7,8]:d.add(Line(570,140,480,cases[i][1],strokeColor=MUTED,strokeWidth=.7))
    figs['use_cases']=d
    d=Drawing(650,490)
    box(d,130,410,390,60,'Web interface\nTeacher screens and administrator screens')
    d.add(Rect(15,100,620,270,fillColor=colors.white,strokeColor=BORDER));text(d,325,350,'Next.js server boundary',12,'SansBold')
    box(d,150,285,350,45,'HTTPS API and session / policy checks')
    arrow(d,325,410,325,330,'validated requests / responses')
    sv=[(35,'Assessment\nservice'),(190,'Recommendation\nservice'),(345,'Learning and\nreview service'),(500,'Progress and\nexport service')]
    d.add(Line(92,268,557,268,strokeColor=MUTED,strokeWidth=1.2));arrow(d,325,285,325,268)
    for x,label in sv:
        box(d,x,185,115,65,label,size=10);arrow(d,x+57,268,x+57,250);arrow(d,x+57,185,x+57,153)
    box(d,35,110,580,43,'Persistence layer: parameterized queries, transactions and migrations')
    box(d,180,10,290,60,'PostgreSQL\nAccounts, content versions and learning records',size=11);arrow(d,325,110,325,70)
    figs['components']=d
    # Reviewable low-fidelity UX figures, deliberately not tracker screenshots.
    d=Drawing(650,420);d.add(Rect(0,0,650,420,fillColor=colors.HexColor('#F6F8F9'),strokeColor=BORDER));d.add(Rect(0,365,650,55,fillColor=INK,strokeColor=INK));text(d,25,387,'Teacher Learning',16,'SansBold',colors.white,'start');text(d,625,387,'DEMO',10,'Sans',colors.white,'end')
    text(d,28,329,'Your next step',20,'SansBold',anchor='start');text(d,28,302,'Start with a short assessment or browse all three modules.',11,anchor='start')
    box(d,25,196,600,77,'Initial assessment\nYour confidence and scenario answers are shown separately.',size=12)
    box(d,25,151,165,31,'Start assessment',BLUE,10)
    for i,(name,status) in enumerate([('Digital resources','Not started'),('Online assessment','Not started'),('Responsible sharing','Not started')]):
        box(d,25+i*205,31,190,100,name+'\n\n'+status,size=10)
    figs['ux_dashboard']=d
    d=Drawing(650,440);d.add(Rect(0,0,650,440,fillColor=colors.HexColor('#F6F8F9'),strokeColor=BORDER));text(d,28,405,'M1  Create a useful learning resource',19,'SansBold',anchor='start');text(d,28,374,'State the lesson objective, describe the resource and explain your choices.',10,anchor='start')
    text(d,28,340,'Your response',11,'SansBold',anchor='start');d.add(Rect(25,167,600,155,fillColor=colors.white,strokeColor=BORDER));text(d,42,296,'Lesson objective...',11,color=MUTED,anchor='start')
    text(d,28,141,'Resource link (optional)',11,'SansBold',anchor='start');box(d,25,96,600,32,'https://...',colors.white,10)
    box(d,25,37,145,36,'Save draft',colors.white,10);box(d,190,37,180,36,'Submit for review',LIGHT,10);text(d,625,47,'Not submitted',10,color=MUTED,anchor='end')
    figs['ux_practice']=d
    for name,d in figs.items():
        renderSVG.drawToFile(d,str(REPO/'diagrams'/f'{name}.svg'))
        renderPDF.drawToFile(d,str(REPO/'diagrams'/f'{name}.pdf'))
    return figs

styles=getSampleStyleSheet()
styles.add(ParagraphStyle(name='B',fontName='Body',fontSize=10.3,leading=15,spaceAfter=8,textColor=INK))
styles.add(ParagraphStyle(name='Ref',parent=styles['B'],leading=14,spaceAfter=6))
styles.add(ParagraphStyle(name='H1x',fontName='SansBold',fontSize=18,leading=23,spaceAfter=14,textColor=INK,keepWithNext=True))
styles.add(ParagraphStyle(name='TitleNoTOC',parent=styles['H1x']))
styles.add(ParagraphStyle(name='H2x',fontName='SansBold',fontSize=12,leading=17,spaceBefore=13,spaceAfter=7,textColor=INK,keepWithNext=True))
styles.add(ParagraphStyle(name='Cell',fontName='Sans',fontSize=8.7,leading=12.1,textColor=INK))
styles.add(ParagraphStyle(name='CompactCell',parent=styles['Cell'],fontSize=8.3,leading=10.5))
styles.add(ParagraphStyle(name='HeadCell',fontName='SansBold',fontSize=8.2,leading=11.5,textColor=colors.white))
styles.add(ParagraphStyle(name='Cap',fontName='Sans',fontSize=8.5,leading=12,spaceAfter=12,textColor=MUTED))
styles.add(ParagraphStyle(name='Cover',fontName='BodyBold',fontSize=24,leading=32,spaceAfter=24,textColor=INK))
styles.add(ParagraphStyle(name='Toc1',fontName='Sans',fontSize=10.5,leading=18,leftIndent=0,firstLineIndent=0,spaceBefore=4))
def esc(t):return html.escape(t).replace('\n','<br/>')
def footer(c,doc):
    c.saveState();w,h=A4;c.setFont('Sans',8);c.setFillColor(MUTED)
    if doc.page>1:c.drawString(48,28,'Ayan Abilbek | First submission review draft | 23 October 2026')
    c.drawRightString(w-48,28,str(doc.page));c.restoreState()
class Doc(SimpleDocTemplate):
    def afterFlowable(self,flow):
        if isinstance(flow,Paragraph) and flow.style.name=='H1x':
            t=flow.getPlainText();key='s'+str(self.seq.nextf('heading'));self.canv.bookmarkPage(key);self.canv.addOutlineEntry(t,key,level=0);self.notify('TOCEntry',(0,t,self.page,key))

CSS='''body{max-width:980px;margin:40px auto;padding:0 30px;color:#182532;font:17px/1.65 Georgia,serif}h1,h2,h3{font-family:Arial,sans-serif;line-height:1.25}h1{font-size:32px}h2{font-size:27px;border-top:1px solid #ccd5dc;padding-top:25px;margin-top:45px}h3{font-size:20px}table{width:100%;border-collapse:collapse;font:14px/1.5 Arial,sans-serif;margin:20px 0}th{background:#275c69;color:white;text-align:left}th,td{padding:10px;vertical-align:top;border:1px solid #d4dce1}tr:nth-child(even){background:#f3f6f7}img{width:100%;max-height:700px;object-fit:contain}figcaption{font:14px/1.5 Arial,sans-serif;color:#526270}a{color:#245f74;overflow-wrap:anywhere}.notice{padding:18px;background:#fff2d9;border-left:4px solid #b0822d}nav{font-family:Arial,sans-serif}section{break-before:page}@media print{body{max-width:none;margin:0;font-size:11pt}nav{display:none}h2{border:0}thead{display:table-header-group}tr,figure{break-inside:avoid}}'''
def main():
    figs=make_diagrams();story=[]
    story.extend([Spacer(1,50),Paragraph('ASTANA IT UNIVERSITY',styles['H2x']),Paragraph('School of Software Engineering',styles['B']),Spacer(1,35),Paragraph(TITLE,styles['Cover']),Paragraph('First submission report',styles['TitleNoTOC']),Paragraph('Ayan Abilbek | SE-2401<br/>Supervisor: Aliya Katyetova<br/>Individual diploma project',styles['B']),Spacer(1,25),Paragraph('23 October 2026<br/>Submission deadline: 24 October 2026, 18:00 Astana time',styles['B']),Spacer(1,25),Paragraph('Review draft. Primary user evidence, substantive supervisor feedback and remote submission checks are still outstanding. Proposed design and evaluation plans are not reported as implemented or measured results.',styles['B']),PageBreak()])
    story.append(Paragraph('Contents',styles['TitleNoTOC']));toc=TableOfContents();toc.levelStyles=[styles['Toc1']];story+=[toc,PageBreak()]
    htmlparts=[f'<!doctype html><html lang="en"><meta charset="utf-8"><title>{esc(TITLE)}</title><style>{CSS}</style><h1>{esc(TITLE)}</h1><p>First submission report · Ayan Abilbek · SE-2401<br>Supervisor: Aliya Katyetova · 23 October 2026</p><p class="notice">Review draft. Interviews and supervisor feedback are missing. No submission is claimed.</p>']
    htmlparts.append('<nav>'+''.join(f'<p><a href="#s{i}">{esc(s["title"])}</a></p>' for i,s in enumerate(sections))+'</nav>')
    for i,s in enumerate(sections):
        if i:story.extend([Spacer(1,18),CondPageBreak(190)])
        story.append(Paragraph(esc(s['title']),styles['H1x']));hs=[f'<section id="s{i}"><h2>{esc(s["title"])}</h2>']
        for b in s['blocks']:
            if b['type'] in ['p','h']:
                story.append(Paragraph(esc(b['text']),styles['B' if b['type']=='p' else 'H2x']));tag='p' if b['type']=='p' else 'h3';hs.append(f'<{tag}>{esc(b["text"])}</{tag}>')
            elif b['type']=='table':
                rows=[[Paragraph(esc(t),styles['HeadCell']) for t in b['heads']]]+[[Paragraph(esc(str(t)),styles['CompactCell' if i==0 else 'Cell']) for t in row] for row in b['rows']]
                ratios=b.get('widths') or [1/len(b['heads'])]*len(b['heads']);width=A4[0]-96
                tbl=Table(rows,colWidths=[x*width for x in ratios],repeatRows=1,hAlign='LEFT')
                tbl.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),BLUE),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),5 if i==0 else 7),('BOTTOMPADDING',(0,0),(-1,-1),5 if i==0 else 7),('LINEBELOW',(0,0),(-1,-1),.4,BORDER),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F4F6F7')])]))
                story.extend([tbl,Spacer(1,12)]);hs.append('<table><thead><tr>'+''.join('<th>'+esc(x)+'</th>' for x in b['heads'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(str(x))+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table>')
            elif b['type']=='figure':
                d=figs[b['name']];scale=(A4[0]-96)/d.width;d=d.copy();d.scale(scale,scale);d.width*=scale;d.height*=scale
                story.append(KeepTogether([d,Spacer(1,6),Paragraph(esc(b['caption']),styles['Cap'])]));hs.append(f'<figure><img src="../diagrams/{b["name"]}.svg" alt="{esc(b["caption"])}"><figcaption>{esc(b["caption"])}</figcaption></figure>')
            else:
                st=f'<b>[{b["id"]}]</b> {esc(b["text"])}<br/><link href="{esc(b["url"])}" color="#275C69">{esc(b["url"])}</link>'
                story.append(Paragraph(st,styles['Ref']));hs.append(f'<p id="{b["id"]}"><strong>[{b["id"]}]</strong> {esc(b["text"])}<br><a href="{esc(b["url"])}">{esc(b["url"])}</a></p>')
        hs.append('</section>');htmlparts+=hs
        slug=re.sub(r'[^a-z0-9]+','-',s['title'].lower()).strip('-')
        (REPO/'docs'/f'{i:02d}-{slug}.html').write_text('<!doctype html><meta charset="utf-8"><style>'+CSS+'</style>'+''.join(hs))
    htmlparts.append('</html>');(REPO/'docs'/'report.html').write_text(''.join(htmlparts))
    doc=Doc(str(OUT/'First_Submission_Report.pdf'),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=47,title=TITLE,author='Ayan Abilbek')
    doc.multiBuild(story,onFirstPage=footer,onLaterPages=footer)
    (REPO/'docs'/'report-source.json').write_text(json.dumps({'title':TITLE,'sections':sections,'references':refs},ensure_ascii=False,indent=2))
    print('Report built:',OUT/'First_Submission_Report.pdf')
if __name__=='__main__':main()
