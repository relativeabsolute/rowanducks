

import unittest
import os
from src.diff import Diff
from src.regex import main
from src.SourceMonitor import SourceMonitor
import json
from datetime import datetime

class TestChangesTestCase(unittest.TestCase):
    # run source monitor on directory of input
    def setUp(self):
        print('setting up TestChangesTestCase')
        print(os.getcwd())
        self.diff = Diff()
        self.diff.readInput('../data/SampleDirectory')
        self.diff.run_diff_on_latest_commit()
        self.sm = SourceMonitor(self.diff)
        # Analyze files
        self.cms2files = main(['src/data/SampleDirectory'])
        # Load expected output
        self.num_changes = json.loads(open('../expected_output/num_changes.json').read())
        self.change_types = json.loads(open('../expected_output/change_types.json').read())

    def test_changes(self):
        print('running test_changes')
        diff_attr = [a for a in dir(self.diff.diff_list[0]) if not a.startswith('__')
                     and not callable(getattr(self.diff.diff_list[0], a))]
        for file_diff in self.diff.diff_list:
            expected = self.find_file(self.num_changes, file_diff)
            for attr in diff_attr:
                self.assertEqual(file_diff.getattr(file_diff, attr), expected['attr'])

    def test_change_types(self):
        print('running test_change_types')
        change_types = ['name', 'notes', 'total_src_lines', 'hl_exec_stmts', 'hl_data_stmts', 'goto_stmts',
                        'direct_exec_stmts', 'direct_comments', 'block_comments', 'hl_multi_stmt_counter']
        for file in self.cms2files:
            expected = self.find_file(self.change_types, file)
            for field in change_types:
                self.assertEqual(file.getattr(field), expected[field])

    def test_monitor_format(self):
        print('running test_monitor_format')
        headings = ['MODULE', 'FILE STATUS', 'INITIAL SIZE', 'CPCR', 'ADDITIONS', 'MODIFICATIONS', 'DELETIONS']
        for heading in headings:
            self.assertTrue(heading in self.sm.header_string)
        current_date = datetime.now().strftime("%d/%b/%Y")
        self.assertTrue(current_date in self.sm.header_string)

    def test_monitor_report(self):
        print('running test_monitor_report')
        columns = open('../expected_output/monitor_headings.txt').read()
        self.assertEqual(columns, self.sm.main_string)

    def find_file(self, expected_output, test_data):
        for file in expected_output:
            if file['filename'] == test_data.filename:
                return file
        self.assertTrue(False)