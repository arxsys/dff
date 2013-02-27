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

class VfsTests(DffUnittest):
    """ Validate environement variable module
    
    """

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

#    def runTest(self):
#        """ For debugging usage ; when methods are called directly
#        """
#        pass

    testFile = "/etc/passwd"
    nonExistentFilePath = "/chifoumi/pouf/pif/paf"
    
    def test01_BadLocalOpen(self):
        """ #01 Output error when loading non existent filepath
        """
        
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        self.ui.cmd('local --path ' + self.nonExistentFilePath + ' --parent /')
        driverStdout, driverStderr = self._restore_streams()

        self.assertEqual(sys.stdout.getvalue(), 'Value error: local path < ' + self.nonExistentFilePath + " > doesn't exist\n")
        self.assertFalse(driverStdout)
        self.assertFalse(driverStderr)
        self.assertFalse(sys.stderr.getvalue())
                          
    def test02_BadReadDirectory(self):
        """ #02 Raise error when reading a directory for data
        """
        
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        self.ui.cmd('local --path ' + self.testFile + ' --parent /')
        driverStdout, driverStderr = self._restore_streams()

        node = self.vfs.getnode('/')
        self.assertRaises(vfsError, lambda: node.open())
        try:
            node.open()
        except vfsError, e:
            self.assertEqual("Node::open(void) throw\nCan't Open file", e.error)
            
        self.assertFalse(driverStderr)
        self.assertFalse(sys.stderr.getvalue())

    def test03_BadSeek0File(self):
        """ #03 Validate error raising : negative seek from 0
        """
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        self.assertRaises(OverflowError, lambda: f.seek(-1))
        try:
            f.seek(-1)
        except OverflowError, e:
            self.assertEqual("in method 'VFile_seek', argument 2 of type 'dff_ui64'", e.message)
               
    def test04_BadSeekNFile(self):
        """ #04 Validate error raising : negative seek from +N
        """
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        f.seek(os.stat(self.testFile).st_size / 2)
        self.assertRaises(OverflowError, lambda: f.seek(-1))
        try:
            f.seek(-1)
        except OverflowError, e:
            self.assertEqual("in method 'VFile_seek', argument 2 of type 'dff_ui64'", e.message)

    def test05_BadSeekMaxFile(self):
        """ #05 Validate empty read starting at filesize
        """
        node = self.vfs.getnode(os.path.basename(self.testFile))
        f = node.open()
        f.seek(os.stat(self.testFile).st_size)
        self.assertFalse('', f.read(512))

        
suite = unittest.TestSuite()
suite.addTest(VfsTests('test01_BadLocalOpen'))
suite.addTest(VfsTests('test02_BadReadDirectory'))
suite.addTest(VfsTests('test03_BadSeek0File'))
suite.addTest(VfsTests('test04_BadSeekNFile'))
suite.addTest(VfsTests('test05_BadSeekMaxFile'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)

#testC = EnvTests()
#testC.setUp()
#testC.test01_GoodEnv()
#testC.test02_BadEnv()
