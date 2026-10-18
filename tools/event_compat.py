#!/usr/bin/env python3
"""Keep only the mod event catalog and remove scheduling of excluded events.

The descriptor replaces events/. This build pass removes obsolete event calls
and event-pool entries from inherited common/ and history/ scripts, retaining
the rest of their behavior. Original source scripts are not rewritten.
"""
from pathlib import Path
from collections import Counter
import json
import re

LEX = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=#"]+')
EVENT_TYPES = {'country_event', 'news_event', 'state_event', 'unit_leader_event', 'operative_leader_event'}
EVENT_ID = re.compile(r'^(?:[A-Za-z_]\w*\.)+\d+$')


def lex(text, strict=True):
    tokens = [m for m in LEX.finditer(text) if not m[0].startswith('#')]
    pairs, stack = {}, []
    for i, token in enumerate(tokens):
        if token[0] == '{':
            stack.append(i)
        elif token[0] == '}':
            if not stack:
                if strict:
                    raise ValueError('Unexpected closing brace')
                continue
            start = stack.pop()
            pairs[start] = i
    if stack and strict:
        raise ValueError('Unclosed brace')
    return tokens, pairs


def value(token):
    return token[0].strip('"')


def definitions(text):
    tokens, pairs = lex(text.lstrip('\ufeff'))
    # Re-tokenize the normalized text to preserve offsets.
    text = text.lstrip('\ufeff')
    result = {}
    i = 0
    while i < len(tokens)-2:
        if tokens[i][0] in EVENT_TYPES and tokens[i+1][0] == '=' and tokens[i+2][0] == '{':
            end = pairs[i+2]
            j = i+3
            while j < end:
                if tokens[j][0] == 'id' and tokens[j+1][0] == '=':
                    event_id = value(tokens[j+2])
                    assert event_id not in result, 'Duplicate event ' + event_id
                    result[event_id] = text[tokens[i].start():tokens[end].end()]
                    break
                j = pairs[j]+1 if tokens[j][0] == '{' else j+1
            i = end+1
        elif tokens[i][0] == '{':
            i = pairs[i]+1
        else:
            i += 1
    return result


def filter_calls(text, allowed):
    # Some inherited vanilla files have unmatched outer braces. Preserve those
    # bytes while pairing complete inner event-call blocks for surgical removal.
    tokens, pairs = lex(text, strict=False)
    removals = []
    removed = Counter()
    for i, token in enumerate(tokens[:-2]):
        kind = token[0]
        if tokens[i+1][0] != '=':
            continue
        if kind in EVENT_TYPES:
            j = i+2
            end = pairs[j] if tokens[j][0] == '{' else j
            event_id = None
            if tokens[j][0] == '{':
                k = j+1
                while k < end-1:
                    if tokens[k][0] == 'id' and tokens[k+1][0] == '=':
                        event_id = value(tokens[k+2])
                        break
                    k = pairs[k]+1 if tokens[k][0] == '{' else k+1
            else:
                event_id = value(tokens[j])
            if event_id and (EVENT_ID.fullmatch(event_id) or event_id.isdecimal()) and event_id not in allowed:
                removals.append((token.start(),tokens[end].end()))
                removed[event_id] += 1
        elif kind in {'events','random_events','random_events_in_scope'} and tokens[i+2][0] == '{':
            opening = i+2
            end = pairs[opening]
            for j in range(opening+1,end):
                event_id = value(tokens[j])
                if not EVENT_ID.fullmatch(event_id) or event_id in allowed:
                    continue
                begin, finish = tokens[j].start(),tokens[j].end()
                if j >= opening+3 and tokens[j-1][0] == '=' and re.fullmatch(r'\d+(?:\.\d+)?',tokens[j-2][0]):
                    begin = tokens[j-2].start()
                if j+2 < end and tokens[j+1][0] == '=' and tokens[j+2][0] == '{':
                    finish = tokens[pairs[j+2]].end()
                removals.append((begin,finish))
                removed[event_id] += 1
    merged = []
    for begin,end in sorted(removals):
        if merged and begin <= merged[-1][1]:
            merged[-1] = (merged[-1][0],max(end,merged[-1][1]))
        else:
            merged.append((begin,end))
    for begin,end in reversed(merged):
        text = text[:begin]+text[end:]
    return text, removed


def apply_event_compatibility(root, game, stage):
    allowed = set()
    for path in (stage/'events').glob('*.txt'):
        ids = definitions(path.read_text(encoding='utf-8-sig',errors='replace'))
        assert not allowed.intersection(ids), 'Duplicate active event definitions'
        allowed.update(ids)
    changed = {}
    removed = Counter()
    for folder in ('common','history'):
        paths = {p.relative_to(game/folder):p for p in (game/folder).rglob('*.txt')}
        paths.update({p.relative_to(stage/folder):p for p in (stage/folder).rglob('*.txt')})
        for relative,path in paths.items():
            text = path.read_text(encoding='utf-8-sig',errors='replace')
            if not any(word in text for word in (*EVENT_TYPES,'events =','events=')):
                continue
            try:
                cleaned, denied = filter_calls(text,allowed)
            except ValueError:
                # A malformed inherited file is not silently rewritten by this pass.
                raise ValueError('Cannot safely filter event calls in '+str(path))
            if denied:
                target = stage/folder/relative
                target.parent.mkdir(parents=True,exist_ok=True)
                target.write_text(cleaned)
                changed[(Path(folder)/relative).as_posix()] = sum(denied.values())
                removed.update(denied)
    report = {'active_event_count':len(allowed),'active_events':sorted(allowed),'filtered_script_files':len(changed),'removed_event_references':sum(removed.values()),'excluded_event_ids':dict(sorted(removed.items())),'files':changed}
    (stage/'.event-compatibility.json').write_text(json.dumps(report,indent=2)+'\n')
    return report
