#!/usr/bin/env python3
"""Run the original storyboard_lint.py on a Korean or English storyboard.

    python3 l10n/scripts/lint.py storyboard.md [--script narration.txt]

The original lint only understands Chinese keys. This maps the lock lines (화풍/팔레트/캐릭터, Style/Palette/
Character), the table header, the camera column and a short list of filler words to the Chinese keys, then calls
the original lint() unchanged. Messages are printed by the original script (in Chinese).
On-screen text: every Hangul word counts as ceil(syllables / 2) characters, an English word as 1, so the
original "<= 8" rule becomes roughly 16 Hangul syllables or 8 English words.
"""
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import storyboard_lint as SL  # noqa: E402

LOCK = {'화풍': '画风', '스타일': '画风', 'style': '画风', '팔레트': '色板', 'palette': '色板',
        '캐릭터': '角色', '인물': '角色', 'character': '角色', 'characters': '角色',
        '파랑보라 허용': '允许蓝紫', 'allow blue-purple': '允许蓝紫'}
HEAD = [('시간', '时间段'), ('time', '时间段'), ('사물', '画面里的物'), ('object', '画面里的物'), ('동작', '它在做什么'),
        ('action', '它在做什么'), ('카메라', '镜头'), ('camera', '镜头'), ('화면 글자', '屏上字'), ('자막', '屏上字'),
        ('on-screen text', '屏上字'), ('text', '屏上字'), ('방법', '做法'), ('method', '做法'), ('how', '做法'),
        ('태그', '标签'), ('tags', '标签')]
CAM = {'정지': '停', '고정': '停', 'hold': '停', '천천히 밀기': '缓推', '슬로 푸시': '缓推', 'slow push': '缓推',
       '빼기': '拉远', '줌아웃': '拉远', 'pull out': '拉远', 'pull back': '拉远', '가로 이동': '横移', '패닝': '横移',
       'pan': '横移', '빠른 밀기': '快推', 'fast push': '快推', '내리꽂기': '砸入', 'slam': '砸入', '휩': '甩',
       'whip': '甩', '컷': '切', 'cut': '切', '밀기': '推', 'push': '推', 'zoom in': '推'}
# Lock values and object/action cells: the few filler words the original checks for.
WORDS = {'없음': '无', 'none': '无', '손': '手', 'hands': '手', 'hand': '手', '뒷모습': '背影', 'back view': '背影',
         '실루엣': '剪影', 'silhouette': '剪影', '프레임 라이브러리': '帧库', 'frame library': '帧库',
         '코드로 그린': '代码画', 'code-drawn': '代码画', '로봇': '机器人', 'robot': '机器人', '졸라맨': '火柴人',
         'stick figure': '火柴人', '캐릭터': '卡通人', 'mascot': '吉祥物',
         '제목': '标题', 'title': '标题', '텍스트': '文字', '글자': '文字', 'text': '文字', '목록': '列表', 'list': '列表',
         '배경': '背景', 'background': '背景', '아이콘': '图标', 'icon': '图标', '빈 화면': '空画面', 'empty frame': '空画面',
         '검은 화면': '黑场', 'black screen': '黑场', '단색': '纯色', 'solid color': '纯色',
         '나타난다': '出现', '나타남': '出现', '등장': '出现', 'appears': '出现', 'appear': '出现', '표시': '显示',
         'shows': '显示', 'show': '显示', '보여준다': '展示', '페이드 인': '淡入', 'fades in': '淡入', 'fade in': '淡入'}


def sub_words(cell, table):
    for k in sorted(table, key=len, reverse=True):
        cell = re.sub(rf'(?<![A-Za-z]){re.escape(k)}(?![A-Za-z])', table[k], cell, flags=re.I)
    return cell


def count_text(cell):
    return re.sub(r'[가-힣]+', lambda m: '字' * math.ceil(len(m.group()) / 2), cell)


def translate(text):
    out, fence, head, cols = [], False, None, {}
    lock = re.compile(r'^(\s*[-*]?\s*(?:\*\*)?)(' + '|'.join(sorted(map(re.escape, LOCK), key=len, reverse=True)) + r')((?:\*\*)?\s*[:：])(.*)$', re.I)
    lines = text.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip().startswith('```'):
            fence = not fence
        if fence:
            out.append(ln); continue
        m = lock.match(ln)
        if m:
            out.append(m.group(1) + LOCK[m.group(2).lower()] + m.group(3) + sub_words(m.group(4), WORDS)); continue
        is_row = ln.strip().startswith('|')
        if is_row and head is None and i + 1 < len(lines) and re.match(r'^\s*\|?\s*:?-{2,}', lines[i + 1]):
            cells = SL.strip_cells(ln); head = []
            for k, h in enumerate(cells):
                zh = next((z for key, z in HEAD if key in h.lower()), h)
                head.append(zh); cols.setdefault(zh, k)
            out.append('| ' + ' | '.join(head) + ' |'); continue
        if is_row and head is not None and not re.match(r'^\s*\|?\s*:?-{2,}', ln):
            cells = SL.strip_cells(ln)
            for name, fn in (('镜头', lambda c: sub_words(c, CAM)), ('屏上字', count_text),
                             ('画面里的物', lambda c: sub_words(c, WORDS)), ('它在做什么', lambda c: sub_words(c, WORDS))):
                k = cols.get(name)
                if k is not None and k < len(cells):
                    cells[k] = fn(cells[k])
            out.append('| ' + ' | '.join(cells) + ' |'); continue
        out.append(ln)
    return '\n'.join(out)


def main(argv):
    if not argv or argv[0] in ('-h', '--help'):
        print(__doc__); return 2
    script = None
    if '--script' in argv:
        k = argv.index('--script'); script = Path(argv[k + 1]).read_text(encoding='utf-8'); del argv[k:k + 2]
    res = SL.lint(translate(Path(argv[0]).read_text(encoding='utf-8')), script)
    print('\n'.join(SL.report(res)))
    if 'error' in res:
        return 2
    return 1 if res['verdict'] == SL.RED else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
