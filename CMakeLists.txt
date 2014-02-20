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
#  Christophe Malinge <cma@digital-forensic.org>
#  Solal Jacob <sja@digital-forensic.org>
#  Frederic Baguelin <fba@digital-forensic.org>
#

cmake_minimum_required(VERSION 2.6)

include("cmake_modules/dff/header.cmake")

set(PROJECT_EDITION "ose")

include("cmake_modules/dff/find_deps.cmake")
include("cmake_modules/dff/macros.cmake")
include("cmake_modules/dff/copy_deps.cmake")

install_file(
  ${CONSOLE_SCRIPT}
  ${GRAPHICAL_SCRIPT}
)

#### Main subdirectories to recurse
add_subdirectory (dff)
add_subdirectory (doc)

if (UNIX)
  include("cmake_modules/dff/unix_install.cmake")
else(UNIX)
  include("cmake_modules/dff/cpack_win.cmake")
endif(UNIX)

include("cmake_modules/dff/footer.cmake")
