#!/usr/bin/env python3
"""Regression fixtures for EOR review defects. These do not execute the HOI4 engine."""
from pathlib import Path
from contextlib import redirect_stdout
import io
import shutil
import tempfile
import unittest

from validate_eor import (ROOT, GAME, blocks, scalar, check,
                          check_equipment_references, check_unit_bonus_stats, check_starting_research)


class AuditRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='ra3_audit_tests_')
        cls.fixture = Path(cls.temp.name)
        for folder in ['common', 'events', 'localisation', 'interface']:
            shutil.copytree(ROOT / folder, cls.fixture / folder)
        for name in ['EOR - The Empire of the Rising Sun.txt','IOT - Imperial Oceanic Territories.txt','SOV - Soviet union.txt']:
            country = Path('history/countries') / name
            (cls.fixture / country).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(ROOT / country, cls.fixture / country)
        for tag in ['IOT','PHI','MAL','INS']:
            shutil.copytree(ROOT / 'gfx/leaders' / tag, cls.fixture / 'gfx/leaders' / tag)
        shutil.copytree(ROOT / 'gfx/flags', cls.fixture / 'gfx/flags')
        shutil.copy2(ROOT / 'descriptor.mod', cls.fixture / 'descriptor.mod')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def source_check(self):
        with redirect_stdout(io.StringIO()):
            check(self.fixture, GAME, source_only=True)

    def rejects(self, file, mutate, message, check_fn=None):
        path = self.fixture / file
        original = path.read_bytes()
        text = path.read_text(encoding='utf-8-sig')
        modified = mutate(text)
        self.assertNotEqual(text, modified)
        try:
            path.write_text(modified, encoding='utf-8')
            with self.assertRaisesRegex(AssertionError, message):
                (check_fn or self.source_check)()
        finally:
            path.write_bytes(original)

    def test_valid_source(self):
        self.source_check()

    def test_missing_iot_menu_entry(self):
        def remove(text):
            return text.replace(blocks(text, '"IOT"')[0], '', 1)
        self.rejects('common/bookmarks/red_alert.txt', remove, 'Missing/duplicate Imperial minor')

    def test_iot_leader_is_valid_for_the_scenario(self):
        self.rejects('history/countries/IOT - Imperial Oceanic Territories.txt',
                     lambda t: t.replace('expire = "2051.1.1"', 'expire = "1989.1.1"', 1),
                     'IOT leader expires before the scenario ends')

    def test_institutional_leaders_last_past_scenario_end(self):
        self.rejects('history/countries/EOR - The Empire of the Rising Sun.txt',
                     lambda t: t.replace('expire = "2051.1.1"', 'expire = "1989.1.1"', 1),
                     'Institutional leader expires before the scenario ends')
        self.rejects('history/countries/EOR - The Empire of the Rising Sun.txt',
                     lambda t: t.replace('Portrait_imperial_philippine_government.dds', 'Portrait_Philippines_Manuel_Luis_Quezon.dds', 1),
                     'Institutional leader has wrong portrait')

    def test_dead_bookmark_preview(self):
        self.rejects('common/bookmarks/red_alert.txt',
                     lambda t: t.replace('SOV_the_red_continent', 'SOV_finish_five_year_plan', 1),
                     'Invalid bookmark focus preview')

    def test_native_china_rewards_cannot_be_hidden(self):
        def hide(text):
            focus = next(b for b in blocks(text, 'focus') if scalar(b, 'id') == 'EOR_the_asian_accord')
            reward = blocks(focus, 'completion_reward')[0]
            modified = reward.replace('completion_reward = {',
                                      'completion_reward = { hidden_effect = {', 1) + '\n}'
            return text.replace(focus, focus.replace(reward, modified, 1), 1)
        self.rejects('common/national_focus/empire_focus.txt', hide, 'Native China effect details were hidden')

    def test_independent_china_cannot_receive_subject_research_membership(self):
        def add(text):
            focus = next(b for b in blocks(text, 'focus') if scalar(b, 'id') == 'EOR_partners_in_asia')
            reward = blocks(focus, 'completion_reward')[0]
            modified = reward[:-1] + ' CHI = { add_to_tech_sharing_group = imperial_research } }'
            return text.replace(focus, focus.replace(reward, modified, 1), 1)
        self.rejects('common/national_focus/empire_focus.txt', add, 'Independent partner sent to subject group')

    def test_ai_plan_cannot_reference_missing_focus(self):
        self.rejects('common/ai_strategy_plans/EOR_default_strategy_plan.txt',
                     lambda t: t.replace('EOR_the_imperial_dawn = 10', 'EOR_missing_focus = 10', 1),
                     'AI plan references unknown focus')

    def test_equipment_load_order(self):
        current = self.fixture / 'common/units/equipment/zz_eor_aircraft.txt'
        old = current.with_name('aa_eor_aircraft.txt')
        current.rename(old)
        try:
            with self.assertRaisesRegex(AssertionError, 'Equipment base loaded too late'):
                check_equipment_references(self.fixture, GAME, '')
        finally:
            old.rename(current)
        check_equipment_references(self.fixture, GAME, '')

    def test_parser_rejected_manpower_stat(self):
        enums = (GAME / 'common/script_enums.txt').read_text()
        with self.assertRaisesRegex(AssertionError, 'Unsupported unit-bonus stat'):
            check_unit_bonus_stats('add_unit_bonus = { category_all_armor = { manpower = -0.05 } }', enums)
        check_unit_bonus_stats((ROOT / 'common/national_focus/empire_focus.txt').read_text(), enums)

    def test_obsolete_starting_doctrine_cannot_be_granted_as_technology(self):
        def obsolete(text):
            return text.replace('set_technology = {', 'set_technology = { trench_warfare = 1', 1)
        self.rejects('history/countries/EOR - The Empire of the Rising Sun.txt',
                     obsolete, 'Invalid EOR starting technology',
                     check_fn=lambda: check_starting_research(self.fixture, GAME))
        check_starting_research(self.fixture, GAME)

    def test_authorization_cooldowns_do_not_add_preparation_again(self):
        text = (ROOT / 'common/decisions/eor_decisions.txt').read_text()
        for key in ['EOR_prepare_major_offensive', 'EOR_omega_assault', 'EOR_omega_sabotage']:
            with self.subTest(decision=key):
                decision = blocks(text, key)[0]
                prepare = int(scalar(decision, 'days_remove'))
                reenable = int(scalar(decision, 'days_re_enable'))
                flags = blocks(blocks(decision, 'complete_effect')[0], 'set_country_flag')
                cooldown = next(f for f in flags if 'cooldown' in scalar(f, 'flag'))
                duration = int(scalar(cooldown, 'days'))
                available = blocks(decision, 'available')[0]
                self.assertIn('NOT = { has_country_flag = ' + scalar(cooldown, 'flag') + ' }', available)
                self.assertEqual(max(duration, prepare + reenable), duration)


if __name__ == '__main__':
    unittest.main(verbosity=2)
