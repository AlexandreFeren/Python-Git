import unittest
import main
import os
import inspect

class CustomTestResult(unittest.TextTestResult):
    def addSuccess(self, test):
        super().addSuccess(test)
        print("Test passed:", test)
    def addFailure(self, test, err):
        super().addFailure(test, err)
        print("Test failed:", test)

class TestFunctionCalls(unittest.TestCase):    
    test_args = ["","none",'diff 1','diff','init',"*","$"]
    file_loc = os.path.dirname(os.path.realpath(__file__))+"\\Staging\\"

def run_tests():
    test_modules = [
        "test_main",
        "Initialization.test_init"
    ]

    suite = unittest.TestSuite()

    for t in test_modules:
        try:
            # If the module defines a suite() function, call it to get the suite.
            mod = __import__(t, globals(), locals(), ['suite'])
            suite_fn = getattr(mod, 'suite')
            suite.addTest(suite_fn())
        except (ImportError, AttributeError):
            # else, just load all the test cases from the module.
            suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner().run(suite)
    
if __name__ == "__main__":
    run_tests()