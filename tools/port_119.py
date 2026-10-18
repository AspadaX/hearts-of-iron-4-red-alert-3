#!/usr/bin/env python3
"""One-time technical port of the legacy map/settings to installed HOI4 1.19.

Preserves originals under archive/compatibility_1_19 and refuses a second run.
No game process is started and no Workshop content is uploaded.
"""
from collections import defaultdict
from pathlib import Path
import json
import re
import shutil

ROOT = Path(__file__).resolve().parents[1]
GAME = Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV'
ARCHIVE = ROOT / 'archive/compatibility_1_19'
TOKENS = re.compile(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]')


def read(path):
    return path.read_text(encoding='utf-8-sig')


def block(text, key, start=0):
    match = re.search(r'(?m)^[ \t]*' + re.escape(key) + r'\s*=\s*\{', text[start:])
    if match is None:
        raise ValueError(f'Missing block {key}')
    begin = start + match.start()
    opening = start + match.end() - 1
    depth = 0
    for token in TOKENS.finditer(text, opening):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return begin, opening, token.end()
    raise ValueError(f'Unclosed block {key}')


def state(text):
    clean = re.sub(r'#[^\n]*', '', text)
    sid = int(re.search(r'\bid\s*=\s*(\d+)', clean)[1])
    _, a, b = block(text, 'provinces')
    provinces = set(map(int, re.findall(r'\d+', re.sub(r'#[^\n]*', '', text[a+1:b-1]))))
    owner = re.search(r'(?m)^[ \t]*owner\s*=\s*(\w+)', clean)[1]
    cores = set(re.findall(r'(?m)^[ \t]*add_core_of\s*=\s*(\w+)', clean))
    return sid, provinces, owner, cores


def validate_world(base, overrides):
    # The engine merges state files by filename, not state ID.
    merged = {p.name: read(p) for p in base.values()}
    merged.update(overrides)
    ids, provinces, owners = {}, {}, {}
    for filename, text in merged.items():
        sid, ps, owner, _ = state(text)
        assert sid not in ids, f'Duplicate state {sid}: {filename}, {ids.get(sid)}'
        ids[sid] = filename
        owners[sid] = owner
        for prov in ps:
            assert prov not in provinces, f'Province {prov} belongs to multiple states'
            provinces[prov] = sid
    expected = {prov for p in base.values() for prov in state(read(p))[1]}
    assert set(provinces) == expected, 'Province coverage differs from installed vanilla map'
    return provinces, owners


def main():
    if ARCHIVE.exists():
        raise SystemExit('Migration archive already exists. Refusing to overwrite later design changes.')
    version = json.loads((GAME / 'launcher-settings.json').read_text())['rawVersion']
    assert version.startswith('1.19.'), f'Expected HOI4 1.19, found {version}'
    original_paths = list((ROOT / 'history/states').glob('*.txt'))
    originals = {state(read(p))[0]: (p, read(p)) for p in original_paths}
    base = {state(read(p))[0]: p for p in (GAME / 'history/states').glob('*.txt')}
    parent_by_province = {}
    original_data = {sid: state(text) for sid, (_, text) in originals.items()}
    for sid, (_, ps, owner, _) in original_data.items():
        for prov in ps:
            assert prov not in parent_by_province, f'Original map has duplicate province {prov}'
            parent_by_province[prov] = sid
    modern_provinces = {prov: sid for sid, p in base.items() for prov in state(read(p))[1]}
    assert set(parent_by_province) <= set(modern_provinces), 'Old provinces missing from modern map'
    outputs, output_by_id = {}, {}
    moved_vps, moved_buildings = defaultdict(list), defaultdict(list)
    inherited, refreshed = [], []
    for sid, path in base.items():
        modern = read(path)
        _, ps, _, _ = state(modern)
        parents = {parent_by_province[p] for p in ps if p in parent_by_province}
        if not parents and sid not in originals:
            continue
        owners = {original_data[parent][2] for parent in parents}
        assert len(owners) <= 1, f'Conflicting old owners for modern state {sid}: {owners}'
        if sid in originals:
            text = originals[sid][1]
            _, old_ps, owner, _ = original_data[sid]
            assert not owners or owners == {owner}, f'Ownership conflict in {sid}'
            _, a, b = block(text, 'provinces')
            _, na, nb = block(modern, 'provinces')
            text = text[:a+1] + modern[na+1:nb-1] + text[b-1:]
            if ps != old_ps:
                refreshed.append(sid)
            # Relocate province-specific data when modern states split an old state.
            for match in reversed(list(re.finditer(r'(?m)^[ \t]*victory_points\s*=\s*\{', text))):
                begin, opening, end = block(text, 'victory_points', match.start())
                numbers = re.findall(r'\d+', re.sub(r'#[^\n]*', '', text[opening+1:end-1]))
                if numbers and int(numbers[0]) not in ps:
                    dest = modern_provinces[int(numbers[0])]
                    moved_vps[dest].append((int(numbers[0]), text[begin:end]))
                    text = text[:begin] + text[end:]
            try:
                _, a, b = block(text, 'buildings')
                building_text = text[a+1:b-1]
                for match in reversed(list(re.finditer(r'(?m)^[ \t]*(\d+)\s*=\s*\{', building_text))):
                    begin, opening, end = block(building_text, match[1], match.start())
                    prov = int(match[1])
                    if prov not in ps:
                        moved_buildings[modern_provinces[prov]].append((prov, building_text[begin:end]))
                        building_text = building_text[:begin] + building_text[end:]
                text = text[:a+1] + building_text + text[b-1:]
            except ValueError as exc:
                if 'Missing block buildings' not in str(exc):
                    raise
        else:
            text = modern
            owner = next(iter(owners))
            # A split state receives the shared cores of its original parent states.
            cores = set.intersection(*(set(original_data[parent][3]) for parent in parents))
            begin, a, b = block(text, 'history')
            history = text[a+1:b-1]
            history = re.sub(r'(?m)^[ \t]*(?:owner|controller|add_core_of|remove_core_of|add_claim_by|remove_claim_by)\s*=\s*\w+[ \t]*(?:#[^\n]*)?(?:\n|$)', '', history)
            political = f'\n\t\towner = {owner}\n' + ''.join(f'\t\tadd_core_of = {core}\n' for core in sorted(cores))
            text = text[:a+1] + political + history + text[b-1:]
            inherited.append(sid)
        output_by_id[sid] = text
    for sid, text in list(output_by_id.items()):
        for prov, record in moved_vps[sid]:
            for match in reversed(list(re.finditer(r'(?m)^[ \t]*victory_points\s*=\s*\{', text))):
                begin, a, b = block(text, 'victory_points', match.start())
                numbers = re.findall(r'\d+', text[a+1:b-1])
                if numbers and int(numbers[0]) == prov:
                    text = text[:begin] + text[b:]
            _, _, end = block(text, 'history')
            text = text[:end-1] + '\n' + record + '\n\t' + text[end-1:]
        for prov, record in moved_buildings[sid]:
            try:
                _, a, b = block(text, 'buildings')
            except ValueError:
                _, _, end = block(text, 'history')
                text = text[:end-1] + '\n\t\tbuildings = {\n\t\t}\n\t' + text[end-1:]
                _, a, b = block(text, 'buildings')
            inner = text[a+1:b-1]
            if re.search(r'(?m)^[ \t]*' + str(prov) + r'\s*=\s*\{', inner):
                begin, _, end = block(inner, str(prov))
                inner = inner[:begin] + inner[end:]
            inner += '\n' + record + '\n\t\t'
            text = text[:a+1] + inner + text[b-1:]
        output_by_id[sid] = text
        outputs[base[sid].name] = text
    world, owners = validate_world(base, outputs)
    for prov, parent in parent_by_province.items():
        assert owners[world[prov]] == original_data[parent][2], f'Changed ownership of province {prov}'
    ARCHIVE.mkdir(parents=True)
    shutil.copytree(ROOT / 'history/states', ARCHIVE / 'history/states')
    for old in (ROOT / 'history/states').iterdir():
        if old.is_dir():
            shutil.rmtree(old)
        else:
            old.unlink()
    for name, text in outputs.items():
        (ROOT / 'history/states' / name).write_text(text)
    for name in ('00_defines.lua', '00_graphics.lua'):
        destination = ARCHIVE / 'common/defines' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.move(ROOT / 'common/defines' / name, destination)
    (ROOT / 'common/defines/ra3_defines.lua').write_text('-- Keep current engine defaults and override only the scenario timeline.\nNDefines.NGame.START_DATE = "2008.1.1.12"\nNDefines.NGame.END_DATE = "2050.1.1.1"\nNDefines.NDiplomacy.TENSION_TIME_SCALE_START_DATE = "2008.1.1.12"\n')
    hooks = 0
    for name in ('armor.txt', 'infantry.txt'):
        path = ROOT / 'common/technologies' / name
        text = read(path)
        source = text
        for match in reversed(list(re.finditer(r'(?m)^([ \t]*)on_research_complete\s*=\s*\{', text))):
            begin, opening, end = block(text, 'on_research_complete', match.start())
            inside = text[opening+1:end-1]
            if not re.match(r'\s*limit\s*=\s*\{', inside):
                continue
            lb, la, le = block(inside, 'limit')
            indent = match[1]
            replacement = indent + 'on_research_complete_limit = {' + inside[la+1:le-1] + '}\n' + indent + 'on_research_complete = {' + inside[:lb] + inside[le:] + '}'
            text = text[:begin] + replacement + text[end:]
            hooks += 1
        destination = ARCHIVE / 'common/technologies' / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(source)
        path.write_text(text)
    path = ROOT / 'common/units/equipment/tsunami_tank_equipment.txt'
    destination = ARCHIVE / 'common/units/equipment' / path.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, destination)
    path.write_text(read(path).replace('archetype = amphibious_tank_equipment', 'archetype = amphibious_tank_chassis'))
    path = ROOT / 'common/national_focus/saf_ideas.txt'
    destination = ARCHIVE / 'common/national_focus' / path.name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(path, destination)
    report = {
        'game_version': version,
        'old_state_overrides': len(originals),
        'ported_state_overrides': len(outputs),
        'state_ids_with_refreshed_province_lists': refreshed,
        'new_states_inheriting_original_ownership': inherited,
        'relocated_victory_point_blocks': sum(map(len, moved_vps.values())),
        'relocated_province_building_blocks': sum(map(len, moved_buildings.values())),
        'validated_land_provinces': len(world),
        'technology_research_hooks_updated': hooks,
        'notes': [
            'Original owners verified for every province covered by the legacy mod.',
            'Original state-level manpower, resources, and buildings retained on original IDs.',
            'New split states retain modern vanilla state-level economic data; balance review remains.',
            'Modern engine and graphics defaults replace legacy full-table overrides; original files archived.',
            'No in-game success claim: manual loading test is still required.'
        ]
    }
    (ARCHIVE / 'migration_report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k: v for k, v in report.items() if not isinstance(v, list)}, indent=2))
    print('Province-list refreshes:', len(refreshed), 'Split-state ownership inherited:', len(inherited))
    print('Original province ownership: preserved. Duplicate states/provinces: zero.')


if __name__ == '__main__':
    main()
