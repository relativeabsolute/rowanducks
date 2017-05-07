# this file contains unit tests for statement related test cases
# see Verification Script steps 1.1-1.4.2 and 2.1
# Author: Johan Burke

import unittest
import os
import json
from src.regex import main

class StatementsTestCase(unittest.TestCase):
    # run source analyzer on directory of input
    def setUp(self):
        print('setting up StatementsTestCase')
        print(os.getcwd())
        self.files_root_dir = 'src/testing/data/SampleDirectory'
        self.cms2files = main([self.files_root_dir])
        # load expected output
        self.exec_stmts = json.loads(open('src/testing/expected_output/exec_stmts.json').read())
        self.goto_stmts = json.loads(open('src/testing/expected_output/goto_stmts.json').read())
        self.num_ml_comments = json.loads(open('src/testing/expected_output/num_ml_comments.json').read())
        self.num_notes = json.loads(open('src/testing/expected_output/num_notes.json').read())
        self.num_sl_comments = json.loads(open('src/testing/expected_output/num_sl_comments.json').read())
        print('JSON Values:')
        print('exec_stmts:')
        print(str(self.exec_stmts))
        print('goto_stmts:')
        print(str(self.goto_stmts))
        print('num_ml_comments:')
        print(str(self.num_ml_comments))
        print('num_notes:')
        print(str(self.num_notes))
        print('num_sl_comments:')
        print(str(self.num_sl_comments))

    def test_linenums(self):
        print('running test_linenums')
        # check that line number is correct here

    def test_goto_stmts(self):
        print('running test_goto_stmts')
        for filename in self.cms2files:
            expected = self.find_file(self.goto_stmts, filename)
            self.assertEqual(expected['goto_stmts'], filename.goto_stmts)


    def find_file(self, expected_data, test_data):
        # find the corresponding data in the json expected_data
        # for the given CMS2File test_data
        to_find = ''
        if test_data.name.startswith(self.files_root_dir):
            to_find = test_data.name[len(self.files_root_dir) + 1:]
        #to_find = os.path.split(test_data.name)[1]
        print('finding file for {0}'.format(to_find))
        for item in expected_data:
            if item['name'] == to_find:
                return item
        self.assertTrue(False, 'could not find {0} in {1}'.format(to_find, str(expected_data)))

            

