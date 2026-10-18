#!/usr/bin/env python3
"""Add reversible startup tracing to the installed development copy only.

Run setup_local.py first. Source content and Workshop metadata are unchanged.
The next setup_local.py synchronization removes this diagnostic overlay.
"""
from pathlib import Path
import json
import re
import runpy

root = Path(__file__).resolve().parents[1]
user = Path.home() / 'Documents/Paradox Interactive/Hearts of Iron IV'
game = Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV'
dev = user / 'mod/red_alert_3_development'
assert (dev / '.development-source').read_text().strip() == str(root)
assert not (dev / '.startup-tracing.json').exists(), 'Run setup_local.py before adding tracing again'
helpers = runpy.run_path(str(root / 'tools/port_119.py'), run_name='trace_helpers')
tokens = helpers['TOKENS']

def end_of_block(text, opening):
    depth = 0
    for token in tokens.finditer(text, opening):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return token.end()
    raise ValueError('Unclosed block while adding diagnostic logging')

country_paths = {p.name: p for p in (game / 'history/countries').glob('*.txt')}
country_paths.update({p.name: p for p in (dev / 'history/countries').glob('*.txt')})
for name, path in country_paths.items():
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    prefix = 'log = ' + json.dumps('RA3_HISTORY BEGIN ' + name) + '\n'
    suffix = '\nlog = ' + json.dumps('RA3_HISTORY END ' + name) + '\n'
    (dev / 'history/countries' / name).write_text(prefix + text + suffix)
action_paths = {p.name: p for p in (game / 'common/on_actions').glob('*.txt')}
action_paths.update({p.name: p for p in (dev / 'common/on_actions').glob('*.txt')})
startup_count = 0
traced_actions = []
for name, path in action_paths.items():
    text = path.read_text(encoding='utf-8-sig', errors='replace')
    matches = list(re.finditer(r'(?m)^[ \t]*on_startup\s*=\s*\{', text))
    if not matches:
        continue
    for index, match in reversed(list(enumerate(matches))):
        opening = match.end()-1
        end = end_of_block(text, opening)
        inside = text[opening+1:end-1]
        effect = re.search(r'(?m)^[ \t]*effect\s*=\s*\{', inside)
        if effect is None:
            raise ValueError('No effect block for startup tracing: ' + name)
        eopen = effect.end()-1
        eend = end_of_block(inside,eopen)
        label = name + ':' + str(index+1)
        begin_log = '\n\t\t\tlog = ' + json.dumps('RA3_STARTUP BEGIN ' + label) + '\n'
        end_log = '\n\t\t\tlog = ' + json.dumps('RA3_STARTUP END ' + label) + '\n'
        inside = inside[:eopen+1]+begin_log+inside[eopen+1:eend-1]+end_log+inside[eend-1:]
        text = text[:opening+1]+inside+text[end-1:]
        startup_count += 1
    (dev / 'common/on_actions' / name).write_text(text)
    traced_actions.append(name)
manifest = {'country_histories':len(country_paths),'startup_blocks':startup_count,'action_files':traced_actions,'removal':'Run tools/setup_local.py to rebuild without diagnostic logging.'}
(dev / '.startup-tracing.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Diagnostic country histories:',len(country_paths))
print('Diagnostic startup blocks:',startup_count)
print('Source gameplay scripts unchanged by tracing; logging exists only in the installed development copy.')
