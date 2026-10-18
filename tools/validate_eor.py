#!/usr/bin/env python3
"""Validate EOR's authored V2 graph, references and presentation, plus IOT's generic tree.

These static checks do not run the engine or establish runtime stability/balance.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,re
from event_compat import lex,definitions,filter_calls

ROOT=Path(__file__).resolve().parents[1]
GAME=Path.home()/'Library/Application Support/Steam/steamapps/common/Hearts of Iron IV'

def blocks(text,key):
    tokens,pairs=lex(text)
    return [text[t.start():tokens[pairs[i+2]].end()] for i,t in enumerate(tokens[:-2]) if t[0]==key and tokens[i+1][0]=='=' and tokens[i+2][0]=='{']

def scalar(text,key):
    return re.search(r'\b'+re.escape(key)+r'\s*=\s*([^\s}]+)',text)[1]

def check(root,game):
    manifest=json.loads((ROOT/'tools/eor_design_manifest.json').read_text())
    assert manifest['version']==2
    names=['common/national_focus/empire_focus.txt','common/national_focus/generic.txt','common/ideas/empire_ideas.txt','common/ideas/eor_v2_ideas.txt','common/characters/EOR.txt','common/country_leader/eor_traits.txt','common/decisions/eor_decisions.txt','common/decisions/categories/eor_categories.txt','common/dynamic_modifiers/eor_operations.txt','common/scripted_effects/eor_effects.txt','common/scripted_triggers/eor_triggers.txt','common/on_actions/eor_on_actions.txt','common/technologies/eor_advanced_technologies.txt','common/units/equipment/eor_aircraft.txt','common/opinion_modifiers/eor_v2_opinions.txt','events/EmpireOfTheRisingSun.txt','interface/eor_equipment.gfx','interface/eor_focus_icons.gfx','interface/eor_spirit_icons.gfx','history/countries/EOR - The Empire of the Rising Sun.txt','common/bookmarks/red_alert.txt','common/technology_sharing/01_tech_sharing_groups.txt']
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
    # Each political ending is reachable while keeping the other route roots excluded.
    victories=manifest['victory_focuses']
    for fid in victories:
        chosen=set();ancestry_choices(fid,chosen);done=reach(chosen)
        assert fid in done and sum(r in done for r in manifest['political_routes'])==1,(fid,'route conflict')
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
    # Localization is unambiguous; the picker remains a short single paragraph.
    loc={};counts=Counter()
    for p in (root/'localisation').glob('*.yml'):
        for k,v in re.findall(r'^\s+([^\s:]+):\d*\s+"(.*)"\s*$',p.read_text(encoding='utf-8-sig'),re.M):loc[k]=v;counts[k]+=1
    authored=set(re.findall(r'^\s+([^\s:]+):\d*', (root/'localisation/eor_design_l_english.yml').read_text(encoding='utf-8-sig'),re.M))
    assert all(counts[k]==1 for k in authored),{k:counts[k] for k in authored if counts[k]!=1}
    for fid in focuses:
        assert fid in loc and fid+'_desc' in loc,fid
        description=loc[fid+'_desc']
        assert description==reviewed_graph[fid]['desc'],('Unreviewed focus description',fid)
        assert len(description.split())>=18 and len(re.findall(r'[.!?](?: |$)',description))>=2,('Incomplete focus prose',fid)
        assert not any(t in description for t in ['advances this program','effects listed below','major political commitment','Balance values are provisional','None']),('Placeholder focus description',fid)

    summary=loc['EOR_WAR_OF_THE_THREE_POWERS_DESC'];assert len(summary.split())<=80 and len(summary)<=600 and '\\n' not in summary
    for key in re.findall(r'\b(?:title|desc|name)\s*=\s*(eor\.\d+\.[a-z]+)',source):assert key in loc,key
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

    dynamic=(root/'common/dynamic_modifiers/eor_operations.txt').read_text();dynamic_ids=set(re.findall(r'^(EOR_\w+)\s*=\s*\{',dynamic,re.M))
    for k in re.findall(r'add_dynamic_modifier\s*=\s*\{\s*modifier\s*=\s*(\w+)',source):assert k in dynamic_ids,k
    doc=(game/'documentation/modifiers_documentation.md').read_text();valid=set(re.findall(r'^## ([\w]+)\s*$',doc,re.M));valid.update(re.findall(r'^## .*?</span>([\w]+)',doc,re.M))
    valid_modifier=lambda k: k in valid or bool(re.fullmatch(r'(?:production_speed|state_production_speed|state_repair_speed)_[a-z_]+_factor|country_resource_cost_[a-z_]+',k))
    for b in blocks(ideas,'modifier'):
        for k in re.findall(r'(\w+)\s*=\s*-?\d',b):assert valid_modifier(k),('Unknown modifier',k)
    for k in re.findall(r'\b(\w+)\s*=\s*-?\d',dynamic):assert valid_modifier(k),('Unknown state modifier',k)
    for asset in re.findall(r'(?:texturefile|large)\s*=\s*"([^"]+)"',source):assert (root/asset).is_file() or (game/asset).is_file(),asset
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
    assert 'mark_focus_tree_layout_dirty = yes' in source and 'eor_secret_path_eligible' in effects
    # Territorial transfers are confined to the approved reform settlement.
    settlement=blocks(effects,'eor_decolonize_direct_holdings')[0]
    assert 'has_country_flag = EOR_route_reform' in settlement
    expected=manifest['new_dawn_state_returns']
    assert expected['CHI']==[524] and set(expected['SOV'])=={537,555,655}
    for tag,ids in expected.items():
        for state in ids:
            b=blocks(settlement,str(state))[-1]
            assert 'is_owned_by = EOR is_fully_controlled_by = EOR' in b
            assert f'transfer_state_to = {tag}' in b
            assert 'clr_state_flag = EOR_initial_home_core' in b
    remainder=effects.replace(settlement,'')
    assert 'transfer_state_to' not in remainder,'Transfers outside approved decolonization'
    assert 'eor_decolonize_direct_holdings = yes' in blocks(effects,'eor_offer_decolonization')[0]
    assert 'replace_path="events"' in (root/'descriptor.mod').read_text()
    # IOT must select the full generic tree, not the former empty stub.
    generic=(root/'common/national_focus/generic.txt').read_text()
    assert 'id = generic_focus' in generic and 'default = yes' in generic
    assert re.search(r'modifier\s*=\s*\{\s*add\s*=\s*100\s+tag\s*=\s*IOT',generic)
    assert len(blocks(generic,'focus'))>40,'IOT generic tree is empty or incomplete'
    assert not (root/'common/national_focus/iot_focus.txt').exists()
    print(f'PASS: {len(focuses)} focus prerequisite graphs, 4 political endings, unique focus/spirit artwork, complete descriptions, connected branches, layout, crisis/civil-war wiring, references, {len(events)} events, compact localization and IOT generic selection.')
    return paths+[root/'localisation/eor_design_l_english.yml']

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--installed',type=Path);p.add_argument('--game-dir',type=Path,default=GAME);a=p.parse_args()
    paths=check(ROOT,a.game_dir)
    if a.installed:
        check(a.installed,a.game_dir)
        for f in paths:assert f.read_bytes()==(a.installed/f.relative_to(ROOT)).read_bytes(),('Installed mismatch',f)
        assert not (a.installed/'.startup-tracing.json').exists()
        assert not (a.installed/'.runtime-tracing.json').exists()
        print('PASS: installed authored content matches source; no diagnostic overlays.')
