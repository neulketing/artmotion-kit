<div align="center">

**English** | [한국어](../README.ko.md) | [原版 (简体中文)](https://github.com/alchaincyf/huashu-art-motion)

# ArtMotion Kit

An agent skill that paints 36 art styles in code and makes them move, plus 9 explainer-animation grammars, with **on-screen text, captions and narration in English or Korean.**

```sh
git clone https://github.com/neulketing/artmotion-kit ~/.claude/skills/artmotion-kit && ~/.claude/skills/artmotion-kit/l10n/apply.sh en
```

<sub>Use `apply.sh ko` for Korean output. Other agents: clone into that agent's skills folder instead of `~/.claude/skills/`.</sub>

</div>

> **Based on [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) by alchaincyf (花叔)**, MIT License.
> This fork keeps every upstream file untouched and adds a localization layer in `l10n/`: Hangul fonts, word-based line breaking for Korean, an English/Korean storyboard lint wrapper, local macOS narration, and English/Korean `SKILL.md`. Details: [NOTICE.l10n.md](../NOTICE.l10n.md).

<img src="https://raw.githubusercontent.com/neulketing/artmotion-kit/main/l10n/demo/demo_ko.gif" alt="Seurat, Van Gogh and Monet styles rendered in code, with Korean captions under each" width="100%" />

<sub>Rendered with this kit: three style scenes (Seurat, Van Gogh, Monet) with Korean captions. 7 s, [MP4 with Korean narration](https://github.com/neulketing/artmotion-kit/releases/download/l10n-demo-ko/demo_ko.mp4) from the macOS built-in voice.</sub>

## Why this fork

The original skill is excellent, but it is written for Chinese output: its guide is in Chinese, its screen fonts carry only Chinese characters, its line breaker splits text one character at a time, and its narration path is a Chinese cloud voice-cloning service. The upstream English README notes that the installed skill itself stays in Chinese.

ArtMotion Kit makes **the results** come out in English or Korean:

| Upstream (China-first) | ArtMotion Kit |
|---|---|
| `SKILL.md` in Chinese | `l10n/SKILL.en.md` / `l10n/SKILL.ko.md`, same rules, output language set to English or Korean, plus a map of which `references/` doc to read when |
| Screen fonts: Chinese subsets (Noto Sans SC, LXGW WenKai) | Hangul added to the same family names through `unicode-range`: Noto Sans KR, Noto Serif KR, Gaegu (all SIL OFL 1.1) |
| Line breaking per character | Korean breaks at spaces, like English |
| Storyboard lint reads Chinese headers only | `l10n/scripts/lint.py` accepts English or Korean tables |
| Narration: Volcengine voice cloning (Chinese cloud, paid) | `l10n/scripts/say.py`: macOS built-in voices (Samantha, Yuna), no account, no key, nothing leaves the machine |

## What it does

| You say | It does |
|---|---|
| "Recreate this animation" | Measures cuts, beat grid and motion heatmaps, then rebuilds the mechanism in code |
| "Make it look like Van Gogh / Monet / Bauhaus" | Designs one frame first, then brings it to life; 36 style recipe cards as starting points |
| "Animate my narration" | Storyboard → one look → world canvas and camera → a picture track |
| "Explainer animation, Kurzgesagt / Vox / whiteboard / 3b1b style" | Picks a grammar and renders a frame-accurate clip from a JSON spec (landscape, portrait or alpha) |
| "Add music" | BPM grid, motif swaps, ending stingers, all synthesized in code |

Before delivery, `qa.py` measures stability, motion and smoothness, and `deliver.py` refuses to ship a film that reads like a slide deck.

<img src="https://raw.githubusercontent.com/neulketing/artmotion-kit/main/l10n/demo/frame_ko_whiteboard.jpg" alt="Whiteboard grammar with Korean handwriting, wrapped at word boundaries" width="100%" />

<sub>Whiteboard grammar with Korean handwriting (Gaegu), wrapped at word boundaries. Spec: [`l10n/demo/y3_whiteboard.ko.json`](../l10n/demo/y3_whiteboard.ko.json).</sub>

## Quick start

Requirements: [uv](https://docs.astral.sh/uv/), ffmpeg, Playwright Chromium (`uv run --with playwright playwright install chromium` once).

```sh
cd ~/.claude/skills/artmotion-kit
l10n/apply.sh en                                    # or: ko
uv run --with playwright python scripts/engine/render.py --solo 09_postimp --stills 0.3 --out stills   # one Van Gogh frame
python3 l10n/scripts/say.py --text "Why does Van Gogh's sky swirl?" --out vo.wav                      # local narration (macOS)
```

Reproduce the demo: copy `scripts/engine` to a project folder after `apply.sh`, drop in [`l10n/demo/eras_ko.js`](../l10n/demo/eras_ko.js), and run `render.py --film ko --fps 30 --out demo.mp4`.

`l10n/apply.sh` copies the Hangul fonts into the engine, applies three small patches (`l10n/patches/`) and swaps in the localized `SKILL.md`. `l10n/apply.sh --revert` restores the upstream files; run it before `git pull`.

## License

- Code and docs: MIT, © 2026 alchaincyf (花叔 · 花生), see [LICENSE](../LICENSE). Localization layer: MIT, © 2026 neulketing.
- Fonts keep their SIL OFL 1.1 licenses (`scripts/engine/lib/fonts/LICENSES.md`, `l10n/fonts/OFL-*.txt`).
- The upstream exceptions still apply: the Arphic-licensed stroke data, the original author's character art and the Clawd fan demo are not covered by MIT. See the upstream [README](../README.md#许可证).

ArtMotion Kit is an independent localization. It is not affiliated with or endorsed by the original author.
