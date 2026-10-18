#!/usr/bin/env python3
"""Trace event execution and daily ticks in the installed development copy.

Changes logging only. Re-running setup_local.py removes this overlay.
"""
from pathlib import Path
import json
import runpy

root = Path(__file__).resolve().parents[1]
user = Path.home() / 'Documents/Paradox Interactive/Hearts of Iron IV'
dev = user / 'mod/red_alert_3_development'
assert (dev / '.development-source').read_text().strip() == str(root)
assert not (dev / '.runtime-tracing.json').exists(), 'Rebuild with setup_local.py before adding tracing again'
helpers = runpy.run_path(str(root / 'tools/event_compat.py'),run_name='runtime_trace_helpers')
traced_events = 0
traced_options = 0
for path in (dev / 'events').glob('*.txt'):
    text = path.read_text(encoding='utf-8-sig')
    for event_id, original in helpers['definitions'](text).items():
        tokens,pairs = helpers['lex'](original)
        root_open = next(i for i,t in enumerate(tokens) if t[0] == '{')
        insertions = []
        immediate = None
        depth = 0
        for i,token in enumerate(tokens[:-2]):
            if token[0] == '{':
                depth += 1
            elif token[0] == '}':
                depth -= 1
            if token[0] == 'immediate' and depth == 1 and tokens[i+1][0] == '=' and tokens[i+2][0] == '{':
                immediate = i+2
            if token[0] == 'option' and depth == 1 and tokens[i+1][0] == '=' and tokens[i+2][0] == '{':
                opening = i+2
                end = pairs[opening]
                name = 'unnamed'
                for j in range(opening+1,end-2):
                    if tokens[j][0] == 'name' and tokens[j+1][0] == '=':
                        name = helpers['value'](tokens[j+2])
                        break
                label = event_id + ' option ' + name
                insertions.append((tokens[opening].end(),'\n        log = '+json.dumps('RA3_RUNTIME BEGIN '+label)+'\n'))
                insertions.append((tokens[end].start(),'\n        log = '+json.dumps('RA3_RUNTIME END '+label)+'\n'))
                traced_options += 1
        label = event_id + ' immediate'
        if immediate is not None:
            insertions.append((tokens[immediate].end(),'\n        log = '+json.dumps('RA3_RUNTIME BEGIN '+label)+'\n'))
            insertions.append((tokens[pairs[immediate]].start(),'\n        log = '+json.dumps('RA3_RUNTIME END '+label)+'\n'))
        else:
            insertions.append((tokens[root_open].end(),'\n    immediate = {\n        log = '+json.dumps('RA3_RUNTIME BEGIN '+label)+'\n        log = '+json.dumps('RA3_RUNTIME END '+label)+'\n    }\n'))
        modified = original
        for at,insert in sorted(insertions,reverse=True):
            modified = modified[:at]+insert+modified[at:]
        helpers['lex'](modified)
        text = text.replace(original,modified,1)
        traced_events += 1
    path.write_text(text)
heartbeat = dev / 'common/on_actions/zzzz_ra3_runtime_trace.txt'
heartbeat.write_text('on_actions = { on_daily = { effect = { log = "RA3_RUNTIME DAILY TICK" } } }\n')
manifest = {'events':traced_events,'options':traced_options,'daily_tick_logging':True,'removal':'Run tools/setup_local.py. No gameplay effects were changed by this overlay.'}
(dev / '.runtime-tracing.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('Runtime tracing installed:',traced_events,'events,',traced_options,'options, and daily heartbeat.')
