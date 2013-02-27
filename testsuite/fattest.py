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

class FatTests(DffUnittest):
    """ Tests on fat filesystem VFS driver
    
    """

    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

# It has to be preprocessed by CMake to find path of test image
    testFile = '${CMAKE_SOURCE_DIR}/testsuite/dftt/5-fat-daylight.zip'
    vfsTestFilePath = '/5-fat-daylight.zip/5-fat-daylight/daylight.dd'
    expectedLoadOutput = '${CMAKE_SOURCE_DIR}/testsuite/results/fattest.5-fat-daylight.load.txt'
    expectedListOutput = '${CMAKE_SOURCE_DIR}/testsuite/results/fattest.5-fat-daylight.ls.txt'
    expectedListAccurateOutput = '${CMAKE_SOURCE_DIR}/testsuite/results/fattest.5-fat-daylight.ls_accurate.txt'

    
    def test01_LoadDumpFailure(self):
        """ #01 Load an non-existent FAT dump and validate error
        """
        self.ui.cmd('local --path ' + self.testFile + ' --parent /')
        self.ui.cmd('unzip ' + os.path.basename(self.testFile))

        if not self.debugTest:
            precOutput = sys.stdout.getvalue()

        # launch command
        self.ui.cmd('fatfs ' + self.vfsTestFilePath[:-1])
       
        # This call must throw UserWarning because vfsTestFilePath minus
        #  last character is non-existant
#        resultArrayString = self._getResultsArrayByProcName('fat')
        self.assertRaises(UserWarning, lambda: self._getResultsArrayByProcName('fatfs'))

        # No result ; VFS module path not found
        expectedOutput = 'Value error: node < ' + self.vfsTestFilePath[:-1] + ' > doesn\'t exist\n'
        if not self.debugTest:
            self.assertEqual(sys.stdout.getvalue()[len(precOutput):], expectedOutput)
            self.assertFalse(sys.stderr.getvalue())

    def test02_LoadDump(self):
        """ #02 Load a FAT dump and validate filesystem metadata
        """
        if not self.debugTest:
            precOutput = sys.stdout.getvalue()
        # avoid output from driver loading in current stdout/stderr
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        
        # launch command
        self.ui.cmd('fatfs ' + self.vfsTestFilePath)

        # get command line output
        driverStdout, driverStderr = self._restore_streams()
        # get framework result from taskmanager
        resultArrayString = self._getResultsArrayByProcName('Fat File System')
        # read expected output from text file
        expectedArrayString = self._readExpectedOutputAsArray(self.expectedLoadOutput)
        
        i = 0
        for oneLine in resultArrayString:
            # compare lines one by one for accurate output in case of failure
            self.assertEqual(expectedArrayString[i], oneLine)
            i += 1

        # validate console output
        # strangely modules loading appears here, so [-len(expectedOut):] on output
        if not self.debugTest:
            self.assertFalse(driverStdout)
            self.assertFalse(driverStderr)
            self.assertFalse(sys.stderr.getvalue())


    def test03_RecurseListing(self):
        """ #03 Recurse list content of the FAT dump
        """
        if not self.debugTest:
            precOutput = sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('ls --recursive')
        
        consoleArrayString = self._getOutputArray(sys.stdout.getvalue()[len(precOutput):])
        expectedArrayString = self._readExpectedOutputAsArray(self.expectedListOutput)
        i = 0
        for oneLine in consoleArrayString:
            # compare lines one by one for accurate output in case of failure
            self.assertEqual(expectedArrayString[i], oneLine)
            i += 1
        self.assertFalse(sys.stderr.getvalue())


    def test04_RecurseAccurateListing(self):
        """ #04 Recurse list content of the FAT dump with fullpath and size of entry
        """
        precOutput = sys.stdout.getvalue()
        # avoid output from driver loading in current stdout/stderr
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        
        # launch command
        self.ui.cmd('ls --recursive --long')
        
        self._restore_streams()
        consoleArrayString = self._getOutputArray(sys.stdout.getvalue()[len(precOutput):])
        expectedArrayString = self._readExpectedOutputAsArray(self.expectedListAccurateOutput)

        i = 0
        for oneLine in consoleArrayString:
            # compare lines one by one for accurate output in case of failure
            self.assertEqual(expectedArrayString[i], oneLine)
            i += 1
        self.assertFalse(sys.stderr.getvalue())


suite = unittest.TestSuite()
suite.addTest(FatTests('test01_LoadDumpFailure'))
suite.addTest(FatTests('test02_LoadDump'))
suite.addTest(FatTests('test03_RecurseListing'))
suite.addTest(FatTests('test04_RecurseAccurateListing'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)
