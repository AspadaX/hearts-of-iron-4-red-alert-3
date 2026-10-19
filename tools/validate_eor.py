#!/usr/bin/env python3
"""Validate EOR's authored three-route graph, references and presentation, plus IOT's generic tree.

These static checks do not run the engine or establish runtime stability/balance.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re

def direct_blocks(text):
    tokens,pairs=lex(text);depth=0;result={}
    for i,t in enumerate(tokens[:-2]):
        if t[0]=='{':depth+=1
        elif t[0]=='}':depth-=1
        elif depth==1 and tokens[i+1][0]=='=' and tokens[i+2][0]=='{':
            assert t[0] not in result,('Duplicate direct block',t[0])
            result[t[0]]=text[t.start():tokens[pairs[i+2]].end()]
    return result

from event_compat import lex,definitions,filter_calls

ROOT=Path(__file__).resolve().parents[1]
GAME=Path.home()/'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV'

def blocks(text,key):
    tokens,pairs=lex(text)
    return [text[t.start():tokens[pairs[i+2]].end()] for i,t in enumerate(tokens[:-2]) if t[0]==key and tokens[i+1][0]=='=' and tokens[i+2][0]=='{']

def scalar(text,key):
    return re.search(r'\b'+re.escape(key)+r'\s*=\s*([^\s}]+)',text)[1]

def check_event_roles(eid,event):
    desc_keys=set(re.findall(r'\bdesc\s*=\s*([\w.]+)',event))
    desc_keys.update(re.findall(r'\btext\s*=\s*([\w.]+)',event))
    option_keys={scalar(b,'name') for b in blocks(event,'option')}
    assert not desc_keys&option_keys,('Event description/option key collision',eid,desc_keys&option_keys)

def check_equipment_references(root,game,source):
    # Stockpile delivery names must exist with or without native equipment overrides.
    equipment_files={q.name:q for q in (game/'common/units/equipment').glob('*.txt')}
    equipment_files.update({q.name:q for q in (root/'common/units/equipment').glob('*.txt')})
    equipment_ids=set()
    equipment_order={}
    for q in sorted(equipment_files.values(),key=lambda q:q.name):
        for container in blocks(q.read_text(encoding='utf-8-sig'),'equipments'):
            for eq,definition in direct_blocks(container).items():
                if eq.startswith('EOR_'):
                    for relation in ['archetype','parent']:
                        target=re.search(r'\b'+relation+r'\s*=\s*(\w+)',definition)
                        if target:
                            assert target[1] in equipment_ids,('Equipment base loaded too late',eq,relation,target[1],q.name)
                equipment_ids.add(eq)
                equipment_order[eq]=q.name
    for delivery in blocks(source,'add_equipment_to_stockpile'):
        eq=scalar(delivery,'type')
        assert eq in equipment_ids,('Unknown stockpile delivery',eq)

def check_unit_bonus_stats(source,enums):
    # A stat existing on a battalion definition is not proof it is accepted in a bonus.
    stat_enum=blocks(enums,'script_enum_equipment_stat')[0]
    stat_tokens,_=lex(stat_enum)
    unit_stats={t[0] for t in stat_tokens[3:-1]}
    for bonus in blocks(source,'add_unit_bonus'):
        for group,body in direct_blocks(bonus).items():
            for stat in re.findall(r'\b(\w+)\s*=\s*-?[\d.]',body):
                assert stat in unit_stats,('Unsupported unit-bonus stat',group,stat)

def check_starting_research(root,game):
    files={q.name:q for q in (game/'common/technologies').glob('*.txt')}
    files.update({q.name:q for q in (root/'common/technologies').glob('*.txt')})
    technologies=set()
    for q in files.values():
        for container in blocks(q.read_text(encoding='utf-8-sig'),'technologies'):
            technologies.update(direct_blocks(container))
    history=(root/'history/countries/EOR - The Empire of the Rising Sun.txt').read_text()
    for grant in blocks(history,'set_technology'):
        for tech in re.findall(r'\b(\w+)\s*=\s*\d+',grant):
            assert tech in technologies,('Invalid EOR starting technology',tech)
    doctrine_files={q.name:q for q in (game/'common/doctrines/grand_doctrines').glob('*.txt')}
    doctrine_files.update({q.name:q for q in (root/'common/doctrines/grand_doctrines').glob('*.txt')})
    doctrines=set()
    for q in doctrine_files.values():
        doctrines.update(re.findall(r'^(\w+)\s*=\s*\{',q.read_text(encoding='utf-8-sig'),re.M))
    for doctrine in re.findall(r'\bset_grand_doctrine\s*=\s*(\w+)',history):
        assert doctrine in doctrines,('Invalid EOR starting doctrine',doctrine)

def check_native(root,game,tree,focuses,positions,manifest,spirits,ideas,dynamic,source,graph):
    # Check actual native GUI geometry, not a second guessed coordinate system.
    gui=(game/'interface/nationalfocusview.gui').read_text()
    spacing=re.search(r'name = "focus_spacing"\s+position = \{ x = (\d+) y = (\d+)',gui)
    sx,sy=map(int,spacing.groups())
    item=re.search(r'name = "national_focus_item".*?size = \{ width = (\d+) height = (\d+)',gui,re.S)
    panel=re.search(r'name = "continuous_focus_window".*?size = \{ width = (\d+) height = (\d+)',gui,re.S)
    iw,ih=map(int,item.groups());pw,ph=map(int,panel.groups())
    cp=re.search(r'continuous_focus_position = \{ x = (\d+) y = (\d+) \}',tree)
    assert cp,'Set an explicit continuous-focus panel position'
    px,py=map(int,cp.groups())
    overlap=lambda a,b: a[0]<b[2] and b[0]<a[2] and a[1]<b[3] and b[1]<a[3]
    rects={f:(x*sx,y*sy,x*sx+iw,y*sy+ih) for f,(x,y) in positions.items()}
    values=list(rects.items())
    for i,(f,a) in enumerate(values):
        for g,b in values[i+1:]:assert not overlap(a,b),('Focus item rectangles overlap',f,g)
    assert all(not overlap((a[0]-20,a[1]-50,a[2]+20,a[3]+50),(px,py,px+pw,py+ph)) for a in rects.values()),'Continuous panel overlaps the tree'
    assert py>=max(a[3]+50 for a in rects.values())+100,'Continuous panel needs a clear gap'
    for fid,requirements in graph.items():
        for parent in set().union(*requirements) if requirements else set():assert positions[parent][1]<positions[fid][1],('Upward prerequisite',parent,fid)
    # Every icon is real, visually distinct at the file level, and matches its reviewed asset.
    interfaces={q.relative_to(game/'interface'):q for q in (game/'interface').rglob('*.gfx')}
    interfaces.update({q.relative_to(root/'interface'):q for q in (root/'interface').rglob('*.gfx')})
    sprites={}
    for q in interfaces.values():
        for b in re.findall(r'\bSpriteType\s*=\s*\{(.*?)\}',q.read_text(encoding='utf-8-sig',errors='replace'),re.S|re.I):
            n=re.search(r'\bname\s*=\s*"([^"]+)"',b,re.I);t=re.search(r'\btexturefile\s*=\s*"([^"]+)"',b,re.I)
            if n and t:sprites[n[1]]=t[1]
    reviewed={f['id']:f for f in manifest['focuses']};hashes={};icons=[]
    for fid,b in focuses.items():
        icon=scalar(b,'icon');icons.append(icon);assert icon in sprites,('Missing sprite',fid,icon)
        asset=sprites[icon];p=root/asset if (root/asset).is_file() else game/asset
        assert p.is_file(),p
        digest=hashlib.sha256(p.read_bytes()).hexdigest();hashes[fid]=digest
        assert digest==reviewed[fid]['artwork_sha256'],('Artwork changed since review',fid)
    assert len(icons)==len(set(icons)),'Repeated focus sprite'
    assert len(hashes)==len(set(hashes.values())),'Repeated focus artwork'
    reviewed_spirits={v['id']:v for v in manifest['spirit_icons']}
    assert set(spirits)==set(reviewed_spirits),'Unreviewed national spirit'
    spirit_hashes=[]
    for key,picture in spirits.items():
        v=reviewed_spirits[key];assert picture==v['picture']
        sprite='GFX_idea_'+picture;assert sprite in sprites,('Unregistered spirit sprite',key)
        assert sprites[sprite]==v['artwork']
        asset=root/v['artwork'] if (root/v['artwork']).is_file() else game/v['artwork']
        assert asset.is_file(),asset
        digest=hashlib.sha256(asset.read_bytes()).hexdigest()
        assert digest==v['sha256'],('Spirit artwork changed since review',key)
        spirit_hashes.append(digest)
    assert len(spirit_hashes)==len(set(spirit_hashes)),'Repeated national-spirit artwork'

    doc=(game/'documentation/modifiers_documentation.md').read_text();valid=set(re.findall(r'^## ([\w]+)\s*$',doc,re.M));valid.update(re.findall(r'^## .*?</span>([\w]+)',doc,re.M))
    valid_modifier=lambda k: k in valid or bool(re.fullmatch(r'(?:production_speed|state_production_speed|state_repair_speed)_[a-z_]+_factor|country_resource_cost_[a-z_]+',k))
    for b in blocks(ideas,'modifier'):
        for k in re.findall(r'(\w+)\s*=\s*-?\d',b):assert valid_modifier(k),('Unknown modifier',k)
    for k in re.findall(r'\b(\w+)\s*=\s*-?\d',dynamic):assert valid_modifier(k),('Unknown state modifier',k)
    for asset in re.findall(r'(?:texturefile|large)\s*=\s*"([^"]+)"',source):assert (root/asset).is_file() or (game/asset).is_file(),asset

    # Decision/category icons and event images must resolve in the effective sprite registry.
    decisions=(root/'common/decisions/eor_decisions.txt').read_text()
    categories=(root/'common/decisions/categories/eor_categories.txt').read_text()
    for key in re.findall(r'\bicon\s*=\s*(\w+)',decisions):
        sprite=key if key.startswith('GFX_') else 'GFX_decision_'+key
        assert sprite in sprites,('Missing decision sprite',key)
    for key in re.findall(r'\bicon\s*=\s*(\w+)',categories):
        assert 'GFX_decision_category_'+key in sprites,('Missing category sprite',key)
    for key in re.findall(r'\bpicture\s*=\s*(GFX_\w+)',(root/'events/EmpireOfTheRisingSun.txt').read_text()):
        assert key in sprites,('Missing event image',key)
        asset=root/sprites[key] if (root/sprites[key]).is_file() else game/sprites[key]
        assert asset.is_file(),asset
    # New fixed-city fort contracts must use the effective filename-merged map.
    state_files={q.name:q for q in (game/'history/states').glob('*.txt')}
    state_files.update({q.name:q for q in (root/'history/states').glob('*.txt')})
    fort_states={282:1182,531:7072,532:10125}
    found={}
    for q in state_files.values():
        state=q.read_text(encoding='utf-8-sig')
        sid=int(scalar(state,'id'))
        if sid in fort_states:
            assert sid not in found,('Duplicate fortress state',sid)
            provinces=blocks(state,'provinces')[0]
            assert fort_states[sid] in set(map(int,re.findall(r'\d+',provinces))),('Fort outside its state',sid)
            found[sid]=q
    assert found.keys()==fort_states.keys(),'Missing fortress grant state'
    check_equipment_references(root,game,source)
    check_unit_bonus_stats(source,(game/'common/script_enums.txt').read_text())
    check_starting_research(root,game)
    print('PASS native static checks: GUI geometry, assets/modifier names, equipment IDs/load order, unit-bonus stats, starting research and fortress locations. Not an engine run or UI confirmation.')

def check(root,game,source_only=False):
    manifest=json.loads((ROOT/'tools/eor_design_manifest.json').read_text())
    assert manifest['version']==3
    names=['common/national_focus/empire_focus.txt','common/national_focus/generic.txt','common/ideas/empire_ideas.txt','common/ideas/eor_v2_ideas.txt','common/characters/EOR.txt','common/country_leader/eor_traits.txt','common/decisions/eor_decisions.txt','common/decisions/categories/eor_categories.txt','common/dynamic_modifiers/eor_operations.txt','common/scripted_effects/eor_effects.txt','common/scripted_triggers/eor_triggers.txt','common/scripted_localisation/eor_authority.txt','interface/eor_decision_icons.gfx','common/on_actions/eor_on_actions.txt','common/technologies/eor_advanced_technologies.txt','common/units/equipment/zz_eor_aircraft.txt','common/opinion_modifiers/eor_v2_opinions.txt','events/EmpireOfTheRisingSun.txt','events/NewsEvents.txt','localisation/events_l_english.yml','localisation/bookmarks_l_english.yml','interface/eor_equipment.gfx','interface/eor_focus_icons.gfx','interface/eor_spirit_icons.gfx','history/countries/EOR - The Empire of the Rising Sun.txt','history/countries/IOT - Imperial Oceanic Territories.txt','common/bookmarks/red_alert.txt','common/technology_sharing/01_tech_sharing_groups.txt']
    paths=[root/p for p in names]
    for p in paths:lex(p.read_text(encoding='utf-8-sig'))
    source='\n'.join(p.read_text(encoding='utf-8-sig') for p in paths)
    tree=(root/'common/national_focus/empire_focus.txt').read_text()
    focus_blocks=blocks(tree,'focus');focuses={scalar(b,'id'):b for b in focus_blocks}
    assert len(focus_blocks)==len(focuses),'Duplicate focus IDs'
    assert set(focuses)==set(manifest['focus_ids']),'Authored focus inventory differs'
    graph={};exclusions={};positions={}
    for fid,b in focuses.items():
        graph[fid]=[set(re.findall(r'focus\s*=\s*([\w-]+)',q)) for q in blocks(b,'prerequisite')]
        exclusions[fid]=set(v for q in blocks(b,'mutually_exclusive') for v in re.findall(r'focus\s*=\s*([\w-]+)',q))
        assert all(group <= focuses.keys() for group in graph[fid]),fid
        assert exclusions[fid] <= focuses.keys(),fid
        positions[fid]=(int(scalar(b,'x')),int(scalar(b,'y')))
    assert len(positions)==len(set(positions.values())),'Focus coordinates overlap'
    assert [f for f in focuses if not graph[f]]==['EOR_the_imperial_dawn'],'Detached focus tree roots'
    reviewed_graph={f['id']:f for f in manifest['focuses']}
    for fid in focuses:
        assert graph[fid]==[set(g) for g in reviewed_graph[fid]['parents']],('Stale prerequisite manifest',fid)
        assert positions[fid]==(reviewed_graph[fid]['x'],reviewed_graph[fid]['y']),('Stale position manifest',fid)
    assert graph['EOR_introduce_the_imperial_mobilization_law']==[{'EOR_the_zaibatsu_economy','EOR_bring_the_zaibatsus_into_the_fold'}],'Mobilization must follow either economic settlement'
    assert graph['EOR_imperial_logistics_network']==[{'EOR_imperial_integration','EOR_asian_cooperation'}]
    for fid in ['EOR_the_nano_construction','EOR_the_robotic_production']:
        assert graph[fid]==[{'EOR_funding_imperial_weaponry_institute'}]

    for fid,b in focuses.items():
        reviewed=reviewed_graph[fid];availability=blocks(b,'available')
        gate=availability[0].split('{',1)[1].rsplit('}',1)[0].strip() if availability else ''
        assert reviewed['gate']==gate,('Stale eligibility manifest',fid)
        assert set(reviewed['excludes'])==exclusions[fid],('Stale exclusion manifest',fid)
        assert reviewed['hidden']==bool(blocks(b,'allow_branch')),('Stale visibility manifest',fid)
        assert reviewed['days']==int(scalar(b,'cost'))*7,('Stale timing manifest',fid)
        assert reviewed['sprite']==scalar(b,'icon'),('Stale sprite manifest',fid)
    for fid,others in exclusions.items():
        assert all(fid in exclusions[o] for o in others),('Asymmetric exclusion',fid)
    for group in manifest['exclusive_groups']:
        for f in group:assert set(group)-{f} <= exclusions[f],('Missing designed exclusion',f)
    # Structural reachability: every focus must have an attainable set of AND/OR
    # prerequisites without requiring two mutually exclusive ancestors.
    groups=[set(g) for g in manifest['exclusive_groups']]
    def ancestry_choices(fid,chosen):
        for g in groups:
            if fid in g:
                assert not (g&chosen-{fid}),('Contradictory required choices',fid,g&chosen)
                chosen.add(fid)
        for alternatives in graph[fid]:ancestry_choices(sorted(alternatives)[0],chosen)
    def reach(chosen):
        blocked=set().union(*(g-(g&chosen) for g in groups if g&chosen))
        done=set()
        while True:
            candidates=[f for f in focuses if f not in done|blocked and not exclusions[f]&done and all(g&done for g in graph[f])]
            if not candidates:break
            for f in candidates:
                if not exclusions[f]&done:done.add(f)
        return done
    for fid in focuses:
        chosen=set();ancestry_choices(fid,chosen);assert fid in reach(chosen),('Unreachable focus',fid)
    for fid,requirements in graph.items():
        for parent in set().union(*requirements) if requirements else set():
            assert positions[parent][1]<positions[fid][1],('Upward prerequisite',parent,fid)
    # Each ordinary policy milestone stays reachable within its political route.
    milestones=manifest['policy_milestones']
    assert len(manifest['political_routes'])==3
    for fid in milestones:
        chosen=set();ancestry_choices(fid,chosen);done=reach(chosen)
        assert fid in done and sum(r in done for r in manifest['political_routes'])==1,(fid,'route conflict')
    # Localization is unambiguous; the picker remains a short single paragraph.
    loc={};counts=Counter()
    for p in (root/'localisation').glob('*.yml'):
        for k,v in re.findall(r'^[ \t]*([^\s:]+):\d*[ \t]+"(.*)"[ \t]*$',p.read_text(encoding='utf-8-sig'),re.M):loc[k]=v;counts[k]+=1
    authored=set(re.findall(r'^[ \t]*([^\s:]+):\d*[ \t]+"', (root/'localisation/eor_design_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
    assert all(counts[k]==1 for k in authored),{k:counts[k] for k in authored if counts[k]!=1}
    for fid in focuses:
        assert fid in loc and fid+'_desc' in loc,fid
        description=loc[fid+'_desc']
        assert description==reviewed_graph[fid]['desc'],('Unreviewed focus description',fid)
        assert len(description.split())>=18 and len(re.findall(r'[.!?](?: |$)',description))>=2,('Incomplete focus prose',fid)
        assert not any(t in description for t in ['advances this program','effects listed below','major political commitment','Balance values are provisional','None']),('Placeholder focus description',fid)

    summary=loc['EOR_WAR_OF_THE_THREE_POWERS_DESC'];assert len(summary.split())<=80 and len(summary)<=600 and '\\n' not in summary
    for key in re.findall(r'\b(?:title|desc|name)\s*=\s*(eor\.\d+\.[a-z_]+)',source):assert key in loc,key
    for key in re.findall(r'custom_effect_tooltip\s*=\s*(EOR_[\w-]+)',source):assert key in loc,key
    assert '[?EOR_imperial_legitimacy' in loc['EOR_imperial_decisions_desc'],'Influence dashboard was overwritten'
    # Definitions and callers must close across the whole active event catalog.
    events={}
    for p in (root/'events').glob('*.txt'):
        new=definitions(p.read_text(encoding='utf-8-sig'));assert not events.keys()&new.keys(),p;events.update(new)
    assert {e for e in events if e.startswith('eor.')}==set(manifest['eor_event_ids'])
    for p in paths:
        _,removed=filter_calls(p.read_text(encoding='utf-8-sig'),set(events));assert not removed,(p,removed)
    for f in re.findall(r'has_completed_focus\s*=\s*(EOR_[\w-]+)',source):assert f in focuses,('Missing focus caller',f)
    custom_defs=set(re.findall(r'^(eor_\w+)\s*=\s*\{',source,re.M));custom_calls=set(re.findall(r'\b(eor_\w+)\s*=\s*(?:yes|no)',source))
    assert custom_calls<=custom_defs,custom_calls-custom_defs
    ideas='\n'.join((root/p).read_text() for p in ['common/ideas/empire_ideas.txt','common/ideas/eor_v2_ideas.txt'])
    idea_ids=set(re.findall(r'^\s*(\w+)\s*=\s*\{',ideas,re.M))
    for k in re.findall(r'\b(?:add_ideas|remove_ideas|add_idea|remove_idea|idea)\s*=\s*(EOR_\w+)',source):assert k in idea_ids,k
    # Every national spirit gets its own reviewed native idea artwork.
    spirits={}
    for country in blocks(ideas,'country'):
        tokens,pairs=lex(country);depth=0
        for i,t in enumerate(tokens[:-2]):
            if t[0]=='{':depth+=1
            elif t[0]=='}':depth-=1
            elif depth==1 and tokens[i+1][0]=='=' and tokens[i+2][0]=='{':
                block=country[t.start():tokens[pairs[i+2]].end()]
                spirits[t[0]]=scalar(block,'picture')
    dynamic=(root/'common/dynamic_modifiers/eor_operations.txt').read_text();dynamic_ids=set(re.findall(r'^(EOR_\w+)\s*=\s*\{',dynamic,re.M))
    for k in re.findall(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*(\w+)',source):assert k in dynamic_ids,k
    # Starting identities and policy boundaries remain explicit.
    h=(root/'history/countries/EOR - The Empire of the Rising Sun.txt').read_text()
    for char in ['EOR_tatsu','EOR_yoshiro','EOR_shinzo']:assert h.count('recruit_character = '+char)==1,char
    assert 'name = "Tatsu"' not in h and 'name = "Shinzo Nagama"' not in h
    assert 'autonomous_state =' not in h,'Use modern autonomy_state'
    assert 'set_popularities' in h and 'EOR_2008' in h
    effects=(root/'common/scripted_effects/eor_effects.txt').read_text();on=(root/'common/on_actions/eor_on_actions.txt').read_text()
    assert 'on_daily_EOR' in on and 'on_monthly_EOR' in on and 'on_daily =' not in on
    assert 'start_civil_war' in effects and 'ideology = neutrality ruling_party = fascism' in effects
    assert 'keep_all_characters = yes' in effects and 'set_nationality = event_target:EOR_loyalist_country' in effects
    assert 'eor_secret_path_eligible' not in source
    # No removed government, automatic border handovers or custom victory system.
    for token in ['EOR_route_reform','EOR_new_dawn_unlocked','eor_secret_path_eligible','eor_decolonize_direct_holdings','eor_offer_decolonization','EOR_v2_victory_achieved','eor_technology_victory','eor_yoshiro_victory','eor_tatsu_victory','eor_shinzo_victory','EOR_voluntary_partner','EOR_regional_partners']:
        assert token not in source,('Discarded design remains active',token)
    assert 'transfer_state_to' not in effects,'Automatic territorial transfers survived removal'
    for key in manifest['removed_focus_ids']:
        assert key not in focuses and not re.search(r'\b'+key+r'\b',source),key
    # Semantic event checks: body descriptions cannot double as option labels.
    for eid,event in events.items():check_event_roles(eid,event)
    for eid,event in definitions((root/'events/EmpireOfTheRisingSun.txt').read_text()).items():
        for key in re.findall(r'\b(?:title|desc|name|text)\s*=\s*(eor\.[\w.]+)',event):
            assert key in loc,('Missing event localization',eid,key)
    # The selected economic spirit is granted centrally and clears competing identities.
    for mode,idea,other in [('corporate','EOR_cooperative_zaibatsus','state'),('state','EOR_controlled_zaibatsus','corporate')]:
        effect=blocks(effects,'eor_choose_'+mode+'_economy')[0]
        assert 'add_ideas = '+idea in effect
        assert 'clr_country_flag = EOR_'+other+'_economy' in effect
        for old in ['traditional_zaibatsus','EOR_cooperative_zaibatsus','EOR_controlled_zaibatsus']:
            assert 'remove_ideas = '+old in effect
    assert 'eor_choose_corporate_economy = yes' in focuses['EOR_corporate_partnership']
    assert 'eor_choose_state_economy = yes' in focuses['EOR_state_control']
    assert not re.search(r'add_ideas\s*=\s*(?:cooperative_zaibatsus|controlled_zaibatsus)\b',source)
    authority=blocks(effects,'eor_refresh_mandate')[0]
    assert authority.index('character = EOR_tatsu')<authority.index('EOR_authority > 79')
    assert authority.count('value = EOR_imperial_legitimacy')==2 and 'value = EOR_divine_mandate' in authority
    assert 'EOR_mandate_reformed' not in authority
    # Current recipients must lose every subject-only benefit, even if it was their only one.
    subjects=blocks(effects,'eor_update_subjects')[0]
    cleanup=blocks(subjects,'every_country')[0]
    assert 'NOT = { is_subject_of = EOR }' in cleanup and 'EOR_voluntary_partner' not in cleanup
    for key in ['EOR_subject_'+v for v in ['centralized','partnership','resource_access','concessions','security','resentment','development']]:
        assert 'has_idea = '+key in blocks(cleanup,'limit')[0]
        assert 'remove_ideas = '+key in cleanup
    # Country spirit prose uses an explicit localized name, independent from focus/decision prose.
    for country in blocks(ideas,'country'):
        for key,block in direct_blocks(country).items():
            name=scalar(block,'name');description=loc.get(name+'_desc','')
            assert name in loc and description,('Missing spirit-role prose',key)
            assert not any(v in description.lower() for v in ['balance values','initial balance','requires testing','choose a ','invest 75 pp']),('Development/choice prose in spirit',key)
    decisions=(root/'common/decisions/eor_decisions.txt').read_text()
    categories=direct_blocks('wrapper = { '+decisions+' }')
    assert len(categories)==5,'Expected five intent-based decision categories'
    entries={}
    for category,block in categories.items():
        assert category in loc and category+'_desc' in loc
        for key,decision in direct_blocks(block).items():
            assert key not in entries,('Duplicate decision',key)
            entries[key]=decision
            assert key in loc and key+'_desc' in loc,key
    assert set(entries)==set(manifest['decision_ids']),'Decision inventory changed'
    for key,decision in entries.items():
        if key.startswith('EOR_subject_'):
            tag=key.split('_')[2].upper();end=blocks(decision,'remove_effect')[0]
            assert 'is_subject_of = ROOT' in end
            assert f'is_owned_by = {tag} is_controlled_by = {tag}' in end
            assert 'is_controlled_by = ROOT' not in end
            assert 'save_global_event_target_as = '+key+'_state' in decision
            assert 'clear_global_event_target = '+key+'_state' in end
    phi=entries['EOR_subject_phi_local_military_administration']
    assert 'EOR = { add_to_variable = { var = EOR_subject_pressure value = -5 } }' in phi
    sabotage=blocks(entries['EOR_omega_sabotage'],'remove_effect')[0]
    assert 'damage_building = { type = arms_factory damage = 2 }' in sabotage
    assert 'modifier = EOR_psionic_factory_disruption days = 60 scope = ROOT' in sabotage
    assert 'FROM = { controller = { has_war_with = ROOT } arms_factory > 0 }' in sabotage
    for kind in ['executioner','giga_fortress','black_tortoise']:
        prepare=entries['EOR_build_'+kind];activate=entries['EOR_activate_'+kind]
        assert 'set_country_flag = EOR_'+kind+'_ready' in blocks(prepare,'remove_effect')[0]
        assert 'add_timed_idea' not in blocks(prepare,'remove_effect')[0]
        assert 'has_war = yes' in blocks(activate,'available')[0]
        assert 'clr_country_flag = EOR_'+kind+'_ready' in activate
    for key in ['EOR_omega_assault','EOR_omega_command_disruption','EOR_omega_sabotage','EOR_omega_counterintelligence']:
        assert 'EOR_omega_cooldown' in entries[key]
        end=blocks(entries[key],'remove_effect')[0]
        assert 'else =' in end and 'country_event' in end,('Missing mission failure report',key)
    # Playability regressions: paid follow-ups must deliver an independent action,
    # bilateral work must have a current partner, and delayed investments must
    # survive neither a changed government nor an invalid recipient as rewards.
    diplomacy=blocks(focuses['EOR_divide_our_enemies'],'completion_reward')[0]
    assert 'eor_event_105' not in diplomacy and 'EOR_targeted_envoys_authorized' in diplomacy,'Duplicate one-time diplomacy reward'
    concessions=blocks(focuses['EOR_resource_concessions'],'completion_reward')[0]
    assert 'EOR_resource_development_authorized' not in concessions
    assert 'add_resource' in concessions and 'is_subject_of = ROOT' in concessions
    for fid in ['EOR_the_asian_accord','EOR_joint_military_plan','EOR_partners_in_asia']:
        assert 'eor_china_partnership_current = yes' in blocks(focuses[fid],'available')[0]
        assert 'add_to_tech_sharing_group' not in focuses[fid],('Independent partner sent to subject group',fid)
    # Unmet partnership conditions must not make the branch look rewardless.
    china_focuses=['EOR_regional_policy','EOR_the_china_question','EOR_cooperate_with_china',
                   'EOR_the_asian_accord','EOR_joint_military_plan','EOR_partners_in_asia',
                   'EOR_subjugate_china','EOR_imperial_ultimatum','EOR_the_chinese_campaign',
                   'EOR_imperial_protectorate']
    for fid in china_focuses:
        reward=blocks(focuses[fid],'completion_reward')[0]
        assert not blocks(reward,'hidden_effect'),('Native China effect details were hidden',fid)
        assert 'custom_effect_tooltip = '+fid+'_reward_tt' in reward,('Missing unconditional China reward preview',fid)
        assert len(loc[fid+'_reward_tt'].split())>=12,('Empty China reward preview',fid)
    assert 'add_equipment_to_stockpile' in focuses['EOR_subjugate_china']
    assert 'modifier = EOR_chinese_offensive' in focuses['EOR_the_chinese_campaign']
    assert 'add_building_construction' in focuses['EOR_imperial_protectorate']
    assert 'is_core_of = CHI' in focuses['EOR_imperial_protectorate']
    for fid in ['EOR_imperial_warrior_armaments','EOR_amphibious_armored_formations','EOR_deploy_king_oni','EOR_mecha_tengu_squadrons']:
        reward=blocks(focuses[fid],'completion_reward')[0]
        assert 'add_equipment_to_stockpile' in reward,('Known technology leaves no service reward',fid)
    for fid,old in [('EOR_dominate_the_skies','EOR_v2_air_superiority'),('EOR_support_the_army','EOR_v2_tactical_support')]:
        assert 'remove_ideas = '+old in focuses[fid],('Endpoint stacks its predecessor',fid)
    review=entries['EOR_schedule_court_review']
    assert 'EOR_global_threat' not in review and 'EOR_intelligence_complete' not in review
    assert 'eor_no_political_route = yes' in blocks(review,'remove_effect')[0]
    for key,route in [
        ('EOR_sacred_mobilization','divine'),('EOR_imperial_prestige_project','divine'),
        ('EOR_fund_homeland_fortress','divine'),('EOR_automated_armored_contract','technocratic'),
        ('EOR_combined_force_contract','technocratic'),('EOR_land_service_program','shinzo'),
        ('EOR_naval_service_program','shinzo'),('EOR_settle_military_administration','shinzo'),
        ('EOR_postwar_imperial','divine'),('EOR_postwar_science','technocratic'),('EOR_postwar_military','shinzo')]:
        end=blocks(entries[key],'remove_effect')[0]
        assert 'has_country_flag = EOR_route_'+route in blocks(end,'limit')[0],('Stale government delivery',key)
        assert 'else =' in end and 'id = eor.145' in end,('Missing invalidation report',key)
    prestige=entries['EOR_imperial_prestige_project']
    assert 'save_global_event_target_as = EOR_prestige_recipient' in prestige
    assert 'clear_global_event_target = EOR_prestige_recipient' in prestige
    assert 'is_owned_by = event_target:EOR_prestige_recipient' in prestige
    assert 'is_controlled_by = event_target:EOR_prestige_recipient' in prestige
    for tag in ['sov','usa','eng','aoe']:
        end=blocks(entries['EOR_prepare_settlement_'+tag],'remove_effect')[0]
        assert 'eor_can_receive_settlement = yes' in blocks(end,'limit')[0]
        assert 'else =' in end and 'id = eor.155' in end
    assert 'factor = 2 has_country_flag = EOR_prepared_settlement' in events['eor.114']
    assert 'add_political_power = -100' not in events['eor.110'],'Chinese terms charge EOR before consent'
    assert 'id = eor.150' in events['eor.110'] and len(blocks(events['eor.150'],'option'))==2
    monthly=blocks(effects,'eor_monthly_update')[0]
    assert 'value = EOR_administration_relief' in monthly
    assert 'has_country_flag = EOR_subject_demands_issued NOT = { has_country_flag = EOR_demands_recent }' in monthly
    assert 'EOR_administration_relief min = 0 max = 6' in monthly
    daily=blocks(effects,'eor_daily_update')[0]
    assert 'eor_moscow_secured = yes NOT = { has_country_flag = EOR_event_14 }' in daily
    assert 'eor_allies_defeated = yes NOT = { has_country_flag = EOR_event_23 }' in daily
    assert 'EOR_northern_preparation_delivered' in daily
    # The selector must list all four starting EOR subjects as ordinary minors, without a custom label tab.
    bookmark=(root/'common/bookmarks/red_alert.txt').read_text()
    assert 'filters' not in bookmark and 'label_order' not in bookmark,'Custom bookmark label filter must stay removed'
    assert 'scrollable_country_list = yes' in bookmark
    for tag in ['IOT','PHI','MAL','INS']:
        country=blocks(bookmark,'"'+tag+'"')
        assert len(country)==1,('Missing/duplicate Imperial minor entry',tag)
        assert 'minor = yes' in country[0] and 'label' not in country[0]
        history=scalar(country[0],'history').strip('"')
        assert history in loc,('Missing minor-country briefing',tag,history)
    authored_focus_ids=set()
    # Preview references use authored trees. Installed compatibility overlays also
    # include unrelated inherited trees, including a malformed native TSR file.
    # Continue strict parsing of every authored tree in source and installed copies.
    for authored in (ROOT/'common/national_focus').glob('*.txt'):
        p=root/'common/national_focus'/authored.name
        authored_focus_ids.update(scalar(b,'id') for b in blocks(p.read_text(encoding='utf-8-sig'),'focus'))
    for preview in blocks(bookmark,'focuses'):
        tokens,_=lex(preview)
        assert {t[0] for t in tokens[3:-1]} <= authored_focus_ids,('Invalid bookmark focus preview',preview)
    assert h.index('set_air_oob = "EOR_2008_air"')>h.rindex('set_naval_oob ='), 'Carrier wings registered before navy'
    iot_history=(root/'history/countries/IOT - Imperial Oceanic Territories.txt').read_text()
    assert 'expire = "2051.1.1"' in iot_history,'IOT leader expires before the scenario ends'
    assert 'picture = "gfx/leaders/IOT/Portrait_the_oceanic_office.dds"' in iot_history
    # PHI/MAL/INS use institutional governments like IOT, each valid past the scenario end.
    institutions={
        'PHI':('history/countries/EOR - The Empire of the Rising Sun.txt','The Imperial Philippine Government','gfx/leaders/PHI/Portrait_imperial_philippine_government.dds'),
        'MAL':('history/countries/EOR - The Empire of the Rising Sun.txt','The Imperial Malayan Government','gfx/leaders/MAL/Portrait_imperial_malayan_government.dds'),
        'INS':('history/countries/EOR - The Empire of the Rising Sun.txt','The Imperial Indonesian Government','gfx/leaders/INS/Portrait_imperial_indonesian_government.dds'),
    }
    for tag,(path,name,picture) in institutions.items():
        leaders=[b for b in blocks((root/path).read_text(),'create_country_leader') if name in b]
        assert len(leaders)==1,('Missing/duplicate institutional government leader',tag)
        assert 'ideology = fascism_ideology' in leaders[0],('Institutional leader has wrong ideology',tag)
        assert 'expire = "2051.1.1"' in leaders[0],('Institutional leader expires before the scenario ends',tag)
        assert f'picture = "{picture}"' in leaders[0],('Institutional leader has wrong portrait',tag)
        assert (root/picture).is_file(),('Missing institutional leader portrait',picture)
    assert 'replace_path="events"' in (root/'descriptor.mod').read_text()
    # IOT must select the full generic tree, not the former empty stub.
    generic=(root/'common/national_focus/generic.txt').read_text()
    assert 'id = generic_focus' in generic and 'default = yes' in generic
    assert re.search(r'modifier\s*=\s*\{\s*add\s*=\s*100\s+tag\s*=\s*IOT',generic)
    assert len(blocks(generic,'focus'))>40,'IOT generic tree is empty or incomplete'
    assert not (root/'common/national_focus/iot_focus.txt').exists()
    print(f'PASS source phase: {len(focuses)} focus graphs, 3 political routes, {len(entries)} decisions, {len(events)} events, economic/authority/recipient invariants, role-specific prose, event keys and IOT selection.')
    if not source_only:
        required=[game/'interface/nationalfocusview.gui',game/'documentation/modifiers_documentation.md']
        missing=[str(p) for p in required if not p.is_file()]
        if missing:raise FileNotFoundError('Native phase blocked; missing '+', '.join(missing)+'. Use --source-only for script checks.')
        check_native(root,game,tree,focuses,positions,manifest,spirits,ideas,dynamic,source,graph)
    return paths+[root/'localisation/eor_design_l_english.yml']

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--source-only',action='store_true');p.add_argument('--installed',type=Path);p.add_argument('--game-dir',type=Path,default=GAME);a=p.parse_args()
    paths=check(ROOT,a.game_dir,a.source_only)
    if a.installed:
        check(a.installed,a.game_dir,a.source_only)
        for f in paths:assert f.read_bytes()==(a.installed/f.relative_to(ROOT)).read_bytes(),('Installed mismatch',f)
        assert not (a.installed/'.startup-tracing.json').exists()
        assert not (a.installed/'.runtime-tracing.json').exists()
        print('PASS: installed authored content matches source; no diagnostic overlays.')
