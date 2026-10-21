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
- The functional alliance-invitation exchange `generic.5`, `.6`, `.7` and faction announcement `news.289` remain the explicit mechanical diplomacy exception after the EOR tree redesign. They are the current explicit mechanical exception, not permission to restore historical chains.
- Custom announcements currently use `news.400`, `.401`, `.403`, `.404`, and `.405`. The European militarization events reference `.400` and `.401`.
- Adding or changing events requires checking both definitions and callers. Retained chains must resolve; excluded events must not remain in direct calls, event pools, or inherited scheduling hooks.
- The current catalog has 102 events, including 72 EOR events. This is a snapshot, not a limit on future user-designed content.

## Compatibility and validation

- The installed development target is **HOI4 1.19.3**. The source descriptor and prepared 0.2.0 release declare `supported_version="1.19.*"`. Static and installed validation pass; a new-campaign runtime check of the release candidate remains required before publishing.
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
- The 2026-10-20 EOR crash report, logs, and 21:38 autosave are preserved with checksums under `<user data>/development_backups/portrait_crash_20261020_213944/`; last logged date `2008.04.20.14`, SIGSEGV, ending in a `Portrait_Soviet_Dasha` small-portrait conversion error.

## Archives, Git, and publishing

- Preserve `archive/compatibility_1_19/`, `archive/scenario_start_fixes_2008/`, and `archive/vanilla_event_removal/` as recovery/reference material. They must remain outside loaded content and release packages.
- Do not edit the base-game installation or the subscribed Workshop download to implement mod changes.
- Work remains local unless the user requests a commit, push, or release. Do not run `cchain_auto_git.json` as a routine task: it stages everything, commits, and pushes.
- The existing Workshop item is **1722615953**. Preserve that release identity; generated development descriptors intentionally omit the Workshop ID.
- Publishing is separate from local synchronization and Git operations. Obtain an explicit release instruction before uploading or changing the live Workshop item.
- Prepare a clean release with all required compatibility transformations applied. Do not upload the raw checkout: exclude Git data, tools, archives, development descriptors, backups, diagnostic overlays, and trace markers.
- Test the prepared release locally, update the existing item through the owning Steam account, and then test the downloaded Workshop build.
- Follow actual environment permissions for writes. Explain required sandbox escalation briefly; do not use GUI tools to bypass a filesystem restriction.

## Rising Sun revision implementation (2026-10-19)

- The current design has 189 focuses, 24 decisions, 77 EOR events and 149 country-spirit definitions. The active event catalog has 107 events. `docs/EOR_IMPLEMENTATION.md` records S01–S25 implementation scope, deferred optional work and runtime tests; the manifest records the current three-route inventory.
- Three political routes only: Yoshiro, Tatsu and Shinzo. New Dawn, its hidden unlock, constitutional council, branch-exclusive independence/federation actions and automatic overseas handovers are removed. Preserve the accepted starting borders. Do not resurrect the discarded route or infer new territorial changes.
- Use standard HOI4 victory, capitulation, war resolution, peace conferences and scoring. The three former final focuses are ordinary government-policy milestones with local route prerequisites and practical rewards. Do not add custom win flags, partner-count victories or mandatory rival/technology/coalition victory gates.
- Preserve unique characters and Tatsu's military role. Armed coups keep the player as fascist EOR/Shinzo against non-aligned loyalists under the existing Yoshiro. Completed focuses remain historical during the explicit coup stand-down or severe countercoup; incompatible regime benefits are cleaned once by government installation helpers.
- First theaters remain mutually exclusive; Global Reassessment permits later campaigns. Use tag-specific `on_daily_EOR` / `on_monthly_EOR`; do not enforce borders or governments daily. All numerical balance remains provisional.
- Imperial Legitimacy is institutional support and political access. Yoshiro's single authority tier uses Divine Mandate; actual Tatsu/Shinzo governments use institutional legitimacy and appropriate dynamic names. Preserve regime-first selection and avoid duplicate authority benefits.
- The authoritative economic spirits are `EOR_cooperative_zaibatsus` / `EOR_controlled_zaibatsus`. Their centralized transitions clear competing ideas/flags. Subject-only benefits follow current subject relationships, with no discarded independent-partner exception.
- Fixed subject projects persist the original capital/recipient, recheck subject status and explicit recipient control at completion, then clear their global event target. Invalidated investments grant no reward/refund and release timed reservations on schedule. Philippine pressure changes belong in EOR scope.
- Tengu fighter and VX CAS remain dedicated land-based aircraft; no carrier embarkation or native transformation is promised. Executioner, Giga Fortress and Black Tortoise are paid preparations into ready assets with separate wartime activation, finite national bonuses and recovery. Yuriko remains one operative with two revalidated missions, assault and sabotage, sharing a cooldown. Do not fabricate giant hybrid map units.
- Keep four intent-based decision categories and separate active-spirit localization identities. Retained focus/idea art remains unique at the file level; signature semantic weaknesses are recorded in the contact sheet and must not be described as resolved solely by hashes.
- Preserve downward prerequisites, the compact picker and continuous panel below all branches. IOT continues to select the full generic tree. Mobilization, institute/experimental research and overseas logistics retain their shared prerequisite merges.
- Run `python3 tools/validate_eor.py --source-only` for installation-independent checks. Default validation adds native geometry/assets/modifiers. Synchronize using `tools/setup_local.py`, then validate `--installed`. A full restart and new non-Ironman campaign are required; the user performs runtime testing.
- Optional new symbolic objectives, hybrid naval equipment, a complete numerical balance pass, signature-art replacement and Nanoswarm/Psionic Decimator operations are not approved implemented content. Record and resolve their design/test gates before adding them.

## EOR playability revision (2026-10-19)

- The user approved proceeding with the playability review's fixes. `docs/EOR_PLAYABILITY_IMPLEMENTATION.md` records the implemented scope and differences from the proposal; the original review remains evidence, not the current inventory.
- Eleven redundant focuses are removed. Yoshiro consolidates directly after the court; a 75-PP, 60-day scheduled review opens the succession debate without inventing evidence or requiring defeat/expansion. Existing revelation and defeat triggers remain alternatives. Administrative steps take 21–35 days; actual successor installations and government milestones retain 70-day commitments.
- Reconciliation and the preserved throne have explicit settlements. Funded sacred, technical and military service programs recheck the government at delivery. Homeland fortress grants are limited to two contracts in Kanto/Kansai/Tokai, with fixed cities checked against the effective map. Projects consume their grant/cost on authorization; invalidation gives no benefit/refund and factory reservations expire normally.
- Chinese bilateral focuses require a current accepted partnership and use finite research exchanges, preserving the subject-only Imperial research group. Extra Chinese economic terms require EOR's explicit event choice; offer AI reflects relative strength/shared enemies/faction commitments. Invalidated partnerships require renewed agreement.
- Divide Our Enemies opens targeted envoy preparation rather than repeating event 105. Successful preparation temporarily improves acceptance weight for a later eligible request; it does not force peace or acceptance. Resource Concessions delivers resources to eligible current subjects rather than an unused permission flag.
- Repeated equipment focuses retain useful delivery/support rewards when technology is already known. Fighter/CAS terminal spirits replace their predecessors. Primary grand projects now use a 35-day program plus 70-day prototype; expensive preparation, readiness, wartime activation and recovery remain. Ordinary national support is still not a hybrid map unit.
- Moscow/Allied achievement announcements fire automatically once their existing operational and control/defeat conditions are met. Odessa and delayed northern preparation provide practical operations; ordinary war/peace rules remain. Durable administrative relief is capped at six points per month; severe subject unrest follows demands with a 60-day grace period.
- All delivery quantities, costs, durations and modifiers remain provisional. Source/native/installed checks do not establish runtime execution, rendering, AI behavior or campaign balance. Use a full restart and new non-Ironman EOR campaign; the user launches the game.

- China display follow-up: all ten regional/China focuses have unconditional reward summaries, while guarded native effect details remain visible. Coercive preparation, China-specific offensive support and actual-recipient industrial consolidation provide concrete rewards; no territorial transfer is added. The user has not yet confirmed the new display or delivery.
- Latest engine logs (preserved under `development_backups/china_focus_report_20261019_232058/`) expose pre-existing EOR aircraft archetype/parent parsing errors and an unsupported armor `manpower` unit bonus. These were missed by the earlier static checks. Source corrections and remaining runtime checks are recorded in `docs/review/EOR_SELF_AUDIT.md`; they are not a proven explanation for blank China tooltips.

## EOR self-audit and minor picker (2026-10-19)

- The current inventory is 189 focuses, 24 decisions and 77 EOR events (107 active overall). The later self-audit removes two more redundant steps and merges bloodless political costs into actual government installation. See `docs/review/EOR_SELF_AUDIT.md` for findings and corrections; do not describe earlier checks as engine or UI confirmation.
- IOT/PHI/MAL/INS are explicit `minor = yes` entries in the standard bookmark minor-country list. Do not restore the removed `filters = { label }` / `label_order` custom tab or per-country `label` keys. Keep `scrollable_country_list = yes` and valid focus previews. SIA is an ally, not a newly inferred puppet. Menu visibility remains pending user confirmation.
- EOR aircraft definitions load in `common/units/equipment/zz_eor_aircraft.txt`, after their conventional parent/archetype definitions. Air OOB registration follows naval registration. Starting doctrines use native 1.19 grand-doctrine setup; removed battery technology IDs are not restored.
- `add_unit_bonus` cannot apply `manpower` in the current engine. Keep the rejected bonus removed; do not claim battalion-manpower reduction or silently substitute another mechanic. China rewards retain native visible effects plus explanatory previews, with factory capacity rechecked.
- Run `python3 tools/test_eor_audit.py` for the self-audit regression fixtures. New authorization-based cooldowns use explicit timed flags; do not stack a second full per-decision re-enable delay after preparation.

- IOT keeps its existing Oceanic Office leader, with expiration extended beyond 2050 and an explicit valid portrait path. Do not restore its expired 1989 definition. This corrects selector data but does not establish on-screen visibility.
- PHI, MAL and INS use institutional fascist leaders mirroring IOT: "The Imperial Philippine Government", "The Imperial Malayan Government" and "The Imperial Indonesian Government", each expiring 2051.1.1. Their portraits reuse the IOT castle asset through per-country paths under `gfx/leaders/PHI|MAL|INS/`; this shared art is provisional, not new signature art. Keep the validator assertions and the institutional-leader regression test passing.
- EOR shared trunks were realigned to keep prerequisite lines off unrelated focus icons (technology column −10; wartime 44; overseas 47). Re-run the crossing check after coordinate edits and keep `tools/eor_design_manifest.json` in sync; the manifest is the validator's source for positions, parents and gates.

## EOR decision simplification (2026-10-20)

- The active inventory is 24 decisions in four categories: Statecraft 9, Military Operations 6, Experimental Projects 4 and Overseas Administration 5. Do not restore the removed 96-decision service, project, court, war-authorization or per-country investment lists.
- Statecraft keeps scheduled court review, negotiated coup transition, post-defeat reconstruction, the Yoshiro fortress grant, China renewal and four settlement requests. Settlement requests cost 75 PP, consume `EOR_prepared_negotiation` when available and set a 180-day recipient preparation flag; refusal costs 15 PP. `EOR_imperial_diplomacy` now sets the preparation flag instead of charging PP, and event 105 no longer charges EOR before consent.
- Military Operations keeps Yuriko's assault and sabotage missions, the three great-machine activations and `EOR_prepare_major_offensive`. Preparations use explicit timed flags; do not stack a second full re-enable delay. The offensive preparation requires war and fires `eor.156`, which offers Soviet, Pacific, general or Yuriko options. Removed unilateral war/peace decisions must not return: use normal declarations, wargoals, capitulation and peace conferences.
- Experimental Projects keeps nanocore deployment and the three paid great-machine preparations. Overseas Administration keeps infrastructure investment plus one 120-day investment decision for IOT, PHI, MAL and INS, with extract or partnership choices in `eor.157`–`eor.160`.
- The active event catalog is 107 events overall and 77 EOR events. New event keys use `eor.156`–`eor.160`; `eor.156.desc` avoids collision with option `eor.156.d`.
- Source, native and installed static checks pass with 189 focuses, 24 decisions and 107 active events. Runtime execution, decision visibility, investment delivery and campaign balance remain unconfirmed; the user launches a fresh non-Ironman campaign.

## EOR AI baseline (2026-10-20)

- `common/ai_strategy_plans/EOR_default_strategy_plan.txt` supplies EOR focus priorities and research weights; `common/ai_strategy/EOR.txt` supplies army, navy, air and production ratios. These are baseline technical behavior, not a claim about campaign balance.
- The AI plan is route-neutral: existing focus `ai_will_do` values retain the Yoshiro/Tatsu/Shinzo selection. Do not add a second route-selection mechanic or restore removed unilateral war/peace decisions.
- AI focus factors and strategy identifiers are statically checked; research weights are reviewed separately. Actual AI focus selection, production, diplomacy and campaign performance require a user-run campaign; source validation does not prove them.
