# Created the Test_Objects folder to hold test case files. None of those files should be modified after the first commit.

import unittest
import Initialization.hash_object as hash_object
import os,stat
import sys
import shutil
import io
import contextlib

class TestHashObject(unittest.TestCase):
    '''
    check against predetermined hashes for the Test_Objects folder
    '''
    