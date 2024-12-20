import unittest
import Initialization.init as init
import os
import sys
import shutil

class TestInit(unittest.TestCase):
    '''
    create and modify .git folders.
    only run tests if there is no .git folder accessible
    otherwise, fail unconditionally
    '''
    
    def create_partial_folder(self):
        '''
        create a .git folder missing some folders
        '''
    
    def delete_folder(self):
        '''
        delete .git folder in between tests. Do not edit
        '''
        path = os.getcwd()+'\\.git'
        print('deleting ' + path)
        shutil.rmtree(path)
        while os.path.exists(path): # wait for rmtree to finish
            pass

    def test_init_full(self):
        '''
        needs to check side effects of init.py so must be only fn
        that is called to test init. Otherwise, effect order
        would be liable to change.
        folder structure should always be:
        .git
            > hooks
            > info
            > objects
            > refs
            HEAD
            config
            description
            index
        '''
        # make sure there is no .git folder to avoid real repo
        self.assertFalse('.git' in os.listdir(os.getcwd()))
        
        
        path = os.getcwd()+'\\.git'
        
        self.create_partial_folder()
        init.init()
        self.check_dir(path)        
        
        self.delete_folder()
        
        return
    
    def check_dir(self,path):
        expected_dirs = ['hooks','info','objects','refs']
        expected_files = ['HEAD','config','description','index']
        
        for _,dirs,files in os.walk(path):
            # check all expected directories/files exist
            self.assertTrue(all([i in dirs for i in expected_dirs]))
            self.assertTrue(all([i in files for i in expected_files]))
            break

    
    def check_init_format(self):
        '''
        check for files being properly formatted where relevant
        '''