import unittest
import git_clone.src.text_colors as color
import git_clone.src.Initialization.init as init
import warnings
import os
import inspect


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
    @classmethod
    def setUpClass(cls):
        """
            set up test directory, confirm you are not in a repo
            move cwd to test directory
        """
        test_dir = "../test_init"
        # check for .git folder/link file or bare repo
        if ".git" in os.listdir(os.getcwd()) or init.valid_git_dir(os.getcwd()):
            cls.assertTrue(False)
            cls.skipTest("starting in a git directory, skipping")

        try:
            os.mkdir(test_dir)
        except FileExistsError:
            warnings.warn(
                color.b_colors.WARNING
                + "Test folder already exists"
                + color.b_colors.END_C
            )
            cls.assertTrue(False)  # fail tests if testing folder not deleted
            cls.skipTest("Testing directory already existed, skipping")
        os.chdir(test_dir)

    @classmethod
    def tearDownClass(cls):
        """
            delete Test Folder and move back to start
        """
        os.chdir("../Git Clone")
        print("deleting"+os.path.abspath(os.getcwd()+"/../test_init"))

    def delete_dir(self):
        path = ""
        if os.path.isfile(".git"):  # delete remote repo
            path = os.path.abspath("./.git")
        elif os.path.isdir(".git"):  # local repo
            path = os.path.abspath("./.git")
        elif init.valid_git_dir("."):  # bare repo
            path = os.getcwd()
        else:
            warnings.warn(color.b_colors.FAIL +
                          "invalid path to delete"+color.b_colors.END_C)
            self.assertTrue(False)

        print("deleting {}".format(path))
        return

    def test_init(self, test_case):
        init.init(test_case)
        return test_case

    def test_re_init(self, test_case):
        warnings.warn(color.b_colors.WARNING + "{} not implemented".format(
            inspect.currentframe().f_code.co_name) + color.b_colors.END_C)
        return

    def test_init_remote(self, test_cases):
        """
            make a .git folder in a subdirectory of the base testing dir
            this is to allow the folder referenced in .git to be untracked
            Simple structure might look like this:

            ┏━test_init
            ┃ ┗━test_init_remote
            ┃   ┗━.git
            ┗━remote_folder

            where .git has the contents:
                gitdir: <absolute path to remote_folder>
        """
        return test_cases

    def test_re_init_remote(self):
        """
            1. .git file exists:
                a. target is valid repo
                    - reinitialize target (regardless of flags)
                b. target is not valid repo
                    - fail (fatal)
            2. .git file does not exist
                - ensure all required git files are in the target
                  leave existing files untouched
        """
        warnings.warn(color.b_colors.WARNING + "{} not implemented".format(
            inspect.currentframe().f_code.co_name) + color.b_colors.END_C)

    def test_init_bare(self, test_cases):
        """
            test initializing in-place
        """
        return test_cases

    def test_re_init_bare(self):
        warnings.warn(color.b_colors.WARNING + "{} not implemented".format(
            inspect.currentframe().f_code.co_name) + color.b_colors.END_C)
        return

    # no need for testing reinitialization
    # these have preset scenarios like invalid/unnatural commands/states
    def test_init_missing_link(self):
        """
            test that .git gets remade if the target exists and is a git repo
            test .git exists, but the target is not a valid repo
        """
        return

    def test_init_bare_remote(self):
        # test bare and remote in same command
        # should fail
        return
