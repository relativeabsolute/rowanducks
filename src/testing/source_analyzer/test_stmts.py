# this file contains unit tests for statement related test cases
# see Verification Script steps 1.1-1.4.2 and 2.1
# Author: Johan Burke

import unittest
import os
from src.regex import main

class StatementsTestCase(unittest.TestCase):
    # run source analyzer on directory of input
    def setUp(self):
        print('setting up StatementsTestCase')
        print(os.getcwd())
        self.cms2files = main(['src/data/SampleDirectory'])

    def test_linenums(self):
        print('running test_linenums')
        # check that line number is correct here
        pass
