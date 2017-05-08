

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
        print('constructing diff object')
        self.diff = Diff()
        print('reading input from sample directory')
        self.diff.readInput(['src/testing/data/SampleDirectory'])
        print('running on latest commit')
        self.diff.run_diff_on_latest_commit()
        self.sm = SourceMonitor(self.diff)
        # Analyze files
        self.cms2files = main(['src/testing/data/SampleDirectory'])
        # Load expected output
        self.num_changes = json.loads(open('src/testing/expected_output/num_changes.json').read())
        self.change_types = json.loads(open('src/testing/expected_output/change_types.json').read())

    def test_changes(self):
        print('running test_changes')
        diff_attr = [a for a in dir(self.diff.diff_list[0]) if not a.startswith('__')
                     and not callable(getattr(self.diff.diff_list[0], a))]
        for file_diff in self.diff.diff_list:
            expected = self.find_file(self.num_changes, file_diff)
            self.assertTrue(expected)
            for attr in diff_attr:
                if(attr in expected):
                    if (attr != 'name'):
                        self.assertEqual(str(getattr(file_diff, attr)), str(expected[attr]))
                    # If the key is 'name' we need to trim it for comparison
                    else:
                        self.assertEqual(os.path.split(getattr(file_diff,attr))[1], expected[attr])

    def test_change_types(self):
        print('running test_change_types')
        change_types = ['name', 'notes', 'total_src_lines', 'hl_exec_stmts', 'hl_data_stmts', 'goto_stmts',
                        'direct_exec_stmts', 'direct_comments', 'block_comments', 'hl_multi_stmt_counter']
        for file in self.cms2files:
            expected = self.find_file(self.change_types, file)
            self.assertTrue(expected)
            for field in change_types:
                if(field in expected):
                    if (field != 'name'):
                        self.assertEqual(getattr(file, field), expected[field])
                    # If the key is 'name' we need to trim it for comparison
                    else:
                        self.assertEqual(os.path.split(getattr(file,field))[1], expected[field])

    def test_monitor_format(self):
        print('running test_monitor_format')
        headings = ['MODULE', 'FILE STATUS', 'INITIAL SIZE', 'CPCR', 'ADDITIONS', 'MODIFICATIONS', 'DELETIONS']
        for heading in headings:
            self.assertTrue(heading in self.sm.header_string)
        current_date = datetime.now().strftime("%d/%b/%Y")
        self.assertTrue(current_date in self.sm.header_string)

    def test_monitor_report(self):
        print('running test_monitor_report')
        columns = open('src/testing/expected_output/monitor_headings.txt').read()
        print(columns)
        print(self.sm.main_string)
        self.assertEqual(str(columns), str(self.sm.main_string))

    def find_file(self, expected_output, test_data):
        to_find = os.path.split(test_data.name)[1]
        print('calling find_file for {0}'.format(to_find))
        for file in expected_output:
            if file['name'] == str(to_find):
                return file
        print(to_find)
