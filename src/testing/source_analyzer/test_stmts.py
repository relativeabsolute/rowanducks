# this file contains unit tests for statement related test cases
# see Verification Script steps 1.1-1.4.2 and 2.1
# Author: Johan Burke

import unittest
from ..regex import main

class StatementsTestCase(unittest.TestCase):
    # run source analyzer on directory of input
    def setUp(self):
        self.cms2files = main('../data/SampleDirectory')

    def test_linenums(self):
        pass
