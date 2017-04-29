# top level script used to run unit testing
# Author: Johan Burke

from unittest import TestLoader, TestResult
from run_tests import run_tests

def run_tests():
    loader = TestLoader()
    suite = loader.discover('.')
    result = TestResult()
    result = suite.run(result)
    print("Errors:")

    """ Check for Erorrs """
    for err in result.errors:
        print("Where: " + str(err[0]))
        print("Error: " + err[1])
    print("Failures:")
    for fail in result.failures:
        print(str(fail))
    for fail in run_tests():
        print(str(fail))

if __name__ == "__main__":
    run_tests()