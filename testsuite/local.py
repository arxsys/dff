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

import unittest, sys, os, random
from dffunittest import DffUnittest

class LocalTests(DffUnittest):
    """ Tests on 'local' VFS driver
    We load several things, and validate basic functionality of the framework.
    Keep in mind that VFS loads are persistant from one test to another.

    TODO
    - seek
    - negative seek
    - open & close many files
    - load same file two times, open both, seek one, check both position are OK

    """
    
    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)

# FIXME what about windows ?
    testFile = '/etc/passwd'

    def test01_LoadOneFile(self):
        """ #01 Load a file present on every Unix
        """

        # launch command
        self.ui.cmd('local --path ' + self.testFile + ' --parent /')
        
        # validate output from framework
        self.assertFalse(sys.stdout.getvalue())
        self.assertFalse(sys.stderr.getvalue())


    def test02_LsOneFile(self):
        """ #02 ls previously loaded file and validate size
        Check if --long (switch for size output) is right size of the file
        """
        
        self.ui.cmd('ls --long /')
        
        fileSize = str(os.stat(self.testFile).st_size)
        expectedStdout = '/' + os.path.basename(self.testFile) + '\t' + fileSize + '\n'

        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertFalse(sys.stderr.getvalue())
        

    def _itemsCount(self, path, onlyFiles = False):
        """ Return number of file in a given directory
        In case 'onlyFiles' is set, return only files count.
        """
        itemsCount = 0
        for root, dirs, files in os.walk(path):
            if onlyFiles:
                itemsCount += len(files)
            else:
                itemsCount += len(dirs) + len(files)
        return itemsCount

    def test03_LoadOneDirectory(self):
        """ #03 Load current working directory and validate number of files loaded
        Make sure number of nodes loaded is the same number as number of file
        stored in current working directory.
        """

        testDirectory = os.getcwd()

        self.ui.cmd('local --path ' + testDirectory + ' --parent /')

        # Expected output after local execution
# TODO Amount of loaded items is now in 'info -> local'
#        expectedItems = str(self._itemsCount(os.getcwd()))
#        expectedStdout = 'nodes created:\n' + expectedItems + '\nresult:\nno problem\n'
#        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        # In case of assertion failure above, hidden files exist in directory
        # loaded by this test

        # validate output from framework
        self.assertFalse(sys.stdout.getvalue())
        self.assertFalse(sys.stderr.getvalue())
        
    def test04_ReadFile(self):
        """ #04 Read 128 byte in previously loaded file
        Make sure content is equal on disk and in vfs
        """
        readAmount = 128
        
        with open(self.testFile, 'r') as f:
            expectedContent = f.read(128)

        checknode = self.vfs.getnode('/passwd')

        nodeFile = checknode.open()
        buff = nodeFile.read(128)
        self.assertEqual(expectedContent, buff)

    def _randomItem(self, path):
        """ Return a random filepath in a given directory
        """
        itemsCount = self._itemsCount(path, True)
        randomItemPosition = 0
        while randomItemPosition == 0 or randomItemPosition > itemsCount:
            randomItemPosition = int(random.random() * itemsCount)
        i = 0
        for root, dirs, files in os.walk(path):
            j = 0
            for j in range(len(files)):
                i += 1
                if i == randomItemPosition:
                    return root + '/' + files[j]


    def test05_RandomReadFile(self):
        """ #05 Randomly check 100 file content
        Read 'randomReadSize' from beginning of file and make sure
        same content is obtained from disk and from VFS.
        This test reads directly through the VFS object.
        """

        checkAmount = 100
        while checkAmount:
            # Obtain a random filepath from given directory
            randomFilepath = self._randomItem(os.getcwd())
            # Compute a random size to read
            randomReadSize = int(random.random() * os.stat(randomFilepath).st_size)
            # Open reference file
            with open(randomFilepath, 'r') as f:
                # Save reference data
                expectedContent = f.read(randomReadSize)
                # Set node path according to VFS format
                vfsNodePath = '/' + randomFilepath[len(os.getcwd()) - len(os.path.basename(os.getcwd())):]
                # Open node file
                nodeFile = self.vfs.getnode(vfsNodePath).open()
                # Save rode date from VFS
                buff = nodeFile.read(randomReadSize)
                # Close node file
                nodeFile.close()
                # Compare both data
                self.assertEqual(expectedContent, buff)
                # Reference file is automatically close ; 'with' statement
            checkAmount -= 1

    def test07_LargeSeek(self):
        """ #07 Large boundary seek
        Seek to limit of addressable offset, read and validate.
        First we create a huge file.

        Max :
        int32           2147483647              1.99 GB
        uint32          4294967295              3.99 GB
        ulonglong       18446744073709551615    16777215.99 TB
        
        """
        
        
    def runTest(self):
        pass


suite = unittest.TestSuite()
suite.addTest(LocalTests('test01_LoadOneFile'))
suite.addTest(LocalTests('test02_LsOneFile'))
suite.addTest(LocalTests('test03_LoadOneDirectory'))
suite.addTest(LocalTests('test04_ReadFile'))
suite.addTest(LocalTests('test05_RandomReadFile'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)

#print "call -> LocalTests()"
#testC = LocalTests()
#print "call -> setUp()"
#testC.setUp()
#print "call -> test01_LoadOneFile()"
#testC.test01_LoadOneFile()
#print "call -> tearDown()"
#testC.tearDown()
