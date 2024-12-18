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
    file_loc = os.path.dirname(os.path.realpath(__file__))+"\\Work_Tree\\"
    def test_call_command_scope(self):
        '''
        check that the path that call_command is working on
        is the same as the path that this program is called from
        '''
        print("\n\t" + inspect.currentframe().f_code.co_name,end = "")
        args = self.test_args[2]
        m = main.Main()
        ret = m.call_command(m.parse_args(args))
        if args.split()[0] in m.commands:
            self.assertEqual(ret[1],os.getcwd())
        else:
            self.assertEqual(ret,None)
    
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
        "Work_Tree.test_work_tree"
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