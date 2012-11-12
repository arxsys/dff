# - Find TRE
# This module finds an installed TRE.  It sets the following variables:
#  TRE_FOUND - set to true if TRE is found
#  TRE_LIBRARY - dynamic libraries for aff
#  TRE_INCLUDE_DIR - the path to the include files
#  TRE_VERSION   - the version number of the aff library
#

SET(TRE_FOUND FALSE)

FIND_LIBRARY(TRE_LIBRARY tre)

IF (TRE_LIBRARY)
   FIND_PATH(TRE_INCLUDE_PATH tre)
   IF (TRE_INCLUDE_PATH)
     IF (CMAKE_GENERATOR MATCHES "Visual Studio")
       STRING(REPLACE "tre" "" TRE_INCLUDE_DIR "${TRE_INCLUDE_PATH}")
       STRING(REPLACE "tre.lib" "" TRE_DYN_LIB_PATH "${TRE_LIBRARY}")
       SET(TRE_DYN_LIBRARIES ${TRE_DYN_LIB_PATH}/tre.dll)
     ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
     if(EXISTS "${TRE_INCLUDE_PATH}/tre/tre-config.h")
       file(READ "${TRE_INCLUDE_PATH}/tre/tre-config.h" _tre_contents)
       #generally, to match dot you have to escape but cmake complains... so leave the interpreted dot version
       string(REGEX REPLACE ".*# *define *TRE_VERSION *\"([0-9].[0-9].[0-9])\".*" "\\1" TRE_VERSION "${_tre_contents}")
       string(REGEX REPLACE ".*# *define *TRE_APPROX *([0-9]+).*" "\\1" TRE_HAVE_APPROX "${_tre_contents}")
       string(REGEX REPLACE ".*# *define *TRE_WCHAR *([0-9]+).*" "\\1" TRE_HAVE_WCHAR "${_tre_contents}")
       string(REGEX REPLACE ".*# *define *TRE_MULTIBYTE *([0-9]+).*" "\\1" TRE_HAVE_MULTIBYTE "${_tre_contents}")
       set(TRE_FOUND TRUE)
     else(EXISTS "${TRE_INCLUDE_PATH}/tre/tre-config.h")
       set(TRE_FOUND FALSE)
     endif(EXISTS "${TRE_INCLUDE_PATH}/tre/tre-config.h")
   ENDIF (TRE_INCLUDE_PATH)
ENDIF (TRE_LIBRARY)