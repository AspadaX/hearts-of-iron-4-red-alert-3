#!/usr/bin/env python3
"""Synchronize this checkout into an isolated local HOI4 development mod.

Run after source edits and before restarting the game. Content is copied into
real directories because linked folders were skipped during the first test.
"""
from pathlib import Path
import argparse
from datetime import datetime
import re
import runpy
import shutil
import tempfile


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--user-dir', type=Path, default=Path.home() / 'Documents/Paradox Interactive/Hearts of Iron IV')
    parser.add_argument('--game-dir', type=Path, default=Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    user = args.user_dir.expanduser().resolve()
    if not user.is_dir():
        parser.error('HOI4 user directory does not exist; specify --user-dir')
    game = args.game_dir.expanduser().resolve()
    if not (game / 'history/countries').is_dir():
        parser.error('HOI4 installation not found; specify --game-dir')
    mods = user / 'mod'
    dev = mods / 'red_alert_3_development'
    marker = dev / '.development-source'
    entry = mods / 'red_alert_3_development.mod'
    if dev.is_symlink():
        parser.error('Development root is a link; refusing to overwrite')
    if dev.exists() and (not marker.is_file() or marker.read_text().strip() != str(root)):
        parser.error('Development directory belongs to another source; refusing to overwrite')
    if entry.exists() and not marker.is_file():
        parser.error('Development launcher entry already exists; refusing to overwrite')
    metadata = (root / 'descriptor.mod').read_text(encoding='utf-8-sig')
    metadata = re.sub(r'^\s*(?:remote_file_id|path|archive)\s*=.*$', '', metadata, flags=re.M)
    metadata = re.sub(r'^name\s*=.*$', 'name="Red Alert 3 - Development"', metadata, flags=re.M).strip() + '\n'
    folders = ('common', 'events', 'gfx', 'history', 'interface', 'localisation', 'music', 'sound', 'map', 'portraits', 'tutorial')
    mods.mkdir(parents=True, exist_ok=True)
    stage = Path(tempfile.mkdtemp(prefix='.red_alert_3_sync_', dir=mods))
    backup = None
    try:
        for folder in folders:
            source = root / folder
            if source.is_dir():
                shutil.copytree(source, stage / folder, symlinks=False, ignore=shutil.ignore_patterns('.DS_Store', '__pycache__'))
        compat = runpy.run_path(str(root / 'tools/history_compat.py'), run_name='stage_history_compat')
        history_report = compat['apply_history_compatibility'](root, game, stage)
        event_compat = runpy.run_path(str(root / 'tools/event_compat.py'), run_name='stage_event_compat')
        event_report = event_compat['apply_event_compatibility'](root, game, stage)
        (stage / '.development-source').write_text(str(root) + '\n')
        (stage / 'descriptor.mod').write_text(metadata)
        if dev.exists():
            backup = user / 'development_backups' / datetime.now().strftime('%Y%m%d-%H%M%S-%f')
            backup.mkdir(parents=True)
            for name in ('system.log', 'game.log', 'error.log', 'setup.log'):
                source = user / 'logs' / name
                if source.is_file():
                    shutil.copy2(source, backup / name)
            if entry.exists():
                shutil.copy2(entry, backup / entry.name)
            dev.rename(backup / dev.name)
        try:
            stage.rename(dev)
        except OSError:
            if backup is not None:
                (backup / dev.name).rename(dev)
            raise
        entry.write_text(metadata + f'path="{dev.as_posix()}"\n')
    finally:
        if stage.exists():
            shutil.rmtree(stage)
    print('Synchronized Red Alert 3 - Development into real content directories.')
    print('Pre-2000 dated history guarded:', history_report['guarded_dated_blocks'], 'blocks in', history_report['guarded_files'], 'countries.')
    print('Active events:', event_report['active_event_count'], 'Excluded event references removed:', event_report['removed_event_references'])
    print(f'Source: {root}')
    print(f'Launcher entry: {entry}')
    if backup is not None:
        print(f'Previous development build and logs: {backup}')
    print('Restart HOI4 and start a NEW campaign using the development playset.')
    print('Expected scenario date: 2008.1.1; custom countries include EOR and AOE.')
    print('Compatibility with the installed game still requires in-game testing.')


if __name__ == '__main__':
    main()
