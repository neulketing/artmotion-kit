#!/usr/bin/env python3
# /// script
# dependencies = ["fonttools"]
# ///
"""Build the Hangul font subsets in l10n/fonts/ (SIL OFL 1.1 fonts from github.com/google/fonts).

    uv run l10n/scripts/build_fonts.py --src <dir with NotoSansKR[wght].ttf, NotoSerifKR[wght].ttf, Gaegu-Bold.ttf>
    uv run l10n/scripts/build_fonts.py --src <dir> --full      # all 11,172 syllables instead of KS X 1001's 2,350 (about 4x larger)
    uv run l10n/scripts/build_fonts.py --src <dir> --text "똠햏"   # add a few rare syllables

Each file holds Hangul only (syllables + compatibility jamo). Latin, digits and punctuation keep coming from the
original faces: l10n/apply.sh registers these files under the original family names with a Hangul unicode-range.
"""
import argparse
from pathlib import Path
from fontTools import subset
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer

OUT = Path(__file__).resolve().parents[1] / 'fonts'
JAMO = {chr(c) for c in range(0x3131, 0x318F)}


def ksx1001():
    out = set()
    for hi in range(0xB0, 0xC9):
        for lo in range(0xA1, 0xFF):
            try: out.add(bytes([hi, lo]).decode('euc-kr'))
            except UnicodeDecodeError: pass
    return out


def build(src, out, chars, wght=None):
    f = TTFont(src)
    if wght is not None:
        f = instancer.instantiateVariableFont(f, {'wght': wght})
    opts = subset.Options(); opts.flavor = 'woff'; opts.layout_features = ['*']; opts.name_IDs = ['*']
    s = subset.Subsetter(opts); s.populate(text=''.join(sorted(chars))); s.subset(f)
    f.flavor = 'woff'; f.save(out)
    print(f'{out.name}: {out.stat().st_size / 1024:.0f} KB')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', required=True); ap.add_argument('--full', action='store_true'); ap.add_argument('--text', default='')
    a = ap.parse_args(); src = Path(a.src)
    chars = ({chr(c) for c in range(0xAC00, 0xD7A4)} if a.full else ksx1001()) | JAMO | set(a.text)
    sans, serif = src / 'NotoSansKR[wght].ttf', src / 'NotoSerifKR[wght].ttf'
    for w in (500, 700, 800, 900):
        build(sans, OUT / f'NotoSansKR-{w}.woff', chars, w)
    build(sans, OUT / 'NotoSansKR-var.woff', chars)
    build(serif, OUT / 'NotoSerifKR-var.woff', chars)
    build(src / 'Gaegu-Bold.ttf', OUT / 'Gaegu-700.woff', chars)
