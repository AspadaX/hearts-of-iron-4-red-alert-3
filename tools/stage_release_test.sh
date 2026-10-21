#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
USER_DIR="${HOI4_USER_DIR:-$HOME/Documents/Paradox Interactive/Hearts of Iron IV}"
GAME_DIR="${HOI4_GAME_DIR:-$HOME/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV}"
RELEASE_DIR=""
VALIDATE=1
FORCE=0
REMOVE=0

die() {
    printf 'error: %s\n' "$*" >&2
    exit 1
}

expand_path() {
    case "$1" in
        "~") printf '%s\n' "$HOME" ;;
        "~/"*) printf '%s/%s\n' "$HOME" "${1#\~/}" ;;
        *) printf '%s\n' "$1" ;;
    esac
}

usage() {
    cat <<'EOF'
Usage: tools/stage_release_test.sh --release-dir PATH [options]

Copy a prepared release folder into a separate local mod named
"Red Alert 3 - Release Test". The development mod is never modified.

Options:
  --release-dir PATH  Prepared release folder (required unless --remove)
  --user-dir PATH     HOI4 user data (default: HOI4_USER_DIR or Documents path)
  --game-dir PATH     HOI4 installation (default: HOI4_GAME_DIR or the Steam path)
  --no-validate       Skip installed validation after staging
  --force             Replace an existing test build and launcher entry
  --remove            Remove the staged test build and launcher entry
  -h, --help          Show this help
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --release-dir)
            [[ $# -ge 2 ]] || die "--release-dir requires a path"
            RELEASE_DIR="$2"
            shift 2
            ;;
        --user-dir)
            [[ $# -ge 2 ]] || die "--user-dir requires a path"
            USER_DIR="$2"
            shift 2
            ;;
        --game-dir)
            [[ $# -ge 2 ]] || die "--game-dir requires a path"
            GAME_DIR="$2"
            shift 2
            ;;
        --no-validate)
            VALIDATE=0
            shift
            ;;
        --force)
            FORCE=1
            shift
            ;;
        --remove)
            REMOVE=1
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

USER_DIR="$(expand_path "$USER_DIR")"
GAME_DIR="$(expand_path "$GAME_DIR")"
MODS="$USER_DIR/mod"
TEST="$MODS/red_alert_3_release_test"
ENTRY="$MODS/red_alert_3_release_test.mod"
MARKER="$TEST/.release-test-source"

if [[ $REMOVE -eq 1 ]]; then
    if [[ -L "$TEST" ]]; then
        die "test path is a symlink; refusing to remove it: $TEST"
    fi
    if [[ -e "$TEST" ]]; then
        [[ -f "$MARKER" ]] || die "refusing to remove unmarked directory: $TEST"
        [[ "$(cat "$MARKER")" == "$ROOT" ]] || die "test build belongs to another source: $TEST"
        rm -rf -- "$TEST"
    fi
    if [[ -e "$ENTRY" || -L "$ENTRY" ]]; then
        rm -f -- "$ENTRY"
    fi
    printf 'Removed Red Alert 3 - Release Test from %s\n' "$MODS"
    exit 0
fi

[[ -n "$RELEASE_DIR" ]] || die "--release-dir is required (use --help)"
RELEASE_DIR="$(expand_path "$RELEASE_DIR")"
[[ -d "$RELEASE_DIR" ]] || die "release folder not found: $RELEASE_DIR"
[[ -f "$RELEASE_DIR/descriptor.mod" ]] || die "release descriptor not found: $RELEASE_DIR/descriptor.mod"

if [[ -L "$TEST" ]]; then
    die "test path is a symlink; refusing to replace it: $TEST"
fi

if [[ -e "$TEST" ]]; then
    [[ -f "$MARKER" ]] || die "refusing to replace unmarked directory: $TEST"
    [[ "$(cat "$MARKER")" == "$ROOT" ]] || die "test build belongs to another source: $TEST"
fi

if [[ $FORCE -eq 0 ]]; then
    if [[ -e "$TEST" || -L "$TEST" ]]; then
        die "release test is already staged; pass --force to replace it"
    fi
    if [[ -e "$ENTRY" || -L "$ENTRY" ]]; then
        die "launcher entry already exists; pass --force to replace it"
    fi
fi

[[ -d "$USER_DIR" ]] || die "HOI4 user directory not found: $USER_DIR"
command -v rsync >/dev/null 2>&1 || die "rsync is required"

mkdir -p "$MODS"
STAGE="$(mktemp -d "$MODS/.red_alert_3_release_test.XXXXXX")"
BACKUP=""

cleanup() {
    if [[ -n "$STAGE" && -d "$STAGE" ]]; then
        rm -rf -- "$STAGE"
    fi
    if [[ -n "$BACKUP" && -d "$BACKUP" ]]; then
        if [[ ! -e "$TEST" && -e "$BACKUP/red_alert_3_release_test" ]]; then
            mv -- "$BACKUP/red_alert_3_release_test" "$TEST"
        fi
        if [[ ! -e "$ENTRY" && -e "$BACKUP/red_alert_3_release_test.mod" ]]; then
            cp -p "$BACKUP/red_alert_3_release_test.mod" "$ENTRY"
        fi
    fi
}
trap cleanup EXIT

rsync -a --exclude 'descriptor.mod' --exclude '.DS_Store' "$RELEASE_DIR/" "$STAGE/"

METADATA="$(sed -E '/^[[:space:]]*(remote_file_id|path|archive)[[:space:]]*=/d; s/^name[[:space:]]*=.*/name="Red Alert 3 - Release Test"/' "$RELEASE_DIR/descriptor.mod")"
grep -q '^name[[:space:]]*=[[:space:]]*"Red Alert 3 - Release Test"' <<<"$METADATA" || die "could not rename the release descriptor"
printf '%s\n' "$METADATA" >"$STAGE/descriptor.mod"
printf '%s\n' "$ROOT" >"$STAGE/.release-test-source"

if [[ -e "$TEST" || -e "$ENTRY" ]]; then
    BACKUP="$USER_DIR/release_test_backups/$(date +%Y%m%d-%H%M%S)-$$"
    mkdir -p "$BACKUP"
    for log in system.log game.log error.log setup.log; do
        if [[ -f "$USER_DIR/logs/$log" ]]; then
            cp -p "$USER_DIR/logs/$log" "$BACKUP/$log"
        fi
    done
    if [[ -e "$ENTRY" ]]; then
        cp -p "$ENTRY" "$BACKUP/"
    fi
    if [[ -e "$TEST" ]]; then
        mv -- "$TEST" "$BACKUP/red_alert_3_release_test"
    fi
fi

mv -- "$STAGE" "$TEST"
STAGE=""
printf '%s\npath="%s"\n' "$METADATA" "$TEST" >"$ENTRY"

if [[ $VALIDATE -eq 1 ]]; then
    [[ -d "$GAME_DIR/history/countries" ]] || die "HOI4 installation not found: $GAME_DIR"
    python3 "$ROOT/tools/validate_eor.py" --installed "$TEST" --game-dir "$GAME_DIR"
fi

printf '\nStaged Red Alert 3 - Release Test\n'
printf 'Release: %s\n' "$RELEASE_DIR"
printf 'Launcher entry: %s\n' "$ENTRY"
if [[ -n "$BACKUP" ]]; then
    printf 'Previous test build and logs: %s\n' "$BACKUP"
fi
printf 'Restart HOI4, enable Red Alert 3 - Release Test, and start a new non-Ironman campaign.\n'
