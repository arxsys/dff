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
#  Frederic Baguelin <fba@digital-forensic.org>
# 

from string import ascii_letters
import sys

alphabet_mapping = [0, 26, 1, 25, 2, 24, 3, 23, 4, 22, 5, 21, 6, 20, 7, 19, 8, 18, 9, 17, 10, 16, 11, 15, 12, 14, 13]

def hard_mapping():
    file = open("hard_mapping.txt", "wb")
    for loop in xrange(0, 5):
        for letter in alphabet_mapping:
            pass

def simple_mapping():
    file = open("simple_mapping.txt", "wb")
    for loop in xrange(0, 10):
        for letter in ascii_letters:
            file.write(letter * 2)
    file.close()


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == "simple":
            simple_mapping()
        elif sys.argv[1] == "hard":
            hard_mapping()
        else:
            print "usage:", sys.argv[0], "[simple|hard]"
    else:
        print "usage:", sys.argv[0], "[simple|hard]"
            
        
