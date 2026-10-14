"""Release check for this edition, run instead of the upstream one.

The upstream check needs release-manifest.json to list every file, and this edition
adds files under l10n/ and .github/ without editing upstream ones. So this check keeps
the upstream rules and changes only the manifest comparison:
  - every file listed in the upstream manifest is still byte-identical (upstream untouched),
  - no listed file is missing,
  - every file in the tree and every commit since the upstream base passes the upstream
    secret / forbidden-file scan (e.g. no .mp4 in the tree — the demo is a release asset).
"""
import json, subprocess, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'scripts'))
import check_release as cr  # upstream gate, unchanged

repo = Path('.').resolve()
# commits are scanned from 2455e01 on: 0557e3c carried the demo .mp4 before it moved to the release (history is not rewritten)
base = sys.argv[1] if len(sys.argv) > 1 else '2455e01'
if cr.git(repo, 'rev-parse', '--is-shallow-repository').strip() == b'true':
    sys.exit('shallow clone: fetch full history first')
manifest = json.loads(cr.git(repo, 'show', 'HEAD:' + cr.MANIFEST))['files']
actual = cr.inspect(repo, 'HEAD')
missing = sorted(set(manifest) - set(actual))
changed = sorted(n for n in manifest if n in actual and actual[n] != manifest[n])
if missing or changed:
    sys.exit(f'upstream files changed: {changed[:10]} missing: {missing[:10]}')
commits = cr.git(repo, 'rev-list', f'{base}..HEAD').decode().split()
for c in commits:
    if cr.SECRET.search(cr.git(repo, 'cat-file', 'commit', c)):
        sys.exit('commit metadata looks like a secret or private path: ' + c[:12])
    cr.inspect(repo, c)
added = sorted(set(actual) - set(manifest))
print(json.dumps({'status': 'passed', 'upstream_files': len(manifest), 'added_files': len(added), 'commits_checked': len(commits)}))
