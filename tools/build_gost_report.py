from pathlib import Path
import os,sys,re,json,html,copy,argparse
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_LEFT,TA_JUSTIFY
from reportlab.lib.pagesizes import A4,A3,landscape
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate,PageTemplate,Frame,Paragraph,Spacer,PageBreak,NextPageTemplate,Table,TableStyle,KeepTogether,Image
from reportlab.platypus.tableofcontents import TableOfContents
import build_report as original_designs
FIGURES=original_designs.make_diagrams()
from pypdf import PdfReader
from report_content import TITLE,sections as original_sections,refs

HERE=Path(__file__).resolve().parent
REPO=HERE.parent if HERE.name=='tools' else HERE.parent/'outputs/diploma-first-submission/repository'
FONT=Path(os.environ.get('DIPLOMA_TIMES_FONT_DIR','/System/Library/Fonts/Supplemental'))
for name,file in [('TNR','Times New Roman.ttf'),('TNRB','Times New Roman Bold.ttf'),('TNRI','Times New Roman Italic.ttf')]:
 if not (FONT/file).exists():raise FileNotFoundError('Set DIPLOMA_TIMES_FONT_DIR to the directory containing licensed Times New Roman TTF files.')
 pdfmetrics.registerFont(TTFont(name,str(FONT/file)))
pdfmetrics.registerFontFamily('TNR',normal='TNR',bold='TNRB',italic='TNRI',boldItalic='TNRB')
L,R,T,B=30*mm,15*mm,20*mm,20*mm
W=A4[0]-L-R
S={
 'body':ParagraphStyle('body',fontName='TNR',fontSize=14,leading=21,alignment=TA_JUSTIFY,firstLineIndent=12.5*mm,spaceAfter=0,allowWidows=0,allowOrphans=0),
 'section':ParagraphStyle('section',fontName='TNRB',fontSize=14,leading=21,firstLineIndent=12.5*mm,spaceAfter=21,keepWithNext=True),
 'sub':ParagraphStyle('sub',fontName='TNRB',fontSize=14,leading=21,firstLineIndent=12.5*mm,spaceBefore=14,spaceAfter=14,keepWithNext=True),
 'structure':ParagraphStyle('structure',fontName='TNRB',fontSize=14,leading=21,alignment=TA_CENTER,spaceAfter=21,keepWithNext=True),
 'center':ParagraphStyle('center',fontName='TNR',fontSize=14,leading=21,alignment=TA_CENTER),
 'cell':ParagraphStyle('cell',fontName='TNR',fontSize=12,leading=14.4,alignment=TA_LEFT),
 'head':ParagraphStyle('head',fontName='TNR',fontSize=12,leading=14.4,alignment=TA_CENTER),
 'caption':ParagraphStyle('caption',fontName='TNR',fontSize=12,leading=18,spaceAfter=8),
 'figcap':ParagraphStyle('figcap',fontName='TNR',fontSize=12,leading=18,alignment=TA_CENTER,spaceBefore=8,spaceAfter=8),
 'ref':ParagraphStyle('ref',fontName='TNR',fontSize=14,leading=21,firstLineIndent=12.5*mm,alignment=TA_LEFT,spaceAfter=7,splitLongWords=True,allowWidows=0),
 'toc0':ParagraphStyle('toc0',fontName='TNR',fontSize=12,leading=18,spaceBefore=1),
 'toc1':ParagraphStyle('toc1',fontName='TNR',fontSize=12,leading=16,leftIndent=10*mm,spaceBefore=0),
}
S['figurelead']=ParagraphStyle('figurelead',parent=S['body'],keepWithNext=True)
def esc(s):return html.escape(str(s)).replace('\n','<br/>')
def clean(s):return str(s).replace('\u2011','-').replace('\u2013','-').replace('\u2014','-').replace('\u2212','-')

# Bibliography metadata comes from the verified sources in the existing report.
bibliography={
'R1':'Redecker C. European Framework for the Digital Competence of Educators: DigCompEdu / ed. Y. Punie. - Luxembourg: Publications Office of the European Union, 2017. - DOI: 10.2760/159770.',
'R2':'UNESCO ICT Competency Framework for Teachers. Version 3 / UNESCO. - Paris: UNESCO, 2018. - ISBN 978-92-3-100285-4.',
'R3':'Falloon G. From digital literacy to digital competence: the teacher digital competency (TDC) framework // Educational Technology Research and Development. - 2020. - Vol. 68. - P. 2449-2472.',
'R4':'The relation between in-service teachers’ digital competence and personal and contextual factors: What matters most? / M. Lucas, P. Bem-Haja, F. Siddiq et al. // Computers & Education. - 2021. - Vol. 160. - Art. 104052.',
'R5':'Design and Validation of t-MOOC for the Development of the Digital Competence of Non-University Teachers / J. Cabero-Almenara, R. Barragán-Sánchez, A. Palacios-Rodríguez, L. Martín-Párraga // Technologies. - 2021. - Vol. 9, no. 4. - Art. 84.',
'R6':'Teachers’ digital competencies in higher education: a systematic literature review / V. Basilotta-Gómez-Pablos, M. Matarranz, L.-A. Casado-Aranda, A. Otto // International Journal of Educational Technology in Higher Education. - 2022. - Vol. 19. - Art. 8.',
'R7':'Heine S., Krepf M., König J. Digital resources as an aspect of teacher professional digital competence: One term, different definitions - a systematic review // Education and Information Technologies. - 2023. - Vol. 28. - P. 3711-3738. - First published online in 2022.',
'R8':'Systematic review of quantitative research on digital competences of in-service school teachers / M. Claro, C. Castro-Grau, J. M. Ochoa et al. // Computers & Education. - 2024. - Vol. 215. - Art. 105030.',
'R9':'Tzafilkou K., Perifanou M., Economides A. A. Assessing teachers’ digital competence in primary and secondary education: Applying a new instrument to integrate pedagogical and professional elements for digital education // Education and Information Technologies. - 2023. - Vol. 28. - P. 16017-16040.',
'R10':'Gallego Joya L., Merchán Merchán M. A., López Barrera E. A. Development and strengthening of teachers’ digital competence: Systematic review // Contemporary Educational Technology. - 2025. - Vol. 17, no. 1. - Art. ep555.',
'R11':'Cosgrove J., Cachia R. DigComp 3.0: European Digital Competence Framework. - 5th ed. - Luxembourg: Publications Office of the European Union, 2025. - DOI: 10.2760/0001149.',
'R12':'Web Content Accessibility Guidelines (WCAG) 2.2 [Electronic resource] / W3C. - W3C Recommendation, 12 December 2024.',
}
for rid,citation,url in refs:
 if rid not in bibliography:bibliography[rid]=citation.rstrip('.')+' [Electronic resource].'
urls={rid:url for rid,_,url in refs}
sections=copy.deepcopy(original_sections[:-1])
sections[0]['title']='INTRODUCTION'
# Make the source for the Git workflow explicit rather than leaving an uncited bibliography item.
sections[10]['blocks'].append({'type':'p','text':'The repository setup follows the GitHub documentation [G1]. The current review package is available in draft pull request 1. Appendix A reproduces selected tracker views; Appendix B records the checks actually performed on the local prototype; Appendix C lists the 40 work items and their current planning states.'})
sections[8]['blocks'].append({'type':'p','text':'The browser checks in Appendix B use synthetic examples. They verify the interaction design and do not establish server security, persistent storage or learning effectiveness.'})
# All references use a single numeric sequence in order of first mention.
order=[]
def strings(b):
 if b['type']=='table':return b['heads']+[x for row in b['rows'] for x in row]
 return [b.get('text',b.get('caption',''))]
for section in sections:
 for block in section['blocks']:
  for s in strings(block):
   for token in re.findall(r'\b(?:R\d+|S\d+|T\d+|G\d+)\b',str(s)):
    if token in urls and token not in order:order.append(token)
assert set(order)==set(urls),(set(urls)-set(order))
nums={rid:i+1 for i,rid in enumerate(order)}
def numeric(s):
 s=clean(s)
 # Existing bracketed references keep their brackets; bare table IDs become numeric references.
 def br(m):return '['+re.sub(r'\b(?:R\d+|S\d+|T\d+|G\d+)\b',lambda q:str(nums[q[0]]),m[1])+']'
 bits=re.split(r'(\[[^\]]+\])',s)
 for i,x in enumerate(bits):
  if x.startswith('['):bits[i]=re.sub(r'\[([^\]]+)\]',br,x)
  else:bits[i]=re.sub(r'\b(?:R\d+|S\d+|T\d+|G\d+)\b',lambda q:'['+str(nums[q[0]])+']' if q[0] in nums else q[0],x)
 return ''.join(bits)
def P(s,style='body'):return Paragraph(esc(numeric(s)),S[style])

table_names=[
'Coverage of the eleven required components','Project objectives and deliverables','Learning modules and competence mapping','Evidence and unresolved assumptions','Protocol for discussions with educators','Assumptions and validation actions','Critical analysis of the core literature','Comparison of existing systems','Server platform alternatives','Data storage alternatives','Component interaction alternatives','Functional requirements and acceptance criteria','Non-functional requirements and acceptance criteria','Component responsibilities and requirement traceability','Initial data model','Key user screens and states','Verification scenarios','Evaluation measures and interpretation','Practical task scoring rubric','Milestones and exit conditions','Project risks and responses','Supervisor review agenda']
table_intro=[
'Table {n} maps the required components to the available material and the remaining evidence.',
'The objectives, deliverables and completion evidence are set out in Table {n}.',
'Table {n} connects each proposed module to a classroom task and a competence reference.',
'Table {n} distinguishes the available context from questions that still require user evidence.',
'The discussion protocol is organised in Table {n}.',
'Table {n} records the main assumptions and the actions needed to check them.',
'The contribution and limits of each core source are compared in Table {n}.',
'Table {n} applies the same eight criteria to three existing systems.',
'The server platform alternatives are compared in Table {n}.',
'Table {n} compares the storage alternatives against the proposed data model.',
'The interaction options and their costs are compared in Table {n}.',
'Table {n} specifies the required functions, priorities and observable acceptance criteria.',
'The quality requirements and their acceptance criteria are listed in Table {n}.',
'Table {n} assigns responsibilities and requirements to the proposed components.',
'The initial entities and their invariants are summarised in Table {n}.',
'Table {n} identifies the main screens and the states each screen must communicate.',
'The planned verification scenarios and expected results are specified in Table {n}.',
'Table {n} distinguishes usability measures from learning-related observations.',
'The proposed four-criterion rubric is shown in Table {n}.',
'Table {n} separates dated first-submission targets from later milestones without an agreed calendar.',
'The principal risks, consequences and responses are recorded in Table {n}.',
'Table {n} is an agenda for obtaining feedback; it does not represent feedback already received.'
]

class NumberedTable(Table):
 def split(self,availWidth,availHeight):
  result=super().split(availWidth,availHeight)
  if len(result)>1 and getattr(self,'caption_no',None):
   for part in result:
    part.caption_no=self.caption_no
   result[1]._cellvalues=[list(row) for row in result[1]._cellvalues]
   result[1]._cellvalues[0][0]=P('Continuation of Table '+self.caption_no,'caption')
  return result

def make_table(heads,rows,widths,no,title,width=W,small=False):
 data=[[P('Table '+str(no)+' - '+title,'caption')]+['']*(len(heads)-1),[P(x,'head') for x in heads]]
 data += [[P(x,'cell') for x in row] for row in rows]
 ratios=widths or [1/len(heads)]*len(heads)
 if len(heads)==4 and ratios[0]<.10:ratios=[.09,.23,.34,.34]
 tbl=NumberedTable(data,colWidths=[width*x for x in ratios],repeatRows=2,hAlign='LEFT')
 tbl.caption_no=str(no)
 tbl.setStyle(TableStyle([('SPAN',(0,0),(-1,0)),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,0),0),('RIGHTPADDING',(0,0),(-1,0),0),('TOPPADDING',(0,0),(-1,0),7),('BOTTOMPADDING',(0,0),(-1,0),3),('LEFTPADDING',(0,1),(-1,-1),5),('RIGHTPADDING',(0,1),(-1,-1),5),('TOPPADDING',(0,1),(-1,-1),5),('BOTTOMPADDING',(0,1),(-1,-1),5),('GRID',(0,1),(-1,-1),.4,colors.black)]))
 return tbl

def footer(c,doc):
 if doc.page>1:
  c.saveState();w,h=c._pagesize;c.setFont('TNR',12);c.setFillColor(colors.black);c.drawCentredString(w/2,10*mm,str(doc.page));c.restoreState()
class Report(BaseDocTemplate):
 def __init__(self,path):
  super().__init__(str(path),pagesize=A4,leftMargin=L,rightMargin=R,topMargin=T,bottomMargin=B,title=TITLE,author='Ayan Abilbek',allowSplitting=1)
  templates=[]
  for name,size in [('main',A4),('shotwide',landscape(A3)),('shottall',A3)]:
   w,h=size;frame=Frame(L,B,w-L-R,h-T-B,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,id=name)
   templates.append(PageTemplate(id=name,frames=frame,pagesize=size,onPage=footer))
  self.addPageTemplates(templates);self.locations={}
 def afterFlowable(self,flow):
  if isinstance(flow,Paragraph) and hasattr(flow,'toc_key'):
   key=flow.toc_key;title=flow.getPlainText();level=flow.toc_level;self.canv.bookmarkPage(key);self.canv.addOutlineEntry(title,key,level=level,closed=False);self.notify('TOCEntry',(level,title,self.page,key));self.locations[key]=self.page

def heading(text,key,level=0,struct=False):
 p=P(text,'structure' if struct else ('sub' if level else 'section'));p.toc_key=key;p.toc_level=level;return p

def vector(name):
 d=copy.deepcopy(FIGURES[name])
 # Preserve the diagram geometry; use a monochrome print palette.
 def recolor(obj):
  if hasattr(obj,'fontName'):
   obj.fontName='TNR'
   if hasattr(obj,'fontSize'):obj.fontSize*=1.15
  if hasattr(obj,'fillColor') and obj.fillColor is not None:
   if hasattr(obj,'text'):obj.fillColor=colors.black
   elif obj.fillColor!=colors.white:obj.fillColor=colors.Color(.95,.95,.95)
  if hasattr(obj,'strokeColor') and obj.strokeColor is not None:obj.strokeColor=colors.black
  for sub in getattr(obj,'contents',[]):recolor(sub)
 recolor(d)
 scale=min(W/d.width,210*mm/d.height);d.scale(scale,scale);d.width*=scale;d.height*=scale
 return d

evidence=json.loads((REPO/'project-management/screenshots/selected-evidence.json').read_text())
shots=[(item['file'],item['title'],item['template']) for item in evidence]

def build(path,page_count=0):
 story=[];htmlparts=[];index=[];table_no=0
 # Title page: this is an interim student report, not an approval or a signed final thesis.
 story += [Spacer(1,8*mm),P('ASTANA IT UNIVERSITY','center'),P('School of Software Engineering','center'),Spacer(1,34*mm),P('FIRST SUBMISSION REPORT','center'),P('(interim diploma project report)','center'),Spacer(1,15*mm),P(TITLE,'center'),Spacer(1,25*mm)]
 details=Table([[P('Student','center'),P('Ayan Abilbek, SE-2401','center')],[P('Supervisor','center'),P('Aliya Katyetova','center')]],colWidths=[W*.28,W*.72]);details.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));story.append(details)
 story.extend([Spacer(1,42*mm),P('Astana 2026','center'),PageBreak()])
 story += [heading('ABSTRACT','abstract',struct=True)]
 story += [P(f'Report: {page_count or "--"} pages, 5 main-text figures, {len(shots)} appendix figures, 22 main-text tables, 1 appendix table, 27 references and 3 appendices.'),Spacer(1,14),P('DIGITAL COMPETENCE, SCHOOL EDUCATORS, WEB APPLICATION, DIAGNOSTIC ASSESSMENT, PRACTICAL TASKS, USABILITY','body'),Spacer(1,14)]
 abstract='This report presents the analysis and design of a web application for school educators. Its purpose is to connect an initial diagnostic activity with three focused learning modules, practical submissions, feedback and progress tracking. The work uses a critical literature review, a comparison of existing systems and a comparison of technical alternatives to define an initial specification. The proposed design contains teacher and administrator roles, versioned learning content, rule-based module recommendations and rubric-based review. A local interactive prototype makes the main learning sequence available for inspection. A testing and evaluation plan defines functional checks, data-protection checks, usability measures, parallel practical tasks and a static resource baseline. The project repository and tracker record the current work and the remaining dependencies. The report contains prepared design material; it does not report an implemented production application or measured learning gains. Discussions with educators, substantive supervisor feedback, recipient-access checks and a final submission receipt remain outstanding. These gaps must be resolved before the package can be treated as a complete first submission.'
 story += [P(abstract),PageBreak(),P('CONTENTS','structure')]
 toc=TableOfContents();toc.levelStyles=[S['toc0'],S['toc1']];toc.dotsMinLevel=0;story += [toc,PageBreak(),heading('ABBREVIATIONS','abbreviations',struct=True)]
 for abbr,meaning in [('API','application programming interface'),('CSV','comma-separated values'),('DigCompEdu','European Framework for the Digital Competence of Educators'),('FR','functional requirement'),('HTTPS','Hypertext Transfer Protocol Secure'),('NFR','non-functional requirement'),('PR','pull request'),('REST','representational state transfer'),('TC','test case'),('UI','user interface'),('UX','user experience'),('WCAG','Web Content Accessibility Guidelines')]:story.append(P(abbr+' - '+meaning))
 for si,section in enumerate(sections):
  story.append(PageBreak());story.append(heading(section['title'],f's{si}',struct=si==0));htmlparts.append('<section><h1>'+esc(section['title'])+'</h1>');sub=0
  for bi,b in enumerate(section['blocks']):
   typ=b['type']
   if typ=='p':story.append(P(b['text']));htmlparts.append('<p>'+esc(numeric(b['text']))+'</p>')
   elif typ=='h':
    sub+=1;title=(str(si)+'.'+str(sub)+' ' if si else '')+b['text'];story.append(heading(title,f's{si}-h{sub}',level=1));htmlparts.append('<h2>'+esc(title)+'</h2>')
   elif typ=='table':
    table_no+=1;title=table_names[table_no-1];story.append(P(table_intro[table_no-1].format(n=table_no)));story.append(make_table(b['heads'],b['rows'],b['widths'],table_no,title));story.append(Spacer(1,10));index.append({'number':table_no,'title':title})
    htmlparts.append(f'<p>Table {table_no} - {esc(title)}</p><table><thead><tr>'+''.join('<th>'+esc(numeric(x))+'</th>' for x in b['heads'])+'</tr></thead><tbody>'+''.join('<tr>'+''.join('<td>'+esc(numeric(x))+'</td>' for x in row)+'</tr>' for row in b['rows'])+'</tbody></table>')
   elif typ=='figure':
    no=int(re.search(r'Figure (\d+)',b['caption'])[1]);cap=re.sub(r'^Figure \d+\.\s*',f'Figure {no} - ',b['caption']);story.append(P('Figure '+str(no)+' shows '+{'context':'the system boundary and its external actors.','use_cases':'the interactions available to each application role.','components':'the proposed server components and persistence boundary.','ux_dashboard':'the proposed teacher dashboard.','ux_practice':'the proposed practical-work submission screen.'}[b['name']],'figurelead'))
    story.append(KeepTogether([Spacer(1,8),vector(b['name']),P(cap,'figcap')]))
    htmlparts.append(f'<figure><img src="../diagrams/{b["name"]}.svg"><figcaption>{esc(numeric(cap))}</figcaption></figure>')
  htmlparts.append('</section>')
 assert table_no==22,table_no
 story += [PageBreak(),heading('CONCLUSION','conclusion',struct=True)]
 for t in ['The first stage has produced a defined project scope, a literature synthesis, comparisons, an initial specification, three architecture diagrams, a reviewable interface prototype and an evaluation plan. The design connects diagnostic questions to three learning modules and practical work, with confidence, quiz results and rubric scores kept separate.', 'These results support the next design review and implementation planning. They do not yet demonstrate that the application improves educators’ digital competence. Local needs remain unverified without the required educator discussions, and the substantive supervisor review is still missing.', 'The next actions are to collect the primary evidence, revise the requirements where necessary, obtain and record supervisor comments, and verify recipient access. Implementation can then proceed through the dependencies recorded in YouTrack. Pilot data must be collected only after the release gates and consent requirements are met. No economic benefit or learning effect is claimed without measurement.']:story.append(P(t))
 story += [PageBreak(),heading('REFERENCES','references',struct=True)]
 scientific=', '.join('['+str(nums['R'+str(i)])+']' for i in range(3,11));story.append(P('The core review contains 12 sources, including eight scientific publications: '+scientific+'. The remaining references support product and engineering decisions. Online source checks were performed on 22 October 2026.'))
 for rid in order:
  u=urls[rid];txt=str(nums[rid])+' '+clean(bibliography[rid])+' - URL: ';mark=esc(txt)+f'<link href="{html.escape(u,quote=True)}" color="black">'+esc(u)+'</link> (accessed: 22.10.2026).';story.append(Paragraph(mark,S['ref']))
 story += [PageBreak(),heading('APPENDIX A','appendix-a',struct=True),P('(informative)','center'),P('Tracker evidence','center'),Spacer(1,21),P('Figures A.1-A.8 reproduce eight YouTrack screenshots from 23 October 2026. Five were supplied by the student and three are earlier browser captures. They show the project overview, separate Diploma and Submission views, three implementation tasks, the proposal review and a widget displaying 40 starred issues. The supplied images are reproduced without alteration. The screenshots are included on A3 sheets to preserve readability. The same evidence is also supplied in the separate tracker PDF required for submission.'),P('The main board contains 30 Diploma tasks: 21 in the backlog and 9 in review. The Submission view contains 10 organisational tasks. Review is a workflow state and does not establish supervisor approval. Nineteen future tasks have no assigned calendar date because the university has not provided the next pre-defence or defence schedule.'),P('Project: https://ayan-educator-diploma.youtrack.cloud/projects/EDU','ref'),P('Repository: https://github.com/ayanvrsn/educator-digital-competencies','ref'),P('Draft review: https://github.com/ayanvrsn/educator-digital-competencies/pull/1','ref')]
 from PIL import Image as PILImage
 for i,(filename,title,template) in enumerate(shots,1):
  story += [NextPageTemplate(template),PageBreak(),P('Appendix A (continued)','center')]
  size=landscape(A3) if template=='shotwide' else A3;maxw=size[0]-L-R;maxh=size[1]-T-B-64
  p=REPO/'project-management/screenshots'/filename;iw,ih=PILImage.open(p).size;scale=min(maxw/iw,maxh/ih)
  story.extend([Spacer(1,8),Image(str(p),width=iw*scale,height=ih*scale),P(f'Figure A.{i} - {title}','figcap')])
 story += [NextPageTemplate('main'),PageBreak(),heading('APPENDIX B','appendix-b',struct=True),P('(informative)','center'),P('Observed prototype checks','center'),Spacer(1,21)]
 txt=(REPO/'prototype/verification.txt').read_text();paragraphs=txt.split('\n\n')
 for t in paragraphs[1:]:
  if t.startswith('Observed:'):
   story.append(P('The following behaviour was observed using synthetic examples:'))
   for line in t.splitlines()[1:]:story.append(P(line))
  else:story.append(P(t))
 story += [PageBreak(),heading('APPENDIX C','appendix-c',struct=True),P('(informative)','center'),P('Project work breakdown','center'),Spacer(1,21),P('Table C.1 lists the 40 actual YouTrack issues. Ayan Abilbek owns all tasks. Diploma covers research, design, implementation and evaluation; Submission covers the first hand-in. The dates are preparation targets, except that future implementation and evaluation dates remain unset. Full outcomes and acceptance criteria are recorded in the live issues and project-management/tasks.csv. Dependencies are issue mentions in descriptions.'),P('Priority abbreviations: C - Critical; H - High; N - Normal. Review means awaiting checks. Blocked is the planning status; these tasks remain in the board backlog.')]
 tasks=json.loads((REPO/'project-management/tasks.json').read_text());rows=[]
 for t in tasks:
  rows.append([t['YouTrack ID'],t['Summary']+'\n'+t['Workstream'],t['Priority'][0]+' / '+t['State'],t['Due Date'] or 'Not scheduled'])
 story.append(make_table(['Issue','Work item / group','Priority / status','Target date'],rows,[.14,.44,.22,.20],'C.1','Project work items'))
 doc=Report(path);doc.multiBuild(story)
 total=len(PdfReader(path).pages)
 css='@page{size:A4;margin:20mm 15mm 20mm 30mm}body{max-width:165mm;margin:20mm auto;font:14pt/1.5 "Times New Roman",serif;color:black}p{text-align:justify;text-indent:12.5mm;margin:0}h1,h2{font-size:14pt}h1{break-before:page}table{border-collapse:collapse;width:100%;font-size:12pt;line-height:1.2;margin:12pt 0}td,th{border:1px solid black;padding:5pt;font-weight:normal;vertical-align:top}img{width:100%}figcaption{font-size:12pt;text-align:center}'
 front='<header><h1>'+esc(TITLE)+'</h1><p>First submission report. Ayan Abilbek, SE-2401. Supervisor: Aliya Katyetova. Astana, 2026.</p></header><section><h1>ABSTRACT</h1><p>'+esc(abstract)+'</p></section>'
 conclusion='<section><h1>CONCLUSION</h1><p>The analysis, design, prototype and evaluation plan are prepared. Local needs and learning effects have not yet been validated. Required primary evidence, supervisor review and access verification remain outstanding.</p></section>'
 refshtml='<section><h1>REFERENCES</h1>'+''.join('<p>'+str(nums[rid])+' '+esc(clean(bibliography[rid]))+' - URL: <a href="'+html.escape(urls[rid],quote=True)+'">'+esc(urls[rid])+'</a> (accessed: 22.10.2026).</p>' for rid in order)+'</section>'
 apphtml='<section><h1>APPENDIX A - Tracker evidence</h1>'+''.join('<figure><img src="../project-management/screenshots/'+fn+'"><figcaption>Figure A.'+str(i)+' - '+esc(title)+'</figcaption></figure>' for i,(fn,title,_) in enumerate(shots,1))+'</section>'
 apphtml+='<section><h1>APPENDIX B - Observed prototype checks</h1>'+''.join('<p>'+esc(t)+'</p>' for t in paragraphs[1:])+'</section>'
 apphtml+='<section><h1>APPENDIX C - Project work breakdown</h1><p>Table C.1 - Project work items. Owner: Ayan Abilbek. Dates for future stages are not scheduled.</p><table><tr><th>Issue</th><th>Work item / group</th><th>Priority / status</th><th>Target date</th></tr>'+''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in row)+'</tr>' for row in rows)+'</table></section>'
 (REPO/'docs/report-gost.html').write_text('<!doctype html><html lang="en"><meta charset="utf-8"><title>'+esc(TITLE)+'</title><style>'+css+'</style>'+front+''.join(htmlparts)+conclusion+refshtml+apphtml+'</html>')
 audit={'pages':total,'a4_pages':sum(abs(float(p.mediabox.width)-A4[0])<1 for p in PdfReader(path).pages),'a3_appendix_pages':len(shots),'main_tables':22,'appendix_tables':1,'main_figures':5,'appendix_figures':len(shots),'references':len(order),'reference_map':nums,'sections':doc.locations,'table_index':index,'font':'Times New Roman','body_font_pt':14,'body_leading_pt':21,'margins_mm':{'left':30,'right':15,'top':20,'bottom':20},'first_line_indent_mm':12.5,'date':'2026-10-23'}
 (REPO/'docs/gost-layout-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
 return total

if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=REPO/'docs/First_Submission_Report.pdf');args=parser.parse_args();args.output.parent.mkdir(parents=True,exist_ok=True)
 count=build(args.output);final=build(args.output,count)
 if final!=count:final=build(args.output,final)
 print(f'GOST report: {final} pages; 11 required sections; 27 references; 3 appendices.')
