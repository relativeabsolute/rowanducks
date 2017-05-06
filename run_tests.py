# top level script used to run unit testing
# Author: Johan Burke

from unittest import TestLoader, TestResult

def run_tests():
    loader = TestLoader()
    suite = loader.discover('src/testing/')
    result = TestResult()
    result = suite.run(result)
    print("Errors:")

    """ Check for Erorrs """
    for err in result.errors:
        print("\tWhere: " + str(err[0]))
        print("\tError: " + err[1])
    print("Failures:")
    for fail in result.failures:
        print("\tTest case: {0}".format(str(fail[0])))
        print("\tFailure string: {0}".format(fail[1]))

if __name__ == "__main__":
    run_tests()
