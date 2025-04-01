import unittest, warnings
import git_clone.src.Initialization.init as init
import git_clone.src.text_colors as color
import os

class TestInit(unittest.TestCase):
    """
    https://stackoverflow.com/questions/2031163/when-to-use-the-different-log-levels
    Set of tests for initialization, need to care a lot about side-effects
    Tests:
    - plain, bare, remote
    - reinitialization of these
    - init, then init remote to move repo
    - init both bare and remote (should fail)
    - custom branch name
    - confirm .git folder is hidden
    - compare all results with native git implementation (parallel)
    """
    def _test_init(self,log_level=7):
        return
    
    def test_init_full(self):
        """
        Central location to call tests
        allows easy change of cwd to temp folder and root of repo
        """
        log_level = 7
        try:
            os.mkdir("../test_init")
        except FileExistsError:
            warnings.warn(color.b_colors.WARNING+"Test folder already exists"+color.b_colors.END_C)
        os.chdir("../test_init")
        init.init()
        
        
        os.chdir("../Git Clone")