from pathlib import Path
import re, html, json, textwrap
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, PageBreak,
    NextPageTemplate, LongTable, TableStyle, KeepTogether, CondPageBreak
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

ROOT=Path('/workspace/scratch/24df8a212037')
OUT=ROOT/'output'
PDF_DIR=OUT/'pdf'
PDF_DIR.mkdir(parents=True,exist_ok=True)
source=OUT/'ChatGPT_Operating_System_Research.md'
md=source.read_text()
# ASCII hyphens for robust PDF text; all wording remains unchanged.
md=md.replace('\u2011','-').replace('\u2013','-').replace('\u2014',' - ')
source.write_text(md)

FONT_DIR=Path('/usr/share/fonts/truetype/dejavu')
for name, filename in [('DVS','DejaVuSans.ttf'),('DVS-Bold','DejaVuSans-Bold.ttf'),('DVM','DejaVuSansMono.ttf')]:
    pdfmetrics.registerFont(TTFont(name,str(FONT_DIR/filename)))
pdfmetrics.registerFontFamily('DVS',normal='DVS',bold='DVS-Bold',italic='DVS',boldItalic='DVS-Bold')

INK=colors.HexColor('#182B3A')
MUTED=colors.HexColor('#526775')
TEAL=colors.HexColor('#126B70')
LIGHT=colors.HexColor('#EDF5F5')
RULE=colors.HexColor('#CDDADD')
BODY=ParagraphStyle('Body',fontName='DVS',fontSize=9.5,leading=13.8,textColor=INK,spaceAfter=6.5,allowWidows=0,allowOrphans=0)
H2=ParagraphStyle('H2',fontName='DVS-Bold',fontSize=15.2,leading=20.2,textColor=TEAL,spaceBefore=17,spaceAfter=9,keepWithNext=True)
H3=ParagraphStyle('H3',fontName='DVS-Bold',fontSize=11.2,leading=15.2,textColor=INK,spaceBefore=10,spaceAfter=7,keepWithNext=True)
SMALL=ParagraphStyle('Small',parent=BODY,fontSize=8.5,leading=12,textColor=MUTED)
TABLE=ParagraphStyle('Cell',parent=BODY,fontSize=7.9,leading=10.6,spaceAfter=0)
TABLE_HEAD=ParagraphStyle('HeadCell',parent=TABLE,fontName='DVS-Bold',textColor=colors.white)
CODE=ParagraphStyle('Code',fontName='DVM',fontSize=8.1,leading=11.6,textColor=INK,spaceAfter=5,backColor=LIGHT,borderPadding=8)
LIST=ParagraphStyle('List',parent=BODY,leftIndent=14,firstLineIndent=0,bulletIndent=0,spaceAfter=5)
TOC_STYLE=ParagraphStyle('TOC',fontName='DVS',fontSize=8.7,leading=11.8,textColor=INK,spaceBefore=1)

refs={m.group(1):m.group(2) for m in re.finditer(r'\*\*(S\d+):\*\* \[[^\]]+\]\((https?://[^)]+)\)',md)}

def inline(value):
    value=html.escape(value,quote=False)
    value=re.sub(r'\[([^\]]+)\]\((https?://[^)]+)\)',lambda m:f'<link href="{m.group(2)}" color="#126B70">{m.group(1)}</link>',value)
    value=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',value)
    value=re.sub(r'`([^`]+)`',r'<font name="DVM">\1</font>',value)
    def cite(m):
        codes=m.group(1).split(', ')
        return '['+', '.join(f'<link href="{refs[c]}" color="#126B70">{c}</link>' if c in refs else c for c in codes)+']'
    value=re.sub(r'\[((?:S\d+)(?:, S\d+)*)\]',cite,value)
    return value

def footer(canvas,doc):
    width,height=canvas._pagesize
    canvas.setStrokeColor(RULE)
    canvas.setLineWidth(.5)
    canvas.line(42,31,width-42,31)
    canvas.setFont('DVS',7.2)
    canvas.setFillColor(MUTED)
    canvas.drawString(42,20,'CHATGPT OPERATING SYSTEM  |  RESEARCH ONLY  |  03 OCT 2026')
    canvas.drawRightString(width-42,20,str(doc.page))

class ResearchDoc(BaseDocTemplate):
    def afterFlowable(self,flowable):
        if getattr(flowable,'toc_level',None) is not None:
            title=flowable.getPlainText()
            key=flowable.bookmark
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,flowable.toc_level,closed=False)
            self.notify('TOCEntry',(flowable.toc_level,title,self.page,key))

portrait=(612,792)
landscape=(792,612)
doc=ResearchDoc(str(PDF_DIR/'ChatGPT_Operating_System_Research.pdf'),pagesize=portrait,leftMargin=46,rightMargin=46,topMargin=44,bottomMargin=45,title='The most useful ChatGPT you can practically build',author='Research prepared for Nathan')
doc.addPageTemplates([
    PageTemplate(id='Portrait',frames=[Frame(46,45,520,703,id='portrait_frame',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],pagesize=portrait,onPage=footer),
    PageTemplate(id='Landscape',frames=[Frame(42,45,708,523,id='landscape_frame',leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0)],pagesize=landscape,onPage=footer)
])

story=[]
story.append(Spacer(1,72))
story.append(Paragraph('A practical operating system<br/>for ChatGPT',ParagraphStyle('CoverTitle',fontName='DVS-Bold',fontSize=28,leading=36,textColor=INK,spaceAfter=20)))
story.append(Paragraph('Research, architecture, proposed configuration,<br/>and a 24-task evaluation benchmark',ParagraphStyle('Subtitle',parent=BODY,fontSize=14,leading=21,textColor=TEAL,spaceAfter=23)))
story.append(Paragraph('Prepared for Nathan<br/>Verified October 3, 2026<br/>Brief dated October 2, 2026',ParagraphStyle('CoverMeta',parent=BODY,fontSize=11,leading=17,spaceAfter=25)))
for text in [
    '<b>Start small:</b> Work, concise instructions, current project context, useful tools, and verification.',
    '<b>Keep control:</b> no settings, skills, connections, agents, or schedules were activated.',
    '<b>Separate access from documentation:</b> Plus features, rollout-dependent tools, and optional Pro capabilities are distinguished.',
    '<b>Measure honestly:</b> local feasibility checks ran; isolated six-configuration model trials did not.'
]:story.append(Paragraph(text,BODY))
story.append(PageBreak())
story.append(Paragraph('Contents',H2))
toc=TableOfContents()
toc.levelStyles=[TOC_STYLE]
story.append(toc)
story.append(PageBreak())

lines=md.splitlines()
i=next(n for n,line in enumerate(lines) if line.startswith('## 1.'))
orientation='Portrait'
bookmark_count=0
in_capability_map=False

def switch(new_orientation):
    global orientation
    if orientation!=new_orientation:
        story.append(NextPageTemplate(new_orientation))
        story.append(PageBreak())
        orientation=new_orientation

def add_heading(text,level,table_caption=False):
    global bookmark_count
    style=H2 if level==2 else H3
    if table_caption:
        story.append(CondPageBreak(120))
        style=ParagraphStyle('TableCaption',parent=H3,keepWithNext=False)
    p=Paragraph(inline(text),style)
    p.is_heading=True
    if level==2:
        bookmark_count+=1
        p.toc_level=0
        p.bookmark=f'section_{bookmark_count}'
    story.append(p)

def add_table(rows):
    global orientation
    cols=len(rows[0])
    wide=cols>=7
    switch('Landscape' if wide else 'Portrait')
    width=708 if wide else 520
    if cols==7: widths=[91,97,97,95,139,89,100]
    elif cols==6: widths=[80,83,85,92,85,95]
    elif cols==5: widths=[100,110,110,100,100]
    elif cols==4: widths=[34,174,166,146] if rows[0][0] in ('ID','Rank') else [118,134,134,134]
    elif cols==3: widths=[135,195,190]
    elif cols==2: widths=[145,375]
    else: widths=[width/cols]*cols
    data=[[Paragraph(inline(cell),TABLE_HEAD if ri==0 else TABLE) for cell in row] for ri,row in enumerate(rows)]
    t=LongTable(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),TEAL),
        ('VALIGN',(0,0),(-1,-1),'TOP'),
        ('LEFTPADDING',(0,0),(-1,-1),6),('RIGHTPADDING',(0,0),(-1,-1),6),
        ('TOPPADDING',(0,0),(-1,-1),4.5),('BOTTOMPADDING',(0,0),(-1,-1),4.5),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F7F8')]),
        ('LINEBELOW',(0,0),(-1,0),.5,TEAL),
        ('LINEBELOW',(0,1),(-1,-1),.35,RULE),
    ]))
    story.append(t)
    story.append(Spacer(1,10))

while i<len(lines):
    line=lines[i]
    if not line.strip():i+=1;continue
    if line.startswith('# '):i+=1;continue
    if line.startswith('## '):
        in_capability_map=line.startswith('## 2.')
        switch('Landscape' if in_capability_map else 'Portrait')
        if line.startswith('## Sources'):story.append(PageBreak())
        add_heading(line[3:],2);i+=1;continue
    if line.startswith('### '):
        j=i+1
        while j<len(lines) and not lines[j].strip():j+=1
        next_wide=(j<len(lines) and lines[j].startswith('|') and len(lines[j].strip().strip('|').split('|'))>=7)
        switch('Landscape' if next_wide else 'Portrait')
        add_heading(line[4:],3,table_caption=next_wide);i+=1;continue
    if line.startswith('```'):
        switch('Portrait')
        i+=1;code=[]
        while i<len(lines) and not lines[i].startswith('```'):
            code.append(lines[i]);i+=1
        i+=1
        # Paragraphs permit clean page breaks inside long copy-paste blocks.
        chunks='\n'.join(code).split('\n\n')
        for chunk in chunks:
            story.append(Paragraph('<br/>'.join(html.escape(s) for s in chunk.splitlines()),CODE))
        story.append(Spacer(1,5))
        continue
    if line.startswith('|'):
        rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            row=[s.strip() for s in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r':?-+:?',s.replace(' ','')) for s in row):rows.append(row)
            i+=1
        assert all(len(r)==len(rows[0]) for r in rows),rows
        add_table(rows);continue
    bullet=re.match(r'^(- |\d+\. )(.*)',line)
    if bullet:
        switch('Portrait')
        marker='\u2022' if bullet.group(1)=='- ' else bullet.group(1).strip()
        story.append(Paragraph(inline(bullet.group(2)),LIST,bulletText=marker));i+=1;continue
    if line.startswith('**Usage and dates'):
        in_capability_map=False
    switch('Landscape' if in_capability_map else 'Portrait')
    para=[line];i+=1
    while i<len(lines) and lines[i].strip() and not re.match(r'^(#|\||```|- |\d+\. )',lines[i]):
        para.append(lines[i]);i+=1
    story.append(Paragraph(inline(' '.join(para)),BODY))

doc.multiBuild(story)
print(json.dumps({'pdf':str(PDF_DIR/'ChatGPT_Operating_System_Research.pdf'),'words':len(md.split()),'source_entries':len(refs),'report_sections':len(re.findall(r'^## \d+\.',md,re.M))}))
