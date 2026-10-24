# AME implementation

## Scope

The former `AOE` country tag and namespace were renamed to `AME` throughout active content, including the country tag, focus and idea IDs, event namespace, history, OOB, flags, leaders, bookmarks, decisions, localisation and tools. The display name remains “Allied Nations' Militarized Zone in Europe.” The only remaining lowercase `aoe` under active content is the unrelated area-of-effect modifier string in `events/RA3Diplomacy.txt`.

The starting scenario remains 2008.1.1. AME starts democratic with modern `set_popularities`/`set_politics`, a 2007.6.3 election baseline, elections enabled, and Robert Bingham valid through 2051.1.1.

## Focus tree

`common/national_focus/ame_focus.txt` defines 69 focuses in four branches:

- Industry, 14 focuses: industrial, construction, infrastructure, research-slot, armament, wartime conversion, continental supply and the European Economic Community capstone.
- European Theatre, 22 focuses: army reform, the shield of Europe, Peacekeeper technology, Copenhagen, Bingham's War Conference, three mutually exclusive strategy routes, liberation preparation, and the post-war settlement route.
- Diplomacy, 19 focuses: allied outreach, British/Irish/Greek/Commonwealth cooperation, the London and Dublin accords, Declaration of the Allied Nations, American support, joint command and the Grand Alliance.
- Contractors, 14 focuses: FutureTech, subcontractors, the Advanced Systems Consortium, Apollo, continental air defense, Vindicator, tactical strike wings, the Century Bomber and Strategic Air Command.

Prerequisite blocks follow standard HOI4 semantics: multiple focuses in one block are OR, while separate blocks are AND. The five convergence focuses use a single OR block so no focus can require mutually exclusive routes: `AME_the_shield_of_europe`, `AME_coordinate_the_liberation`, `AME_declaration_of_the_allied_nations`, `AME_joint_command` and `AME_the_grand_alliance`. The strategy branches are gated by `AME_strategy_fortress`, `AME_strategy_mobile` or `AME_strategy_resistance`. Post-war settlement is gated by `AME_restore_republics` or `AME_transitional_administration_route`.

Bingham's War Conference fires `ame.7`; The Future of Liberated Europe fires `ame.8`; American Response fires `ame.9` to the USA. USA options set `AME_usa_aid`, `AME_usa_expeditionary` or `AME_usa_intervention` on AME. The accords and militarization branches are mutually exclusive by focus and event.

The Industry branch occupies `y=0` through `y=7`. Do not shift it downward into the bottom-left continuous-focus window; the European Economic Community capstone is offset to `x=6` so its card clears the panel horizontally. Its longer feeder connectors are an accepted layout tradeoff. The future-tech contractor columns align their parent and child focuses at `x=34`, `x=36` and `x=38`. `AME_support_greece` requires `AME_the_allied_cause`, gives political power and opinion, and only invites `GRE` into the AME-led faction when AME is the faction leader and Greece is not already in a faction or a subject. Greece remains outside the 33-tag release route.

The new focus rewards reference 30 new national spirits in `common/ideas/ame_ideas.txt` and the release helper in `common/scripted_effects/ame_focus_effects.txt`.

## Release route

`AME_release_european_republics` explicitly handles 33 tags:

`ALB AUS BEL BOS BUL CRO CZE DEN ENG EST FIN FRA GER HOL HUN ICE IRE ITA LAT LIT LUX MAC MNT NOR POL POR ROM SER SLV SPR SWE SWI YUG`

Greece remains a guaranteed ally and is not released.

The effect only acts when AME owns or controls a core state of the target and no country exists, or when the existing country is an AME subject. The TFV path uses `release_autonomy` with `autonomy_free`, `release_non_owned_controlled` and controller correction; the fallback uses `release` plus `set_autonomy`. Released countries receive `AME_restored_republic` and, if they lack a ruling leader, a democratic provisional government valid through 2051. AME cores are removed from states owned by restored republics. All quantities, thresholds and modifiers are provisional.

HOI4 scripted effects do not substitute `$PARAM$` parameters. The earlier parameterized helper was rejected by the engine and has been replaced with literal tag blocks; do not restore `$TAG$` calls.

## Runtime corrections (2026-10-22)

- The reported `add .` focus rewards were caused by a UTF-8 BOM at the start of `common/ideas/ame_ideas.txt`. The engine rejected the whole file as `Unexpected token: ﻿ideas`, so every AME idea was invalid. Keep active AME script files BOM-free.
- Stripping the UTF-8 BOM from the four active AME localisation YAMLs made the engine reject them (`should be in in utf-8-bom encoding` / `Missing UTF8 BOM`), so focus, spirit and event names rendered as raw keys. Localisation files require the BOM; script files must remain BOM-free.
- `add_country_flag` is not a HOI4 effect and did not set the Bingham, settlement or USA response flags. Use `set_country_flag`.
- Twelve national-spirit IDs collided with focus localisation keys. They now use `_spirit` suffixes; focus IDs and their prerequisites are unchanged.
- Bingham's three strategy routes now have explicit pairwise `mutually_exclusive` links in addition to their event-gated `available` flags.
- The release helper uses literal country tags and no scripted-effect parameters.
- Robert Bingham's DDS header was normalized to the engine's standard 156x210 ARGB layout; the pixel content is unchanged.
- AME starts the `allied_nations` faction without the USA. The USA joins through `USA_join_the_allied_nations` and `usa2.10`; refusal creates the `american_coalition` instead.

## Validation

- `python3 tools/validate_eor.py --source-only` passes.
- `python3 tools/validate_eor.py --installed <development mod>` passes source/native checks and reports no diagnostic overlays.
- `python3 tools/test_eor_audit.py` passes all 19 regression tests.
- `hoi4_focus_inspect`/`hoi4_focus_render` and event inspection report no static parse failure for the AME tree and events.
- The AME tree has 69 unique focus IDs, 69 unique coordinates, no missing prerequisites, no upward prerequisite edges, and all icons resolve.
- `tools/validate_eor.py` asserts convergence OR blocks, defined AME `add_ideas` targets, pairwise Bingham route exclusivity, BOM-free active script files, BOM-present active localisation files, no scripted-effect parameters, no invalid `add_country_flag`, no USA in the starting AME-led faction, and no duplicate AME focus/spirit localisation keys.
- Static checks are not an engine run and do not establish runtime execution, AI behavior, event delivery, release behavior or campaign balance.

## Remaining runtime checks

Use a new non-Ironman 2008 campaign and select AME:

1. Confirm the tree opens with four branches and 69 focuses, including bookmark previews. Confirm the Industry branch and its European Economic Community capstone clear the bottom-left continuous-focus window, the future-tech focuses do not overlap, and focus names and descriptions are localised. Confirm the USA is not in the starting Allied Nations faction.
2. Complete either army reform branch and confirm `AME_the_shield_of_europe` becomes available. Take Bingham's War Conference, confirm exactly one strategy branch remains available, then confirm `AME_coordinate_the_liberation` becomes available from that route's follow-up.
3. Complete American Response and confirm one USA flag gates its matching follow-up. Confirm `AME_joint_command` becomes available from that branch and `AME_the_grand_alliance` from expeditionary or direct intervention.
4. Confirm the London/Dublin accords and the UK/Ireland militarization branches are mutually exclusive. Confirm `AME_declaration_of_the_allied_nations` becomes available after any one completed outreach branch. Complete Support Greece while AME leads the faction and confirm Greece joins only if it is unaligned; repeat without faction leadership and confirm no invitation is issued.
5. After liberation, take the settlement route and confirm the 33-tag release helper, provisional leaders and AME core cleanup.
6. Confirm all new focus, event and spirit localisation displays without blanks.

Any remaining runtime failures must be checked against the latest `logs/error.log`, `logs/game.log` and crash report; static validation is not proof of successful execution.
