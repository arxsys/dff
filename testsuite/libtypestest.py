#!/usr/bin/python -i
# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2013 ArxSys
#
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

import api
import traceback
import sys, os

if os.name == "posix": 
    try :
        import dl
        sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
    except ImportError:
        import ctypes
        sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)

from api.types.libtypes import *
from api.vfs.libvfs import VFS
from modules.connector.local import LOCAL
from modules.builtins.ls import LS


v = VFS.Get()

## STRING_OptionalSingleInputWithFixedParam = Argument("string", OptionalSingleInputWithFixedParam|typeId.String,
##                                                        "an optional string argument with fixed parameters and single input")

## STRING_OptionalSingleInputWithCustomizableParam = Argument("string", OptionalSingleInputWithCustomizableParam|typeId.String,
##                                                        "an optional string argument with customizable parameters and single input")

## STRING_RequiredSingleInputWithFixedParam = Argument("string", RequiredSingleInputWithFixedParam|typeId.String,
##                                                        "a required string argument with fixed parameters and single input")

## STRING_RequiredSingleInputWithCustomizableParam = Argument("string", RequiredSingleInputWithCustomizableParam|typeId.String,
##                                                        "a required string argument with customizable parameters and single input")

## STRING_OptionalListInputWithFixedParam = Argument("string", OptionalListInputWithFixedParam|typeId.String,
##                                                        "an optional string argument with fixed parameters and list input")

## STRING_OptionalListInputWithCustomizableParam = Argument("string", OptionalListInputWithCustomizableParam|typeId.String,
##                                                        "an optional string argument with customizable parameters and list input")

## STRING_RequiredListInputWithFixedParam = Argument("string", RequiredListInputWithFixedParam|typeId.String,
##                                                        "a required string argument with fixed parameters and list input")

## STRING_RequiredListInputWithCustomizableParam = Argument("string", RequiredListInputWithCustomizableParam|typeId.String,
##                                                        "an optional string argument with customizable parameters and list input")


## STRING_OptionalSingleInputWithFixedParam.setEnabled(True)
## print "flags:", hex(STRING_OptionalSingleInputWithFixedParam.flags())
## print "type:", hex(STRING_OptionalSingleInputWithFixedParam.type())
## print "inputype:", hex(STRING_OptionalSingleInputWithFixedParam.inputType())
## print "paramstype:", hex(STRING_OptionalSingleInputWithFixedParam.parametersType())
## print "neededtype:", hex(STRING_OptionalSingleInputWithFixedParam.requirementType())
## print "=== TESTING SETTING METHOD ==="
## print "    Optional --> Required"
## print "    SingleInput --> ListInput"
## print "    FixedParams --> CustomizableParams"
## print "    String --> UInt64"
## STRING_OptionalSingleInputWithFixedParam.setType(typeId.UInt64)
## STRING_OptionalSingleInputWithFixedParam.setInputType(ListInput)
## STRING_OptionalSingleInputWithFixedParam.setParametersType(CustomizableParam)
## STRING_OptionalSingleInputWithFixedParam.setRequirementType(Required)
## print "flags:", hex(STRING_OptionalSingleInputWithFixedParam.flags())
## print "type:", hex(STRING_OptionalSingleInputWithFixedParam.type())
## print "inputype:", hex(STRING_OptionalSingleInputWithFixedParam.inputType())
## print "paramstype:", hex(STRING_OptionalSingleInputWithFixedParam.parametersType())
## print "neededtype:", hex(STRING_OptionalSingleInputWithFixedParam.requirementType())

## print type(STRING_OptionalSingleInputWithFixedParam)

No = 0
Enabled = True
Disabled = False

conf = [{"name": "arg1",
        "input": Argument.Optional|Argument.Single|typeId.Node,
         "description": "optional and unique argument of type Node with parameter either provided by user or based on default",
         "parameters": {"type": Parameter.Customizable,
                        "predefined": ["/", "/logical evidences"],
                        #"default": "/"#predefined parameters are provided when user configure input
                        },
         "runtime": {"status": Disabled,
                     "parameters": "/"
                     }
         },

        {"name": "arg2",
         "input": Argument.Optional|Argument.Single|typeId.Int32,
         "description": "optional argument of type Int32 with fixed parameter selected by user",
         
         # !!! When parameter is fixed, "predefined" field MUST be filled !!!
         "parameters": {"type": Parameter.Fixed,
                        "predefined": [512, 1024, 2048, 4096], #fixed predefined parameters, modules is not able to manage other type
                        },
         "runtime": {"status": Enabled,
                     "parameters": 512
                     }
         },
        
        {"name": "arg3",
         "input": Argument.Optional|Argument.List|typeId.String,
         "description": "optional list of argument of type String with fixed parameters selected by user",
         
         # !!! When parameters are fixed, they MUST be setted in "predefined" field !!!
         "parameters": {"type": Parameter.Fixed,
                        "predefined": ["md5", "sha1", "sha256", "sha512"] #fixed predefined parameters, modules is not able to manage other type
                        },
         
         "runtime": {"status": Enabled,
                     "parameters": ["md5", "sha512"]
                     }
         #md5 and sha512 parameters used by default (if not filled by user or if preconfigured for automation)
         },
        
        
        {"name": "arg4"
         "input": Argument.Optional|Argument.List|typeId.String,
         "description": "optional list of argument of type String with parameters either provided by user or based on default",
         
         "parameters": {"type": Parameter.Customizable,
                        "predefined": ["md5", "sha1", "sha256", "sha512"] #fixed predefined parameters, modules is not able to manage other type
                        },
         #default is used for run time execution. parameters defined here will be used as default when not specified or when configured
         #for automation
         "runtime": {"status": Enabled,
                     "parameters": ["md5", "sha512"] #md5 and sha512 parameters used by default (if not filled by user or if preconfigured for automation)
                     }
         },
        
        
        {"name": "arg5",
        "input": Argument.Required|Argument.Single|typeId.Int64,
         "description": "required argument of type Int64 with fixed parameter selected by user",
         "parameters": {"type": Parameter.Fixed,
                        "predefined": [2**60, -(2**60)], #fixed predefined parameters, modules is not able to manage other type
                        },
         # !!! When parameter is fixed, "predefined" field MUST be filled !!!
         "runtime": {"parameters": 2**60}
         },
                
        {"name": "arg6",
         "input": Argument.Required|Argument.List|typeId.Path,
         "description:": "required list of argument of types Path with parameters provided by user" #no predefined parameters, no default
         },
        
        {"name": "arg7",
         "input": Argument.Empty,
         "description": "optional argument with no parameter enabled by default",
         "runtime": {"status": Enabled}
         },
        
        {"name": "arg8",
         "input": No,
         "description": "optional argument with no parameter disabled by default",
         "runtime": {"status": Disabled}
         },

        {"name": "arg9",
         "input": Argument.Required|Argument.List|typeId.String,
         "description": "required ",
         "parameters": {"type": Parameter.Fixed,
                        "predefined": ["md5", "sha1", "sha256", "sha512"],
                        },
         "runtime": {"parameters": ["md5", "sha512"]}
         }
        ]


pyListToVariant(["test", "for", "string", "weird behaviour if no =..."], 1)
        
res = pyListToVariant(["test", "for", "string", "weird behaviour if no =..."], 1)

print type(res)

lres = res.value()

for x in lres:
    print x

cstr = pyObjectToVariant("test", typeId.String)
print cstr

cint = pyObjectToVariant(10000000, typeId.UInt16)
print cint

l = LOCAL.local()
vm = VMap()
vm.thisown = False

n = v.GetNode("/")

print n.name()

vn = Variant(n)
vn.thisown = False

vm["parent"] = vn

vl = VList()
vl.thisown = False

#print "GENERATING Variant(Path) for"
for node in os.listdir("/home/udgover"):
    path = Path("/home/udgover/" + node)
    #print "        ", path.path
    path.thisown = False
    vp = Variant(path)
    vp.thisown = False
    vl.append(vp)

vvl = Variant(vl)
vvl.thisown = False
vm["path"] = vvl

try:
    l.start(**vm)
except TypeError:
    l.start(vm)

vm = VMap()
vm.thisown = False

n = v.GetNode("/")
vn = Variant(n)
vn.thisown = False

vm["node"] = vn
vb = Variant(True)
vb.thisown = True
vm["long"] = vb
vm["recursive"] = vb

ls = LS()
ls.start(**vm)

import time, traceback

vlist = VList()
vlist2 = VList()
pylist = []
pylist2 = []
vmap = VMap()
vmap2 = VMap()
pymap = {}
pymap2 = {}

nbitem = 10

print "=" * 50
print "Creating vlist, vvlist, pylist, pylist2, vmap, vvmap, pymap and pymap2 with", nbitem, "items :"
t = time.time()
for i in xrange(0, nbitem):
    vlist.append(i)
    vlist2.append(i)

    pylist.append(i)
    pylist2.append(i)

    vmap[str(i)] = i
    vmap2[str(i)] = i

    pymap[str(i)] = i
    pymap2[str(i)] = i

pylist2[nbitem - 1] = 0
vlist2[nbitem-1] = nbitem

pymap2[str(nbitem - 1)] = 0
vmap2[str(nbitem-1)] = nbitem

vvlist = Variant(vlist)
vvlist2 = Variant(vlist2)

vvmap = Variant(vmap)
vvmap2 = Variant(vmap2)

vstr1 = Variant("str1")
vstr2 = Variant("str2")

vmaplist = VMap()
vmaplist2 = VMap()

vmaplist["LIST"] = vvlist
vmaplist["str"] = vstr1

vmaplist2["LIST"] = vvlist2
vmaplist2["str"] = vstr2

vvmaplist = Variant(vmaplist)
vvmaplist2 = Variant(vmaplist2)

vlistmap = VList()
vlistmap2 = VList()
vlistmap.append(vmap)
vlistmap2.append(vmap2)

vvlistmap = Variant(vlistmap)
vvlistmap2 = Variant(vlistmap2)

extime = time.time() - t
print "exec time:", extime
print ("=" * 50) + "\n"

tests = [
    "vstr1 op vstr1", "vstr2 op vstr1", "vstr1 op 'str1'", "vstr1 op ''", "vstr1 op 'different'",
    
    "vlist op vlist", "vlist op vlist2", "vlist op pylist", "vlist op pylist2",
    "vvlist op vvlist", "vvlist op vvlist2",  "vvlist op vlist", "vvlist op vlist2", "vvlist op pylist", "vvlist op pylist2",
    "nbitem - 1 in vlist", "Variant(nbitem - 1) in vlist", "nbitem in vlist", "Variant(nbitem) in vlist",

    "vmap op vmap", "vmap op vmap2", "vmap op pymap", "vmap op pymap2",
    "vvmap op vvmap", "vvmap op vvmap2", "vvmap op vmap", "vvmap op vmap2", "vvmap op pymap", "vvmap op pymap2",
    
    "vlistmap op vlistmap", "vlistmap op vlistmap2", 
    "vvlistmap op vvlistmap", "vvlistmap op vvlistmap2",

    "vmaplist op vmaplist", "vmaplist op vmaplist2",
    "vvmaplist op vvmaplist", "vvmaplist op vvmaplist2"]


print "=" * 50
print "Starting tests:"
print tests
print ("=" * 50) + "\n"

def evalexpr(first, second, operator):
    print "=" * 50
    real_test = first + operator + second
    print "Current test --->", real_test
    print eval(first)
    print "\n", 25*" ", operator, "\n"
    print eval(second), "\n"
    try:
        t = time.time()
        res = eval(real_test)
        extime = time.time() - t
        print "\n< " + real_test + " > terminated"
        print "result:" + (" " * 3), res
        print "exec time:", extime
        print ("=" * 50) + "\n"
    except:
        print "error with test", test
        traceback.print_exc(file=sys.stdout)    


for test in tests:
    idx = test.find("op")
    if idx != -1:
        first = test[:idx]
        second = test[idx+2:]
        for operator in ["==", "!=", ">", "<", ">=", "<="]:
            evalexpr(first, second, operator)
    else:
        idx = test.find("in")
        operator = "in"
        first = test[:idx]
        second = test[idx+2:]

print "==", Variant(123456) == Variant(123456), 123456 == 123456
print "!=", Variant(123456) != Variant(123456), 123456 != 123456
print ">", Variant(123456) > Variant(123456), 123456 > 123456
print "<", Variant(123456) < Variant(123456), 123456 < 123456
print ">=", Variant(123456) >= Variant(123456), 123456 >= 123456
print "<=", Variant(123456) <= Variant(123456), 123456 <= 123456
