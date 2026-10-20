# Rising Sun implementation — 19 October 2026

The current build has **189 focuses, 24 decisions, 77 EOR events (107 active events overall), and 149 national-spirit definitions**. Three political routes remain: Yoshiro, Tatsu and Shinzo. All routes use HOI4's normal capitulation, war resolution, peace conferences and scoring. Government milestones neither announce a custom victory nor end the campaign.

The later [decision simplification](EOR_PLAYABILITY_IMPLEMENTATION.md#decision-simplification-20-october-2026) supersedes the 96-decision inventories and four-mission Yuriko descriptions below. Those sections remain a historical record of the earlier implementation.

EOR also has a baseline AI plan at `common/ai_strategy_plans/EOR_default_strategy_plan.txt` and force-structure/subject-support strategies at `common/ai_strategy/EOR.txt`. The plan keeps the existing Yoshiro/Tatsu/Shinzo focus weights and adds route-neutral economic, research, army, navy and air priorities. Static validation resolves every named focus and strategy token; actual AI focus selection, production and campaign performance remain runtime-unverified.

This revision supersedes the former four-route implementation. New Dawn, its council and exclusive spirits, hidden-unlock checks, independence/federation programs, automatic direct-state handovers and bespoke victory gates are removed from loaded content. Starting history, the 2008–2050 timeline, EOR's borders and dedicated deployments are unchanged. Old saves are not migrated; use a new campaign.

The later approved [playability implementation](EOR_PLAYABILITY_IMPLEMENTATION.md) supersedes the pacing, eleven redundant nodes, bilateral China rewards, continuing-policy programs and project-authorization details below. The S01–S25 table and observed validation record describe the earlier revision as historical evidence; they are not a claim that later work is still deferred.

## Institutions, economy and relationships

Imperial Legitimacy measures support for governing institutions and controls political access. Divine Mandate measures belief in Yoshiro's sacred mission. The authority refresh selects the actual government before applying one of five mutually exclusive tiers: Yoshiro uses Divine Mandate, Tatsu and installed Shinzo use Imperial Legitimacy. Thresholds remain 20, 40, 60 and 80. Successor authority is labeled Confidence in Modernization or Military Authority. Values remain available for historical events; sacred belief grants no second authority tier under a successor.

Explicit installation helpers govern Tatsu, Shinzo and the restoration of Yoshiro. The severe Tatsu countercoup removes incompatible technocratic institutional spirits once; completed focuses remain historical. Tatsu retains his military character role. The armed coup still keeps the player as fascist EOR/Shinzo against non-aligned loyalists under the existing Yoshiro character. Peaceful and armed consolidation receive different aftermath reports.

The authoritative economic pair is `EOR_cooperative_zaibatsus` / `EOR_controlled_zaibatsus`, using the newer authored trade-offs. Corporate partnership improves research, production learning and output at a political cost. State control improves output and factory construction at a research and consumer-goods cost. Each transition clears traditional/competing identities and the opposite policy flag before adding its replacement. Compatibility rebates retain their once-only flags. This intentional change in granted modifiers remains provisional balance.

Centralized and cooperative overseas administration remain. Cleanup checks every subject-only spirit independently, including security, concessions, resentment, development and resource access. Leaving EOR subjection removes those benefits and tracked subject logistics/research membership. No discarded voluntary-partner exception survives. The retained Imperial research group admits only EOR and its current subjects.

Fixed-country investments save the original recipient capital in a unique persistent global event target. Delivery requires the recipient still to be an EOR subject and to own and control that original state. Moving the capital does not retarget construction. The target is cleared at resolution. All repeated capital-construction checks use the explicit recipient, including the Oceanic development focus. Philippine local stability stays in PHI; central pressure changes in EOR. State-targeted overseas investments preserve the original recipient too. Invalidated contracts grant no benefit or refund and their timed reservation ends on schedule. Completion and invalidation have separate reports.

## Equipment, operations and capacity

Ordinary Imperial equipment remains accessible through common manufacturers and paid development, independently of political and doctrine choices. Tengu are dedicated **land-based fighters**; VX are dedicated CAS. Fleet coordination does not enable carrier embarkation or transformation. Conventional carriers retain their own supported aircraft; a hybrid naval redesign was not added.

Great machines remain national operational bonuses, not map units. Preparation now creates readiness and releases the shared industrial queue. Ready assets have no maintenance charge. A separate wartime activation consumes readiness and applies the timed support. The asset cannot prepare again while ready, active or recovering.

| Asset | Preparation | Active support | Recovery after activity | Preparation cost |
| --- | ---: | ---: | ---: | --- |
| Executioner | 180 days | 60 days | 365 days | 150 PP, 8 civilian factories, output penalty |
| Giga Fortress | 240 days | 90 days | 540 days | 200 PP, 8 civilian factories, output penalty |
| Black Tortoise | 180 days | 180 days | 365 days | 150 PP, 8 civilian factories, output penalty |

Initial project exclusions and the costly secondary-program exception remain. The former annual/540-day cooldown is now explicitly a recovery period after active support; this timing change needs campaign comparison. Preparation no longer requires war, so peace during construction does not waste the operation. Readiness and activation each produce a report. There is no manual cancellation button or refund program.

Yuriko remains one operative represented by four decisions sharing a 180-day cooldown from authorization. Each prepares for 30 days. Assault supports an existing occupied enemy foothold; command disruption weakens a current enemy; sabotage damages one military-factory level in a currently enemy-controlled industrial state; counterintelligence protects the government if it has not capitulated. Completion rechecks targets before recording success. Invalidation receives a separate report and retains the paid cost/cooldown. Sabotage applies its building damage in the selected state's scope.

The existing capacity model remains: central development reserves three civilian factories across civil construction, research and overseas projects; procurement has a separate three-factory allocation; grand projects reserve eight factories and reduce factory output. Timed reservation spirits and active decisions expose capacity and remaining time. No optional new queue architecture or broad balance consolidation was introduced.

## Diplomacy and presentation

Settlement requests require a legal acceptance path before payment: an independent recipient outside EOR's faction, without an existing settlement, either at war with EOR above 35% surrender progress, or at peace and weaker than an EOR government that has neither capitulated nor entered civil war. Technological/custom-victory tests are removed. Eligible recipients can still refuse; refusal retains the existing extra 25 PP cost. Acceptance creates the existing non-aggression pact and one-year truce. Renewed war invalidates recognition. Coalition choices and settlements report full cooperation, limited support, refusal or acceptance. Contextual factors supplement AI weights; engine behavior remains unobserved.

Decisions are grouped into Court, Operations, Research and Prototypes, Overseas Administration, and Diplomacy. Categories have relevant dashboards and visibility gates. Construction, research, military and court actions use distinct native motifs; Yuriko and each great machine have dedicated semantic sprite aliases. The earlier category migration retained 83 actions; the approved playability pass adds 13, bringing the current inventory to 96.

All 149 country-spirit definitions have separately localized names/descriptions, using the native idea `name` override. This prevents focus/decision instructions from appearing as an active spirit description. Development balance notes are removed from spirit prose. Retained focus descriptions remain complete. The coup description and abandon option have separate keys. Event 60 now reports a government-policy settlement. Validation also found and corrected the same key collision in news.400 and news.401 without changing their effects.

The focus graph is preserved apart from discarded content and policy-milestone gates. Economics/overseas administration and manufacturing occupy a bank below the political/strategy area, with doctrine and experimental support underneath. Horizontal coordinates now span 0–65 instead of 4–147. Native 96×130 spacing and 165×128 rectangles pass overlap checks; every prerequisite points downward. The continuous panel is at (50, 5900), below the final row. Long root connectors and readability at the user's display scale still need visual runtime review.

## Narrative contract and artwork review

The opening states that this is the mod's alternate 2008 based on RA3's altered timeline. It assumes no mandatory RA3 campaign ending. No occupation/origin storyline or fourth political route was added. Suki reports evidence and uncertainty; Kenji advocates prototypes; Naomi asks for fuel, escorts and operational reach; Shinzo demands accountable command. Briefings acknowledge actual authorization and preparation rather than claiming an unperformed landing or capture. Revelation text distinguishes completed investigation, intercepted communications and verified evidence without a recorded provenance.

| Premise | Classification | Source / intended route |
| --- | --- | --- |
| Imperial commanders and Yoshiro/Tatsu's competing priorities | Established setting used by the supplied revision | [RA3 manual reference](https://static.wikia.nocookie.net/cnc_gamepedia_en/images/5/5c/RA3_Manual_-_Mac.pdf/revision/latest); all three routes |
| Evidence of Soviet intervention reaches the court | Campaign-specific development | Supplied revision S01/S17 and existing `eor.40`; discovery occurs through campaign conditions |
| Stable technical or military government and later policy settlement | Original mod extrapolation | S03/S05/S08; Tatsu or Shinzo, with Yoshiro restoration limited to the explicit stand-down |
| Great machines as temporary support and Yuriko as decisions | Gameplay abstraction, no added narrative continuity | Existing approved representation; common research programs |

The source references above are inherited from the design specification, not a claim of a new canon-source audit.

The [signature contact sheet](review/EOR_SIGNATURE_ICONS.png) was inspected using actual native textures at small display sizes. Castle/handshake symbols fit court/conspiracy; tools communicate construction. Soldier salute for Tatsu, radio for the mainframe, the weapon memorial for Yuriko, and generic troops/ships for great-machine deployment are **ambiguous**. Existing machine spirits/decision aliases also lack distinctive RA3 silhouettes. Their unique hashes do not establish semantic fit. Retained artwork was preserved; a coherent new signature set remains an optional art pass. Selected decisive scenes use registered native officer, treaty and laboratory imagery as deliberate fallbacks. Full event-window cropping and text fit remain unverified.

## Revision register

All source changes below pass source validation. Runtime results for **every item are pending user testing**. Optional work is identified separately instead of being represented as completed.

| ID | Implemented scope / files | Remaining gate or optional work |
| --- | --- | --- |
| S01 | Opening/contingent prose; localization, events, this lore table | Runtime reading and narrative review |
| S02 | No new objective tracker | Optional symbolic/practical target operation needs selected target, deadline and reward design |
| S03 | Command-failure/ultimatum prose and distinct peaceful/armed aftermath; events/localization | Test both takeovers; no new unapproved numeric penalties |
| S04 | Principal voices in major Imperial briefings and result reports; events/localization | In-game voice/readability review; dialogue uses existing identities and native fallback images |
| S05 | Removed fourth-route graph, decisions, events, character, spirits, icons and dependencies; manifest/validator | New-campaign check; no old-save migration |
| S06 | [Three source route schedules](EOR_ROUTE_SCHEDULES.md) including crisis and project waits | Optional duration/node tuning awaits comparable campaigns |
| S07 | Land-basing/carrier wording; localization | Optional hybrid maritime branch/carrier Tengu not implemented |
| S08 | Removed custom victory helpers/flags; rewired three policy milestones and settlement eligibility | Test ordinary capitulation/peace and milestones independently |
| S09 | Centralized newer economic pair; focuses/effects/ideas/art mappings | Compare actual before/after modifiers; balance provisional |
| S10 | Regime-first single authority tier, named government helpers and transition cleanup | Check low/middle/high values under all governments |
| S11 | Separate spirit-role localization and complete prose | Verify native name override and dynamic authority labels render |
| S12 | Replacement for economic/authority identities and countercoup cleanup | Optional wider consolidation and complete-build numerical audit not performed |
| S13 | Native signature contact sheet and semantic findings; unchanged retained artwork | Optional RA3 signature-art replacement and whole-inventory human review remain |
| S14 | Four categories, dashboards, semantic decision icon aliases | Runtime visibility, scroll and cooldown review |
| S15 | Position-only repack; manifest/native geometry checks | Inspect long connectors and display-scale usability |
| S16 | Coup key repaired; event 60 repurposed to policy feedback; validator | Verify full descriptions/options in game |
| S17 | Recorded evidence provenance, honest authorization text, selected native images, project/mission outcomes | Full longest-window rendering and all cancellation paths need engine checks |
| S18 | Shared recipient eligibility, contextual AI factors and diplomatic result reports | Strong peaceful, defeated wartime and incompatible-recipient trials |
| S19 | Complete former-subject cleanup and original-recipient investment checks | Test independence/overlord change during and after investment |
| S20 | Optional prepared/ready/active/recovering operation redesign implemented | Test peace during preparation, deliberate activation and full recovery |
| S21 | Two revalidated missions, distinct result/invalidation reports and shared cooldown | Test foothold loss, factory target loss and capitulation during preparation |
| S22 | Existing three allocations explained; grand-project release helper and target cleanup | Optional queue separation not implemented; verify reservation expiry |
| S23 | Explicit recipient building checks, original-capital persistence, EOR-scoped Philippines pressure | Static defects fixed; suspected engine behavior still requires before/after observation |
| S24 | No new superweapon operation | Optional Nanoswarm/Psionic Decimator need target, warning/counterplay, effects and cooldown design |
| S25 | Source/native phases, event-role regressions, inventory/economy/authority/subject/mission checks | Static passes do not establish engine execution, stability or balance |

## Validation and user test

Run `python3 tools/validate_eor.py --source-only` without a game installation. This checks script structure, graph/reference closure, inventories, role-specific prose and known semantic invariants. Default validation additionally checks the installed game's geometry, sprites, textures and modifier documentation. Missing native inputs are reported after the source phase, with the missing path. The old `eor.60` and `eor.102` collisions were also checked as negative regression fixtures and both are rejected.

After `python3 tools/setup_local.py`, run `python3 tools/validate_eor.py --installed "$HOME/Documents/Paradox Interactive/Hearts of Iron IV/mod/red_alert_3_development"`. Installed parity includes new script-localization/decision-sprite files and the adjacent news-key fixes. Event replacement/filtering and country-history compatibility remain in place. No diagnostic overlay belongs in this build.

Fully restart HOI4 yourself, choose **Red Alert 3 Development** with only **Red Alert 3 - Development**, and start a **new non-Ironman EOR campaign**. Use separate saves for the three governments.

1. Confirm only Yoshiro, Tatsu and Shinzo exist as political routes. Starting borders/deployments should match the accepted scenario; no automatic independence or state-return program appears. Inspect the two-bank tree, continuous panel and four decision categories.
2. Check authority at 15, 50 and 85 under each actual leader. Expect one tier with the appropriate government name; Tatsu/Shinzo use institutional legitimacy. Test both coup outcomes and the severe countercoup; old completed focuses remain visible without stale regime benefits.
3. In separate saves choose each economic branch. Expect exactly its newer corporate/state spirit and matching modifiers. Finish a government milestone without defeating every rival; normal play must continue and its continuing-policy decision must unlock.
4. Fund an IOT/PHI capital project. Keep the original capital controlled for successful construction, then repeat with lost control or independence in another save. Expect success versus invalidation reports and no reward on invalidation. The PHI administration action should reduce **EOR** pressure by five.
5. Finish a great-machine preparation at peace. Expect released factories and a ready asset, with no combat bonus yet. Activate during war; expect one timed bonus, then the documented recovery. Test each Yuriko mission and a target invalidated during its 30-day preparation.
6. Request settlements from an eligible strong/weak peaceful target and a badly defeated enemy; compare against a subject/faction partner or existing settlement. Only legal requests should charge PP; refusals remain possible and report their cost. Preserve logs if anything fails.

The user launches the game. This pass did not control the desktop, launch HOI4, commit, push or publish. Source/native/installed validation is not runtime confirmation; civil-war allocation, AI behavior, exact rendering and long-running campaign balance remain open.

### Observed validation for this revision

- Source phase passed, including a run with a deliberately unavailable game directory.
- Native phase passed against the local HOI4 installation.
- Negative regression fixtures rejected the original event 60 and 102 key collisions.
- Development synchronization applied 319 dated-history guards in 245 countries, retained 94 events, and filtered 4,144 inherited excluded-event references.
- Previous build/log backup: `development_backups/20261019-215804-484337/` in HOI4 user data.
- Installed source/native validation and byte parity passed; no startup/runtime diagnostic overlays were present.
- The revision input file was deleted after implementation and verification as requested. Its hash remains in the design manifest.
- Runtime tests were not performed; no game was launched.
