#!/usr/bin/env python3
"""Build a static course index from repository resource files. No third-party dependencies."""
import json
import hashlib
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SEMESTERS = ['大一上-第1学期', '大一下-第2学期', '大二上-第3学期', '大二下-第4学期', '大三上-第5学期', '大三下-第6学期', '小学期', '英语体育公选课']
IGNORED = {'.DS_Store', '.gitkeep'}
BINARY = {'.exe', '.out', '.o', '.obj', '.pyc', '.class', '.dll', '.so', '.bpl'}

def category(path):
    for label, pattern in [('试卷复习', r'试卷|真题|考试|试题|复习|期末|期中'), ('课件', r'课件|ppt|slides|lecture'), ('笔记资料', r'笔记|note'), ('作业答案', r'作业|答案|习题|homework|hw\d|exercise'), ('实验实践', r'实验|实践|lab|experiment|课程设计')]:
        if re.search(pattern, path, re.I):
            return label
    return '其他资料'

def build():
    paths = subprocess.check_output(['git', 'ls-files', '--cached', '--others', '--exclude-standard', '-z'], cwd=ROOT).decode().split('\0')
    history = subprocess.check_output(['git', '-c', 'core.quotepath=false', 'log', '--format=@@%cs', '--name-only'], cwd=ROOT).decode()
    updated = {}
    date = ''
    for line in history.splitlines():
        if line.startswith('@@'):
            date = line[2:]
        elif line and date:
            updated.setdefault(line, date)
    courses = {}
    files = []
    for relative in sorted(set(filter(None, paths))):
        parts = Path(relative).parts
        if len(parts) < 2 or parts[0] not in SEMESTERS or (parts[0] != '英语体育公选课' and len(parts) < 3):
            continue
        path = ROOT / relative
        if path.name in IGNORED or path.suffix.lower() in BINARY or not path.is_file() or any(p.startswith('.') or p in {'__pycache__', 'node_modules'} for p in parts):
            continue
        guide = parts[0] == '英语体育公选课'
        guide_root = guide and len(parts) == 2
        key = parts[0] if guide_root else '/'.join(parts[:2])
        course = courses.setdefault(key, {'id': key, 'name': parts[0] if guide_root else parts[1], 'semester': parts[0], 'overview': '', 'overviewPath': '', 'count': 0})
        if len(parts) == (2 if guide_root else 3) and path.name.lower() == 'readme.md':
            course['overviewPath'] = relative
            course['overview'] = path.read_text(encoding='utf-8', errors='replace')
        files.append({'path': relative, 'name': path.name, 'course': key, 'semester': parts[0], 'category': category('/'.join(parts[2:])), 'type': path.suffix[1:].upper() or 'FILE', 'size': path.stat().st_size, 'updated': updated.get(relative, updated.get('英语体育公选课.md', '') if guide_root else '')})
        if path.suffix.lower() == '.md':
            files[-1]['markdown'] = path.read_text(encoding='utf-8', errors='replace')
        course['count'] += 1
    data = {'repository': os.environ.get('GITHUB_REPOSITORY', 'Harrisonls2004/BUPT-SCSS-2023'), 'branch': 'main', 'semesters': SEMESTERS, 'courses': list(courses.values()), 'files': files}
    destination = ROOT / 'site' / 'data.js'
    output = 'window.COURSE_DATA = ' + json.dumps(data, ensure_ascii=False, separators=(',', ':')) + ';\n'
    if not destination.exists() or destination.read_text(encoding='utf-8') != output:
        destination.write_text(output, encoding='utf-8')
    # Content versions keep a refreshed page from loading a previous data or UI bundle.
    index = ROOT / 'site' / 'index.html'
    html = index.read_text(encoding='utf-8')
    for asset in ['data.js', 'app.js', 'styles.css']:
        version = hashlib.sha256((ROOT / 'site' / asset).read_bytes()).hexdigest()[:12]
        html = re.sub(r'([\"\'])' + re.escape(asset) + r'(?:\?v=[a-f0-9]+)?\1',
                      lambda match: match[1] + asset + '?v=' + version + match[1], html)
    if html != index.read_text(encoding='utf-8'):
        index.write_text(html, encoding='utf-8')
    print(f'Indexed {len(courses)} courses and {len(files)} files → {destination.relative_to(ROOT)}')

if __name__ == '__main__':
    build()
