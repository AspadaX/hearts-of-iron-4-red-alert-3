# Soviet Union — National Focus Tree and Narrative Design

## Red Alert 3 × Hearts of Iron IV

**Status:** Design specification  
**Scenario start:** January 1, 2008  
**Country:** Soviet Union (`SOV`)  
**Faction:** The Comintern  
**Political routes:** Cherdenko, Krukov, Commander/Dasha  
**Scope:** Soviet Union only

---

# 1. Design Principles

The Soviet Union begins as the strongest continental military power in the world, having conquered most of Europe.

However, Soviet military expansion has created three strategic problems:

1. The occupied European and Scandinavian territories remain politically unstable.
2. The Soviet Navy is significantly weaker than the navies of its principal rivals.
3. The Kremlin is divided between competing visions for the future of the Soviet Union.

The national focus tree must allow players to resolve these challenges through different political, diplomatic, economic, and military strategies.

## 1.1 Core Gameplay Identity

**Strengths**

- The strongest starting land forces among the three major powers.
- Powerful armored warfare and artillery.
- An extensive continental industrial base.
- Vast natural resources.
- Strong offensive potential.
- Strategic depth across the Soviet heartland.

**Weaknesses**

- The weakest starting navy among the major powers.
- Political instability within the Soviet leadership.
- Heavy administrative burdens associated with European occupation.
- Vulnerable logistics across enormous distances.
- Technological disadvantages against certain Imperial weapons.
- Difficulty projecting military power overseas.

## 1.2 Fixed Scenario Requirements

The following decisions are mandatory:

1. The Soviet faction is named **The Comintern**, replacing "The Soviet Republic".
2. Mongolia remains an independent member of the Comintern. It is not annexed or converted into a Soviet puppet.
3. The Soviet Union maintains two occupation zones at game start:
   - `SOE`: Soviet Occupation Zone in Europe.
   - `SOS`: Soviet Occupation Zone in Scandinavia.
4. Both occupation zones initially remain Soviet subjects.
5. Both occupation zones retain their existing generic focus trees.
6. Occupation-zone administration and political reorganization are handled through the **Soviet national focus tree**, events, and decisions.
7. Three mutually exclusive Soviet political routes are available:
   - Premier Anatoly Cherdenko.
   - General Nikolai Krukov.
   - The Soviet Commander, supported by Dasha Fedorovich.
8. Each political route determines a fundamentally different future for the occupation zones.
9. The United States is not an Allied faction member at scenario start. Any necessary scenario correction is separate from this Soviet-only focus design.
10. Military victory continues to use ordinary HOI4 war, capitulation, faction, and peace mechanics. There is no custom victory system.

---

# 2. Historical and RA3 Lore Foundation

## 2.1 The Altered Timeline

In the original Red Alert 3 storyline, Soviet leaders travel into the past and remove Albert Einstein from history, seeking to prevent the technological dominance of the Allied Nations.

The resulting timeline dramatically changes the geopolitical balance and gives rise to the Empire of the Rising Sun.

This mod begins with the Soviet Union having conquered most of continental Europe.

The remaining Allied forces hold only a limited European enclave, while overseas Allied countries continue resisting Soviet expansion.

The Empire of the Rising Sun constitutes a major threat to the Soviet Union's eastern territories.

The Soviet Union therefore faces the danger of overextension despite its formidable military power.

## 2.2 Soviet Political Leadership

### Premier Anatoly Cherdenko

Cherdenko represents authoritarian centralization, aggressive military expansion, and personal control over the Soviet state.

His political route is based on the premise that the revolution can be secured only through Soviet military domination.

### General Nikolai Krukov

Krukov represents military authority, strategic realism, and a disciplined approach to Soviet national security.

His proposed military-government and peace route is an alternative-history interpretation, not a canonical RA3 campaign ending.

He believes that continuously expanding Soviet territory will eventually exhaust the Red Army and destroy the state.

### The Soviet Commander and Dasha Fedorovich

The Commander is the Soviet campaign's player character.

Dasha serves as an intelligence officer, political liaison, and trusted adviser.

Their route takes inspiration from the original campaign's overthrow of Cherdenko, but develops an original reformist political direction.

The Commander seeks to renew the socialist revolution by rejecting compulsory territorial expansion and building an international community of independent communist nations.

This is the most optimistic political route in the mod.

---

# 3. Starting Soviet Situation

## 3.1 Territorial Structure

At game start:

- The Soviet Union controls its extensive core territories.
- Mongolia remains a Comintern member.
- The Soviet Occupation Zone in Europe administers most conquered European territories.
- The Soviet Occupation Zone in Scandinavia administers the occupied Scandinavian territories.
- Only a small Allied-controlled area remains in continental Europe.

The occupation zones are administrative formations, not permanent national identities.

Their eventual political fate depends on the Soviet political route.

## 3.2 Starting National Spirits

### The Red Army Triumphant

**Description:**

> From the plains of Eastern Europe to the conquered industrial cities of the West, the Red Army has demonstrated its superiority over every continental adversary. Yet the weight of victory now threatens to become a burden.

**Proposed effects:**

- Division attack: +10%.
- Organization recovery: +10%.
- Land doctrine research bonus.

### A Continent Under Occupation

**Description:**

> Our victories in Europe have placed millions of unwilling citizens under Soviet administration. Factories must be restored, resistance movements suppressed, and the loyalty of local governments secured.

**Proposed effects:**

- Political power gain: -15%.
- Stability: -10%.
- Occupation administration costs.

The severity of this spirit may decrease as the occupation zones become stable.

### The Red Fleet's Deficiencies

**Description:**

> Soviet military doctrine has historically emphasized continental warfare. Our naval forces remain poorly equipped to challenge the formidable fleets protecting our enemies' overseas territories.

**Proposed effects:**

- Naval organization: -15%.
- Dockyard output: -10%.

### Fractured Supreme Command

**Description:**

> The Premier, the General Staff, and an increasingly influential generation of officers are divided over the future of the Soviet Union.

**Proposed effects:**

- Planning speed: -10%.
- Stability: -5%.

Removed or replaced through the chosen political route.

### Soviet Industrial Colossus

**Description:**

> A vast network of factories, mining operations, and armament facilities sustains the Soviet war machine.

**Proposed effects:**

- Military factory output: +10%.

---

# 4. National Focus Tree Architecture

The Soviet national focus tree consists of seven major sections.

```text
                        THE RED CONTINENT
                                |
                       THE BURDEN OF VICTORY
                                |
                      THE KREMLIN DIVIDED
                                |
                      THE FUTURE OF THE UNION
                                |
             +------------------+------------------+
             |                  |                  |
       CHERDENKO             KRUKOV          COMMANDER/DASHA
             |                  |                  |
      ABSOLUTE POWER      MILITARY RULE      NEW REVOLUTION
             |                  |                  |
       DIRECT CONTROL     PUPPET STATES      INDEPENDENCE
             |                  |                  |
      WORLD CONQUEST       ARMED PEACE       WORLD REVOLUTION


  SHARED BRANCHES (AVAILABLE TO ALL THREE ROUTES)

  +------------------+------------------+
  |                  |                  |
  OCCUPATION       RED ARMY          RED NAVY
  MANAGEMENT

  +------------------+------------------+
  |                  |                  |
  AIR FORCES        INDUSTRY          TECHNOLOGY

  +-------------------------------------+
  |
  FOREIGN STRATEGY
  |
  +------------------+------------------+
  |                                     |
  EASTERN FRONT                       OVERSEAS WAR
```

**Important:** The opening political focuses do not block access to military, economic, research, or occupation-management focuses.

Only the three political routes are mutually exclusive.

The occupation-zone outcomes are determined by political focuses, not by separate SOE or SOS focus trees.

---

# 5. Political Opening — The Kremlin Divided

## Focus 1: The Red Continent

**Description:**

> From Moscow to the Atlantic approaches, the red banners of the revolution fly over a conquered continent. Yet the triumph of Soviet arms has created burdens that no military victory alone can resolve.

**Effects:**

- +50 political power.
- Unlock occupation administration.
- Introduce the Soviet strategic situation.

## Focus 2: The Burden of Victory

**Description:**

> Conquest is not the same as governance. The future of our European possessions will determine whether the Soviet Union enters a new era of prosperity or collapses under its own ambitions.

**Effects:**

- Initialize occupation loyalty values.
- Unlock occupation-management decisions.
- Activate occupation instability events.

## Focus 3: The Kremlin Divided

**Description:**

> The Premier demands continued expansion. General Krukov warns of dangerous overextension. Meanwhile, the Commander has earned the loyalty of an increasingly influential group of officers.

**Effects:**

- Introduce the three Soviet political factions.
- Trigger an introductory leadership event.

## Focus 4: The Future of the Union

**Description:**

> The Soviet Union stands at a crossroads. Its immense military power may be used to conquer the world, preserve the state, or give new meaning to the international revolution.

**Effects:**

- Unlock one of three mutually exclusive political routes.
- Set the appropriate political-route flag.
- Lock the remaining routes.

---

# 6. Political Route A — Premier Cherdenko

## Theme: The World Under One Red Banner

**Political leader:** Anatoly Cherdenko  
**Government:** Authoritarian Soviet communist leadership  
**Diplomatic strategy:** Military conquest  
**Occupation strategy:** Strengthen direct Soviet control  
**Final objective:** Establish worldwide Soviet military supremacy.

## 6.1 Narrative

Premier Cherdenko believes the Soviet Union must continue its military expansion until no rival power can threaten the revolution.

The European occupation zones are not independent states in his vision. They are administrative instruments through which Moscow governs conquered territories.

Any suggestion of independence or decentralization is interpreted as a threat to the Union.

Cherdenko intends to strengthen political surveillance, replace unreliable officials, and enforce direct Soviet authority over the occupation zones.

However, increasing central control will produce resentment and strengthen resistance movements.

## 6.2 Focus Tree

```text
The Premier's Authority
          |
Reaffirm the Party Line
          |
The Security Directorate
          |
Enemies Within the Kremlin
          |
A Plot Against the Premier
          |
Discredit General Krukov
          |
The Supreme Commander-in-Chief
          |
    +-----+------------------+
    |                        |
The European             The Northern
Directive                Directive
    |                        |
Direct Rule              Direct Rule
in Europe                in Scandinavia
    |                        |
    +------------+-----------+
                 |
       An Indivisible Empire
                 |
        Mobilize the War Machine
                 |
        The Empire Must Kneel
                 |
      The End of Allied Resistance
                 |
       No Compromise, No Retreat
                 |
     The World Under the Red Banner
```

## 6.3 Political Focuses

| Focus | Effects |
| --- | --- |
| The Premier's Authority | Strengthen Cherdenko; increased political power gain |
| Reaffirm the Party Line | Party loyalty and stability |
| The Security Directorate | Unlock repression-oriented decisions |
| Enemies Within the Kremlin | Intelligence and investigation events |
| A Plot Against the Premier | Initiates Cherdenko's staged assassination narrative |
| Discredit General Krukov | Removes Krukov's political influence |
| The Supreme Commander-in-Chief | Consolidates Cherdenko's military authority |
| Mobilize the War Machine | Military factory output and war support |
| The Empire Must Kneel | Offensive preparation against the Empire of the Rising Sun |
| The End of Allied Resistance | Overseas offensive preparation and conditional war goals |
| No Compromise, No Retreat | Offensive military bonuses |
| The World Under the Red Banner | Final political consolidation |

## 6.4 Occupation Policy — Strengthen Direct Control

The Premier retains SOE and SOS as large administrative subjects.

They will not be divided into smaller countries or granted independence.

### The European Directive

**Description:**

> Europe was conquered by Soviet blood and Soviet steel. Its administration must obey Moscow without hesitation or compromise.

**Effects:**

- Reduce SOE autonomy.
- Increase Moscow's control over its economy.
- Improve short-term occupation loyalty.
- Increase long-term resistance pressure.

### Direct Rule in Europe

**Description:**

> The European administration must be transformed into an instrument of the central government. Political opposition will be suppressed and industrial production directed toward Soviet priorities.

**Effects:**

- SOE remains a Soviet subject.
- Strengthen its integrated-puppet status.
- Increase industrial contributions to the Soviet war effort.
- Apply an authoritarian administration spirit.
- Increase the consequences of low loyalty.

### The Northern Directive

**Description:**

> The strategically important northern territories cannot be permitted to challenge Soviet authority. Their administration must answer directly to Moscow.

**Effects:**

- Reduce SOS autonomy.
- Increase short-term occupation loyalty.
- Improve Soviet military access and logistical control.

### Direct Rule in Scandinavia

**Description:**

> The Scandinavian administration will be permanently subordinated to the Soviet center, securing our northern approaches against foreign interference.

**Effects:**

- SOS remains a Soviet subject.
- Strengthen its integrated-puppet status.
- Improve resource and military contributions.
- Increase long-term political resistance.

### An Indivisible Empire

**Requirements:**

- Complete both occupation directives.
- SOE and SOS remain Soviet subjects.
- Neither occupation administration has collapsed.

**Effects:**

- Both occupation zones remain intact.
- Moscow gains additional economic benefits.
- Replace the occupation spirit with **The Soviet Imperial Administration**.

### National Spirit: The Soviet Imperial Administration

**Positive effects:**

- Additional military industrial output from subjects.
- Improved military logistics across subject territory.
- Increased political control.

**Negative effects:**

- Higher occupation-management costs.
- Reduced local political legitimacy.
- Greater risk of organized resistance.

## 6.5 Route Consequences

Cherdenko possesses the strongest offensive potential.

However, his centralization policies increase resistance risks, making the occupation zones difficult to manage during prolonged overseas campaigns.

A successful Soviet military conquest does not automatically eliminate internal resistance.

**Ending:** An authoritarian Soviet superpower pursuing worldwide military domination.

---

# 7. Political Route B — General Nikolai Krukov

## Theme: Peace Through Strength

**Political leader:** Nikolai Krukov  
**Government:** Soviet military administration  
**Diplomatic strategy:** Strategic agreements and limited warfare  
**Occupation strategy:** Partition the occupation zones into smaller puppet states  
**Final objective:** Secure Soviet interests through military strength and diplomacy.

## 7.1 Narrative

General Krukov believes the Premier's ambitions threaten the survival of the Soviet state.

The Soviet Union has conquered more territory than its centralized administrative structure can effectively govern.

Krukov proposes reorganizing the occupied territories into smaller socialist client states.

These governments will retain local political institutions while remaining subordinate to Moscow through treaties, military obligations, and puppet relationships.

A network of smaller Soviet-aligned governments will serve as a strategic buffer against foreign threats.

Krukov also seeks to avoid an endless confrontation with the Allied Nations, preferring a negotiated peace when Soviet interests can be preserved.

## 7.2 Focus Tree

```text
The Generals' Petition
          |
The Red Army Stands United
          |
Expose the Premier's Conspiracy
          |
The Moscow Military Council
          |
Restore the Chain of Command
          |
A War on Two Fronts Is Folly
          |
    +-----+--------------------+
    |                          |
Reorganize Europe         Reorganize Scandinavia
    |                          |
European Client           Northern Client
Republics                 Republics
    |                          |
    +-------------+------------+
                  |
          A Federation of Puppets
                  |
         A Message to the Allies
                  |
       A Common Enemy in the East
                  |
        The Soviet Defensive Perimeter
                  |
        Settle the European Question
                  |
            Peace Through Strength
                  |
              An Uneasy Peace
```

## 7.3 Political Focuses

| Focus | Effects |
| --- | --- |
| The Generals' Petition | Increase support for Krukov |
| The Red Army Stands United | Army organization and command power |
| Expose the Premier's Conspiracy | Political confrontation event |
| The Moscow Military Council | Krukov becomes Soviet leader |
| Restore the Chain of Command | Remove divided-command penalties |
| A War on Two Fronts Is Folly | Unlock strategic diplomatic policy |
| A Message to the Allies | Offer a conditional peace agreement |
| A Common Enemy in the East | Enable temporary military cooperation where appropriate |
| The Soviet Defensive Perimeter | Fortification and defensive preparation |
| Settle the European Question | Secure diplomatic recognition of Soviet client-state arrangements where possible |
| Peace Through Strength | Defensive and organizational bonuses |
| An Uneasy Peace | Final military-government consolidation |

## 7.4 Occupation Policy — Divide into Puppet States

Krukov abolishes the existing large occupation administrations and replaces them with smaller communist puppet governments.

### Reorganize Europe

**Description:**

> A single administration ruling over the conquered European continent is inefficient and dangerously vulnerable to coordinated rebellion. The General Staff proposes replacing it with smaller governments answerable to Moscow.

**Effects:**

- Begin the administrative partition of SOE.
- Unlock the establishment of individual European puppet states.
- Temporary administrative disruption.

### European Client Republics

**Effects:**

- Transfer SOE-owned territory into smaller puppet countries.
- Establish communist governments.
- Make each new state a Soviet puppet.
- Keep the new puppet countries in the Comintern.
- Remove the previous unified occupation administration once its territory has been fully allocated.

Potential successor governments may correspond to existing European countries such as France, Germany, Italy, or Spain, **only where their territories are actually administered by SOE**.

Final borders and participating countries must be determined using the current scenario map, existing national cores, and available country tags.

Do not create fictional territorial claims or transfer territory outside Soviet control.

### Reorganize Scandinavia

**Description:**

> The northern territories require administrations capable of responding to their own geographic, economic, and military circumstances.

**Effects:**

- Begin the partition of SOS.
- Unlock country-specific puppet establishment.
- Improve local administrative efficiency.

### Northern Client Republics

**Effects:**

- Divide SOS into smaller communist puppet governments.
- Preserve Soviet military access.
- Keep all newly established puppets subordinate to Moscow.
- Retire SOS as a territorial administration after partition is complete.

Possible successors include Sweden, Norway, and other Scandinavian or Nordic countries whose territory actually belongs to SOS.

### A Federation of Puppets

**Requirements:**

- European and Scandinavian restructuring completed, or appropriately bypassed if territory has already been lost.
- At least one functioning Soviet client state remains.

**Effects:**

- Replace the occupation burden with **The Soviet Security Bloc**.
- Improve client-state coordination.
- Reduce the cost of administering occupied territory.
- Strengthen military contributions from the puppet states.

### National Spirit: The Soviet Security Bloc

**Positive effects:**

- Reduced administrative costs.
- Better subject military contributions.
- Better defensive planning.
- Improved logistics through Soviet-controlled client states.

**Negative effects:**

- Reduced direct control over regional industrial output.
- Continuing dependency on the political stability of subordinate governments.

## 7.5 Diplomatic Strategy

Krukov's military government may propose peace with the Allied Nations.

A successful agreement could recognize a strategic status quo, suspend hostilities, and enable temporary cooperation against the Empire of the Rising Sun.

The agreement must not automatically merge the Comintern with another faction.

If peace is rejected, Krukov retains the option to continue the war.

His preferred strategy is defensive consolidation rather than unconditional conquest.

## 7.6 Route Consequences

Krukov sacrifices centralized administrative power for a more flexible structure of Soviet puppet states.

This reduces the danger that a single uprising could destabilize the entire European occupation system.

However, separate puppet governments may still experience local political instability and can become vulnerable to external military pressure.

**Ending:** A Soviet military government maintaining a network of subordinate socialist states while seeking long-term strategic security.

---

# 8. Political Route C — The Commander and Dasha

## Theme: The Revolution Renewed

**Political leader:** The Soviet Commander  
**Key adviser:** Dasha Fedorovich  
**Government:** Reformed socialist republic  
**Diplomatic strategy:** International communist cooperation  
**Occupation strategy:** Encourage independent communist countries  
**Final objective:** Establish an international revolutionary movement based on sovereign socialist states.

## 8.1 Narrative

The Commander has fought for the Soviet Union and earned widespread respect within the military.

Through Dasha's intelligence reports, the Commander discovers the extent of corruption, political manipulation, and authoritarian abuses within the Kremlin.

The Commander concludes that the Soviet revolution has departed from its ideals.

The revolution cannot succeed by replacing foreign governments with permanent Soviet occupation administrations.

Instead, the people of Europe and Scandinavia must be allowed to establish their own independent communist governments.

The Soviet Union will lead the international revolution through diplomacy, cooperation, economic assistance, and ideological solidarity.

It will no longer treat territorial conquest as the ultimate measure of revolutionary success.

## 8.2 Focus Tree

```text
The Commander's Reputation
          |
Dasha's Secret Reports
          |
Officers of the Revolution
          |
The People's Congress
          |
The Kremlin Reckoning
          |
A New Soviet Republic
          |
The Rights of the Republics
          |
    +-----+-----------------------+
    |                             |
The Liberation of Europe     The Nordic Revolution
    |                             |
Independent European         Independent Nordic
Republics                    Republics
    |                             |
    +---------------+-------------+
                    |
          Liberation, Not Subjugation
                    |
          A Revolution Worth Defending
                    |
           Workers of Every Nation
                    |
           The International Congress
                    |
             The World Revolution
```

## 8.3 Political Focuses

| Focus | Effects |
| --- | --- |
| The Commander's Reputation | Strengthen the Commander's political support |
| Dasha's Secret Reports | Reveal Kremlin conspiracies |
| Officers of the Revolution | Build military support for reform |
| The People's Congress | Establish a reformist political coalition |
| The Kremlin Reckoning | Remove Cherdenko and resolve the political confrontation |
| A New Soviet Republic | Establish the Commander's government |
| The Rights of the Republics | Unlock independence and self-determination policies |
| A Revolution Worth Defending | Stability and defensive bonuses |
| Workers of Every Nation | International communist diplomatic outreach |
| The International Congress | Strengthen international socialist cooperation |
| The World Revolution | Establish the final revolutionary political system |

## 8.4 Occupation Policy — Independent Communist Countries

The Commander dismantles the existing occupation governments and encourages the creation of sovereign communist states.

These new countries are **not Soviet puppets**.

They retain political sovereignty, domestic governmental authority, and control of their own economic systems.

The Soviet Union will attempt to maintain relationships through voluntary Comintern membership and cooperative agreements.

### The Liberation of Europe

**Description:**

> Europe cannot be truly liberated while its people remain subjects of a foreign military administration. The revolution must belong to those who live under it.

**Effects:**

- Begin the dismantling of SOE.
- Prepare country-specific independence events.
- Reduce occupation resentment.
- Temporarily reduce Soviet industrial benefits.

### Independent European Republics

**Effects:**

- Release communist countries from SOE territory.
- Remove Soviet puppet relationships.
- Establish genuinely independent communist governments.
- Offer Comintern membership through diplomacy.
- Grant initial positive diplomatic relations with the Soviet Union.

The newly independent countries are free to accept or reject participation in the Comintern.

Refusal does not reverse their independence.

### The Nordic Revolution

**Description:**

> The people of Scandinavia have a right to determine their future without permanent occupation. The Soviet Union shall support their right to construct their own socialist republics.

**Effects:**

- Begin dismantling SOS.
- Prepare independence events for its constituent territories.
- Reduce occupation-related political instability.

### Independent Nordic Republics

**Effects:**

- Release independent communist nations from SOS territory.
- End Soviet puppet relationships.
- Offer voluntary Comintern membership.
- Improve diplomatic cooperation where accepted.
- Retire the unified Scandinavian occupation administration.

### Liberation, Not Subjugation

**Requirements:**

- European and Scandinavian independence processes completed, or validly bypassed where territory was previously lost.

**Effects:**

- Remove the occupation-related national penalty.
- Establish **The International Socialist Commonwealth** national spirit.
- Improve diplomatic relations with friendly communist governments.
- Unlock cooperative economic and research policies.

### National Spirit: The International Socialist Commonwealth

**Positive effects:**

- Improved political stability.
- Diplomatic influence among communist countries.
- Improved economic and research cooperation.
- Reduced administrative burdens.

**Negative effects:**

- Loss of direct industrial extraction from former occupation zones.
- Reduced direct control over European military resources.

## 8.5 World Revolution

The Commander's international revolution is not defined by automatic annexation or forced puppet governments.

It proceeds through:

### International Political Cooperation

Support communist political movements in other countries.

### Voluntary Comintern Expansion

Invite independent socialist nations into the Comintern without imposing puppet status.

### Economic Reconstruction

Provide industrial and technological assistance to socialist partner countries.

### Revolutionary Solidarity

Support threatened socialist governments through diplomacy, volunteers, military assistance, or defensive wars when appropriate.

### The International Congress

Create a platform for diplomatic and economic cooperation between communist countries.

The World Revolution focus grants continuing diplomatic tools and a final national spirit.

It does not automatically convert the world to communism or end the campaign.

## 8.6 Route Consequences

The Commander route provides the strongest potential long-term political stability.

However, granting independence means losing direct access to much of the Soviet-occupied industrial base.

Former occupation territories become international partners rather than permanent administrative dependencies.

**Ending:** A reformed Soviet Union leading an international movement of independent communist nations.

---

# 9. Comparison of the Three Political Routes

| Feature | Cherdenko | Krukov | Commander |
| --- | --- | --- | --- |
| Political system | Personal dictatorship | Military government | Reformed socialist republic |
| Main strategy | World conquest | Strategic security | World revolution |
| European policy | Preserve unified occupation zone | Divide into puppets | Establish independent countries |
| Scandinavian policy | Preserve unified occupation zone | Divide into puppets | Establish independent countries |
| New countries' sovereignty | No independence | Soviet puppets | Full independence |
| Military bonuses | Offensive | Defensive and logistical | Balanced, with defensive emphasis |
| Industrial policy | Direct extraction | Shared puppet production | Cooperative development |
| Diplomacy | Aggressive coercion | Negotiation and deterrence | Ideological cooperation |
| Occupation stability | Short-term coercion | Decentralized administration | Long-term voluntary legitimacy |
| Main disadvantage | High unrest | Puppet dependency | Reduced direct economic control |

## 9.1 Essential Mechanical Distinction

These three outcomes must not be cosmetic changes.

They must produce actual changes in the HOI4 political map.

### Cherdenko

```text
SOV
 |
 +-- SOE (integrated Soviet subject)
 |
 +-- SOS (integrated Soviet subject)
```

### Krukov

```text
SOV
 |
 +-- European Communist Puppet A
 |
 +-- European Communist Puppet B
 |
 +-- European Communist Puppet C
 |
 +-- Nordic Communist Puppet A
 |
 +-- Nordic Communist Puppet B
```

### Commander

```text
THE COMINTERN
 |
 +-- SOV (independent)
 |
 +-- Mongolia (independent)
 |
 +-- European Communist Country A (independent, if joined)
 |
 +-- European Communist Country B (independent, if joined)
 |
 +-- Nordic Communist Country A (independent, if joined)
```

Country names and territorial borders must reflect the actual game map.

---

# 10. Occupation Stability System

## 10.1 Design Purpose

The two occupation zones represent the Soviet Union's greatest internal strategic vulnerability.

The player must stabilize them while preparing for major international conflicts.

Failure to manage either zone can lead to rebellion.

The system is controlled from the Soviet perspective.

**No unique SOE or SOS national focus trees are required.**

## 10.2 Occupation Loyalty

Two separate loyalty values are maintained:

- `SOV_europe_loyalty`
- `SOV_scandinavia_loyalty`

Each ranges from 0 to 100.

### Proposed Starting Values

| Territory | Initial loyalty |
| --- | ---: |
| SOE | 55 |
| SOS | 45 |

### Loyalty States

| Loyalty | Status | Effects |
| --- | --- | --- |
| 70–100 | Secure | Minimal instability |
| 45–69 | Uneasy | Moderate productivity penalty |
| 26–44 | Unstable | Significant political and economic penalties |
| 0–25 | Critical | Uprising warning and countdown |

If loyalty remains at or below 25 for 60 consecutive days, an uprising event becomes available.

The player receives warnings and opportunities to respond before open rebellion.

These values are provisional and should be adjusted through playtesting.

## 10.3 Shared Occupation Focuses

These focuses are available regardless of the chosen political route.

### The Occupation Council

Unlocks occupation-management decisions.

### Survey the Conquered Territories

Improves intelligence concerning local resistance.

Provides a small loyalty bonus to both zones.

### Restore Continental Supply Lines

Improves logistics and infrastructure connecting Soviet territory to the occupation zones.

### Rebuild the Occupied Economy

Provides economic reconstruction options when the zones are sufficiently stable.

### The Cost of Empire

Partially reduces the national occupation penalty after both territories are stabilized.

## 10.4 Soviet Occupation Decisions

The Soviet Union can use a limited number of recurring decisions.

| Decision | Cost | Effect |
| --- | --- | --- |
| Reinforce Occupation Garrisons | Equipment, manpower | Temporary loyalty and security |
| Restore Local Infrastructure | Civilian industrial capacity | Sustainable loyalty improvement |
| Economic Assistance | Political power, industrial resources | Loyalty increase |
| Investigate Resistance Networks | Political power | Reveals imminent uprising risks |
| Negotiate with Local Administrators | Political power | Diplomatic loyalty improvement |

Availability and effectiveness depend on the chosen political route.

### Cherdenko

Coercive decisions are more effective immediately but may increase subsequent unrest.

### Krukov

Military security and administrative restructuring decisions are more effective.

### Commander

Economic assistance, political reform, and independence preparation provide more sustainable results.

## 10.5 Uprising Consequences

An uprising can occur before the political route finishes reorganizing the zone.

### European Uprising

Possible consequences:

- Formation of a local rebel government.
- Armed revolt within SOE territory.
- Industrial production disruption.
- Loss of Soviet military access in contested areas.
- Increased pressure on Soviet leadership.

### Scandinavian Uprising

Possible consequences:

- Formation of a local rebel government.
- Armed revolt within SOS territory.
- Disruption of northern supply routes.
- Reduced access to regional resources and naval facilities.

### Soviet Responses

The Soviet Union can:

1. Suppress the rebellion militarily.
2. Offer emergency political concessions.
3. Accelerate an appropriate political settlement.

The final option is influenced by the political route.

Cherdenko can impose emergency central control.

Krukov can accelerate the establishment of regional puppet governments.

The Commander can accelerate genuine independence.

## 10.6 Post-Reorganization Stability

After Krukov or the Commander has fully dismantled an occupation zone, its original occupation loyalty variable is retired.

### Krukov

Individual puppet governments use ordinary subject relationships, national spirits, and limited instability events.

The original SOE/SOS uprising countdown must no longer operate on territory they do not administer.

### Commander

Independent communist countries are no longer subject to Soviet occupation loyalty mechanics.

They retain ordinary national stability and political gameplay.

The Soviet Union cannot continue treating them as occupied territories.

### Cherdenko

SOE and SOS remain intact, so the original occupation stability system continues to matter.

---

# 11. The Red Army — Land Forces

**Design objective:** Preserve the Soviet Union's overwhelming advantage in continental warfare.

| Focus | Primary effect |
| --- | --- |
| The Army That Conquered Europe | Land doctrine research |
| Modernize the Armored Corps | Armor research |
| The Apocalypse Program | Advanced heavy armor |
| Hammer and Sickle | Mechanized and armored warfare |
| The V4 Artillery Directorate | Artillery and rocket development |
| The Soviet Logistics Corps | Supply efficiency |
| Combined Arms Command | Planning and coordination |
| The Invincible Red Army | Final land-warfare bonuses |

## Military Identity

The Soviets emphasize:

- Heavy armor.
- Mechanized warfare.
- Massed artillery.
- Strong defensive fortifications.
- High industrial output.
- Large-scale offensives.

The land branch should improve the Red Army's existing strengths without making Soviet divisions invulnerable.

The Soviet player must still manage supply, equipment, and combat losses.

---

# 12. The Red Navy — Naval Modernization

**Design objective:** Address the Soviet Union's greatest military weakness.

| Focus | Primary effect |
| --- | --- |
| Rebuild the Red Fleet | Naval recovery |
| The Baltic Shipyards | Dockyard construction |
| The Akula Submarine Program | Submarine development |
| Defend the Soviet Coast | Coastal defense and naval mines |
| The Dreadnought Project | Heavy naval weapons |
| Escort the Invasion Fleets | Escort and naval invasion support |
| The Soviet Oceanic Fleet | Late-game naval capability |

## Strategic Choice

Following *Rebuild the Red Fleet*, two mutually exclusive approaches are available.

### Submarine and Coastal Warfare

Emphasizes:

- Akula submarines.
- Naval mines.
- Convoy raiding.
- Coastal defense.
- Affordable sea-denial capabilities.

### The Great Surface Fleet

Emphasizes:

- Major shipyards.
- Heavy surface combatants.
- Dreadnought development.
- Fleet coordination.
- Long-term overseas naval power.

The Soviet Navy must not immediately become equal to the Allied or Imperial fleets.

Naval modernization should require substantial economic investment.

---

# 13. Soviet Air Forces

| Focus | Primary effect |
| --- | --- |
| Air Power of the Revolution | Air doctrine |
| The MiG Design Bureau | Fighter development |
| Twinblade Assault Aviation | Ground-support aviation |
| The Kirov Airship Program | Strategic bombing |
| Airborne Combined Operations | Airborne operations |
| Control the Skies | Final air coordination bonus |

The branch should emphasize the distinctive Soviet aircraft from RA3.

It should also support the Red Army through close air support and troop mobility.

---

# 14. Soviet Science and Technology

| Focus | Primary effect |
| --- | --- |
| The Soviet Battle Laboratories | Research improvements |
| Expand the Tesla Program | Tesla technology |
| The Iron Curtain Project | Temporary defensive special operation |
| Industrial Super-Reactors | Advanced industrial development |
| The Vacuum Imploder Project | Late-game special weapon |
| Zelinsky's Research Archives | Experimental research |
| Secrets of the Altered Timeline | Research-related narrative and intelligence benefits |

## 14.1 Tesla Technology

Improves specialized Soviet equipment and defensive installations.

## 14.2 Iron Curtain

A temporary, powerful defensive effect requiring preparation and significant costs.

It must not grant permanent unit invulnerability.

## 14.3 Vacuum Imploder

A late-game special operation with:

- Extensive research requirements.
- High construction costs.
- Strict cooldowns.
- Significant strategic effects.

It must not act as an automatic victory mechanic.

## 14.4 Altered Timeline

Research narratives can examine the consequences of Einstein's removal from history.

This branch must remain consistent with the RA3 timeline.

---

# 15. Soviet Industry and Economy

**Design objective:** Support the enormous Soviet military without removing the economic costs of occupation and overseas warfare.

| Focus | Primary effect |
| --- | --- |
| The Soviet Industrial Colossus | Construction research |
| National Ore Extraction Program | Resource extraction |
| The Five-Year Production Directive | Industrial expansion |
| The Trans-Siberian Railway | Eastern logistics |
| The Siberian Industrial Corridor | Siberian development |
| Modernize the Great Shipyards | Dockyard development |
| War Factories of the Union | Production efficiency |
| Rebuild the Conquered Economy | Conditional occupation reconstruction |

## Economic Policy Choice

### Centralized War Economy

Advantages:

- Increased military factory output.
- Faster equipment production.
- Strong wartime mobilization.

Disadvantages:

- Higher administrative and economic pressure.
- Reduced civilian economic development.

### Socialist Reconstruction

Advantages:

- Faster civilian construction.
- Improved regional economic development.
- More sustainable occupation recovery.

Disadvantages:

- Lower immediate military output.

These two economic approaches are mutually exclusive.

They are available to all three Soviet political routes.

---

# 16. Soviet Foreign Strategy

Only Soviet national focuses, decisions, and events are included here.

This section does not introduce designs for foreign countries.

## 16.1 Eastern Strategic Branch

The Empire of the Rising Sun represents the Soviet Union's most dangerous continental challenger.

| Focus | Effect |
| --- | --- |
| The Threat from the East | Strategic preparation |
| Hold Vladivostok | Coastal and regional defenses |
| Secure the Siberian Supply Route | Infrastructure and logistics |
| Mobilize the Far Eastern Army | Mobilization bonuses |
| Break the Imperial Offensive | Defensive and counteroffensive bonuses |
| The Road to Japan | Late-game overseas planning |

The Soviet response depends on the player's political strategy.

Cherdenko favors an offensive war.

Krukov favors containing and defeating the immediate threat.

The Commander favors collective defense and revolutionary diplomacy, while retaining the ability to fight.

## 16.2 Western Strategic Branch

The Soviet Union must overcome the naval and geographical obstacles separating it from overseas opponents.

| Focus | Effect |
| --- | --- |
| The Last Allied Stronghold | Intelligence and regional preparation |
| Secure the Atlantic Coast | Coastal defense |
| The Cross-Channel Problem | Naval invasion preparation |
| The Allied Overseas Empire | Overseas intelligence |
| The Final Western Offensive | Conditional strategic war goals |

The Final Western Offensive is primarily suited to the Cherdenko route.

Krukov's route may pursue a diplomatic settlement instead.

The Commander pursues political cooperation where possible.

The Soviet focus tree must not automatically declare war on every major foreign country.

War goals and military escalation should depend on the political route, diplomatic situation, and existing wars.

---

# 17. Major Soviet Narrative Events

## Political Events

1. **Three Visions of the Revolution**
   - Opens the three political routes.

2. **The Premier's Assassination**
   - Cherdenko's staged assassination narrative.

3. **The General Accused**
   - Cherdenko moves against Krukov.

4. **The Moscow Military Council**
   - Krukov establishes military authority.

5. **Dasha's Secret Reports**
   - Reveals Kremlin conspiracies.

6. **The Kremlin Reckoning**
   - The Commander challenges Cherdenko.

7. **The New Soviet Republic**
   - The Commander's political consolidation.

## Occupation Events

1. **Unrest in Europe**
   - Warning of falling SOE loyalty.

2. **The Northern Resistance**
   - Warning of falling SOS loyalty.

3. **The European Uprising**
    - Major SOE rebellion.

4. **The Scandinavian Uprising**
    - Major SOS rebellion.

5. **The European Directive**
    - Cherdenko strengthens direct control.

6. **The Partition of Europe**
    - Krukov divides SOE into smaller puppets.

7. **The Partition of Scandinavia**
    - Krukov divides SOS into smaller puppets.

8. **The Liberation of Europe**
    - The Commander establishes independent communist states.

9. **The Liberation of Scandinavia**
    - The Commander establishes independent communist states.

## Diplomatic Events

 1. **A Message to the Allies**
    - Krukov offers negotiations.

 2. **An Uneasy Agreement**
    - A negotiated settlement or diplomatic rejection.

 3. **The International Congress**
    - The Commander establishes international socialist cooperation.

 4. **The Fate of the Revolution**
    - Final political-route narrative.

All events must be triggered by valid focus completion, national conditions, or defined on-actions.

Do not reintroduce unrelated vanilla historical events.

---

# 18. Soviet AI Behavior

The Soviet AI should choose a political route and pursue it coherently.

## Cherdenko AI

Priorities:

1. Secure central authority.
2. Strengthen the occupation administrations.
3. Expand military production.
4. Prepare for offensive warfare.
5. Pursue overseas conquest when military conditions permit.

Higher willingness to accept occupation instability in exchange for military power.

## Krukov AI

Priorities:

1. Consolidate the military government.
2. Reorganize the occupation zones into puppets.
3. Strengthen logistics and defense.
4. Pursue diplomatic agreements when advantageous.
5. Avoid unnecessary simultaneous major wars.

## Commander AI

Priorities:

1. Secure political leadership.
2. Stabilize the occupation zones.
3. Establish independent communist countries.
4. Strengthen the Comintern through diplomacy.
5. Support friendly socialist states without forced annexation.

## Occupation AI Safeguards

All three routes must:

- Respond to critical occupation loyalty.
- Avoid continuously selecting unusable decisions.
- Reevaluate policies when occupation zones lose territory.
- Avoid attempting to reorganize countries that no longer exist.
- Recover from failed occupation policies where possible.

---

# 19. Technical Implementation Specification

## 19.1 Existing Files to Modify

### Soviet National Focus Tree

`common/national_focus/soviet.txt`

Implement:

- Political opening.
- Three political routes.
- Soviet-controlled occupation policies.
- Land, naval, air, economic, and research branches.
- Soviet foreign strategy.

### Soviet National Spirits

`common/ideas/soviet_ideas.txt`

Implement:

- Starting strengths and weaknesses.
- Political-route national spirits.
- Occupation administration modifiers.
- Military and economic modifiers.

### Occupation-Zone Spirits

`common/ideas/soviet_occupation_zone_ideas.txt`

Implement:

- Subject loyalty tiers.
- Authoritarian administration where applicable.
- Temporary restructuring modifiers.
- Appropriate removal when zones cease to exist.

### Soviet Events

`events/SovietUnion.txt`

Implement:

- Political confrontations.
- Occupation crises.
- Puppet-state restructuring.
- Independence processes.
- Soviet diplomatic initiatives.

### Soviet Decisions

Add a dedicated Soviet decision file, for example:

`common/decisions/soviet_decisions.txt`

Implement:

- Occupation-management actions.
- Political-route-specific administration decisions.
- Limited special military and diplomatic operations.

### Localisation

`localisation/sov_core_l_english.yml`

Add:

- Focus names and descriptions.
- National-spirit names and descriptions.
- Event titles, descriptions, and choices.
- Decision names and descriptions.

### Soviet Country History

`history/countries/SOV - Soviet union.txt`

Update:

- Faction naming.
- Starting national spirits.
- Required leadership and character setup.
- Preserve Mongolia as a Comintern member.
- Preserve the two starting occupation-zone subject relationships.

## 19.2 Puppet and Independence Implementation

### Cherdenko

Retain SOE and SOS.

Strengthen Soviet subject authority.

Do not annex or partition their territories.

### Krukov

Partition SOE and SOS into geographically valid successor puppet states.

Use actual owned states and existing country tags where suitable.

Transfer territory through country-specific scripted effects.

Set appropriate communist governments and Soviet subject relationships.

Remove the original administrative zones after their territories have been fully allocated.

### Commander

Partition SOE and SOS into sovereign communist countries.

Establish independent governments and end Soviet subject relationships.

Offer Comintern membership through diplomatic events or suitable faction mechanics.

Membership must not be compulsory.

Remove obsolete occupation administrations after liberation is completed.

### Common Safeguards

- Never duplicate territorial ownership.
- Do not transfer states beyond the occupation zone's actual territory.
- Do not release a country with no valid territory.
- Preserve appropriate national cores.
- Handle occupied states that have changed ownership during war.
- Do not create duplicate instances of existing countries.
- Avoid soft-locking the Soviet focus tree when territories are lost.
- Ensure division and unit handling is consistent with HOI4 country-release mechanics.
- Avoid unintended peace or faction changes.
- All successor states may continue using generic focus trees.

## 19.3 Mongolia

Mongolia must:

- Remain independent.
- Remain a member of the Comintern.
- Retain its own territorial ownership.
- Remain outside the European and Scandinavian occupation systems.

No Soviet political route may automatically annex or puppet Mongolia.

## 19.4 Excluded Work

This design does not include:

- Unique national focus trees for SOE or SOS.
- Unique national focus trees for successor European or Scandinavian states.
- Redesigns of Allied national focuses.
- Redesigns of Empire of the Rising Sun national focuses.
- New foreign-country political systems.
- A custom victory mechanic.
- The RA3 Uprising expansion storyline.

---

# 20. Implementation Priorities

## Phase 1 — Soviet Scenario Foundation

- Correct faction name to The Comintern.
- Preserve Mongolia's membership.
- Verify SOE and SOS subject relationships.
- Establish Soviet starting national spirits.
- Prepare Soviet political characters.

## Phase 2 — Soviet Political Routes

- Implement the common political opening.
- Implement Cherdenko's route.
- Implement Krukov's route.
- Implement the Commander/Dasha route.
- Enforce mutual exclusivity.

## Phase 3 — Occupation System

- Implement SOE and SOS loyalty values.
- Add Soviet occupation decisions.
- Add warning and uprising events.
- Implement Cherdenko's direct-control policies.
- Implement Krukov's partition-into-puppets policies.
- Implement the Commander's independence policies.

## Phase 4 — Soviet Military and Economy

- Red Army branch.
- Red Navy branch.
- Soviet Air Forces branch.
- Industrial development.
- Research and special technology.

## Phase 5 — Soviet Diplomatic and Strategic Content

- Eastern military strategy.
- Overseas strategic preparation.
- Krukov's peace initiative.
- The Commander's international revolution.
- Cherdenko's military conquest strategy.

## Phase 6 — Validation and Balancing

Test:

1. Every Soviet political route.
2. Mutual exclusivity.
3. Occupation loyalty progression.
4. European and Scandinavian uprisings.
5. Direct-control subject outcomes.
6. Partition into valid Soviet puppet states.
7. Creation of independent communist countries.
8. Mongolia's continued independent Comintern membership.
9. Army and naval balance.
10. AI behavior and campaign stability.

---

# 21. Final Design Summary

The Soviet Union begins the campaign as a powerful but overstretched continental empire.

Its greatest military strength is the Red Army.

Its greatest military weakness is the Navy.

Its greatest political challenge is maintaining control over the territories conquered in Europe.

The three political routes determine the Soviet Union's future.

## Cherdenko — One Empire

The occupation zones remain under strong, centralized Soviet administration.

The Soviet Union prioritizes military conquest and direct political control.

**Core identity: Domination.**

## Krukov — Many Puppets

The occupation zones are divided into smaller communist puppet states.

The Soviet Union becomes the center of a network of subordinate governments, pursuing strategic security and negotiated peace where possible.

**Core identity: Military pragmatism.**

## Commander and Dasha — Free Socialist Nations

The occupation zones are dismantled and replaced with independent communist countries.

The Soviet Union seeks to lead the world revolution through diplomacy, cooperation, and international socialist solidarity.

**Core identity: Revolutionary renewal.**

These routes must create fundamentally different political maps, economic relationships, military strategies, and long-term gameplay experiences.

The player is not merely choosing who rules Moscow.

**The player is choosing what the Soviet Union means to the rest of the world.**
