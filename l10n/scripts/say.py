#!/usr/bin/env python3
"""Korean / English narration with the macOS built-in voices. No account, no key, nothing leaves the machine.

    python3 l10n/scripts/say.py --text "고흐의 하늘은 왜 소용돌이칠까" --out vo/01.wav [--fit 3.2] [--match 원본.wav]
    python3 l10n/scripts/say.py --text "Why does Van Gogh's sky swirl?" --out vo/01.wav
    python3 l10n/scripts/say.py --list                      # installed Korean / US English voices

Hangul in the text -> a Korean voice (Yuna first), otherwise a US English voice (Samantha first).
Override with --voice NAME or ARTMOTION_VOICE_KO / ARTMOTION_VOICE_EN. Everything else (--fit, --match,
--loudness, the 48 kHz WAV + .json receipt, the near-silence check) is the original
`scripts/capabilities.py say --mode system`; this file only picks the voice.
More voices: System Settings > Accessibility > Spoken Content > System voice > Manage Voices.
"""
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PREFER = {'ko_KR': ['Yuna', 'Sora', 'Jian', 'Suhyun'], 'en_US': ['Samantha', 'Alex', 'Ava', 'Allison', 'Tom']}
NOVELTY = {'Albert', 'Bad News', 'Bahh', 'Bells', 'Boing', 'Bubbles', 'Cellos', 'Wobble', 'Good News', 'Jester',
           'Organ', 'Superstar', 'Trinoids', 'Whisper', 'Zarvox', 'Fred', 'Junior', 'Ralph', 'Kathy'}


def voices():
    out = subprocess.run(['say', '-v', '?'], capture_output=True, text=True, check=True).stdout
    found = {}
    for line in out.splitlines():
        m = re.match(r'(.+?)\s{2,}(ko_KR|en_US)\s+#', line)
        if m:
            name = re.sub(r'\s*\(.*\)$', '', m.group(1).strip())   # "Eddy (한국어(한국))" -> "Eddy"
            if name not in NOVELTY and name not in found.setdefault(m.group(2), []):
                found[m.group(2)].append(name)
    return found


def pick(text):
    lang = 'ko_KR' if re.search(r'[가-힣]', text) else 'en_US'
    env = os.getenv('ARTMOTION_VOICE_KO' if lang == 'ko_KR' else 'ARTMOTION_VOICE_EN')
    if env:
        return env
    have = voices().get(lang, [])
    for name in PREFER[lang]:
        if name in have:
            return name
    if have:
        return have[0]
    sys.exit(f'No {lang} system voice installed. Add one in System Settings > Accessibility > Spoken Content.')


def main(argv):
    if '--list' in argv:
        for lang, names in voices().items():
            print(lang, ', '.join(names))
        return 0
    if '--text' not in argv:
        print(__doc__); return 2
    k = argv.index('--text'); text = argv[k + 1]; rest = argv[:k] + argv[k + 2:]
    if '--voice' not in rest:
        rest += ['--voice', pick(text)]
    cmd = [sys.executable, str(ROOT / 'scripts' / 'capabilities.py'), 'say', text, '--mode', 'system', *rest]
    return subprocess.run(cmd).returncode


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
