import unittest
import git_clone.src.text_colors as color
import git_clone.src.Initialization.init as init
import os
import io
import sys
import inspect
import shutil
import subprocess
import contextlib


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
    # helper functions

    def moveToTestInit(self):
        # this is currently only for use with separate-git-dir=...
        while (os.getcwd() != os.path.abspath(os.getcwd()+"\\..") and
                ("remote_git_files" not in os.listdir() or
                 "remote_repo" not in os.listdir())
               ):
            os.chdir("..")
        if (os.getcwd() == os.path.abspath(os.getcwd()+"\\..") or
                os.getcwd().split("\\")[-1] != "test_init"):
            print(color.b_colors.FAIL +
                  "unsafe to delete {}\n".format(os.getcwd().split("\\")[-1]) +
                  "Expected dir with remote_git_files and remote_repo in hierarchy" +
                  color.b_colors.END_C)
            sys.exit(1)

    def _testValidGitDir(self, expect_valid=True):
        """
            check if `git status` exits with code 0
        """
        self.assertTrue(init.valid_git_dir(os.getcwd()+"\\.git"))
        if expect_valid:
            self.assertEqual(0,
                             subprocess.run(['git', 'status'],
                                            stdout=subprocess.DEVNULL,
                                            stderr=subprocess.DEVNULL).returncode)
        else:
            self.assertNotEqual(0,
                                subprocess.run(['git', 'status'],
                                               stdout=subprocess.DEVNULL,
                                               stderr=subprocess.DEVNULL).returncode)

    def standardTearDown(self):
        if os.getcwd().split("\\")[-1] != "test_init":
            print(color.b_colors.FAIL +
                  "unsafe to delete {}".format(os.getcwd())+color.b_colors.END_C)
            sys.exit(1)
        path = os.path.abspath("./.git")
        shutil.rmtree(path)

    def remoteTearDown(self):
        '''
            This isn't just test_init/.git because of how I want to test it
            The tracked files should not be in the directory with the .git file
            Also added some safety checks after almost deleting my desktop files

            ends in */test_init which contains ["remote_repo","remote_git_files"]
        '''
        self.moveToTestInit()

        lnk_path = os.path.abspath("./remote_repo/.git")
        with io.open(lnk_path) as file:
            dir_path = file.read().split()[1]
        os.remove(lnk_path)
        shutil.rmtree(dir_path)
        os.mkdir(dir_path)

        # TODO: verify that this is needed
        self.moveToTestInit()

    def bareTearDown(self):
        if os.getcwd().split("\\")[-1] != "test_init":
            print("unsafe to delete {}".format(os.getcwd()))
        for filename in os.listdir("."):
            file_path = os.path.join(".", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def compare_output(self, command, teardown=True, move_to="."):
        """
        Args:
            command (string list): flags to pass into git
            teardown (bool, optional): Default True
                True: delete contents of git repo and link
                False: ignore deletion
            move_to (str, optional): Default "."
                Dir to move to if not test_init.
                should never be outside of test_init

        expects start in */test_init
        Ends either in */test_init/<move_to>
        """
        # pass in command, check if git and git-clone have same output
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            os.chdir(move_to)
            init.init(command)
        git_clone_output = output.getvalue()
        output.close()

        self._testValidGitDir()
        if teardown:
            self.tearDown()
        else:
            self.moveToTestInit()
        os.chdir(move_to)
        git_output = subprocess.run(
            ["git"]+command, capture_output=True).stdout.decode("utf-8")

        self.assertEqual(git_output, git_clone_output)
        # This is not a complete check, but works for current tests
        if move_to != ".":
            self.moveToTestInit()

    # class housekeeping functions
    @classmethod
    def setUpClass(self):
        """
        set up test directory, confirm you are not in a repo
        move cwd to test directory
        sys.exit(1) is to cause CI to fail if reached
        """
        test_dir = init.get_git_dir()
        if not test_dir:
            test_dir = os.getcwd()
        test_dir += "\\..\\test_init"
        try:
            os.mkdir(test_dir)
        except FileExistsError:
            # this will always fail when using pre-commit because of input call
            if (
                input(
                    color.b_colors.FAIL
                    + "skip TestInit: Test folder already exists. Continue (Y/N)?"
                    + color.b_colors.END_C
                ).lower()[0]
                != "y"
            ):
                print(color.b_colors.FAIL +
                      "aborting tests" + color.b_colors.END_C)
                sys.exit(1)
        os.chdir(test_dir)

    @classmethod
    def tearDownClass(self):
        """
            delete Test Folder and move back to start
        """
        os.chdir("../Git Clone")
        to_delete = os.path.abspath(os.getcwd()+"/../test_init")
        shutil.rmtree(to_delete)

    def setUp(self):
        print(color.b_colors.HEADER+"\ncalling {}{}".format(self._testMethodName,
              color.b_colors.END_C), end="")
        if os.getcwd().split("\\")[-1] != "test_init":
            print(color.b_colors.FAIL +
                  "setUp ended in {}".format(os.getcwd())+color.b_colors.END_C)
            sys.exit(1)

    def tearDown(self):
        """
            start somewhere in */test_init
            end in */test_init
        """
        if os.path.isdir(".git"):       # local repo
            # print("standard")
            self.standardTearDown()
        elif os.path.isfile(".git"):    # delete remote repo
            # print("remote")
            self.remoteTearDown()
        elif init.valid_git_dir("."):   # bare repo
            # print("bare")
            self.bareTearDown()
        else:
            print(color.b_colors.WARNING +
                  "Expected git repo, nothing to delete"+color.b_colors.END_C)

        # safety check, all tests should start and end in same location
        if os.getcwd().split("\\")[-1] != "test_init":
            print(color.b_colors.FAIL +
                  "tearDown ended in {}".format(os.getcwd())+color.b_colors.END_C)
            sys.exit(1)

    # @unittest.skip('\n')
    def test_init(self):
        self.compare_output(["init"])
        self.tearDown()

        self.compare_output(["init", "-q"])
        self.tearDown()

        self.compare_output(["init", "--quiet"])

    # @unittest.skip('\n')
    def test_re_init(self):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            init.init(["init"])  # prime to reinit
        output.close()

        self.compare_output(["init"], False)
        self._testValidGitDir()

        self.compare_output(["init", "-q"], False)
        self._testValidGitDir()

        self.compare_output(["init", "--quiet"], False)
        self._testValidGitDir()

    # @unittest.skip('\n')
    def test_init_remote(self):
        """
        make a .git folder in a subdirectory of the base testing dir
        this is to allow the folder referenced in .git to be untracked
        Simple structure might look like this:
            test_init
            ┣━remote_repo/
            ┃ ┗━.git
            ┃
            ┗━━remote_git_files/
               ┣━hooks/
               ┃  ┗━...
               ┣━info/
               ┃  ┗━...
               ┣━objects/
               ┃  ┗━...
               ┣━refs/
               ┃  ┗━...
               ┣━HEAD
               ┣━config
               ┣━description
               ┗━...

        can test with different folder structures, but always want
        this to be the base of the structure
            test_init
                ┣━remote_repo/
                ┗━━remote_git_files/
        """
        try:
            os.mkdir("remote_repo")
        except FileExistsError:
            pass
        try:
            os.mkdir("remote_git_files")
        except FileExistsError:
            pass

        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/"], move_to="remote_repo")
        os.chdir("remote_repo")
        self.tearDown()

        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/", "-q"], move_to="remote_repo")
        os.chdir("remote_repo")
        self.tearDown()

        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/", "--quiet"], move_to="remote_repo")
        os.chdir("remote_repo")

    # @unittest.skip('\n')
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
        try:
            os.mkdir("remote_repo")
        except FileExistsError:
            pass
        try:
            os.mkdir("remote_git_files")
        except FileExistsError:
            pass
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            os.chdir("remote_repo")
            init.init(["init", "--separate-git-dir=../remote_git_files/"])
            os.chdir("..")
        output.close()

        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/"], False, "remote_repo")
        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/", "-q"], False, "remote_repo")
        self.compare_output(
            ["init", "--separate-git-dir=../remote_git_files/", "--quiet"], False, "remote_repo")
        os.chdir("remote_repo")

    @unittest.skip('\n')
    def test_init_bare(selfs):
        """
            test initializing bare
            should basically work the same as remote
        """

    @unittest.skip('\n')
    def test_re_init_bare(self):
        print(
            color.b_colors.WARNING
            + "{} not implemented".format(inspect.currentframe().f_code.co_name)
            + color.b_colors.END_C
        )
        return None

    @unittest.skip('\n')
    def test_init_missing_link(self):
        """
        test that .git gets remade if the target exists and is a git repo
        test .git exists, but the target is not a valid repo
        """
        # no need for testing reinitialization
        # these have preset scenarios like invalid/unnatural commands/states
        return None

    @unittest.skip('\n')
    def test_init_bare_remote(self):
        # bare and remote cannot be used in same command
        with self.assertRaises(ValueError):
            init.init(["init", "--bare", "--separate-git-dir=../"])
