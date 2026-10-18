# Rising Sun V2 implementation

The revised design contains 213 focuses, 85 decisions and 43 EOR events (73 active events overall). All focus icons use distinct artwork textures. Numerical costs, thresholds, durations and AI weights are provisional. Static checks do not establish successful engine loading, stability or balance.

## Political progression

EOR starts in 2008 under Yoshiro. Imperial legitimacy begins at 75, technocratic influence at 30 and military influence at 40. These pools are independent and bounded to 0–100. The older Divine Mandate system is retained separately. Court choices, advisors, research, campaign results and political events affect progression. Combat influence changes share a country-wide 30-day cooldown.

The crisis can emerge from time-travel evidence, low legitimacy, strategic defeat or an escalated-war intelligence investigation. The ordinary political roots are mutually exclusive: Yoshiro's divine monarchy, Tatsu's technocracy, Shinzo's military government and hidden New Dawn. Each contains internal choices. The secret route requires legitimacy below 30, administrative pressure above 39, defeat or stability below 30%, and support for a reform movement. Reform establishes an elected democratic council and chooses a ceremonial monarchy or republic.

Shinzo can negotiate, seize power peacefully with strong military support, or start an actual civil war. The player remains fascist EOR under Shinzo. Non-aligned loyalists receive the same Yoshiro character, not a duplicate. Stronger conspirators face a 25% loyalist land/air split based in Tokyo; weak conspirators face 45% based in Tokyo, Osaka and Nagoya. Naval shares are 20%/40%. Consolidation requires defeating actual loyalists. These partition sizes need runtime and balance review.

Two explicit later transitions exist: abandoning the conspiracy restores Yoshiro, while a severe technocratic counterconspiracy can install Shinzo. Completed focuses remain historical, but unfinished descendants require the currently active government. Tatsu and Shinzo retain their military identities when taking political roles.

## Strategy, economy and warfare

Northern Thunder, Pacific Storm and Consolidate Asia select the first theater. Global Reassessment permits later campaigns after meaningful progress, defeat or a major opponent's defeat. Conquest branches are unavailable under reform. China can accept cooperation, demand concessions or refuse; submission has its own acceptance/refusal chain. Reform offers equal partnership.

Corporate/state economics, three resource policies, three army doctrines, three naval doctrines and two air doctrines have real exclusions and trade-offs. Political preferences grant modest discounts; incompatible combinations require concessions. Ordinary Imperial equipment remains available through common manufacturers and paid development decisions, independent of doctrine specialization.

Coalition negotiations depend on accumulated threat rather than a fixed date. Rival powers can cooperate fully, partially or refuse. Individual Tatsu settlements require accepted negotiations under strength/peace or surrender conditions; acceptance establishes a non-aggression pact and a one-year truce. War invalidates settlement recognition.

Yoshiro's victory requires his completed route, secure homeland and defeated rivals. Tatsu needs technological achievement and defeated or individually settled rivals. Shinzo needs consolidated military government and major victories. New Dawn needs constitutional reconstruction, completed decolonization, a secure retained homeland and at least two independent voluntary partners. No single captured capital grants every victory.

## Equipment and operations

Existing Imperial Warrior, Tsunami, King Oni, Wave-Force and Shogun equipment stays in production. Tengu and Striker-VX use the approved dedicated fighter/CAS equipment representation. Rocket Angels use paratrooper improvements; Tankbusters use infantry anti-tank improvements; Shinobi use intelligence/special forces; Yari uses submarine research and doctrine. These are engine representations, not native transforming units.

Executioner, Giga Fortress and Black Tortoise are costly preparation/deployment operations with finite duration, shared preparation queues and long cooldowns. Initial grand projects exclude one another. A secondary-program exception requires 60 military and 40 civilian factories, 300 PP, eight reserved civilian factories, an output penalty and 360 days. Yuriko remains one decision-based operative with shared mission cooldowns. Nanocores and overseas investments reserve factories and recheck ownership/control at completion.

## Decolonization and overseas administration

Subject pressure, investment and policy bonuses apply to current dependencies and are removed after independence. Native occupation resistance cannot model unrest on subject-owned cores, so administrative pressure and stability penalties supply that representation. IOT uses the complete generic focus tree.

The New Dawn decolonization focus also performs these explicitly approved direct territorial handovers:

| Recipient | State IDs |
| --- | --- |
| China (Taiwan) | 524 |
| Korea | 525, 527, 1028, 1029, 1030, 1031 |
| Vietnam | 286, 671, 1017, 1066 |
| Laos | 670, 1068, 1069 |
| Cambodia | 741, 1067 |
| USA (Hawaii, Johnston, Midway, Wake, Guam, Saipan) | 629, 630, 631, 632, 638, 646 |
| Soviet Union (Sakhalin and Kurils) | 537, 555, 655 |
| Independent Oceanic Territories (remaining overseas islands, including Timor) | 270, 633, 635, 636, 639, 641, 642, 643, 647, 648, 684, 721, 725, 727, 734, 1071 |

Handovers require EOR ownership and full control, peace with the recipient, and a recipient independent or subject to EOR. EOR dependencies receiving direct handovers are freed; third-party overlords are not overridden. Delayed handovers can be retried through Renew Independence Negotiations. Former direct holdings lose EOR cores/claims and homeland-security flags when transferred. Starting borders are unchanged. The legacy filename `555-Lagos.txt` contains the Kurils; no Nigerian state is transferred.

Remaining subjects receive independence offers and may accept a voluntary alliance, choose independence outside it, or request further negotiations. Restored regional countries can receive voluntary Asian Congress invitations. The reform ending stays blocked while any specified direct holding remains EOR-owned, any subject remains, or an initial subject is an enemy. Membership is recounted daily.

## Presentation and validation

All 213 icons are checked for unique texture hashes and valid installed assets. The 96×130 native focus grid and 165×128 item rectangles have no overlaps; prerequisites point downward. The continuous panel is at (50, 3500), below the last row with a clear gap. The country picker uses a short paragraph. Exact appearance at the user's UI scale needs runtime review.

Run `python3 tools/validate_eor.py`. After `python3 tools/setup_local.py`, run the validator with `--installed` and the development mod path. Checks cover focus inventory and structural reachability, exclusions, four endings, layout, artwork, localization, modifiers, event closure, characters, civil-war wiring, territorial mappings, IOT selection and source/build parity.

Fully restart HOI4. Select **Red Alert 3 Development** with only **Red Alert 3 - Development** enabled and start a **new non-Ironman campaign**.

1. As EOR, inspect the picker and all political branches. Scroll below the main tree: continuous focuses must not cover any node. Check unique icons and the influence dashboard.
2. In separate saves, test Yoshiro, Tatsu, Shinzo and secret reform. Check normal route exclusions and active-government requirements. Test both peaceful and armed coups; EOR should remain the player country under Shinzo.
3. For New Dawn, finish decolonization. Taiwan must pass to CHI, the other listed holdings to their recipients, and IOT become independent. Retry delayed handovers after restoring control/peace. Check voluntary subject responses and the two-partner victory gate.
4. Test equipment unlocks, paid construction, experimental preparation/deployment, cooldowns and subject investments. Confirm lost subjects lose Imperial benefits.
5. Start a separate new IOT campaign and confirm its industry, army and political generic branches appear.

Loading, event execution, civil-war allocation, AI choices, exact rendering and long-running balance still require user runtime confirmation. No game or desktop control, commit, push or publishing was performed.

## Spirit artwork, focus prose and connected support branches (2026-10-18)

All 156 Imperial country spirits now have separate, reviewed native idea textures, registered in `interface/eor_spirit_icons.gfx`. Artwork depicts the corresponding government, production, research, resource, military or administrative theme. The five Mandate tiers have distinct political symbols. Manufacturer and advisor definitions are preserved.

All 213 focus descriptions are complete prose explaining the purpose of the node. Numerical effects remain in the engine-generated reward panel. The manifest stores the reviewed descriptions; validation rejects the former fragments and generic filler.

Mobilization now merges the completed corporate or state economic branch before its two amendments. The Weaponry Institute follows the high-tech company dialogue, and nanoconstruction/robotic production lead from the institute into a single experimental subtree. Army landing and terrain support sit beside the main army doctrine choices as a common support branch. Overseas logistics merges the centralized or cooperative administration branches, then leads to Oceanic development and co-development. Equal partnership with China sits beside New Dawn's diplomacy.

These prerequisite changes require a full restart and a new non-Ironman EOR campaign. Check the starting spirits, both economic paths into mobilization, the research/experimental sequence, and overseas development. The newly added icon registration is included in installed-source parity checks. Exact rendering still needs in-game confirmation.
