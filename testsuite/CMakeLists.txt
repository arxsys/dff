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

## Main purpose of this macro if to copy Python test files at build.
# without it python is unable to load DFF API
macro(deploytestfile target_name)
  foreach(file ${ARGN})
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
      # Be carreful, SWiG generate .py files, which sits in builddir,
      #  so we have to check if file exists in source dir before copying it.
      add_custom_target("testdeploy.${target_name}.${file}" ALL
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
	  ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
	)
    endif(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
  endforeach(file ${ARGN}) 
endmacro(deploytestfile target_name)

# Define 'simple' files to deploy
SET(testsuite_srcs
  dffunittest.py	# Base unittest file, specific test follows
  local.py
  hashtest.py
  enverrortest.py
  vfserrortest.py
)
deploytestfile(testsuite ${testsuite_srcs})

# Here we use configure_file because content of those files have variable
# to be replaced by CMake
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/fattest.py ${CMAKE_CURRENT_BINARY_DIR}/fattest.py)

# unittest
ADD_TEST(modules.fs.local python local.py)
ADD_TEST(modules.parser.hash python hashtest.py)
ADD_TEST(modules.fs.fat python fattest.py)
ADD_TEST(modules.api.env.error python enverrortest.py)
ADD_TEST(modules.api.vfs.error python vfserrortest.py)
