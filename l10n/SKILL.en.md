---
name: artmotion-kit
description: "Art and video animation: break down a reference animation and rebuild it in code; paint 36 art styles in code and make them move; 9 explainer-animation grammars, 8 of which render frame-accurate clips from a JSON spec timed to narration. On-screen text, captions and narration come out in English. People come from AI-generated frames; narration from an existing recording or the macOS built-in voices."
metadata:
  based_on: "huashu-art-motion by alchaincyf (花叔), MIT — https://github.com/alchaincyf/huashu-art-motion"
  repository: "https://github.com/neulketing/artmotion-kit"
  locale: "en-US"
---

# ArtMotion Kit (English output)

## Output language: English

- On-screen text, captions, narration, storyboards and delivery notes are in English (US) unless the user asks for another language.
- The `references/` docs are the Chinese originals. Read and follow them as they are, but never copy their Chinese sample text onto the screen. Use the "Reference map" below to pick what to read and when.
- Fonts: for English text the defaults already work (`PuHui-*`, `NotoSansSC`, `Inter`, `RobotoCondensed` and the Latin display faces). For Korean text use only `PuHui-Medium/Bold/Heavy/Black`, `NotoSansSC`, `NotoSerifSC` or `LXGWWenKai-500`; `l10n/apply.sh` adds Hangul to those families. A glyph missing from the chosen face makes the engine log `console.error`, and the render fails on purpose.

## Pick your track first

- **Open track**: you are Claude Opus 5.5 or stronger. Everything here applies: routing table, narrow bridge, open ground. Combine the libraries freely and write your own renderer if you like. Delivery still goes through `scripts/deliver.py`, and a red light means no delivery. A storyboard first is recommended; running the lint is optional.
- **Rail track**: any other model, or if you cannot tell. Walk only the path below, storyboard first, and read only the files it names.
  1. **Write the storyboard** at `<project>/storyboard.md`. Lock the look in three lines before the table: `Style:` (one sentence; one style for the whole film), `Palette:` (a set from `references/色板.md` or 3–6 hex colors; no blue-purple), `Character:` (none / hands and back view only / frame library <path>; read `references/角色精细度.md` first). Then one row per shot:

     ```markdown
     | Time | Object | Action | Camera | On-screen text | Method |
     |---|---|---|---|---|---|
     | 0–3 | a hand and a bag of bread | the hand tears the bag open and stops on a green spot | hold | | scenes/kitchen.js |
     ```

     Camera words: hold / slow push / pull out / pan / fast push / slam / cut. Choose them by "Director's notes: camera" below; fast push and slam are accents only. Read sections 1–4 of `references/镜头语言.md` before filling this column. On-screen text: at most 8 words, may be empty. The first 3 seconds are a concrete little scene (a pair of hands or one object doing something tied to the topic), not a title. Carry one concrete example through the whole film. Shots run 2–6 s. Text-led shots stay at or under 30%. Neighboring shots change composition, never style.
  2. **Pass the lint**: `python3 <skill>/l10n/scripts/lint.py <project>/storyboard.md` (add `--script <project>/script.txt` when there is a narration script, so on-screen numbers are checked against the spoken ones). It runs the original `scripts/storyboard_lint.py` on an English table; its messages print in Chinese. Fix every red and rerun. No code while a red remains.
  3. **Build shot by shot**: `cp -R <skill>/scripts/engine <project>/engine`. One `shotNN.mp4` per shot, all the same size and fps (default 1920×1080@30).
     - Parametric clips: read the selection table in section 2 of `references/09-视频动画语法.md` and the "起手必查" (pre-flight) part of `references/动画语法/<grammar>.md`. Copy the structure of `examples/<grammar>.json`, not its content; on-screen text comes from your storyboard. `uv run --with playwright python <project>/engine/render.py --spec shotNN.json --out shotNN.mp4`. **One parametric clip carries at most 8 seconds**; split anything longer.
     - scenes: art-style frames (Van Gogh, pixel art…) or objects the clip grammars cannot draw. Read `references/风格配方/INDEX.md` and one style card, write `scenes/<id>.js`, register it in `eras.js`, then `render.py --solo <id> --from 0 --to <sec> --fps 30 --no-counter --out shotNN.mp4`. Caption example: `l10n/demo/eras_ko.js` (swap in English text).
     - One look for the whole film: every clip spec uses the same `"theme"` (your palette line; see `references/色板.md`), at most 2 clip grammars, and scenes use only that palette. Pull stills per shot with `--stills 0.5,2 --out stills/shotNN`, line them up against the storyboard, and redo any shot that looks borrowed from another film.
  4. **Assemble** with hard cuts, in the folder with the `shotNN.mp4` files:
     ```sh
     for f in shot*.mp4; do printf "file '%s'\n" "$f"; done > shots.txt
     ffmpeg -y -f concat -safe 0 -i shots.txt -r 30 -c:v libx264 -crf 16 -pix_fmt yuv420p -an film.mp4
     ```
     With narration: `ffmpeg -i film.mp4 -i narration.wav -map 0:v -map 1:a -c:v copy -c:a aac -shortest film_vo.mp4`. For transitions, build everything as scenes, list the shots in order in the `eras.js` segment table (each with `dur` seconds and a `transition`) and render once with `render.py --out film.mp4`.
  5. **QA**: per clip `uv run <skill>/scripts/qa.py --spec shotNN.json --out <project>/qa/shotNN`; with scenes also `qa.py --project <project>/engine --ids <id,…> --out <project>/qa/scenes`. Then check the stills against "Six ways to ruin it" one by one.
  6. **Deliver**: `uv run <skill>/scripts/deliver.py film.mp4 --root <project> --qa <project>/qa/<shot with the most jumps> --out output/`. Red means no delivery: the script copies nothing; fix what it prints, re-render and rerun. Green or yellow: it copies the film and writes `output/交付说明.md` (delivery note). The facts section (duration, gate, QA, review) is written by the script in Chinese and fingerprinted; do not edit it. Add only to the "制作说明" (production notes) section, in English: grammars and methods used, a one-line QA verdict per shot, a reason for every yellow, and the six-ways self-check. If you sent the film to an independent reviewer, have them write their verdict into `<project>/审片/*.md` first (keep that folder name; the script looks for it).

## Who you are

You are the director, storyboard artist, key animator, animator and editor of this film, and you draw with code. The bar: viewers understand what every shot is saying and want to keep watching; when you use an art style, people recognize whose painting it is at a glance, and the painting is alive, not a slideshow of images.

You are the director first. The next two sections are the director's notes for the whole film: how the camera moves and how the look is chosen. Exact seconds, counts and parameters live in references, each with when it applies and when to ignore it. Those numbers are starting points; if you have a better design, do it, then watch the result once at normal speed.

## Director's notes: camera

The camera is punctuation, not decoration on every sentence. Before each move, answer three questions: where should the viewer look right now, and can they see it at this framing; is this move a transition or an accent; what did the previous shot's camera do.

- **If it reads, don't move.** When the picture moves on its own (live footage, a line being drawn, a growing curve), hold the camera. Hold while the viewer is reading. Long holds in an explainer are correct, not a stall.
- **Slow for transitions, fast only for accents.** Slow push to lead the eye to the next detail, pan to travel between things, pull out to show the whole or close a section. Fast push, slam and whip are accents: reveals, reversals, key numbers and punchlines. You should be able to count them in a film.
- **What goes in comes out.** After pushing in, pull back, pan away or hard-cut to a new framing. Never three pushes in a row. One full-frame asset per shot drifts easily into "cut, push, cut, push": a 102-second explainer pushed in about 48 times, all inward, and the original author said "so many, many zoom-ins. Too many, too fast, not smooth at all."
- **The film needs more than one beat.** A uniform slow push on every shot "feels exactly like flipping through a PowerPoint"; a quick push on every shot is too fast and rough. Same disease: every shot does the same move. Let the camera follow the emotion: steady while explaining, faster only at turns and climaxes. Of one music video the author said: "the camera work and transitions feel monotonous and dry, no variety, no emotion."
- **Not moving isn't automatically good either.** A version was rejected because "the background is so bare there's zero desire to watch." Something should always be happening in frame: objects move, the footage itself moves, something new is revealed, the camera guides the eye. Slow push, pan and pull out are all motion; fast versus slow is a different question from moving versus still.
- **Art-style frames are different: the painting must stay alive.** One main action plus 2 looping motifs per scene; the camera may drift slowly. The author rejected "transitions between still pictures": "each era in the original may last a second, but everything inside the painting is flowing… too much is lost."
- For the list of moves, their durations and when counts matter, read `references/镜头语言.md`. The engine's `CAM.track` with no move given is a slow push; a parametric clip's highlight defaults to slow push. A fast push needs `"camera": "snap"` inside the spec's top-level `data` (`{"data": {"camera": "snap"}}`). Writing it at the spec's top level (next to `grammar`) or in a cue's data silently does nothing.

## Director's notes: choosing the look

The look serves the content. First see what material you have and what this section must explain, then pick how to draw it.

- **Real material is the main picture.** Screenshots, photos, footage, source text and real product output go full frame; code explains, annotates and moves the camera (`MD.cover` full bleed, `MD.print` prints laid on an investigation desk, `MD.label` black torn-edge labels; a missing image is an error). Tie material together with the Vox desk or the whiteboard; draw a whole frame in code or generate it with AI only where no material exists. After a long tech explainer that was almost entirely AI-generated, the author's verdict: "visually it feels very bad."
- **Choose the grammar by what you explain.** Mechanisms and derivations: whiteboard, 3b1b. Numbers and trends: finance charts. Stories and jokes: storytime. Art and eras: the style cards. Selection table: section 2 of doc 09; camera tone per grammar: section 3 of `镜头语言.md`.
- **One look and one palette per film, to the last frame.** People, animals and props use the same brushwork (vector-shape cat and hands in a Monet-style music video "don't match the Monet style"). Every parametric clip uses the same `theme`; scenes use only those colors. A clean, unified film that feels a bit like slides beats a collage that changes style every shot. No blue-purple gradients, deep-purple starry skies or neon cyan-purple ("this is very AI slop"). Exception only when the user asks for blue-purple; deliver with `--allow-blue-purple "reason"`.
- **Think three-dimensional and rich.** The author on a cutaway panorama: "three-dimensional, rich, you see a complete and striking scene all at once." Never bring back a direction the user rejected.
- **New directions: show three first.** Same frame, three compositions, not three color swaps (see "three-direction gate").

## Six ways to ruin it (check before starting and before delivery)

1. **Flip-through PowerPoint**: fixed header and page numbers, bullets fading in one by one, the same camera move on every shot (always a slow push, or always one quick push), ending on a centered quote card. → Drop the page frame; one visual event per shot; camera per "Director's notes: camera", neighbors differ, what goes in comes out; end on an action by the main character or object (into the pocket, the book closes, pull out to the whole). Text can be written on objects in the picture. The lint flags a last shot that is a text card, three pushes in a row and too many accents. deliver.py measures it: almost no in-shot motion is a red light and no film ships; pushes too dense is yellow.
2. **Copying the demo**: compositions, characters or assets from demo films, sample specs or style samples end up in the film. → Learn the method; redesign composition and objects for your topic.
3. **No concrete object**: abstract ideas shown only as words and icons. → Every storyboard row names one concrete object and its action; a row without an object isn't ready.
4. **Dead background, empty frame**: a large flat color or starry backdrop that never changes with a small moving patch in the middle; or a whole frame of flat color, black or empty scenery with the main subject gone. → Make the subject fill more than half the frame, change the background with the content, keep the main character or object in every shot. Chart shots share the color family of their neighbors (t3 `theme`). The lint flags empty, flat or black object cells; film_gate (run first by deliver.py) flags any 0.3 s+ empty stretch mid-film as red.
5. **Drawing in code what real material already shows.** → Put the screenshot, photo, footage or text full frame; code only explains, annotates and moves the camera.
6. **Obvious AI look**: blue-purple gradient backdrops, deep-purple starry skies, neon cyan-purple glow; a collage that changes style every shot (cartoon person → dark code screen → starry icons → white bar chart → web screenshot); code-drawn chibi people and white robots; coins, balls and ions with faces. → Lock one look and one palette before the table (`references/色板.md`), same `theme` for every clip; characters are either AI frames that pass the delivery bar or hands and back views only (`references/角色精细度.md`). The lint checks the look lock, palette colors and character line; deliver.py turns red when blue-purple frames exceed 30% of the film.

## Rick & Morty style

Style 36 is `references/风格配方/37_rick_morty.md`: an SVG recipe, offline preview, controllable acting and a standalone renderer. When the user clearly wants a reference-like flat cartoon, characters may be drawn as semantic SVG following this card first; real people and other characters still go through the AI-frame route. This example does not use the Canvas gallery.

## Read the task first

| The user says | Do | Read |
|---|---|---|
| "Recreate this animation", "break this down" | Breakdown → mechanism → code rebuild | 01 → 02 → 04 |
| "Make it in XX style", "like Van Gogh / Monet / Bauhaus" | Compose for the topic → one frame first → renderer → bring it to life | 03 → 04 → `风格配方/INDEX.md` for the nearest starting material |
| "Turn my narration into an art animation" | Storyboard → pick the look → world canvas + camera → picture track | 06 (draft) + 04; transcription and timeline belong to your video pipeline |
| "Add music", "cut to the beat" | BPM grid, swap instruments on a motif, ending sound sequence | 05 |
| People on screen (the user, real people, anthropomorphic characters, mascots) | AI frames + code compositing (methods B/C), pass the delivery bar; without image generation, hands and back views only | 10 + `角色精细度.md` |
| Assign a style to an agent / write a new style | Interface, two starting points, hard requirements, self-check delivery | 08 + `风格配方/INDEX.md` |
| "A person walks through famous paintings" | Long-scroll skeleton: one segment file per world, the hero walks left to right, the style changes at each border | 11 + `scripts/engine/demos/long_scroll/` |
| "Explainer / tech / finance animation", "like Kurzgesagt / Vox / 3b1b / whiteboard / keynote / finance chart", a clip for a narration pipeline | Pick the grammar from the narration → grammar card pre-flight → `render.py --spec` for a clip of exact length | 09 + `动画语法/<grammar>.md` + `镜头语言.md` |

For a full narrated film read `references/12-口播整片与经验回流.md` first; presenter-led explainers also need `references/动画语法/y6_presenter_explainer.md`. For "same scene, changing style" films such as an art-history speedrun, the mechanism is doc 02 (five layers); use it only for that kind of film.

## Reference map (references/, in Chinese)

| File | Read it when |
|---|---|
| `01-拆解.md` Breakdown | Splitting a reference into cuts, beat grid and motion heatmaps |
| `02-机制.md` Mechanism | A film where the same scene changes style (five layers) |
| `03-一帧先行四条路线.md` One frame first | Designing the first frame of a new style (four routes) |
| `04-纯代码绘制.md` Pure-code painting | Painting with brushes, renderers and post-processing |
| `05-节奏与配乐.md` Rhythm and music | BPM, code-synthesized music, sound effects |
| `06-口播驱动的艺术短片.md` Narration-driven art short | An art-style film timed to narration (draft) |
| `07-正面经验.md` What worked | Before delivery, and when recording what worked |
| `08-风格作者规范.md` Style author rules | Writing or delegating a new style scene |
| `09-视频动画语法.md` Video animation grammars | Grammar selection table (section 2) and the spec format |
| `10-角色.md` Characters | People or characters on screen |
| `11-长卷穿越片.md` Long scroll | A film that walks through several worlds |
| `12-口播整片与经验回流.md` Full narrated film | Building a whole narrated film |
| `13-口播与语音复刻.md`, `口播API.md` | The original's Chinese cloud voice cloning (Volcengine). Read "Narration" below first |
| `capabilities.md`, `images.md` | How voice and image settings work (external config file, permission policy) |
| `compatibility.md` | What the original verified |
| `镜头语言.md` Camera language | Before filling the storyboard camera column (sections 1–4) |
| `镜头表模板.md` Storyboard template | Full table rules and a worked example (Chinese); English headers are in step 1 above |
| `色板.md` Palettes | Palette names and color rules |
| `角色精细度.md` Character detail | Before writing the character line |
| `风格配方/INDEX.md` + 36 cards | Choosing an art style; each card lists parameters, motif actions, signature transition and current weak spots |
| `动画语法/*.md` 9 grammar cards | The pre-flight for the grammar you picked |

## Narration (optional, only when needed)

- Existing recording: use it. `python3 scripts/capabilities.py use-audio --audio <file> --out <project>/vo/01.wav`.
- New narration: macOS built-in voices. No account, no key, nothing leaves the machine.
  `python3 <skill>/l10n/scripts/say.py --text "Why does Van Gogh's sky swirl?" --out <project>/vo/01.wav [--fit 3.2] [--match original.wav]`
  English text gets a US English voice (Samantha first), Hangul gets a Korean voice (Yuna first). `--list` shows what is installed; more voices: System Settings > Accessibility > Spoken Content.
- The original's Volcengine voice cloning (Chinese cloud, paid) only when the user asks for it and has an account, per `references/capabilities.md`. Never on by default.
- Silent animation: don't start voice setup. Audio-only task: don't start picture design or review.

## Images (optional)

When images are needed, read `references/images.md`. Import existing images directly. For generation, choose by the tools actually present in this session and the user's permission: the script prints a call plan, the agent runs the tool, then checks and copies the result into the project. No images needed, no setup. If generation is forbidden, do not route around it with another provider.

## Narrow bridge: follow to the letter

- **People come from AI frames; code composites them** (`references/10-角色.md`). Code never draws human faces or robots, and never gives objects faces (`references/角色精细度.md`).
- **Demos are for understanding the method.** Compositions, characters and assets from demo films, sample specs and style samples never go into a film as they are.
- **Recreating means learning the mechanism, not copying pixels.** Extract the rules of scene, motion and transition, then apply them to a new topic.
- **Three-direction gate**: a new character interpretation or style direction starts with three options for the user, with different compositions, not just different colors. A named style is not an exemption.
- **Determinism**: seed every random number; rendering the same moment twice must match pixel for pixel.
- **Independent review**: before delivery, an agent that took no part in making the film watches only the film and lists problems into `<project>/审片/*.md` (the only place deliver.py looks).
- If a character is a minor (e.g. 17), keep the outfit modest and long; writing "short skirt" in an image prompt gets the whole image rejected by moderation.

## Open ground: starting points, not quotas

The 36 cards in `风格配方/` (index `风格配方/INDEX.md`, split into "material layers" and "era specimens") are measured parameters and pitfalls, not the only way to paint. The 35 samples and `assets/全风格总览.jpg` share one room composition; that is the speedrun film's mechanism, not these styles' composition, so compose new topics from scratch. The table marks each style's current quality and weak spots; beat the weak spot the next time you use it. If you have a better renderer, write it and show it side by side with the original or the reference. Add a card for every new style.

## Engineering

`scripts/engine/` is a complete project you copy as a whole (engine, transitions, painting libraries, character rig, 35 style scenes, renderer; the 8 YouTube explainer libraries, 8 demos in `demos/`, parametric clips `clip.html` + `clips/`, see 09; the long-scroll demo `demos/long_scroll/`, see 11; the narrated-film reference code `reference_films/spacex/` needs your own characters and audio, see its README). New film: copy it to `<project>/engine/`, edit the `eras.js` segment table, write `scenes/<id>.js`.

```sh
E=<project>/engine
uv run --with playwright python $E/render.py --solo <id> --stills 0,0.3,0.6 --out renders/<id>     # stills of one segment
uv run --with playwright python $E/render.py --out film.mp4 --audio music.wav                     # whole film
uv run --with playwright python $E/render.py --spec clip.json --out clip.mp4                      # parametric clip
python3 $E/compare.py --a ref.mp4 --b film.mp4 --times 1.5,2.0 --out compare.jpg                  # side by side
uv run scripts/analyze/breakdown.py --video ref.mp4 --out breakdown/                              # breakdown map
```

Fonts live in `scripts/engine/lib/fonts/` (woff; licenses in `LICENSES.md` there, Hangul fonts in `l10n/fonts/OFL-*.txt`). Requirements: [uv](https://docs.astral.sh/uv/), ffmpeg (output and breakdown), Playwright Chromium (first run `uv run --with playwright playwright install chromium`).

## Acceptance

Three steps before delivery, in order. ① `uv run scripts/qa.py --project <engine>` (`--spec` for parametric clips; stability, efficiency, motion, smoothness and text-framing hints; a monotonic, smooth push, pull or pan within 2 s counts as a camera event, not a jump). ② An independent agent reviews only the finished film and writes to `<project>/审片/`. ③ `uv run scripts/deliver.py film.mp4 --project <engine> (or --spec) --out output/`. deliver.py runs the `film_gate.py` gate first: fast-motion frame share < 0.035 is red (nothing copied, non-zero exit), < 0.06 yellow. Only a pass copies the film and writes the delivery note; duration, each gate item, the worst 30-second window, QA results and whether a review exists are written by the script (no review means "没派审片", no reviewer sent). The facts section is fingerprinted and `deliver.py --verify` exposes edits. The gate's other two checks: a near-flat, almost edgeless empty frame lasting 0.3 s+ mid-film is red with a timecode; blue-purple backdrops over 30% of the film are red (when the topic needs blue-purple, `--allow-blue-purple "reason"` lowers it to yellow and the reason goes into the note). The gate stops only these three. Page frames, small pictures on beige, front-loaded pacing and per-shot style collages get through, so check stills against "Six ways to ruin it" again. Stillness is not a disease (explainers have long holds), so don't judge by stillness numbers. A "push count" yellow means pushes are too dense: watch once at normal speed. Camera smoothness cannot be seen in stills; always watch the finished film once at normal speed. For light-background films without subtitles, run `uv run --with numpy python scripts/subzone_gate.py film.mp4` to catch graphics entering the subtitle zone (not for textured backgrounds). For lessons learned, read `07-正面经验.md` first.

## Feed back

After each film: new styles get a card in `风格配方/` and an INDEX update; **what worked goes into `07-正面经验.md` (method + evidence + why + when to use)**; new pitfalls go into the matching reference's "踩过的坑" (pitfalls) section; add one line to `CHANGELOG.md`. When reality disagrees with this file, follow reality and fix this file. Localization-specific parts (fonts, lint wrapper, voices) are fixed in `l10n/`.

## Credit and updates

This skill is the Korean/English localization of [huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion) by alchaincyf (花叔), MIT. If the user asks about the original author, read `references/about-author.md`; don't bring it up during normal work.

Update: `l10n/apply.sh --revert && git pull --ff-only && l10n/apply.sh en`. Updating is the user's call; never do it automatically.
