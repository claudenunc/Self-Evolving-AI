import argparse
import json
import os
import pty
import select
import shlex
import subprocess
import time
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('chapter')
parser.add_argument('command', nargs=argparse.REMAINDER)
args = parser.parse_args()
if args.command and args.command[0] == '--':
    args.command = args.command[1:]
if not args.command:
    parser.error('supply a command after --')

root = Path('/workspace/scratch/24df8a212037/tmp/os_recording')
root.mkdir(parents=True, exist_ok=True)
cast_path = root / 'terminal.cast'
meta_path = root / 'chapters.jsonl'
if not cast_path.exists():
    cast_path.write_text(json.dumps({'version': 2, 'width': 100, 'height': 25,
                                   'title': 'ChatGPT OS skill creation and validation',
                                   'env': {'TERM': 'xterm-256color'}}) + '\n')
offset = 0.0
with cast_path.open() as cast:
    for line in list(cast)[1:]:
        offset = max(offset, json.loads(line)[0])
offset += 1.5
start = time.monotonic()
plain_output = []
with cast_path.open('a') as cast:
    def event(text):
        cast.write(json.dumps([round(offset + time.monotonic() - start, 3), 'o', text]) + '\n')
        cast.flush()
    event('\x1b[2J\x1b[H' + args.chapter + '\r\n\r\n$ ' + shlex.join(args.command) + '\r\n')
    master, slave = pty.openpty()
    process = subprocess.Popen(args.command, stdin=subprocess.DEVNULL, stdout=slave,
                               stderr=slave, env=dict(os.environ, TERM='xterm-256color'))
    os.close(slave)
    try:
        while True:
            ready, _, _ = select.select([master], [], [], 0.1)
            if ready:
                try:
                    data = os.read(master, 65536)
                except OSError:
                    break
                if not data:
                    break
                output = data.decode('utf-8', errors='replace')
                plain_output.append(output)
                event(output)
            elif process.poll() is not None:
                break
    finally:
        os.close(master)
    code = process.wait()
    event(f'\r\nCompleted with exit code {code}\r\n')
with meta_path.open('a') as meta:
    meta.write(json.dumps({'chapter': args.chapter, 'command': args.command,
                           'start': offset, 'exit_code': code,
                           'output': ''.join(plain_output)}) + '\n')
print(''.join(plain_output), end='')
print(f'Recorded: {args.chapter}; exit code {code}')
raise SystemExit(code)
