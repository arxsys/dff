#!/usr/bin/python -i
# DFF -- An Open Source Digital Forensics Framework
# Copyright (C) 2009-2011 ArxSys
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
#  Solal Jacob <sja@digital-forensic.org>
#

"""@package dff
Digital-forensic framework launcher
"""
import os, sys, getopt

# ensure dist-packages will be loaded be pyshared on Debian
# else private modules won't be found
from distutils.sysconfig import get_python_lib
if not os.path.exists(os.path.join("dff", "modules")) and os.path.exists(os.path.join(get_python_lib(), "dff")):
    sys.path.insert(0, os.path.join(get_python_lib()))

if os.name == "posix": 
    try :
        import dl
        sys.setdlopenflags(sys.getdlopenflags() | dl.RTLD_GLOBAL)
    except ImportError:
        import ctypes
        sys.setdlopenflags(sys.getdlopenflags() | ctypes.RTLD_GLOBAL)

from dff.api.manager.manager import ApiManager
from dff.ui.gui.gui import GUI
from dff.ui.console.console import Console
from dff.ui.ui import Usage

MODULES_PATHS = []

if os.path.exists(os.path.join("dff", "modules")):
    MODULES_PATHS = [os.path.join("dff", "modules")]
elif os.path.exists(os.path.join(get_python_lib(), "dff")):
    MODULES_PATHS = [os.path.join(get_python_lib(), "dff", "modules")]

def fg():
    """Launch shell loop"""
    ui.launch()

if __name__ == "__main__":
    """You can place some script command here for testing purpose"""
    argv = Usage(sys.argv[1:])
    if argv.batch:
       console = Console(argv.debug, argv.verbosity)
       console.loadModules(MODULES_PATHS)
       console.onecmd("batch " + argv.batch, False)
    ui = GUI(argv.debug, argv.verbosity)
    ui.launch(MODULES_PATHS)
