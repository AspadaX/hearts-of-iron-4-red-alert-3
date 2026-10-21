#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GAME_DIR="${HOI4_GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV}"
OUTPUT="$ROOT/dist"
ZIP=0
FORCE=0
ALLOW_DIRTY=0

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

usage() {
    cat <<'EOF'
Usage: tools/prepare_release.sh [options]

Build a clean Red Alert 3 release folder from this checkout. The prepared
folder can be staged with tools/stage_release_test.sh.

Options:
  --game-dir PATH   HOI4 installation (default: HOI4_GAME_DIR or the Steam path)
  --output PATH     Output directory (default: <repo>/dist)
  --zip             Also write the release archive next to the folder
  --allow-dirty     Build from an uncommitted worktree; recorded in the manifest
  --force           Replace an existing release folder and archive
  -h, --help        Show this help

This does not upload anything to Steam Workshop.
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --game-dir)
            [[ $# -ge 2 ]] || die "--game-dir requires a path"
            GAME_DIR="$2"
            shift 2
            ;;
        --output)
            [[ $# -ge 2 ]] || die "--output requires a path"
            OUTPUT="$2"
            shift 2
            ;;
        --zip)
            ZIP=1
            shift
            ;;
        --allow-dirty)
            ALLOW_DIRTY=1
            shift
            ;;
        --force)
            FORCE=1
            shift
            ;;
        -h | --help)
            usage
            exit 0
            ;;
        *)
            die "unknown argument: $1 (use --help)"
            ;;
    esac
done

case "$GAME_DIR" in
    "~") GAME_DIR="$HOME" ;;
    "~/"*) GAME_DIR="$HOME/${GAME_DIR#\~/}" ;;
esac

[[ -d "$GAME_DIR/history/countries" ]] || die "HOI4 installation not found: $GAME_DIR"
[[ -f "$ROOT/descriptor.mod" ]] || die "descriptor.mod is missing from the repository"

python3 -m py_compile "$ROOT/tools/release_build.py" "$ROOT/tools/history_compat.py" "$ROOT/tools/event_compat.py"

printf 'Checking source content...\n'
python3 "$ROOT/tools/validate_eor.py" --source-only
python3 "$ROOT/tools/test_eor_audit.py"

BUILD_ARGS=(
    --game-dir "$GAME_DIR"
    --output "$OUTPUT"
)

if [[ $ZIP -eq 1 ]]; then
    BUILD_ARGS+=(--zip)
fi

if [[ $FORCE -eq 1 ]]; then
    BUILD_ARGS+=(--force)
fi

if [[ $ALLOW_DIRTY -eq 1 ]]; then
    BUILD_ARGS+=(--allow-dirty)
fi

python3 "$ROOT/tools/release_build.py" "${BUILD_ARGS[@]}"
