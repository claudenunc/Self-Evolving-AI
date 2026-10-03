from pathlib import Path
import re
import html
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

root = Path('/workspace/scratch/24df8a212037')
font_root = Path('/usr/share/fonts/truetype/dejavu')
pdfmetrics.registerFont(TTFont('Guide', str(font_root / 'DejaVuSans.ttf')))
pdfmetrics.registerFont(TTFont('GuideBold', str(font_root / 'DejaVuSans-Bold.ttf')))
pdfmetrics.registerFontFamily('Guide', normal='Guide', bold='GuideBold', italic='Guide', boldItalic='GuideBold')

output = root / 'output/pdf/ChatGPT_OS_Teaching_Guide.pdf'
output.parent.mkdir(exist_ok=True)
styles = {
 'title': ParagraphStyle('title', fontName='GuideBold', fontSize=20, leading=25, spaceAfter=16, textColor=colors.HexColor('#143b43')),
 'h2': ParagraphStyle('h2', fontName='GuideBold', fontSize=12.8, leading=17, spaceBefore=15, spaceAfter=8, keepWithNext=True, textColor=colors.HexColor('#143b43')),
 'body': ParagraphStyle('body', fontName='Guide', fontSize=10, leading=14.2, spaceAfter=8, allowWidows=0, allowOrphans=0),
 'cell': ParagraphStyle('cell', fontName='Guide', fontSize=8.7, leading=12.2, spaceAfter=0),
 'tablehead': ParagraphStyle('tablehead', fontName='GuideBold', fontSize=8.7, leading=12.2, textColor=colors.white),
 'caption': ParagraphStyle('caption', fontName='Guide', fontSize=8, leading=11, spaceBefore=6, spaceAfter=12, textColor=colors.HexColor('#496069')),
}

def markup(text):
    text = text.replace('\u2014', '-').replace('\u2013', '-').replace('\u2011', '-')
    text = html.escape(text)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<link href="\2" color="#08736b"><u>\1</u></link>', text)
    text = re.sub(r'\*\*([^*]+)\*\*', r'<b>\1</b>', text)
    return text

lines = (root / 'output/ChatGPT_OS_Teaching_Guide.md').read_text().splitlines()
story = []
i = 0
while i < len(lines):
    line = lines[i].strip()
    if not line:
        i += 1
        continue
    if line.startswith('# '):
        story.append(Paragraph(markup(line[2:]), styles['title']))
    elif line.startswith('## '):
        story.append(Paragraph(markup(line[3:]), styles['h2']))
    elif line.startswith('|'):
        rows = []
        while i < len(lines) and lines[i].strip().startswith('|'):
            cells = [s.strip() for s in lines[i].strip().strip('|').split('|')]
            if not all(re.fullmatch(r'[-: ]+', cell) for cell in cells):
                rows.append(cells)
            i += 1
        table = Table([[Paragraph(markup(c), styles['tablehead'] if r == 0 else styles['cell']) for c in row] for r, row in enumerate(rows)], colWidths=[155, 361], repeatRows=1, hAlign='LEFT')
        table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#143b43')),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 9), ('RIGHTPADDING', (0,0), (-1,-1), 9),
            ('TOPPADDING', (0,0), (-1,-1), 8), ('BOTTOMPADDING', (0,0), (-1,-1), 8),
            ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor('#eef5f5'), colors.white]),
            ('LINEBELOW', (0,0), (-1,-1), 0.3, colors.HexColor('#c6d9dc')),
        ]))
        story.extend([table, Spacer(1, 10)])
        continue
    elif line.startswith('!['):
        match = re.fullmatch(r'!\[([^]]*)\]\(([^)]+)\)', line)
        if not match:
            raise ValueError(line)
        picture = Image(str(root / 'output' / match.group(2)))
        picture.drawHeight *= 516 / picture.drawWidth
        picture.drawWidth = 516
        story.append(KeepTogether([picture, Paragraph(markup(match.group(1)) + ' - actual completed-state capture.', styles['caption'])]))
    else:
        story.append(Paragraph(markup(line), styles['body']))
    i += 1

def page_decor(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor('#c6d9dc'))
    canvas.line(48, 748, 564, 748)
    canvas.setFont('Guide', 8)
    canvas.setFillColor(colors.HexColor('#496069'))
    canvas.drawString(48, 758, 'NATHAN / SELF IMPROVEMENT')
    canvas.drawRightString(564, 758, 'VERIFIED OCTOBER 3, 2026')
    canvas.drawString(48, 27, 'Teaching guide - observed actions, checks, and repeatable steps')
    canvas.drawRightString(564, 27, str(doc.page))
    canvas.restoreState()

doc = SimpleDocTemplate(str(output), pagesize=letter, rightMargin=48, leftMargin=48, topMargin=61, bottomMargin=48, title='ChatGPT Operating System: teaching guide', author='Nathan', pageCompression=1)
doc.build(story, onFirstPage=page_decor, onLaterPages=page_decor)
print(output)
