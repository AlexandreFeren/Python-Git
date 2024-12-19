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

    def test_parse_args(self):
        """
        test that arguments are parsed correctly
        - split, and add .py to [0]
        """
        print("\n\t" + inspect.currentframe().f_code.co_name,end = "")
        m = main.Main()
        for case in self.test_args:
            test_args = case.split()
            if test_args: 
                test_args[0] = test_args[0] + ".py"
            self.assertEqual(m.parse_args(case),test_args)

def run_tests():
    test_modules = [
        "test_main",
        "Remote.test_remote",
        "Branch.test_branching",
        "Staging.test_staging",
        "Upkeep.test_upkeep"
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