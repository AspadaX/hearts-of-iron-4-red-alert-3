# EOR playability review and proposed revision

Review date: 19 October 2026. **Historical review. The user subsequently approved proceeding with the fixes.** See [implementation scope and tests](../EOR_PLAYABILITY_IMPLEMENTATION.md) for what is now authored; the inventory and current-behavior findings below describe the pre-fix snapshot.

## Assessment

EOR has enough material for a substantial campaign, but its focus count overstates the number of meaningful things the player gets to do. The weakest areas are the long political consolidation chains, repeated equipment unlocks, the diplomacy finale, and experimental-project administration. Several well-named focuses deliver only another small modifier or permission to pay for a later reward. Adding more focuses would make this worse unless those focuses introduce different actions.

The review covers all 200 focus rewards and their prerequisites/availability, all 64 EOR event definitions, and the connected 83 decisions, government/economy/authority helpers, subject logic, technologies and spirits. It is a source review, not an observed playthrough. Existing uncommitted work was reviewed as the current design and left intact.

The source validator passes. This establishes structural/reference checks, not enjoyable pacing, AI competence, engine execution or numerical balance. There are 147 35-day focuses, 51 70-day focuses and two 14-day focuses. Of 64 EOR events, 35 have one option; many of these are useful delivery/activation/invalidation reports. Their single-option structure is appropriate and is not itself a defect. Conversely, `eor.60` has three scripted options but shows only the option matching the selected route: it is a policy report, not a three-way player choice.

Review standard: a focus is substantial when it changes a practical plan—equipment production, deployment, construction, diplomacy, political management or the timing of an operation. A small modifier can support that change. It rarely justifies a long mandatory step on its own. A gate that prevents premature access can be useful, but repeated gates should not consume most of a branch.

Keep the stronger foundations: the corporate/state economic trade-offs, resource-security alternatives, common manufacturers, nanocore construction tools, mutually exclusive opening theaters with later reassessment, Shinzo's coup, and deliberate special-asset activation. These already connect national development to practical choices. They need targeted improvements, not wholesale replacement.

## Findings, in priority order

### 1. A diplomacy focus has no additional reward

`EOR_imperial_diplomacy` and its direct successor `EOR_divide_our_enemies` each cost 35 days and subtract 75 PP, then call `eor_event_105`. That helper fires only once. After the prerequisite's event has fired, Divide Our Enemies delivers no additional effect. The first event also subtracts 25 PP, making the pair cost 175 PP for one negotiation authorization.

Evidence: `common/national_focus/empire_focus.txt:3934`, `:3953`; `common/scripted_effects/eor_effects.txt:366`; `events/EmpireOfTheRisingSun.txt`, event 105.

**Proposal:** retain Imperial Diplomacy as the settlement unlock. Replace Divide Our Enemies with a distinct, targeted diplomatic action: spend PP and an intelligence preparation period to improve the chance of a separate agreement with one eligible rival. The recipient still decides. On success, use the existing normal pact/settlement framework; on refusal, report the result and apply a cooldown. If that new action is not desired, merge the two focuses and remove the second payment. Do not retain an empty node for visual symmetry.

There is a second direct reward defect in **Resource Concessions** (`common/national_focus/empire_focus.txt:2126`). Its 35-day reward raises subject pressure by 10 and sets `EOR_resource_development_authorized`, which has no located gameplay reader. Resource development decisions already open at Resource Security Program. It therefore supplies a penalty and a prerequisite step, without its own practical concession. Replace the unused authorization with an actual limited resource contract or fold it into Overseas Extraction; preserve the pressure cost only when an extraction benefit is delivered.

### 2. China's cooperation branch can continue without cooperation

Asian Accord, Joint Military Plan and Partners in Asia do not require China to have accepted the offer in their availability conditions. After refusal, the player can keep taking focuses whose international rewards are skipped. Joint Military Plan also repeats military access already granted by an accepted offer. Partners in Asia tries to put CHI into `imperial_research`, but that group's availability admits only EOR and its subjects. That reward is incompatible with an independent Chinese partner.

China's response AI is also almost entirely a fixed lottery: cooperation uses 45/35/20 weights; submission uses 15/85. Relative power and political circumstances do not alter those weights.

Evidence: `common/national_focus/empire_focus.txt`, China branch, especially `:1504`; `events/EmpireOfTheRisingSun.txt`, events 110–111; `common/technology_sharing/01_tech_sharing_groups.txt`.

**Proposal:** require a current, valid Chinese partnership for bilateral follow-ups. Give refusal a visible renegotiation/reorientation path rather than letting the player buy ineffective cooperation. Make Joint Military Plan deliver an actual joint exercise and a military planning benefit instead of another access grant. Replace independent CHI's research-group entry with a bilateral, finite research exchange; preserve the accepted subject-only group rule. Make offer/submission acceptance depend on strength, ongoing wars and existing relationships, with the criteria explained before the offer. Add an EOR-facing response report identifying acceptance, concessions or refusal and the actual terms.

### 3. Yoshiro has too many 70-day steps with little practical change

Examples:

| Focus | Current outcome | Problem |
| --- | --- | --- |
| Restore Imperial Authority | +5 percentage points stability, +5% PP gain | A long generic administrative step |
| Reconcile the Court | +5 points stability, -75 PP, +10 technocratic/+5 military influence | No court settlement or new institution to interact with |
| Imperial Unity | +5 points stability, +5% recruitable-population factor | Another passive step after reconciliation |
| The Emperor's Sacred Will | +5 mandate/+5 legitimacy; prestige decision | The decision then charges 100 PP and reserves three civilian factories for 90 days for another +5/+5 |
| Imperial Fortresses | Faster land/coastal fort construction, +3% core defence | Does not actually build a fortress or select a defensive program |

Evidence: `common/national_focus/empire_focus.txt:170`, `:237`, `:261`, `:282`, `:369`; `common/decisions/eor_decisions.txt:110`; corresponding ideas in `common/ideas/eor_v2_ideas.txt`.

Mandate also starts at 75 and rises through route selection, discoveries and conquest. Additional small positive rewards can be capped away, especially during successful campaigns. That makes some already thin rewards less visible.

**Proposal:** consolidate Restore Authority/Reconcile Court/Imperial Unity into fewer institutional steps. Give reconciliation a negotiated court settlement that preserves Tatsu's advisory contribution at a recurring political cost, while the purge alternative offers faster command cohesion with its existing research/personnel consequences. Do not remove his military character role. Make Sacred Will unlock a choice of a domestic mobilization program or an overseas prestige investment, each with a concrete deliverable as well as authority. Make Imperial Fortresses fund a limited, player-selected homeland construction program, with ordinary ownership/control checks. Keep route identity around sacred authority, resilience and mobilization; avoid making it merely a weaker research route.

### 4. Tatsu's monarchy settlement is repetitive and only weakly differentiated

Preserve the Emperor takes 70 days for +5 points stability and a flag already set by Tatsu's installation event. The Silent Throne takes another 70 days for +5 points stability and a spirit giving +3% PP gain but -2% research speed. This can represent a compromise, but the player spends 140 days without getting a new policy to pursue.

Evidence: `common/national_focus/empire_focus.txt:503`, `:525`; event 42; `common/ideas/eor_v2_ideas.txt:50`.

**Proposal:** make this one monarchy-settlement focus with a real event choosing the terms of the preserved throne. A ceremonial settlement protects legitimacy and reduces traditionalist opposition at an administrative cost; abdication offers greater executive control with the existing opposition risk. Then let technical government choose and fund a military-industrial modernization program. Automated Warfare should emphasize expensive equipment replacing manpower; Human-Machine Doctrine should emphasize training, organization and adaptable mixed forces. Give each a visible funded deliverable instead of spreading its identity across many small permanent spirits.

### 5. Shinzo has the strongest transition, but a thinner government afterward

The bloodless/negotiated/armed coup structure changes what the player does and risks. It is worth keeping. Army versus navy supremacy also has meaningful production trade-offs. However, The Land Shogunate is another 70 days for +5% armor speed and -3% supply consumption; subsequent consolidation tends to return to passive bonuses.

Evidence: Shinzo branch in `common/national_focus/empire_focus.txt`, especially `:876`; events 100–109; coup helpers.

**Proposal:** retain the coup and the army/navy priority choice. Make the follow-up a funded service program: armor/refit and land logistics for the army; fleet repair, escort preparation and amphibious planning for the navy. Add a limited civilian-administration settlement after consolidation, connecting military rule's extraction benefits to its subject-pressure cost. Do not introduce a new route, daily government enforcement or forced border changes.

### 6. Several equipment and doctrine focuses repeat earlier access

Transformable Aircraft already unlocks both Tengu and VX. Mecha Tengu Squadrons later unlocks the same Tengu technology and adds only 20 air XP. Shirada Shipworks already unlocks Shogun battleships; Shogun Battleship Program unlocks the same technology later, although it also opens a paid construction-support decision. Tsunami tanks have multiple access paths, and King Oni can be researched through a decision before the army focus. Alternate access is useful; repeating the same unlock without compensation is not.

There are also weak terminal rewards: Dominate the Skies grants only +5% interception efficiency; Support the Army grants +3% CAS presence and efficiency. Neither creates a convincing culmination of its branch.

Evidence: `common/national_focus/empire_focus.txt:2297`, `:2779`, `:2892`, `:3117`, `:3191`; common-aircraft focus and research/procurement decisions.

**Proposal:** keep common equipment access independent of political/doctrine choice. Convert later focuses into specialization and service introduction: a finite production incentive, funded initial procurement, training support, or a practical equipment improvement. Provide an appropriate alternate reward when the technology is already known. Rework the carrier-chain Tengu node as land-based coastal air/fleet coordination, explicitly keeping Tengu off carriers. Give the fighter and CAS endpoints a substantial service program, using an upgraded branch spirit rather than another tiny additive badge.

### 7. Grand projects charge for too many permissions before anything arrives

Experimental Projects costs 70 days and 100 PP merely to authorize the next branch. Each primary project then has three 70-day focuses before a further paid decision. Giga Fortress's complete sequence after the mainframe costs 280 focus-days, 400 PP in focus rewards, then 200 PP and 240 preparation days, with eight civilian factories reserved and -10% military output during preparation. The resulting 90-day support grants +10% capital-ship attack/+10% air attack with a fuel-gain penalty, followed by 540 days of recovery. That may be balanced numerically, but its practical payoff is modest relative to the theatrical presentation and repeated waiting.

The documented mixed equipment/project plan takes 630 focus-days before machine preparation, excluding political/economic detours. This is an example plan, not the earliest possible route. Likewise, the route schedules' 889–945 focus-days are example mixed plans, not mandatory minimums.

Evidence: `common/national_focus/empire_focus.txt:3294`, `:3430`, `:3450`, `:3469`; project decisions and spirits; `docs/EOR_ROUTE_SCHEDULES.md`.

**Proposal:** fold general authorization into the mainframe and reduce each project to a meaningful program choice plus one prototype milestone. Put the substantial industrial cost and wait into the existing preparation decision. Give each prototype a small lasting practical benefit, so the branch has value before activation. Keep prepared/ready/active/recovering stages and deliberate wartime activation. Make activated support better match its role through a bounded, clearly explained operation; numerical changes require comparison with normal investment in tanks, aircraft or ships. Do not promise giant map units, transformation, new hybrid equipment or unapproved superweapon operations.

### 8. Political access favors crisis engineering over an understandable opening

Question of Destiny needs a succession crisis. That crisis depends on discoveries, low legitimacy, major defeat or completed intelligence plus threat. A healthy peaceful empire has no straightforward route-selection timetable. The peaceful intelligence approach is real, but it is a 100-PP, three-factory, 120-day investigation gated by threat above 19; another investigation takes 180 days and requires deeper institute investment. For a player expecting to choose Tatsu or Shinzo at the start, the tree provides a potentially long and indirect wait.

Evidence: `common/scripted_effects/eor_effects.txt:189`; `common/decisions/eor_decisions.txt:536`; Question of Destiny availability.

**Proposal:** show the crisis requirements and investigation path prominently at the opening. My preferred design change is a deliberate court-review path after the opening that can begin the succession debate at a known cost and duration, without requiring defeat or expansion. Keep revelation/defeat as alternative triggers with different event context. Allow Yoshiro's basic loyalist consolidation without manufacturing a succession emergency. This changes political pacing and needs the user's design decision before implementation.

### 9. Some event choices describe more than they actually change

In event 4, Strategic Flexibility gives 10 army/10 navy XP and charges 25 PP, while continental priority gives 20 army XP plus a temporary coordination spirit, and naval priority gives 20 navy XP plus a research bonus. Flexibility lacks a distinct compensating advantage. In event 10, both choices grant the same preparation spirit, but Continue Preparations additionally grants XP; Begin the Offensive sets a flag with no located gameplay reader and raises world tension. Its wording suggests an actual offensive begins, but the war goal and declaration are elsewhere. Event 50's centralization/partnership preference flags have no located gameplay readers, so the expressed preference does not define the later administrative policy.

Evidence: events 4, 10, 50; loaded `common/` and `events/` references to `EOR_soviet_operations`, `EOR_preference_centralization`, `EOR_preference_partnership`.

**Proposal:** make flexibility a real reserve/combined-service choice; make event 10 explicitly choose immediate operational readiness versus a delayed, stronger preparation, with costs and timing enforced across supported declaration paths. Make event 50 advisory wording explicit, or let its preference alter the later policy negotiation. Keep descriptive reports as reports, but ensure events presented as decisions have different practical consequences and follow-up acknowledgement.

### 10. Wartime focuses can miss the moment they are supposed to represent

Odessa Operation takes 35 days for 15 army XP and a flag; its later capture reward is another authority/XP payout. Other campaign nodes mostly grant national preparation/logistics modifiers. Capture/defeat-gated celebration focuses make the player spend another 35 days after the achievement for political rewards. These are weak incentives to stop military development during the campaign.

Evidence: Soviet/Allied branches, especially `common/national_focus/empire_focus.txt:1167`; capture checks in `eor_daily_update`.

**Proposal:** use automatic events for simple capture celebrations. Use campaign focuses to authorize practical logistics, repair and preparations before the operation, with player-triggered timed benefits. Give Odessa a regional support operation instead of an objective flag and XP. Keep normal wars, capitulation and peace conferences; rewards must not automatically transfer states or establish custom victory gates.

### 11. Subject management risks becoming a repeated maintenance payment

Monthly pressure rises by 2 normally, another 3 for centralization, another 3 for overseas extraction, and another 3 under Shinzo; partnership subtracts 4. Centralized extraction under Shinzo therefore produces +11/month before player interventions. At high pressure, both demands and unrest can fire on the same monthly tick, each with a 180-day cooldown. Available responses mostly pay PP, equipment or factory time to reduce the same global number. Cooperative and coercive administration differ, but the repeated crisis can become a tax instead of a changing political situation.

Evidence: `common/scripted_effects/eor_effects.txt:250`; events 51–52; overseas decisions.

**Proposal:** preserve the existing single pressure system initially. Give completed subject development and administrative settlements durable, bounded pressure relief, rather than requiring the same payment indefinitely. Stage demands before severe unrest instead of routinely delivering both together; make the affected subject and reason clear. Give centralization a visible extraction reward worth managing and partnership a tangible logistical/research return. Avoid adding a second subject-management resource unless campaign tests show the current system cannot support this.

### 12. Route endpoints and repeatable programs are uneven

All three milestones have the same direct reward: 200 PP, +5 points stability and event 60. That event provides different route benefits, but the continuing programs are unequal: the Imperial program costs 75 PP and three factories for 180 days to return 25 PP and +3 points stability; science delivers two research bonuses; military delivers 25 army XP and +3 points stability. The Imperial prestige project competes for the same investment reservation. These programs do not provide equally compelling reasons to continue managing each government.

Evidence: the three government-policy milestones; event 60; `common/decisions/eor_decisions.txt:21` and continuing science/military programs.

**Proposal:** retain ordinary government-policy milestones. Give each a distinct continuing policy: Yoshiro chooses mobilization or homeland resilience; Tatsu funds an industrial/research application; Shinzo funds a service-readiness campaign. Give each a useful concrete deliverable and an explicit cost, with no mandatory victory targets. Preserve meaningful investment competition, but consider separate administrative and construction capacity only after shorter project chains have been tested.

## Proposed implementation batches

All new policies, event outcomes and numbers below are proposed design, not accepted content. Preserve three routes, starting borders, 2008–2050, unique characters, common equipment availability and standard HOI4 war resolution.

1. **Reward integrity and communication.** Resolve duplicate event 105 use, Resource Concessions' unused authorization, Chinese follow-up eligibility/research exchange, equipment-already-known rewards, and misleading event labels. Add focused source checks for each corrected case. This removes wasted selections before broader balance work.
2. **Yoshiro and Tatsu political substance.** Settle the intended early political access, consolidate repetitive court nodes, and implement one substantive court-settlement chain per route. Keep Shinzo's coup; add its practical government follow-up in the same review of political pacing. Proposed duration rule: routine steps 14–35 days, 70 days reserved for transformations with substantial immediate benefits. Do not cut every focus indiscriminately.
3. **Military service programs.** Replace repeated unlocks and weak doctrine endpoints with procurement, production, training or logistical outcomes. Consolidate sequential small spirits into readable upgraded spirits. Keep real doctrine trade-offs and alternate equipment access.
4. **Experimental projects.** Remove repeated authorization fees/waits, retain industrial preparation/readiness/activation/recovery, and compare each program with conventional production. Yuriko's four missions stay; review the sabotage reward in particular—100 PP, 30 preparation days and the shared 180-day cooldown currently buy one level of military-factory damage.
5. **Campaign and overseas consequences.** Move simple celebrations into automatic reports, improve theater operations and diplomatic responses, then tune subject-pressure progression and government continuing programs.

Do not preserve 200 focuses as a target. A shorter tree with distinct choices is preferable. Also do not force an event onto every focus: construction, equipment access and useful operational tools can be substantial without a popup.

## Verification after an approved revision

Run source validation, relevant native checks, local synchronization and installed validation. The user then fully restarts HOI4 with Red Alert 3 Development and starts new non-Ironman EOR campaigns. No game or desktop was controlled for this review.

Use separate Yoshiro, Tatsu and Shinzo saves. Record first route availability, first distinctive route action, first substantial war, first usable special asset and total PP/factory commitments. Test China acceptance and refusal, already-known equipment, delayed war activation, and subject pressure through at least two demand cycles. Compare roughly equal calendar dates and investment, rather than comparing an untouched start against a completed branch. Runtime success and campaign balance remain unverified until these tests.
