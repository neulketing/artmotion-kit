#!/bin/sh
# ArtMotion Kit: switch this checkout to Korean (ko) or US English (en) output.
#   l10n/apply.sh ko        Hangul fonts + 3 small engine patches + Korean SKILL.md
#   l10n/apply.sh en        same engine changes + English SKILL.md
#   l10n/apply.sh --revert  back to the untouched upstream files (run this before `git pull`)
set -eu
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
FONTS=scripts/engine/lib/fonts

if [ "${1:-}" = "--revert" ]; then
  for p in l10n/patches/*.patch; do git apply -R --check "$p" 2>/dev/null && git apply -R "$p"; done
  for f in l10n/fonts/*.woff; do rm -f "$FONTS/$(basename "$f")"; done
  [ -f l10n/.SKILL.upstream.md ] && mv l10n/.SKILL.upstream.md SKILL.md
  echo "reverted"; exit 0
fi

LANG_CODE=${1:-}
case "$LANG_CODE" in ko|en) ;; *) echo "usage: l10n/apply.sh ko|en|--revert" >&2; exit 2 ;; esac

cp l10n/fonts/*.woff "$FONTS/"
for p in l10n/patches/*.patch; do
  if git apply -R --check "$p" 2>/dev/null; then echo "already applied: $(basename "$p")"
  else git apply "$p" && echo "applied: $(basename "$p")"; fi
done
[ -f l10n/.SKILL.upstream.md ] || cp SKILL.md l10n/.SKILL.upstream.md
cp "l10n/SKILL.$LANG_CODE.md" SKILL.md
echo "ArtMotion Kit ($LANG_CODE) ready. Restart your agent so it reloads SKILL.md."
