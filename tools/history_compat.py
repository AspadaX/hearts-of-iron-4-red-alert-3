#!/usr/bin/env python3
"""Generate country-history compatibility for the RA3 2008 scenario.

Keep initial country setup. Restrict dated 1936-1999 updates to pre-2000
campaigns so vanilla 1939 focus/decision completions cannot replay in RA3.
Source history files are not rewritten by this staging operation.
"""
from pathlib import Path
import json
import re
import runpy


def apply_history_compatibility(root, game, stage):
    helpers = runpy.run_path(str(root / 'tools/port_119.py'), run_name='history_compat_helpers')
    tokens = helpers['TOKENS']
    paths = {p.name: p for p in (game / 'history/countries').glob('*.txt')}
    paths.update({p.name: p for p in (stage / 'history/countries').glob('*.txt')})
    updated = {}
    pattern = re.compile(r'(?m)^[ \t]*(\d{4}\.\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\s*=\s*\{')
    for name, path in paths.items():
        text = path.read_text(encoding='utf-8-sig', errors='replace')
        changes = []
        for match in reversed(list(pattern.finditer(text))):
            date = tuple(map(int, match[1].split('.')))
            if not ((1936, 1, 1, 12) < date + (0,) * (4-len(date)) < (2000, 1, 1, 0)):
                continue
            opening = match.end()-1
            depth = 0
            for token in tokens.finditer(text, opening):
                if token[0] == '{':
                    depth += 1
                elif token[0] == '}':
                    depth -= 1
                    if depth == 0:
                        end = token.end()
                        break
            else:
                raise ValueError('Unclosed dated history block: ' + name + ':' + match[1])
            inside = text[opening+1:end-1]
            label = json.dumps('RA3_HISTORY_COMPAT SKIPPED ' + name + ':' + match[1])
            wrapped = '\n\tif = {\n\t\tlimit = { date < 2000.1.1 }\n' + inside + '\n\t}\n\telse = {\n\t\tlog = ' + label + '\n\t}\n'
            text = text[:opening+1] + wrapped + text[end-1:]
            changes.append(match[1])
        if changes:
            (stage / 'history/countries' / name).write_text(text)
            updated[name] = list(reversed(changes))
    manifest = {'guarded_files': len(updated), 'guarded_dated_blocks': sum(map(len, updated.values())), 'history_cutoff': '2000.1.1', 'files': updated}
    (stage / '.history-compatibility.json').write_text(json.dumps(manifest, indent=2)+'\n')
    return manifest
