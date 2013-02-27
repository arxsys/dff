#!/usr/bin/python 
# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2013 ArxSys
# This program is free software, distributed under the terms of
# the GNU General Public License Version 2. See the LICENSE file
# at the top of the source tree.
#  
# See http://www.digital-forensic.org for more information about this
# project. Please do not directly contact any of the maintainers of
# DFF for assistance; the project provides a web site, mailing lists
# and IRC channels for your use.
# 
# Author(s):
#  Christophe M. <cma@digital-forensic.org>
#

import unittest, sys, os
from dffunittest import DffUnittest
from api.exceptions.libexceptions import *

class EnvTests(DffUnittest):
    """ Validate environement variable module
    
    """

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

    def runTest(self):
        """ For debugging usage ; when methods are called directly
        """
        pass

    testFile = "/etc/passwd"

    def test01_ValueError(self):
        """ #01 ValueError raise when loading a non-existent path
        """
        badPath = '/non/existent'
        
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        self.ui.cmd('local --path ' + badPath)
        driverStdout, driverStderr = self._restore_streams()

        expectedStdout = 'Value error: local path < ' + badPath + ' > doesn\'t exist\n'
        self.assertFalse(driverStdout)
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertFalse(driverStderr)
        self.assertFalse(sys.stderr.getvalue())

    def test02_GoodEnv(self):
        """ #02 Get three existing value from environement module
        """
        
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        self.ui.cmd('local --path ' + self.testFile + ' --parent /')
        driverStdout, driverStderr = self._restore_streams()
        
        # Obtain environement object by processus name
        env = self._getEnvObjByProcName('local')

        # Validate type of the object returned by get_path
        self.assertEqual("<class 'api.type.libtype.Path'>", str(type(env.get_path('path'))))
        # Validate --path argument
        self.assertEqual(self.testFile, env.get_path('path').path)
        # Validate type of the object returned by get_node
        self.assertEqual("<class 'api.vfs.libvfs.Node'>", str(type(env.get_node('parent'))))
        # Validate '/' is root of VFS
        self.assertTrue(env.get_node('parent').is_root)
        self.assertFalse(env.get_node('parent').is_file)

        self.assertFalse(driverStderr)
        self.assertFalse(sys.stderr.getvalue())


    def test03_BadEnv(self):
        """ #03 Error getting a non-existent value from environement module
        """

        # Obtain environement object by processus name
        #  remember, load are persistant
        env = self._getEnvObjByProcName('local')

        for type, name, val in self.tm.env.get_val_map(env.val_m):
            print type, name, val
        env.thisown = 0

        self.assertFalse(env.val_m.has_key('bad'))
        self.assertRaises(IndexError, lambda: env.val_m['bad'])
        self.assertRaises(IndexError, lambda: self.tm.env.vars_db['bad'])
# FIXME unable to test env.get_bool('bad') because it segfault


        
suite = unittest.TestSuite()
suite.addTest(EnvTests('test01_ValueError'))
suite.addTest(EnvTests('test02_GoodEnv'))
suite.addTest(EnvTests('test03_BadEnv'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)

#testC = EnvTests()
#testC.setUp()
#testC.test01_GoodEnv()
#testC.test02_BadEnv()
