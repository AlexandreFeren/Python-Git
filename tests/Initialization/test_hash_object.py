# Created the Test_Objects folder to hold test case files. None of those files should be modified after the first commit.

import unittest
import git_clone.Initialization.hash_object as hash_object
import os,stat
import sys
import shutil
import io
import contextlib

# TODO: Make test that use file locations and the corresponding hashes 
# files_and_hashes = {"README.md":"a522da6e8c23b4da792335364211fa2ff9efe78a"}
# folders_and_hashes = {"Source":"6f7831be3fc92736e185c20fadae9d61504dff4e"}

class TestHashObject(unittest.TestCase):
    '''
    check against predetermined hashes for the Test_Objects folder
    '''
    