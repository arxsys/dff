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

import unittest, sys, os, hashlib
from dffunittest import DffUnittest

class HashTests(DffUnittest):
    """ Tests on 'hash' module
    We load a file present on every computer, and validate hashing functionality.
    Algorithm checked :
     - md5
     - sha1
     - sha224
     - sha256
     - sha384
     - sha512

    TODO
    - test on a huge file

    """

# FIXME what about windows ?
    testFile = '/etc/passwd'
    
    def __init__(self, name='runTest'):
        unittest.TestCase.__init__(self, name)
        self.outBuff = ''

    def setUp(self):
        DffUnittest.setUp(self)
        # avoid output from driver loading in current stdout/stderr
        self._hook_streams(sys.__stdout__.fileno(), sys.__stderr__.fileno())
        
        # launch command
        self.ui.cmd('local --path ' + self.testFile + ' --parent /')
        
        # get output
        self._restore_streams()

    def _hashLocalFile(self, hash, file):
        if hash == "md5":
            m = hashlib.md5()
        elif hash == "sha1":
            m = hashlib.sha1()
        elif hash == "sha224":
            m = hashlib.sha224()
        elif hash == "sha256":
            m = hashlib.sha256()
        elif hash == "sha384":
            m = hashlib.sha384()
        elif hash == "sha512":
            m = hashlib.sha512()
        else:
            return
        
        with open(file, 'r') as f:
            buff = f.read(512)
            while len(buff) > 0:
                m.update(buff)
                buff = f.read(512)

        return m.hexdigest()

            
    def test01_HashMD5(self):
        """ #01 MD5 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm md5')
        
        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('md5', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')


    def test02_HashSHA1(self):
        """ #02 SHA1 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm sha1')
        
        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('sha1', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')


    def test03_HashSHA224(self):
        """ #03 SHA224 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm sha224')

        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('sha224', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')


    def test04_HashSHA256(self):
        """ #04 SHA256 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm sha256')

        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('sha256', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')


    def test05_HashSHA384(self):
        """ #05 SHA384 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm sha384')
        
        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('sha384', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')


    def test06_HashSHA512(self):
        """ #06 SHA512 hash of a file present on every Unix
        """
        self.outBuff += sys.stdout.getvalue()
        
        # launch command
        self.ui.cmd('hash --file /' + os.path.basename(self.testFile) + ' --algorithm sha512')

        expectedStdout = self.outBuff + 'result:\n' + self._hashLocalFile('sha512', self.testFile) + '  /' + os.path.basename(self.testFile) + '\n'
        # validate output from framework
        self.assertEqual(sys.stdout.getvalue(), expectedStdout)
        self.assertEqual(sys.stderr.getvalue(), '')

     
suite = unittest.TestSuite()
suite.addTest(HashTests('test01_HashMD5'))
suite.addTest(HashTests('test02_HashSHA1'))
suite.addTest(HashTests('test03_HashSHA224'))
suite.addTest(HashTests('test04_HashSHA256'))
suite.addTest(HashTests('test05_HashSHA384'))
suite.addTest(HashTests('test06_HashSHA512'))
res = unittest.TextTestRunner(verbosity=2).run(suite)

if (len(res.errors) or len(res.failures)):
    sys.exit(1)
