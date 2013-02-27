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
#  Frederic B. <fba@digital-forensic.org>


from api.vfs import *
#from api.module.script import*
from api.module.module import Module

#from api.env import *
from api.env.libenv import *
from api.variant.libvariant import Variant
#from api.type.libtype import *
#from api.module import *
from api.vfs.libvfs import *
#from api.exceptions.libexceptions import *

from string import ascii_letters

class MfsoContiguousNode(Node):
    def __init__(self, letter, mfso, origin):
        Node.__init__(self, letter, 1040, origin, mfso)
        self.thisown = False
        self.origin = origin
        self.size = 1040
        setattr(self, "attributes", self.attributes)
        setattr(self, "fileMapping", self.fileMapping)

    
    def fileMapping(self):
        fm = FileMapping()
        fm.thisown = False
        i = 0
        voffset = 0
        while i != self.size:
            fm.push(voffset, 2, self.origin, i)
            voffset += 2
            i += 2
        return fm

    def attributes(self):
        #print "Python node attributes requested"
        attr = Attributes()
        attr.thisown = False
        sizeattr = Variant(self.size)
        sizeattr.thisown = False
        attr.push("size", sizeattr)
        return attr


class MfsoContiguous(mfso):
    def __init__(self):
        mfso.__init__(self, "mfso_contiguous")
        self.name = "nothing"
    
    def map(self):
        i = 0
        MfsoContiguousNode("contiguous_chunck", self, self.parent)

    def start(self, args):
        self.parent = args.get_node("parent")
        #self.file = self.parent.open()
        self.map()
    

class mfso_contiguous(Module):
    def __init__(self):
        Module.__init__(self, 'mfso_contiguous', MfsoContiguous)
        self.conf.add("parent", "node")
        self.tags = "file system"
