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
- `tools/release_build.py`: shared release-package builder used by the shell entry points. It requires a clean worktree by default, applies both compatibility passes, writes `dist/red_alert_3-<version>/` and a manifest, and supports `--allow-dirty`, `--force`, and `--zip`.
- `tools/prepare_release.sh`: runs source validation and the audit regression suite before calling the builder. The release folder is the primary artifact; the zip is optional.
- `tools/stage_release_test.sh`: stages a prepared release folder as a local **Red Alert 3** entry in `mod/red_alert_3_release_test`, separate from the development mod. It preserves Workshop ID **1722615953** so the launcher uploader updates the existing item, backs up the prior test build and logs, and runs installed validation. `--remove` deletes only a marked test build. The local entry uses the release name so the upload title stays correct; select the local copy, not the subscribed Workshop copy.
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
- Preserve custom USA (`usa2`), Soviet (`ussr`), European (`ame`), African (`ra3_africa`), and RA3 news chains.
- The functional alliance-invitation exchange `generic.5`, `.6`, `.7` and faction announcement `news.289` remain the explicit mechanical diplomacy exception after the EOR tree redesign. They are the current explicit mechanical exception, not permission to restore historical chains.
- Custom announcements currently use `news.400`, `.401`, `.403`, `.404`, and `.405`. The European militarization events reference `.400` and `.401`.
- Adding or changing events requires checking both definitions and callers. Retained chains must resolve; excluded events must not remain in direct calls, event pools, or inherited scheduling hooks.
- The current catalog has 102 events, including 72 EOR events. This is a snapshot, not a limit on future user-designed content.

## Compatibility and validation

- The installed development target is **HOI4 1.19.3**. The source descriptor and prepared 0.2.2 release declare `supported_version="1.19.*"`. Static and installed validation pass; a new-campaign runtime check of the release candidate remains required before publishing.
- Keep engine settings additive in `common/defines/ra3_defines.lua`. Do not restore the archived full `00_defines.lua` or `00_graphics.lua`; they removed required modern defaults.
- Preserve current research-interface widgets and modern sprite definitions. Extra RA3/legacy sprites live in `interface/ra3_technologies.gfx`; do not restore the obsolete full `Technologies.gfx` override.
- Loading backgrounds are explicitly registered in `common/frontend/backgrounds/base_backgrounds.txt` using the existing RA3 images.
- The RA3 soundtrack is intentionally RA3-only: `music/music.asset` overrides the vanilla music asset, and `music/songs.txt` must begin with `music_station = "base_music"`. All 44 tracks live in `music/`. Keep music chance triggers on `fascism` and `EOR`, not legacy `fascist`/`JAP`.
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
- Prepare a clean release with `tools/prepare_release.sh` so all required compatibility transformations are applied. Do not upload the raw checkout: exclude Git data, tools, archives, development descriptors, backups, diagnostic overlays, and trace markers.
- Stage the prepared folder with `tools/stage_release_test.sh`, test the local **Red Alert 3** copy locally, then select that local copy in the launcher uploader to update the existing item through the owning Steam account. Verify Workshop target **1722615953**, and test the downloaded Workshop build afterward.
- Follow actual environment permissions for writes. Explain required sandbox escalation briefly; do not use GUI tools to bypass a filesystem restriction.

## Rising Sun revision implementation (2026-10-19)

- The current design has 189 focuses, 24 decisions, 77 EOR events and 149 country-spirit definitions. The active event catalog has 114 events. `docs/EOR_IMPLEMENTATION.md` records S01–S25 implementation scope, deferred optional work and runtime tests; the manifest records the current three-route inventory.
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

- The current inventory is 189 focuses, 24 decisions and 77 EOR events (114 active overall). The later self-audit removes two more redundant steps and merges bloodless political costs into actual government installation. See `docs/review/EOR_SELF_AUDIT.md` for findings and corrections; do not describe earlier checks as engine or UI confirmation.
- IOT/PHI/MAL/INS are explicit `minor = yes` entries in the standard bookmark minor-country list. Do not restore the removed `filters = { label }` / `label_order` custom tab or per-country `label` keys. Keep `scrollable_country_list = yes` and non-empty generic focus previews. SIA is an ally, not a newly inferred puppet. Menu visibility remains pending user confirmation.
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
- The active event catalog is 114 events overall and 77 EOR events. New event keys use `eor.156`–`eor.160`; `eor.156.desc` avoids collision with option `eor.156.d`.
- Source, native and installed static checks pass with 189 focuses, 24 decisions and 114 active events. Runtime execution, decision visibility, investment delivery and campaign balance remain unconfirmed; the user launches a fresh non-Ironman campaign.

## EOR AI baseline (2026-10-20)

- `common/ai_strategy_plans/EOR_default_strategy_plan.txt` supplies EOR focus priorities and research weights; `common/ai_strategy/EOR.txt` supplies army, navy, air and production ratios. These are baseline technical behavior, not a claim about campaign balance.
- The AI plan is route-neutral: existing focus `ai_will_do` values retain the Yoshiro/Tatsu/Shinzo selection. Do not add a second route-selection mechanic or restore removed unilateral war/peace decisions.
- AI focus factors and strategy identifiers are statically checked; research weights are reviewed separately. Actual AI focus selection, production, diplomacy and campaign performance require a user-run campaign; source validation does not prove them.

## Soviet occupation and diplomacy routes (2026-10-21)

- The shared Soviet occupation and Comintern expansion branches are removed. The Soviet tree now has 47 unique focuses. The Union starts with exactly three route-linked crises: `SOV_continent_under_occupation` (Cherdenko), `SOV_fractured_supreme_command` (Krukov) and `SOV_diplomatic_isolation` (Commander). `SOV_red_fleet_deficiencies` is no longer a starting idea. Route selection occurs after `SOV_the_burden_of_victory` through `SOV_the_future_of_the_union`.
- Route-specific occupation and diplomacy branches are hidden by `available = { has_country_flag = SOV_route_cherdenko|SOV_route_krukov|SOV_route_commander }`. Preserve this visibility gate so only the chosen route's policy branch appears.
- Cherdenko tightens direct rule: European and Scandinavian garrison networks, internal security, imperial integration, a continental diktat and a preemptive-war line. Krukov breaks the zones into smaller client republics, then adds armed deterrence, fortress economics and pragmatic eastern outreach. The Commander releases the zones as independent republics and pursues anti-colonial solidarity and revolutionary diplomacy.
- The old shared focuses must not return: `SOV_occupation_administration`, `SOV_european_garrison`, `SOV_northern_garrison`, `SOV_suppress_dissent`, `SOV_integrate_occupation`, `SOV_consolidate_comintern`, `SOV_support_colonial_revolution`, `SOV_courting_the_east`, `SOV_global_revolution`.
- Autonomy semantics: `release = TAG` creates a puppet, not an independent state. Independence helpers use `release = TAG` followed by `set_autonomy = { target = TAG autonomy_state = autonomy_free }`; puppet helpers retain `release_autonomy` plus no-TFV `release`/`set_autonomy` fallbacks. Use `autonomy_state`, not `autonomous_state`.
- New spirits are `SOV_krukov_deterrence_doctrine`, `SOV_krukov_fortress_doctrine` and the starting `SOV_diplomatic_isolation`; Cherdenko reuses `SOV_comintern_direction` and `SOV_global_revolutionary_line`; Commander reuses `SOV_anti_colonial`, `SOV_liberation_doctrine`, `SOV_internationalist_union` and `SOV_world_revolution`; Krukov reuses `SOV_eastern_outreach`. All active Soviet spirits have matching `sov_spirit_*` pictures and `GFX_idea_sov_spirit_*` sprites.
- Each route capstone resolves only its own crisis: `SOV_cherdenko_red_century` removes the occupation burden, `SOV_krukov_peace_through_strength` removes fractured command, and `SOV_export_the_revolution` removes diplomatic isolation. Route directives must not remove a crisis early. Commander rewards use diplomacy modifiers (`opinion_gain_monthly_factor`, `improve_relations_maintain_cost_factor`, `faction_influence_contribution_factor`) rather than generic stability.
- SOE/SOS no longer have empty focus-tree overrides; they and IOT/PHI/MAL/INS explicitly weight `generic_focus`. Their bookmark entries use real generic focus previews. `SOV_red_fleet_deficiencies` remains defined for old saves but is not granted at start.
- Source, native and installed validation pass with 47 SOV focuses and 45 Soviet spirit definitions. Runtime icon rendering, bookmark minor visibility, branch visibility, release behavior and campaign balance remain unconfirmed; test with a new non-Ironman 2008 campaign.

## AME migration and focus tree (2026-10-22)

- The active country tag and namespace are `AME`, not `AOE`. The display name remains “Allied Nations' Militarized Zone in Europe.” The rename covers active scripts, history, states, OOB, flags, leaders, bookmarks, tools and localisation; the only remaining lowercase `aoe` is the unrelated area-of-effect string in `events/RA3Diplomacy.txt`.
- `common/national_focus/ame_focus.txt` defines 69 focuses: 14 Industry, 22 European Theatre, 19 Diplomacy and 14 Contractors. Bingham's War Conference fires `ame.7` and gates one of three strategy branches. The Future of Liberated Europe fires `ame.8` and gates immediate release versus transitional administration. American Response fires `ame.9` to the USA and gates aid, expeditionary or intervention follow-ups.
- The Industry branch occupies `y=0` through `y=7`. Do not shift it downward into the bottom-left continuous-focus window; the European Economic Community capstone is offset to `x=6` to clear that panel horizontally. Its long connector warning is an accepted tradeoff. Future-tech parent/child columns align at `x=34`, `x=36` and `x=38`. `AME_support_greece` requires `AME_the_allied_cause`, uses `GFX_focus_generic_befriend_greece`, and invites `GRE` only when AME leads the faction and Greece is unaligned. New icon assignments use existing vanilla `GFX_focus_*` sprites and resolve in `goals.gfx`.
- Five convergence focuses use a single OR prerequisite block so they never require mutually exclusive routes: `AME_the_shield_of_europe`, `AME_coordinate_the_liberation`, `AME_declaration_of_the_allied_nations`, `AME_joint_command` and `AME_the_grand_alliance`. Do not split their alternatives into separate `prerequisite` blocks; separate blocks are AND and make the focus unreachable.
- The London/Dublin accords and UK/Ireland militarization branches remain mutually exclusive. The 33-tag release list is `ALB AUS BEL BOS BUL CRO CZE DEN ENG EST FIN FRA GER HOL HUN ICE IRE ITA LAT LIT LUX MAC MNT NOR POL POR ROM SER SLV SPR SWE SWI YUG`; Greece remains a guaranteed ally and is not released.
- `common/scripted_effects/ame_focus_effects.txt` uses literal tag blocks, not parameterized `$TAG$` helpers, because HOI4 scripted effects do not substitute parameters. It releases republics through `release_autonomy` with `autonomy_free`, `release_non_owned_controlled` and controller correction, with a non-TFV `release`/`set_autonomy` fallback. Released countries receive `AME_restored_republic`; a democratic provisional government is installed only when no ruling leader exists. AME cores are removed from restored-republic states. All values remain provisional.
- The tree references 30 new national spirits in `common/ideas/ame_ideas.txt`. Twelve spirit IDs that collided with focus IDs use `_spirit` suffixes; focus IDs and prerequisites are unchanged. Keep active AME script files free of UTF-8 BOMs: a BOM made the engine reject the entire ideas file and produced invalid-idea/`add .` focus rewards. Conversely, active AME localisation YAMLs require the UTF-8 BOM; stripping it made the engine reject the files and render focus, spirit and event names as raw keys. Use `set_country_flag`, not `add_country_flag`. Bingham's three strategy routes are explicitly pairwise `mutually_exclusive` as well as event-gated. The previous designer availability problem is fixed by ORing the AME and USA mirror focuses. USA contractor focus icons, `news.400`/`news.401` option triggers and the missing Bingham description were also corrected.
- AME starts the `allied_nations` faction with `ENG`, `CAN`, `SAF`, `DEN` and `IRE`; do not add `USA` to the starting faction. The USA joins through `USA_join_the_allied_nations` and `usa2.10`, or creates the `american_coalition` if admission is refused.
- The active event catalog is 124 events overall after the USA redesign. Source and installed static checks pass with 69 AME focuses and 30 new spirits and 19 regression tests; `docs/AME_IMPLEMENTATION.md` records the design and test checklist. Runtime focus visibility, continuous-window clearance, future-tech layout, Greek faction invitation, event delivery, release behavior, localisation rendering, faction membership and campaign balance remain unconfirmed; test with a new non-Ironman 2008 campaign.

## USA 2008 election and national focus tree (2026-10-23)

- `common/national_focus/usa.txt` defines 53 focuses after the 2026-10-24 rebalance and UI compaction. Focus durations use only 7, 70 or 140 displayed days; 70 is normal. The engine `cost` field is in focus points at 7 days per point, so use `cost = 1`, `10` or `20` respectively. `USA_2008_us_election` is 7 days, the normal USA focuses are 70 days, and the seven major convergence/capstone focuses are 140 days: `USA_liberate_europe`, `USA_project_rushmore`, `USA_americas_war`, `USA_question_the_constitution`, `USA_the_new_american_order`, `USA_the_american_industrial_giant` and `USA_the_american_century`. The 2008 election opens the mutually exclusive Ackerman (`USA_america_leads`) and Rockwell (`USA_america_alone`) routes; shared industry, military, Monroe Doctrine, contractor and American Century branches follow. The tree replaced the previous 2018-election tree, so do not restore `USA_2018_us_election`, `USA_rally_the_allies`, `USA_war_in_europe` or `USA_withdraw_from_allied_nations`. Do not restore the twelve focuses merged in the rebalance: `USA_the_washington_coalition`, `USA_victory_through_unity`, `USA_rushmore_ascendancy`, `USA_national_sovereignty_act`, `USA_continental_deterrent`, `USA_ideological_mobilization`, `USA_fort_bradley`, `USA_maritime_bastions`, `USA_mirage_technology`, `USA_strategic_air_dominance`, `USA_combined_arms_command` and `USA_the_allies_military`. The `USA_strike_the_empire` focus was removed; its spirit definition remains for save compatibility and is no longer obtainable.
- `USA_modern_monroe_doctrine` grants guarantees through `common/scripted_triggers/usa_triggers.txt` to the 21 American nations existing in 2008: `CAN MEX CUB HAI DOM GUA HON ELS NIC COS PAN VEN COL ECU PRU BRA BOL CHL PAR ARG URG`. Guarantees are focus-granted, not present at scenario start. `USA_hemispheric_security` unlocks coercive enforcement rather than granting a passive planning idea.
- `USA_2008_us_election` fires `usa2.2`; the history leader is Howard T. Ackerman with `Portrait_USA_Howard.dds`. The election's Rockwell option uses `retire_country_leader` plus `create_country_leader` with `Portrait_USA_Rockwell.dds`. `USA_question_the_constitution` converts the current Rockwell to `fascism_ideology` or creates him if absent; do not restore string-based `set_country_leader_name`. `usa2.4` still uses `set_country_leader_*` and requires runtime confirmation. Portrait GFX registrations are in `interface/usa_portraits.gfx`. The old “Waiting For the Next President”/Himmler placeholder must not return.
- The Ackerman route can join the AME-led `allied_nations` through `usa2.10`, create `american_coalition` if refused, or take an independent command. If AME is absent, `USA_join_the_allied_nations` falls back to `american_coalition` instead of blocking the route. `USA_the_allied_war_council` and `USA_the_washington_leadership_conference` require AME faction membership; `usa2.11` can transfer faction leadership to the USA. Do not add the USA to AME's starting faction in history.
- The Rockwell route runs through `USA_the_new_order`, `USA_presidential_power_act` and `usa2.7`. Escalation adds 15% fascism support; `USA_the_new_order` and `USA_presidential_power_act` add 15% and 12%, so the path reaches 45% from the 3% start. `USA_question_the_constitution` requires `fascism > 0.4`, sets fascism to 55%, converts Rockwell to `fascism_ideology`, and starts the civil war with `size = 0.35` and capital state 361. John Smith is created with unit-leader ID 1000; after the civil war starts the player transfers any leader with ID 1000 back to USA and removes the `reassigned` trait. `usa2.4` installs the post-war Rockwell/Smith choice. Backing down removes the emergency powers and public objection.
- `common/decisions/USA.txt` uses the vanilla `USA_war_measures` category and contains seven decisions: the four-division Armed Protection Squadron, the one-use Rushmore strike, the Mexican state-277 wargoal, Enforce Hemispheric Security (75 PP, puppet wargoal against a valid SOV/EOR target), Lend-Lease to Europe (50 PP, 180-day re-enable, 5,000 infantry equipment to AME), Federalize the National Guard (75 PP, three six-infantry divisions at 0.3 experience) and the National Propaganda Campaign (50 PP, 180-day re-enable, fascism +2%, democratic −2%, war support +3%, stability −2%). Do not restore the old large APS decision or unilateral war/peace decisions.
- The USA has 13 new spirits in `common/ideas/usa.txt` plus the reused `USA_homeland_defense`; the obsolete `USA_the_pentagon` and `USA_intervention_in_the_americas` spirits are removed. `USA_homeland_defense` now includes the Pentagon's planning bonus, and `USA_preserve_allied_unity` upgrades to `USA_leadership_of_the_free_world_2`. `USA_war_department` localisation remains in `focus_l_english.yml`. USA focus/event/spirit/decision localisation is in `localisation/usa_core_l_english.yml`; `american_coalition` is in `factions_l_english.yml`. Keep script files BOM-free and localisation files BOM-encoded.
- Active event count is 124 (117 + seven net new USA events): `usa2.1`–`usa2.4` replace prior USA events and `usa2.5`–`usa2.11` are new. All focus references, icons, idea references, event references and localisation keys pass static checks. A 2026-10-24 USA first-focus crash (SIGSEGV after `usa2.2`) is preserved under `development_backups/crash_20261024_194052/`; `usa2.2` now sets `ruling_party` and replaces Rockwell via `retire_country_leader`/`create_country_leader`. A later 2026-10-24 civil-war crash (SIGSEGV at `2009.09.25`, AI army/navy stack) and its `2009.09.25` autosave are preserved under `development_backups/civil_war_crash_20261024_205208/`; the 40% gate/leader transfer await runtime confirmation and crash reproduction remains open. Runtime leader transformation, Monroe guarantee application, decision visibility/delivery, civil-war behavior, Rushmore strike effects, faction admission/leadership and campaign balance remain unconfirmed; test with a new non-Ironman 2008 campaign.
