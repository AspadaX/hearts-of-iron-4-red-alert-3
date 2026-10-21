# EOR playability implementation — 19 October 2026

The user approved proceeding with the [playability review](review/EOR_PLAYABILITY_REVIEW.md). The authored build now has **189 focuses, 24 decisions, 77 EOR events, 107 active events overall and 149 country-spirit definitions**. The 19 October sections below describe the earlier 96-decision implementation; the [decision simplification](#decision-simplification-20-october-2026) at the end of this document supersedes their decision inventory. All quantities, costs, durations and modifiers remain provisional. No runtime playthrough was performed by the agent.

## Focus substance and pacing

Eleven focuses were removed: Restore Imperial Authority, Imperial Unity, The Silent Throne, Experimental Projects, Psionic Research, Executioner Heavy Robotics, Strategic Naval Fortress, Fall of the Kremlin and Fall of Allied Command, Prepare the Final Struggle and Silence the Court. Their prerequisite connections were rewired. Restored authority/unity benefits are combined in the surviving loyalist institution; preserved-throne terms are chosen through an event. The two achievement announcements now fire automatically once their existing operation/control/defeat conditions are met, with once-only guards and the former rewards. They do not change ordinary capitulation, peace or state ownership.

Most political administration now takes 21–35 days. Tatsu's actual installation, Shinzo's Military Government and the three policy milestones retain 70-day commitments. Yoshiro can reaffirm directly after Convene the Imperial Court. A new 75-PP Scheduled Court Review opens the succession debate after 60 days if no earlier crisis or route has settled it. It fabricates no intelligence evidence and requires neither defeat nor expansion. Revelation and defeat remain alternative crisis triggers. The historical focuses remain completed during explicit coup transitions.

Reconcile the Court offers a 75-PP technical advisory settlement (research support with continuing political overhead) or a 25-PP joint service compact (experience and planning). Tatsu remains an existing unique character with his military role and advisor eligibility. Preserve the Emperor chooses a ceremonial settlement (stability, political administration and legitimacy) or a scientific court (research, production learning and planning with legitimacy/military-influence costs). Abdication remains the exclusive alternative with its existing opposition risk.

Sacred Will opens a funded mobilization program or a subject-state industrial prestige project. They share a yearly authorization cooldown. Imperial Fortresses provides two construction grants: select Kanto, Kansai or Tokai; each uses three civilian factories for 90 days and supplies two land-fort levels at Tokyo/Osaka/Nagoya plus two state anti-air levels, subject to normal building caps. Each region can receive one grant. Province IDs are checked against the effective filename-merged state map.

Tatsu's doctrine choice opens either an armored equipment contract or a combined-force infantry/support contract. Shinzo's land/naval settlement opens armored/logistical readiness or conventional shipyard/repair readiness. His civilian-administration settlement trades military influence for stability and durable pressure relief. Continuing government programs deliver homeland construction/repair, scientific applications, or service readiness rather than the former small PP/XP rebates.

## Rewards and diplomacy

Divide Our Enemies no longer repeats the one-time event 105 or charges another 75 PP for it. It opens separate envoy preparations for SOV/USA/ENG/AOE: 75 PP and 60 days, one preparation at a time. A valid completion doubles the recipient's acceptance weight for a later settlement request for 180 days. The normal request cost, eligibility, refusal and cooldown still apply; preparation guarantees no pact or peace.

Resource Concessions directly delivers eight rubber to a controlled Malayan subject state and eight oil to a controlled Indonesian subject state, when each recipient is eligible. It adds ten subject pressure when a valid resource recipient exists. It no longer grants an unused authorization flag; availability requires an eligible recipient.

China cooperation and its follow-up focuses check current recipient conditions. Rejection leaves the existing renewed-offer decision; bilateral follow-ups stay unavailable without a partner. Research exchange is finite and bilateral, preserving the subject-only Imperial research group. The joint plan gives staff experience and temporary planning support. China evaluates relative strength, shared enemies and faction commitments. Requested extra concessions now present EOR with a separate 100-PP accept/decline event before any additional charge. Acceptance/refusal/protectorate reports confirm the result. Hostile or invalid relationships clear the historical partnership flag so renewed cooperation needs a fresh agreement.

Late equipment focuses keep practical rewards even if the technology is already known: initial Imperial Warrior, Tsunami, King Oni and coastal Tengu batches; Shogun shipyard support; and shared landing-support compensation. Fighter and VX service focuses deliver twenty-four aircraft each. Fighter/CAS terminal institutions replace their predecessors and preserve the earlier benefits while adding their own specialization. Shadow operations receive support equipment/command capacity; submarine consolidation receives naval experience and temporary repair support. Tengu/VX remain dedicated land-based aircraft.

## Prototypes and theater operations

The mainframe authorizes primary experimental selection directly. Each branch now has a **35-day program plus a 70-day prototype**, charging 50 PP in the program. The program grants an immediate lasting institution: scientific administration for Omega, procurement learning for Executioner or heavy-ship support for Giga Fortress. The expensive machine preparation decisions retain their costs, factory reservations and durations; completion produces readiness, followed by separate wartime activation and recovery. The refined Executioner choice adds 90 engineering days instead of 180. Giga's existing active support also includes shore-bombardment and naval coordination. No giant hybrid unit or new superweapon operation was added.

The [recomputed mixed route schedules](EOR_ROUTE_SCHEDULES.md) show 490 focus-days for the illustrated Yoshiro plan, 602 for Tatsu and 630 for bloodless Shinzo, plus documented review/event/decision waits. These are examples with common aircraft investment, not minimum completion times or observed game dates. The same equipment-to-primary-project example falls from 630 to 455 focus-days before machine preparation.

Odessa unlocks a paid 30-day preparation for 90 days of Soviet offensive and urban support. The northern event now explicitly chooses immediate readiness or a delayed 90-day preparation with stronger eventual staff support. The delay blocks the mod-authored northern war-goal/declaration path; it does not impose a general ban on other normal diplomatic actions. The delayed benefit rechecks the recipient and delivers once. Strategic Flexibility has command capacity and combined-service planning benefits instead of an extra PP penalty. The opening overseas recommendation yields a once-only 25-PP rebate when the matching policy is enacted.

Yuriko retains four missions and the shared cooldown. Sabotage now costs 75 PP, prepares for 30 days, damages two factory levels and applies 60 days of local resource/factory-sabotage disruption. Enemy control and military industry are rechecked; this remains targeted support rather than an army-destruction mechanic.

## Delivery and subject-management safeguards

New funded route programs recheck the actual route at completion and report invalidation after a government change. Prestige construction persists the original subject, rechecks that relationship and the selected state's ownership/control, then clears its event target. Fort grants are consumed on authorization and recheck government and full state control. Costs and grants are sunk on invalidation; timed factory reservations expire on schedule. Existing fixed-capital/original-recipient projects retain their safeguards.

Earned administrative relief subtracts from monthly pressure, capped at six. PHI/MAL administration, a shared centralization/partnership settlement, Shinzo's civilian settlement and the first successful prestige investment provide bounded awards; repeatable payments cannot grow it without limit. High-pressure unrest requires prior demands and a 60-day grace period, preventing both notices from first arriving on the same monthly tick. Cooperation/extraction costs remain different. No second subject-management resource or independent-partner exception was introduced.

## Scope differences from the proposal

The pass consolidates eleven nodes and upgrades the two air-service endpoint spirits; it does not reorganize every one of the 149 retained spirit definitions. No whole-tree numerical balance claim is made. Independent Chinese research uses finite exchanges rather than a new research group. Envoys improve existing settlement willingness rather than forcing a coalition member out. Primary project industrial preparation and recovery were retained; general queue separation was not added. Fixed-city homeland grants provide concrete fort construction without trying to infer arbitrary border provinces. The three political routes, accepted borders, 2008–2050 timeline, unique characters and normal HOI4 war outcomes remain the scenario constraints.

## Verification and user test

Observed checks:

- Source and native validation passed for the revised graph, inventories, event roles/references, government/recipient guards, geometry, equipment delivery IDs, fortress provinces, existing art and modifiers.
- A valid isolated source fixture passed. Four negative fixtures restored the duplicated diplomacy reward, independent China research-group mistake, ineffective known-Tengu reward and countercoup delivery exploit; all four were rejected by the validator.
- Development synchronization completed: 319 inherited history guards in 245 countries; 102 retained events; 4,144 excluded event references filtered.
- Installed source/native validation and authored-byte parity passed; no startup/runtime tracing overlays were present. `git diff --check` passed.
- The previous development build and available logs were preserved under `development_backups/20261019-231519-189921/` in HOI4 user data.
- Static checks do not prove engine execution, rendering, AI behavior or balance.

The user fully restarts HOI4, chooses **Red Alert 3 Development** with only **Red Alert 3 - Development**, and starts a **new non-Ironman EOR campaign**. Use separate saves for the governments.

1. After the court, confirm Yoshiro is available directly. In a successor save, fund Scheduled Court Review and wait 60 days; the debate should open without a war, defeat or invented Soviet evidence. Support military influence for the illustrated bloodless Shinzo route.
2. Try both reconciliation and preserved-throne terms in separate saves. Inspect costs and spirits. Tatsu must remain a unique commander; the monarchy choice must change practical benefits. An abandoned/armed coup must retain the accepted player side and standard civil-war behavior.
3. Complete an already-known equipment focus and inspect the stockpile. Select the fighter/CAS endpoint and check the predecessor is replaced. Tengu/VX should still require ordinary land-based air-wing deployment and never embark on carriers.
4. Fund a fortress grant, note its regional city, and wait 90 days. Expect forts/anti-air in that same region. Repeat with lost control or a government transition: no reward/refund, and the reservation ends on schedule. Try one of the route-specific equipment/readiness programs similarly.
5. Offer China cooperation: test full acceptance, requested concessions, refusal and a relationship invalidated by war. Extra 100-PP terms must require EOR consent; bilateral focuses require an actual partner and grant finite research support. Refusal should leave renewal available after its cooldown.
6. Complete Divide Our Enemies, prepare envoys to an eligible rival, then request a settlement. Preparation alone must not sign peace; the later request can still fail. Invalidate the target during preparation and expect no advantage/refund.
7. Choose a primary experimental program and verify its immediate institution. Complete the prototype, fund preparation at peace, then activate during war. Readiness/active/recovery exclusions remain. Test Yuriko sabotage with valid and invalidated targets.
8. Observe northern delayed readiness and Odessa support, then capture Moscow/defeat the relevant Allies after the operational prerequisites. Announcements should fire automatically once, without a celebration focus or automatic state transfer.
9. Complete subject-administration projects and inspect earned relief. Observe at least two demand cycles: relief is capped, severe unrest follows demands with a grace period, and invalidated subject investments grant no benefits.

No game/desktop control, commit, push or Workshop publication is part of this work. Long-running campaign stability and comparative balance remain unverified.


## China follow-up after user launch feedback

The user reported that the China focuses still appeared empty. The development copy matched the repository byte-for-byte and the launch configuration selected it. The source review found no unconditional reward preview for conditional bilateral rewards, and the coercive approach still had thin/duplicated rewards. Conditional preview behavior has not been visually confirmed by the agent.

All ten regional/China entry and branch focuses now have explicit unconditional reward text. Scripted delivery remains guarded. The subsequent self-audit restores native effect visibility alongside the explanatory preview; hiding the actual effect details was not an adequate fix. Regional Policy takes 14 days; China Question takes 21 days and adds an industry research bonus. Subjugate China now delivers staff experience, support equipment and planning support. The ultimatum takes 14 days; Chinese Campaign grants a China-specific offensive and bypasses after successful submission. Protectorate consolidation builds industry in the actual subject capital or an already owned/controlled Chinese core after annexation; it cannot award territory or reward another power's conquest. These quantities remain provisional.

The launch logs were preserved in `development_backups/china_focus_report_20261019_232058/`. They also reveal pre-existing aircraft archetype/parent parsing errors and an unsupported armor `manpower` unit bonus. These were separate compatibility findings, not a proven cause of the China reward display. Subsequent source corrections are documented in the [self-audit](review/EOR_SELF_AUDIT.md); fresh engine confirmation remains pending.

For the immediate display test: fully restart, start a new non-Ironman EOR campaign, open the tree and inspect Asian Accord, Subjugate China and Imperial Protectorate. Each should show its concrete reward summary before any prerequisites have been completed. Verify actual delivery in the appropriate accepted-partnership or conquest/subject state separately.

China follow-up synchronization: `development_backups/20261019-232304-253138/` preserves the preceding build and logs. Revised source/native/installed checks and authored-byte parity passed; native UI display and delivery remain pending user confirmation.

The later [self-audit](review/EOR_SELF_AUDIT.md) supersedes earlier hidden-effect, registration-order, starting-research, cooldown and country-picker details. It records the additional two-node consolidation and the remaining runtime evidence limits.

## Decision simplification (20 October 2026)

The user requested a smaller, clearer decision system. The active inventory is now **24 decisions in four categories**: Statecraft 9, Military Operations 6, Experimental Projects 4 and Overseas Administration 5. The 96-decision service, project, court, war-authorization, convoy, per-country investment and secondary-project lists are removed from loaded content and recorded in the manifest's removed list.

Statecraft retains scheduled court review, negotiated coup transition, post-defeat reconstruction, the Yoshiro fortress grant, China renewal and four settlement requests. Settlement requests cost 75 PP, consume `EOR_prepared_negotiation` when available, set a 180-day recipient preparation flag, and fire the recipient's existing event 114; refusal costs 15 PP. `EOR_imperial_diplomacy` sets the preparation flag instead of charging 75 PP, and event 105 no longer charges EOR before Chinese consent. Removed unilateral war, peace and reconstruction decisions are not replaced: normal declarations, wargoals, capitulation and peace conferences apply.

Military Operations keeps Yuriko's assault and sabotage missions, the three great-machine activations and the new `EOR_prepare_major_offensive`. The offensive preparation costs 75 PP, requires an ongoing war, prepares for 30 days and shares a 120-day authorization cooldown; its event `eor.156` offers Soviet, Pacific, general or Yuriko options. Experimental Projects keeps nanocore deployment and the three paid great-machine preparations. Overseas Administration keeps infrastructure investment plus one 120-day investment decision for each current subject — IOT, PHI, MAL and INS — whose events `eor.157`–`eor.160` offer an extraction or partnership settlement.

Focus rewards compensate for the removed programs: `EOR_military_government` grants administrative relief, the land and oceanic shogunates deliver immediate equipment/experience/timed support, the mobilization-law amendments grant permanent spirits and an instant factory, Odessa grants direct Soviet offensive support, and the sacred-will focus delivers a one-time manpower and equipment package. The active event catalog is **107 events overall and 77 EOR events**; `eor.156.desc` avoids collision with option `eor.156.d`.

The baseline EOR AI uses `common/ai_strategy_plans/EOR_default_strategy_plan.txt` for route-neutral focus and research weights and `common/ai_strategy/EOR.txt` for force ratios, production emphasis and subject support. It does not add a new route-selection mechanic; the existing focus weights still choose Yoshiro, Tatsu or Shinzo. AI behavior and campaign balance remain unverified until a user-run campaign.

Source, native and installed static checks pass with 189 focuses, 24 decisions and 107 active events. Runtime execution, decision visibility, investment delivery, settlement refusal and campaign balance remain unconfirmed; the user launches a fresh non-Ironman campaign.
