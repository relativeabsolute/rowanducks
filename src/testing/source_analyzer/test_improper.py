# script used to test improper cases (see verification Script Steps: 1.5.1-1.5.4)
# Author: Chris Curreri
# Note: Class connot be completed since functionality is not implemented.

import unittest
from src.regex import main

class ImproperTestCase(unittest.TestCase):

    # 1.5.1 Run test_bad_ext...ok
    # Will print ok if and only if the number of files
    # with incorrect extensions match the ones found
    # in num_bad_ext.txt.
    def test_bad_ext(self):
        # check if bad extensions are the same
        pass

    # 1.5.2 test_misplace_end_sys...ok
    # Will print ok if and only if the number of instances
    # of misplaced "END-SYSTEM" statements match the number
    # found in num_misplaced_end_sys.txt.
    def test_misplace_end_sys(self):
        # check if end system states are correct
        pass

    # 1.5.3 test_multi_component...ok
    # Will print ok if and only if the number matches
    # the number found in num_multi_component.txt.
    def test_multi_component(self):
        # check if multiple compontents are correct
        pass

    # 1.5.4 test_name_mismatch...ok
    # Will print ok if and only if the number of
    # mismatches between component name and filename
    # match the number in num_name_mismatch.txt.
    def test_name_mismatch(self):
        # check if the name and filename match the number here
        pass

if __name__ == "__main__":
    print('Running TestImproper:')
    unittest.main()