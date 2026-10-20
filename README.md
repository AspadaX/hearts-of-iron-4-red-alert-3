# Red Alert 3 for Hearts of Iron IV

A Red Alert 3 total conversion for Hearts of Iron IV.

## Local development on macOS

Run `python3 tools/setup_local.py` from this checkout. It registers **Red Alert 3 - Development** in the HOI4 user mod directory and copies the game-content folders into real directories for the engine to load. Run this command again after source changes, then fully restart the game. I handle this synchronization during technical work. Each refresh preserves the previous development build and available logs under `development_backups` in the HOI4 user directory. The checkout remains the source of truth. Re-run the command after moving the checkout only after removing its old development registration.

In the Paradox Launcher, create a playset named **Red Alert 3 Development**, add only **Red Alert 3 - Development**, and select that playset before playing. Keep the subscribed Workshop version disabled in this playset.

The development descriptor intentionally has no Workshop ID. The original `descriptor.mod` retains the existing release identity. Local changes and Git commits do not publish Workshop updates.

## Testing

Start a new non-Ironman game after restarting HOI4. First verify that the main menu and country selection load. Confirm the custom scenario begins in **2008** and includes **Empire of the Rising Sun** and the **Allied Nations militarized zone in Europe**, then enter the campaign and advance time. A vanilla 1936 campaign is not proof the mod loaded. Check the focus tree and the changed features. Run longer campaigns before release.

On macOS logs are in `~/Documents/Paradox Interactive/Hearts of Iron IV/logs/`. The most useful files are `error.log`, `game.log`, `setup.log`, and `system.log`. Logs are overwritten on subsequent launches, so preserve logs from a failure before trying again.

The installed game was 1.19.3 when development was resumed. The original mod declares 1.16.0 support; compatibility must be established through fixes and in-game testing before that declaration is updated.

## Publishing

Prepare a clean release folder containing game content and release metadata, excluding development tools and Git data. Test it locally, then use the launcher upload tools with the owning Steam account and verify the existing Workshop item **1722615953** is the update target. Test the downloaded Workshop build after uploading. Publishing is a separate release action.

## Compatibility recovery for HOI4 1.19

The first loaded development build crashed before reaching the main menu. The first repair replaces the legacy full engine/graphics settings with three additive timeline overrides, updates state filenames and province lists against the installed 1.19 map, and gives newly split states their unambiguous original RA3 owner. Province-level victory points and buildings move to their modern state. Original state-level economic values remain on the original state IDs; new split states retain current vanilla economic values and need balance review.

Original map files and changed legacy scripts are preserved under `archive/compatibility_1_19/`, outside the game-content folders. Its `migration_report.json` records the changes. `tools/port_119.py` documents the one-time migration and refuses a second run to protect later design changes. Deprecated technology research conditions, the Tsunami tank archetype reference, a misplaced ideas file, and five unbalanced script files are also repaired.

Static map, script, and Lua validation do not prove the game reaches the menu. A fresh manual loading test is required. Further legacy-content errors remain to be addressed.

## Startup diagnostics

After `python3 tools/setup_local.py`, run `python3 tools/trace_startup.py` when a crash needs startup tracing. This adds BEGIN/END messages for country history and startup hooks to `game.log` in the installed development copy. It does not change source gameplay behavior. Running `setup_local.py` again removes the diagnostic overlay. Diagnostic overlays must not be published.

The technology interface is based on current vanilla widgets with the existing RA3 year labels carried over. Extra legacy/RA3 sprites are defined in `interface/ra3_technologies.gfx` so the modern `Technologies.gfx` database remains available. The background registry explicitly uses the nine existing RA3 loading images.

## Dated history compatibility

The 2008 scenario must not replay vanilla 1939 territorial changes and focus/decision completions. All country initializers completed in the diagnostic test, then the engine crashed during the dated-history pass after Germany activated its Bohemia/Moravia decision. Local build preparation now wraps dated updates after the 1936 baseline and before 2000 in a `date < 2000.1.1` condition. This preserves those updates for earlier scenarios while skipping them during RA3 setup. It does not alter source country history, initial setup, RA3 events, or future-dated content. The development build records guarded blocks in `.history-compatibility.json`. `--game-dir` can specify a different installed HOI4 directory.

## Scenario start corrections

The designer confirmed China should control Japanese-held areas within China, Vladivostok should be Soviet, and the Rising Sun forces should deploy within EOR territory. State 408 is now Soviet. The unused JAP country history no longer spawns a second vanilla Japanese military. EOR uses its own army, navy, and air deployments: foreign land positions and air bases move into EOR territory while unit counts are preserved.

Soviet and EOR party support now uses modern `set_popularities` syntax with their original intended percentages. Their leaders remain valid through the scenario end, and elections remain disabled. A guarded startup hook applies the intended borders and governments once per new campaign, after inherited hooks. It does not reset governments or territorial gains every day. New campaigns are required to test these initialization changes. Original files and the relocation report are under `archive/scenario_start_fixes_2008/`.

## RA3 event isolation

The descriptor replaces the `events` directory so base-game and DLC historical event files are not loaded. The mod keeps its USA, Soviet, European, African, and custom news events. The functional generic faction invitation exchange (`generic.5` through `.7`) and its faction announcement (`news.289`) remain as the explicit mechanical diplomacy exception. These are diplomatic mechanics, not historical story chains.

The local build filters calls and random-event pool entries for excluded events from inherited `common` and `history` scripts. Other effects in those scripts remain. The active event catalog and filtering report are recorded in `.event-compatibility.json` inside the development build. Original event files are preserved under `archive/vanilla_event_removal/`. Start a new campaign so old saves do not retain already queued historical events.

## Runtime crash replay

An earlier high-speed run crashed with SIGSEGV after the last log entry at `2008.03.02.14`. A later 20 October non-Ironman EOR run also ended in SIGSEGV after the last logged date `2008.04.20.14`; its crash report, logs and pre-crash autosave are preserved under `development_backups/portrait_crash_20261020_213944/`. The last non-repeating portrait-conversion warning is a clue, not a proven cause. Long-running stability remains unverified. The original pre-crash autosave and logs remain at `development_backups/runtime_hoi4_20261018_202526/`.

Run `python3 tools/trace_runtime.py` after preparing the development build to add event/option BEGIN/END markers and a daily heartbeat. This changes only the installed copy and does not alter gameplay effects. Rebuilding with `setup_local.py` removes it. Replay the same autosave at speed 2 or 3 through March 3 to check whether the failure repeats near the same game time. Do not publish runtime tracing overlays.

## Rising Sun campaign redesign

EOR has **189 focuses, 24 decisions and three political routes: Yoshiro, Tatsu and Shinzo**. There are 77 EOR events and 107 active events overall. All routes use standard HOI4 outcomes; the final political focuses consolidate government policy. New Dawn, its automatic territorial-return programs and the custom victory layer are removed. The accepted starting borders and 2008 scenario remain unchanged.

Decisions are organized into Statecraft, Military Operations, Experimental Projects and Overseas Administration. The emergency relocation decision is removed. Great machines prepare into ready assets and require separate wartime activation. Yuriko missions and subject projects recheck recipients/targets and report invalidation. The newer corporate/state spirit pair is authoritative, government authority uses one regime-appropriate tier, and active spirits have separate descriptive prose. A baseline EOR AI plan and force-structure strategy prioritize industry, research, defense and current subjects without replacing the existing route weights.

See the [self-audit and minor-country menu fixes](docs/review/EOR_SELF_AUDIT.md), [playability changes and user tests](docs/EOR_PLAYABILITY_IMPLEMENTATION.md), [earlier implementation and revision status](docs/EOR_IMPLEMENTATION.md), [source route schedules](docs/EOR_ROUTE_SCHEDULES.md), and the [signature-art review sheet](docs/review/EOR_SIGNATURE_ICONS.png). The approved playability pass removes eleven redundant focuses, adds substantive government programs, repairs diplomacy and equipment rewards, and shortens experimental authorization. Optional objective/superweapon additions, a complete numerical balance pass and a new signature-art set remain follow-up design work. Retained art is unique, but some signature imagery remains ambiguous.

Run `python3 tools/validate_eor.py --source-only` for script checks without a game installation. Default validation also checks native assets and geometry. Synchronize with `python3 tools/setup_local.py`, then validate `--installed`. Fully restart and use a **new non-Ironman EOR campaign** in **Red Alert 3 Development**. Check all three governments, economic modifiers, original-recipient projects, ready/active operations and normal war resolution. The user launches HOI4; static checks do not establish successful event execution, rendering, stability or campaign balance. IOT continues to use its complete generic tree.
