#!/usr/bin/env python3
from pathlib import Path
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
import re
import runpy
import shutil
import subprocess
import sys
import tempfile
import zipfile

CONTENT_FOLDERS = (
    'common',
    'events',
    'gfx',
    'history',
    'interface',
    'localisation',
    'music',
    'sound',
    'map',
    'portraits',
    'tutorial',
)
REQUIRED_FOLDERS = ('common', 'events', 'gfx', 'history', 'interface', 'localisation')
FORBIDDEN_ROOT = (
    '.git',
    'tools',
    'archive',
    'docs',
    'AGENTS.md',
    'README.md',
    'Change Note.txt',
    'cchain_auto_git.json',
    '.development-source',
    '.release-test-source',
    '.history-compatibility.json',
    '.event-compatibility.json',
    '.startup-tracing.json',
    '.runtime-tracing.json',
)
IGNORE_PATTERNS = shutil.ignore_patterns('.DS_Store', '__pycache__', '*.pyc', '*.pyo', '.git')
DEFAULT_GAME = Path.home() / 'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV'


def fail(message):
    raise SystemExit('error: ' + message)


def descriptor_values(text):
    values = {}
    for key in ('version', 'name', 'supported_version', 'remote_file_id'):
        match = re.search(r'(?m)^\s*' + re.escape(key) + r'\s*=\s*"([^"]*)"', text)
        if match:
            values[key] = match.group(1)
    values['replace_paths'] = re.findall(r'(?m)^\s*replace_path\s*=\s*"([^"]+)"', text)
    return values


def git_state(root, allow_dirty):
    inside = subprocess.run(
        ['git', '-C', str(root), 'rev-parse', '--is-inside-work-tree'],
        capture_output=True,
        text=True,
    )
    if inside.returncode != 0:
        fail('release preparation must run from a Git worktree')
    status = subprocess.run(
        ['git', '-C', str(root), 'status', '--porcelain'],
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    dirty = bool(status.strip())
    if dirty and not allow_dirty:
        fail('worktree is dirty; commit the release source or pass --allow-dirty')
    check = subprocess.run(
        ['git', '-C', str(root), '-c', 'core.whitespace=cr-at-eol', 'diff', '--check'],
        capture_output=True,
        text=True,
    )
    if check.returncode != 0:
        fail('git diff --check failed:\n' + (check.stdout + check.stderr).strip())
    commit = subprocess.run(
        ['git', '-C', str(root), 'rev-parse', '--short', 'HEAD'],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    branch = subprocess.run(
        ['git', '-C', str(root), 'rev-parse', '--abbrev-ref', 'HEAD'],
        capture_output=True,
        text=True,
        check=True,
    ).stdout.strip()
    return {'commit': commit, 'branch': branch, 'dirty': dirty}


def checked_descriptor(root):
    path = root / 'descriptor.mod'
    if not path.is_file():
        fail('descriptor.mod is missing')
    text = path.read_text(encoding='utf-8-sig')
    values = descriptor_values(text)
    missing = [key for key in ('version', 'name', 'supported_version', 'remote_file_id') if not values.get(key)]
    if missing:
        fail('descriptor.mod is missing ' + ', '.join(missing))
    if 'events' not in values['replace_paths']:
        fail('descriptor.mod must declare replace_path="events"')
    if re.search(r'(?m)^\s*(?:path|archive)\s*=', text):
        fail('descriptor.mod must not contain path or archive entries')
    if values['name'].strip().lower().endswith('development'):
        fail('descriptor.mod is a development descriptor, not a release descriptor')
    return path, text, values


def checked_game(game):
    game = game.expanduser().resolve()
    if not (game / 'history/countries').is_dir():
        fail('HOI4 installation not found; pass --game-dir')
    return game


def copy_content(root, stage):
    included = []
    for folder in CONTENT_FOLDERS:
        source = root / folder
        if not source.is_dir():
            continue
        shutil.copytree(source, stage / folder, symlinks=False, ignore=IGNORE_PATTERNS)
        included.append(folder)
    missing = [folder for folder in REQUIRED_FOLDERS if folder not in included]
    if missing:
        fail('required content folders are missing: ' + ', '.join(missing))
    return included


def apply_compatibility(root, game, stage):
    history_module = runpy.run_path(str(root / 'tools/history_compat.py'), run_name='release_history_compat')
    history_report = history_module['apply_history_compatibility'](root, game, stage)
    event_module = runpy.run_path(str(root / 'tools/event_compat.py'), run_name='release_event_compat')
    event_report = event_module['apply_event_compatibility'](root, game, stage)
    for name in ('.history-compatibility.json', '.event-compatibility.json'):
        (stage / name).unlink(missing_ok=True)
    return history_report, event_report


def clean_stage(stage):
    for path in sorted(stage.rglob('*'), reverse=True):
        if path.name in ('.DS_Store', '__pycache__') or path.suffix in ('.pyc', '.pyo'):
            if path.is_dir():
                shutil.rmtree(path)
            else:
                path.unlink(missing_ok=True)
    for name in FORBIDDEN_ROOT:
        if (stage / name).exists():
            fail('forbidden release entry: ' + name)
    for path in stage.rglob('*'):
        if path.is_symlink():
            fail('release package contains a symlink: ' + str(path.relative_to(stage)))


def tree_metrics(stage):
    digest = hashlib.sha256()
    count = 0
    size = 0
    for path in sorted(stage.rglob('*')):
        if not path.is_file():
            continue
        relative = path.relative_to(stage).as_posix()
        digest.update(relative.encode('utf-8'))
        digest.update(b'\0')
        with path.open('rb') as handle:
            for chunk in iter(lambda: handle.read(1024 * 1024), b''):
                digest.update(chunk)
                size += len(chunk)
        digest.update(b'\0')
        count += 1
    return {'file_count': count, 'size_bytes': size, 'sha256': digest.hexdigest()}


def zip_package(output, package_name):
    package = output / package_name
    archive = output / (package_name + '.zip')
    temporary = output / ('.' + package_name + '.zip.tmp')
    with zipfile.ZipFile(temporary, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=6, allowZip64=True) as handle:
        for path in sorted(package.rglob('*')):
            if path.is_file():
                handle.write(path, (Path(package_name) / path.relative_to(package)).as_posix())
    os.replace(temporary, archive)
    digest = hashlib.sha256()
    with archive.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return {'path': archive.as_posix(), 'size_bytes': archive.stat().st_size, 'sha256': digest.hexdigest()}


def human_size(value):
    for unit in ('bytes', 'KiB', 'MiB', 'GiB'):
        if value < 1024 or unit == 'GiB':
            return f'{value:.1f} {unit}' if unit != 'bytes' else f'{value} bytes'
        value /= 1024


def checked_output(root, output, folder_names):
    output = output.expanduser().resolve()
    if output == root:
        fail('output directory must not be the repository root')
    protected = [root / name for name in folder_names] + [root / 'tools', root / 'archive', root / '.git']
    for path in protected:
        if output == path or path in output.parents:
            fail('output directory must be outside source content: ' + str(output))
    return output


def build(args):
    root = Path(__file__).resolve().parents[1]
    descriptor_path, descriptor_text, descriptor = checked_descriptor(root)
    git = git_state(root, args.allow_dirty)
    game = checked_game(args.game_dir)
    output_arg = args.output
    if not output_arg.is_absolute():
        output_arg = root / output_arg
    output = checked_output(root, output_arg, CONTENT_FOLDERS)
    output.mkdir(parents=True, exist_ok=True)
    version = re.sub(r'[^A-Za-z0-9._-]+', '_', descriptor['version'])
    package_name = 'red_alert_3-' + version
    package_dir = output / package_name
    manifest_path = output / (package_name + '.manifest.json')
    archive_path = output / (package_name + '.zip')
    if package_dir.exists() and not args.force:
        fail('release folder exists; pass --force to replace ' + str(package_dir))
    stage = Path(tempfile.mkdtemp(prefix='.red_alert_3_release_', dir=output))
    old_package = None
    try:
        included = copy_content(root, stage)
        history_report, event_report = apply_compatibility(root, game, stage)
        shutil.copy2(descriptor_path, stage / 'descriptor.mod')
        clean_stage(stage)
        metrics = tree_metrics(stage)
        if package_dir.exists():
            old_package = output / ('.' + package_name + '.old-' + str(os.getpid()))
            if old_package.exists():
                shutil.rmtree(old_package)
            package_dir.rename(old_package)
        stage.rename(package_dir)
        stage = None
        if old_package is not None:
            shutil.rmtree(old_package)
            old_package = None
        if args.zip:
            archive = zip_package(output, package_name)
        else:
            archive = None
            archive_path.unlink(missing_ok=True)
        manifest = {
            'schema': 1,
            'package': package_name,
            'built_at': datetime.now(timezone.utc).isoformat(),
            'source': root.as_posix(),
            'git': git,
            'descriptor': {
                'name': descriptor['name'],
                'version': descriptor['version'],
                'supported_version': descriptor['supported_version'],
                'remote_file_id': descriptor['remote_file_id'],
                'replace_paths': descriptor['replace_paths'],
            },
            'compatibility': {'history': history_report, 'events': event_report},
            'contents': {'folders': included, **metrics},
            'archive': archive,
        }
        temporary_manifest = output / ('.' + package_name + '.manifest.tmp')
        temporary_manifest.write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
        os.replace(temporary_manifest, manifest_path)
    finally:
        if stage is not None and stage.exists():
            shutil.rmtree(stage)
        if old_package is not None and old_package.exists():
            if not package_dir.exists():
                old_package.rename(package_dir)
            else:
                shutil.rmtree(old_package)
    print('Release package:', package_dir)
    print('Manifest:', manifest_path)
    print('Workshop ID:', descriptor['remote_file_id'])
    print('Version:', descriptor['version'])
    print('Files:', metrics['file_count'], 'Size:', human_size(metrics['size_bytes']))
    if git['dirty']:
        print('WARNING: package built from a dirty worktree.')
    if archive is not None:
        print('Archive:', archive['path'], '(' + human_size(archive['size_bytes']) + ')')
    print('Stage for test:')
    print('  ' + str(root / 'tools/stage_release_test.sh') + ' --release-dir "' + package_dir.as_posix() + '"')
    return 0


def main():
    parser = argparse.ArgumentParser(description='Build a clean Red Alert 3 release package.')
    parser.add_argument('--game-dir', type=Path, default=DEFAULT_GAME)
    parser.add_argument('--output', type=Path, default=Path('dist'))
    parser.add_argument('--allow-dirty', action='store_true')
    parser.add_argument('--force', action='store_true')
    parser.add_argument('--zip', action='store_true')
    args = parser.parse_args()
    return build(args)


if __name__ == '__main__':
    sys.exit(main())
