import unittest
import os


class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertTrue(True)


def run_tests():
    test_modules = []
    path = "."
    # Always run tests from the root of the repo
    # This mainly matters to have a consistent location for testing init
    # which would be something like ../test_init/
    while os.getcwd() != os.getcwd() + "\\..":
        if ".git" in next(os.walk(path))[1]:
            path = os.path.abspath(path)
            break
        path += "\\.."
    os.chdir(path)
    print(os.getcwd())
    test_modules = ["test_main", "Initialization.test_init"]

    suite = unittest.TestSuite()

    for t in test_modules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ["suite"])
            suite_fn = getattr(mod, "suite")
            suite.addTest(suite_fn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner().run(suite)


if __name__ == "__main__":
    run_tests()
