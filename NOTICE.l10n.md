# NOTICE — ArtMotion Kit localization layer

## Original work

- Project: **huashu-art-motion** — https://github.com/alchaincyf/huashu-art-motion
- Author: alchaincyf (花叔 · 花生)
- License: MIT (`LICENSE`, unchanged). Upstream exceptions remain in force: the Arphic Public License stroke data in `reference_films/spacex/spacex_wb/assets/strokes.js`, the SIL OFL fonts in `scripts/engine/lib/fonts/`, the original author's character art and frames, and the unofficial Clawd fan demo are not covered by MIT (see the upstream `README.md`, section 许可证).
- Upstream history is kept as is; this repository tracks it as the `upstream` remote and merges `upstream/main`.

"huashu" and "花叔" are the original author's personal brand. ArtMotion Kit does not use them as its name or logo and is not affiliated with or endorsed by the original author.

## What ArtMotion Kit adds (no upstream file is modified)

| Path | Purpose |
|---|---|
| `.github/README.md` | English front page |
| `README.ko.md` | Korean guide |
| `NOTICE.l10n.md` | This file |
| `l10n/SKILL.ko.md`, `l10n/SKILL.en.md` | The upstream `SKILL.md` instructions with Korean / English output, a reference-reading map, and the adapters below |
| `l10n/apply.sh` | Copies the Hangul fonts, applies `l10n/patches/*.patch`, swaps in the localized `SKILL.md`; `--revert` restores upstream |
| `l10n/patches/0001-hangul-fonts.patch` | `scripts/engine/lib/fonts.js`: adds Hangul faces to `PuHui-*`, `NotoSansSC`, `NotoSerifSC`, `LXGWWenKai-500` via `unicode-range` |
| `l10n/patches/0002-cmap-union.patch` | `scripts/engine/lib/util.js`: glyph check merges cmaps when one family has several files |
| `l10n/patches/0003-hangul-word-wrap.patch` | `scripts/engine/lib/typo.js`: Hangul words wrap at spaces instead of per character |
| `l10n/fonts/` | Noto Sans KR 500/700/800/900 and variable, Noto Serif KR variable, Gaegu Bold — KS X 1001 Hangul subsets in WOFF, with their OFL texts |
| `l10n/scripts/build_fonts.py` | Rebuilds the font subsets from the Google Fonts sources |
| `l10n/scripts/lint.py` | Runs the upstream `storyboard_lint.py` on Korean or English storyboards |
| `l10n/scripts/say.py` | Picks a Korean or US English macOS voice and calls the upstream `capabilities.py say --mode system` |
| `l10n/tests/` | Unit test for the lint wrapper |
| `l10n/demo/` | Korean demo: `eras_ko.js`, `y3_whiteboard.ko.json`, rendered `demo_ko.gif` and frames (the MP4 is a release asset: `l10n-demo-ko`) |

## China-specific dependencies and their replacements

| Upstream | Replacement |
|---|---|
| Chinese-only screen fonts (Noto Sans SC / LXGW WenKai GB2312 subsets) | Hangul faces under the same family names (Noto Sans KR, Noto Serif KR, Gaegu; SIL OFL 1.1) |
| Per-character line breaking (Chinese typesetting) | Word-based breaking for Hangul |
| Volcengine (ByteDance) voice cloning, Chinese cloud, paid | macOS built-in voices via `l10n/scripts/say.py` (local, free, no key); Volcengine stays available but off by default |
| Automatic system voice only for Mandarin (`zh_CN`, Tingting) | Automatic Korean (`ko_KR`) / US English (`en_US`) voice selection |
| Chinese storyboard headers and camera vocabulary | Korean and English headers and camera words, mapped for the upstream lint |

## Font credits

- Noto Sans KR — Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. SIL OFL 1.1 (`l10n/fonts/OFL-NotoSansKR.txt`).
- Noto Serif KR — Copyright 2012 Google Inc. SIL OFL 1.1 (`l10n/fonts/OFL-NotoSerifKR.txt`).
- Gaegu — Copyright 2018 The Gaegu Project Authors. SIL OFL 1.1 (`l10n/fonts/OFL-Gaegu.txt`).

The subsets are modified versions under the OFL and are distributed only as part of this software, not sold on their own.

## Localization layer license

MIT, © 2026 neulketing. Same terms as the upstream `LICENSE`.
