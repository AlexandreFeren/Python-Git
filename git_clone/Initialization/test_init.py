import unittest
import Initialization.init as init
import os,stat
import sys
import shutil
import io
import contextlib

class TestInit(unittest.TestCase):
    '''
    needs to check side effects of init.py so must be only fn
    that is called to test init. Otherwise, effect order
    would be liable to change.
    folder structure should always be:
    .git (not used if bare)
        > hooks
        > info
        > objects
        > refs
        HEAD
        config
        description
        index
        
    test cases:
        - init plain
        - init bare
        - init remote
        - reinit bare
        - reinit remote
        - reinit plain
        - init, then init remote to move
        - init both bare and remote
        TODO: - custom branch name
        
        for all:
        - check that all required files are in directory
        TODO: - check that .git folder gets hidden
        TODO: - compare with results from native git implementation
    '''
    
    # utility functions
    def check_stdout(self,stdout,expected):
        """
        check for valid print to stdout
        """
        # expected text for various cases
        checks = {  'init':'Initialized empty Git repository in ',
                    'reinit':'Reinitialized existing Git repository in ',
                    'conflict':'',
                    '':None}
        
        # \\ can cause issues with native git implementation
        self.assertTrue("\\" not in stdout)
        # print('checking stdout')
        print((stdout,expected))
        for i in range(len(expected)):
            self.assertTrue(checks[expected[i]] in stdout.split('\n')[i])
        
    def is_hidden(self, path):
        '''
        check if file/folder is hidden
        '''
        self.assertTrue(bool(os.stat(path).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN))

    def empty_dir(self):
        '''
        confirm that target folder(s) is/are empty
        '''
        self.assertTrue(os.listdir(os.getcwd()) == [])
        
    def is_valid_repo(self,args):
        """
        TODO: full validation check including contents of HEAD and config
        Args:
            path (str): path to initialize repo at
        """
        expected_dirs = ['hooks','info','objects','refs']
        expected_files = ['HEAD','config','description']
        path = ["","","/.git"]
        main = 'master'
        
        for i in range(len(args)):
            args[i] = args[i].split()
            
            if args[i][0] == "--separate-git-dir": path[1] = args[i][1]
            else: path[1] = os.getcwd()
            
            if args[i][0] == "--bare": path[2] = ''
            
            if args[i][0] == '-b' or args[i][0] == '--initial-branch': main = args[i][1]
        
        path = "".join(path[1:])
        # print("is_valid_repo",path,main)
        
        for _,dirs,files in os.walk(path):
            # check all expected directories/files exist
            #print("checking for validity:",path)
            self.assertTrue(all([i in dirs for i in expected_dirs]))
            self.assertTrue(all([i in files for i in expected_files]))
            break
    
    def check_init_format(self):
        '''
        TODO: this should be done after init stuff gets formatted
        check for files being properly formatted where relevant
        '''
    
    def check_against_git(self):
        '''
        TODO
        run git status on command line to check result
        '''
        
    
    def cleanup(self):
        '''
        delete contents of testing folder after checking validity
        '''
        print("deleting contents of",os.getcwd())
        for i in os.listdir(os.getcwd()):
            if os.path.isdir(i): shutil.rmtree(i)
            else: os.remove(i)
        while os.listdir(os.getcwd()) != []: continue

    def test_init_bare(self):
        test_cases = [["init","-q", "--bare"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                self.assertTrue(f.getvalue() == "")
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_reinit_bare(self):
        test_cases = [["init", "--bare"]]
        b = ''
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                    init.init(case) # re-init
                self.check_stdout(f.getvalue(),['init','reinit'])
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_init_remote(self):
        test_cases = [["init","--separate-git-dir=./.separate-git"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                self.check_stdout(f.getvalue(),['init'])
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_reinit_remote(self):
        test_cases = [["init","--separate-git-dir=./.separate-git"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                    init.init(case)
                self.check_stdout(f.getvalue(),['init','reinit'])
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_reinit_as_remote(self):
        """
        not confident about this one
        """
        with io.StringIO() as f:
            self.empty_dir()
            with contextlib.redirect_stdout(f):
                init.init(["init"])
                init.init(["init","--separate-git-dir=./.separate-git"])
            self.check_stdout(f.getvalue(),['init','reinit'])
            self.is_valid_repo(["init","--separate-git-dir=./.separate-git"])
            self.cleanup()
        
        
    def test_init_quiet(self):
        test_cases = [["init","-q"],["init","--quiet"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                self.assertTrue(f.getvalue() == "")
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_init(self):
        test_cases = [["init"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                self.check_stdout(f.getvalue(),['init'])
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_reinit(self):
        test_cases = [["init"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stdout(f):
                    init.init(case)
                    init.init(case)
                self.check_stdout(f.getvalue(),['init','reinit'])
                self.is_valid_repo(case)
                self.cleanup()
    
    def test_bare_and_remote(self):
        '''
        expect fail/error message
        '''
        test_cases = [["init", "--bare","--separate-git-dir=./.separate-git"]]
        with io.StringIO() as f:
            for case in test_cases:
                self.empty_dir()
                with contextlib.redirect_stderr(f):
                    try:
                        init.init(case)
                    except ValueError:
                        self.assertTrue(True)
                        continue
                    #this should not be reached: ValueError gets raised, skips this line
                    self.assertTrue(False)