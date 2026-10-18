# Repository working agreement

## Roles and decisions

- The user owns game design: lore, countries, borders, leaders, ideologies, focus trees, events, choices, and intended outcomes.
- The agent owns technical implementation: HOI4 scripting, compatibility, localization wiring, asset integration, debugging, validation, local build preparation, and release preparation.
- Work in manageable batches, usually one country, focus branch, event chain, or compatibility issue. Rough notes and diagrams are valid design input; the user does not need to supply script IDs or code.
- Preserve the user's intended behavior. Ask about meaningful missing design choices; proceed independently with routine technical work. Label provisional balance values and assumptions instead of treating them as approved design.
- Explain engine limitations and workable alternatives. Do not silently replace a design with a different mechanic.

## How we coordinate and test

- The user explicitly asked the agent to stop computer use. Do not control Steam, the launcher, the game, or the desktop, and do not launch the game, unless the user later explicitly changes this instruction.
- The agent reads and edits files, prepares builds, and inspects logs. The user launches HOI4 and reports what happens.
- After preparing a build, give a short, concrete test: which playset/country, whether a new campaign is required, what to try, and the expected result.
- On a crash, inspect the latest logs and crash report before proposing another patch. Distinguish the last logged operation from a proven crash cause. Preserve the evidence before another launch overwrites it.
- Report what changed, relevant checks, and what still needs runtime confirmation. Static validation is not proof of successful loading, political stability, or campaign balance.
- Keep this file and README.md current when the workflow or accepted design changes.

## Source, development build, and commands

The repository is the source of truth. The installed development copy is generated; make lasting fixes in repository content or build tools, not only in that copy.

Run from the repository root:

```sh
python3 tools/setup_local.py
```

This synchronizes real content directories, prepares country-history compatibility, filters excluded event references, and registers **Red Alert 3 - Development**. Re-run after content changes. Do not use linked content folders: the initial symlink-based setup appeared enabled but loaded vanilla content.

Defaults on this Mac:

- Game: `~/Library/Application Support/Steam/steamapps/common/Hearts of Iron IV`
- User data: `~/Documents/Paradox Interactive/Hearts of Iron IV`
- Development content: `<user data>/mod/red_alert_3_development/`
- Launcher entry: `<user data>/mod/red_alert_3_development.mod`
- Playset: **Red Alert 3 Development**, with only the local development mod enabled.

`setup_local.py` accepts `--game-dir` and `--user-dir`. Each refresh backs up the preceding development build and available logs under `<user data>/development_backups/`.

For a loading crash, prepare diagnostic logging after synchronization:

```sh
python3 tools/trace_startup.py
```

Tracing modifies only the installed development copy. It adds country-history and startup BEGIN/END markers to `game.log`. A subsequent synchronization removes the tracing overlay. Do not publish a diagnostic build.

Build tools:

- `tools/setup_local.py`: local registration, synchronization, and compatibility passes.
- `tools/history_compat.py`: guards inherited dated history after the 1936 baseline and before 2000 during build preparation. Preserve this recovery mechanism unless a tested replacement is implemented.
- `tools/event_compat.py`: retains the active event catalog and removes excluded event scheduling from inherited `common/` and `history/` scripts.
- `tools/trace_startup.py`: reversible development-only tracing.
- `tools/port_119.py`: one-time map/settings migration. **Do not rerun it** to refresh a build; it refuses to overwrite its archive to protect subsequent design work.

Generated `.history-compatibility.json`, `.event-compatibility.json`, and `.startup-tracing.json` describe the installed build. They are diagnostic/build metadata, not authored gameplay designs.

## Accepted scenario decisions

- Current scenario starts on **2008-01-01** and ends in 2050. Do not change the timeline without a design request.
- The Empire of the Rising Sun uses **EOR**. **JAP** is an unused legacy tag and must not spawn a second vanilla Japanese military or run its WWII scenario setup.
- Japanese-held areas within China should belong to China (**CHI**). Do not infer new border changes beyond the user's instructions.
- Vladivostok, state **408**, belongs to the Soviet Union (**SOV**) and is a Soviet core. Other Soviet Far East territory must not become Chinese through inherited setup.
- Rising Sun forces start inside EOR borders. Dedicated `EOR_2008` army, navy, and air files preserve forces while correcting foreign deployments. Validate land province locations and naval/air bases against the effective state map.
- SOV starts communist with the authored support distribution: communism 95, fascism 3, democracy 2, neutrality 0. EOR starts fascist with fascism 100 and other support 0. Both have elections disabled and leaders valid beyond the scenario end.
- Use modern `set_popularities`, separate from `set_politics`. Do not restore obsolete nested `parties` syntax.
- `common/on_actions/zz_ra3_scenario_setup.txt` applies the start once, guarded by `ra3_scenario_setup_complete`. Do not enforce governments or borders every day: that would overwrite later player choices, wars, and designed events.

## Event policy

The user requested removal of vanilla historical events.

- Preserve `replace_path="events"` in the release descriptor and generated development descriptors. Base-game and DLC historical event directories must not merge back in.
- Preserve custom USA (`usa2`), Soviet (`ussr`), European (`aoe`), African (`ra3_africa`), and RA3 news chains.
- The functional alliance-invitation exchange `generic.5`, `.6`, `.7` and faction announcement `news.289` are retained because the Empire's China-cooperation focus depends on them. They are the current explicit mechanical exception, not permission to restore historical chains.
- Custom announcements currently use `news.400`, `.401`, `.403`, `.404`, and `.405`. The European militarization events reference `.400` and `.401`.
- Adding or changing events requires checking both definitions and callers. Retained chains must resolve; excluded events must not remain in direct calls, event pools, or inherited scheduling hooks.
- The current catalog has 30 events. This is a snapshot, not a limit on future user-designed content.

## Compatibility and validation

- The installed development target is **HOI4 1.19.3**. The source descriptor still declares `supported_version="1.16.0"`; this is stale metadata, not evidence of compatibility. Update release compatibility metadata only after the relevant verification.
- Keep engine settings additive in `common/defines/ra3_defines.lua`. Do not restore the archived full `00_defines.lua` or `00_graphics.lua`; they removed required modern defaults.
- Preserve current research-interface widgets and modern sprite definitions. Extra RA3/legacy sprites live in `interface/ra3_technologies.gfx`; do not restore the obsolete full `Technologies.gfx` override.
- Loading backgrounds are explicitly registered in `common/frontend/backgrounds/base_backgrounds.txt` using the existing RA3 images.
- The engine merges state files by filename. Check the effective vanilla-plus-mod map for unique state IDs, unique province assignments, complete coverage, valid victory-point/building locations, and intended ownership.
- Modern split states inherited unambiguous RA3 owners. Some retain modern vanilla economic data and still need balance review; do not describe the migration as balanced or complete.
- Check script structure and references, relevant deployment/political invariants, and synchronization of the actual installed build. Use focused checks appropriate to the change; do not add redundant tests or install tooling unnecessarily.

Useful evidence under the user-data directory:

- `logs/error.log`, `logs/game.log`, `logs/setup.log`, `logs/system.log`
- `crashes/<latest>/exception.txt` and `meta.yml`

Testing requires a full restart. Use a **new non-Ironman campaign** for changes to initial borders, deployments, governments, or event isolation; old saves retain prior state and may contain queued historical events.

User-confirmed runtime baseline: the mod loads, USA/Soviet/Rising Sun campaigns can start, and time advances. An earlier event-isolated run ended in a high-speed simulation crash; the last log entry is `2008.03.02.14` and the crash signal is SIGSEGV. The user reported that the latest retry did not crash; its duration and speed were not specified. Maximum speed is not a proven cause. Border and government correctness have not yet been explicitly reconfirmed. Long-running campaign stability remains unverified. A pre-crash autosave and logs are preserved under `<user data>/development_backups/runtime_hoi4_20261018_202526/`. Use `tools/trace_runtime.py` for reversible event/option and daily-tick logging when replaying the failure; never publish that overlay.

## Archives, Git, and publishing

- Preserve `archive/compatibility_1_19/`, `archive/scenario_start_fixes_2008/`, and `archive/vanilla_event_removal/` as recovery/reference material. They must remain outside loaded content and release packages.
- Do not edit the base-game installation or the subscribed Workshop download to implement mod changes.
- Work remains local unless the user requests a commit, push, or release. Do not run `cchain_auto_git.json` as a routine task: it stages everything, commits, and pushes.
- The existing Workshop item is **1722615953**. Preserve that release identity; generated development descriptors intentionally omit the Workshop ID.
- Publishing is separate from local synchronization and Git operations. Obtain an explicit release instruction before uploading or changing the live Workshop item.
- Prepare a clean release with all required compatibility transformations applied. Do not upload the raw checkout: exclude Git data, tools, archives, development descriptors, backups, diagnostic overlays, and trace markers.
- Test the prepared release locally, update the existing item through the owning Steam account, and then test the downloaded Workshop build.
- Follow actual environment permissions for writes. Explain required sandbox escalation briefly; do not use GUI tools to bypass a filesystem restriction.
