import json
import re
import subprocess
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

base = Path('/workspace/scratch/24df8a212037')
recording = base / 'tmp/os_recording'
frames = recording / 'frames'
frames.mkdir(exist_ok=True)
output = base / 'output/ChatGPT_OS_Terminal_Walkthrough.mp4'
font_root = Path('/usr/share/fonts/truetype/dejavu')
mono = ImageFont.truetype(str(font_root / 'DejaVuSansMono.ttf'), 18)
small = ImageFont.truetype(str(font_root / 'DejaVuSans.ttf'), 19)
title = ImageFont.truetype(str(font_root / 'DejaVuSans-Bold.ttf'), 32)
heading = ImageFont.truetype(str(font_root / 'DejaVuSans-Bold.ttf'), 23)
chapters = [json.loads(line) for line in (recording / 'chapters.jsonl').read_text().splitlines()]
slides = []

def draw(title_text, subtitle, lines, footnote, duration=7):
    image = Image.new('RGB', (1280, 900), '#101827')
    d = ImageDraw.Draw(image)
    d.text((45, 30), 'RESEARCH → IMPLEMENTATION', font=heading, fill='#69ddc4')
    d.text((45, 77), title_text, font=title, fill='white')
    d.text((45, 128), subtitle, font=small, fill='#b9c7dc')
    d.rounded_rectangle((30, 177, 1250, 798), radius=16, fill='#07101d', outline='#33465f', width=2)
    y = 202
    for line in lines[:25]:
        color = '#75e5ad' if '[OK]' in line or 'passed' in line or 'valid!' in line else '#f6ba71' if '[ERROR]' in line else '#e4eafa'
        d.text((50, y), line, font=mono, fill=color)
        y += 23
    for i,line in enumerate(textwrap.wrap(footnote, width=110)):
        d.text((45, 819 + i * 24), line, font=small, fill='#b9c7dc')
    file = frames / f'{len(slides):03d}.png'
    image.save(file)
    slides.append({'path': file, 'duration': duration, 'title':title_text})

draw('A recorded terminal walkthrough',
     'Actual command output captured during skill creation and checks — October 3, 2026',
     ['Purpose: turn reviewed research into working, verified configuration.',
      '', 'Capture begins after source review and the first skill initialization.',
      'It covers the remaining skill creation, corrections, and validation.',
      '', 'This is a chaptered terminal-session replay.',
      'It does not capture ChatGPT interface clicks or the Android screen.',
      'Sign-in, private files, credentials, and installation infrastructure are omitted.',
      '', 'Watch the completion signals; do not infer success from an attempt.'],
     'Timing is expanded for teaching. Paths are abbreviated for readability. No narration audio.', duration=9)

for chapter in chapters:
    clean = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', chapter['output']).replace('\r', '')
    clean = clean.replace('/root/.codex/skills/remote-skills', 'personal-skills')
    clean = clean.replace('/root/.codex/skills/oai/skill-creator', 'skill-creator')
    lines = []
    for line in clean.splitlines():
        lines.extend(textwrap.wrap(line, width=108, replace_whitespace=False, drop_whitespace=False) or [''])
    if len(lines) > 25:
        pages = [lines[i:i+25] for i in range(0, len(lines), 25)]
    else:
        pages = [lines]
    is_error = chapter['exit_code'] != 0
    lesson = ('A real metadata error: short_description must be 25–64 characters. The next step corrects it.'
              if is_error else 'Exit code 0 confirms this command completed. Structural checks and behavioral checks serve different purposes.')
    for page_number, page in enumerate(pages):
        label = chapter['chapter'] + (f' ({page_number + 1}/{len(pages)})' if len(pages) > 1 else '')
        draw(label, f"Captured terminal output • exit code {chapter['exit_code']}", page, lesson, duration=7)

draw('Verify installation separately',
     'Creation and validation are necessary; saved installation is a separate check.',
     ['Five workflows were structurally validated and saved:',
      '  Evidence Research', '  Decision and Experiment', '  Verified Execution',
      '  Research to Implementation', '  Teach and Repeat', '',
      'Realistic behavior checks covered current facts, must-have criteria,',
      'code correctness, and permitted implementation scope.', '',
      'Use the written guide for the final confirmed installation status.',
      'Direct Android invocation still needs a device check.',
      'Global and Self Improvement instructions were saved and reopened.',
      'The guide contains actual settings screenshots and source checks.'],
     'This closing card reports separate checks. Account setup appears in the guide, not in this terminal capture.', duration=9)

concat = recording / 'video_frames.txt'
with concat.open('w') as f:
    for slide in slides:
        f.write(f"file '{slide['path']}'\nduration {slide['duration']}\n")
    f.write(f"file '{slides[-1]['path']}'\n")
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-f', 'concat', '-safe', '0',
                '-i', str(concat), '-vsync', 'vfr', '-vf', 'format=yuv420p', '-c:v', 'libx264',
                '-preset', 'veryfast', '-crf', '22', '-movflags', '+faststart', str(output)], check=True)
timeline = []
t = 0
for slide in slides:
    timeline.append({'start_seconds':t,'duration_seconds':slide['duration'],'title':slide['title']})
    t += slide['duration']
(recording / 'video_chapters.json').write_text(json.dumps(timeline, indent=2))
print(json.dumps({'file':str(output),'duration_seconds':t,'chapters':len(slides),'bytes':output.stat().st_size}))
