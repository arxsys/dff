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
#  Christophe Malinge <cma@digital-forensic.org>
#  Solal Jacob <sja@digital-forensic.org>

project (dff)

#### Basic Cmake definitions
cmake_minimum_required (VERSION 2.6)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake_modules/")

set(CMAKE_INCLUDE_PATH "${INCLUDEDIR}")
set(CMAKE_LIBRARY_PATH "${LIBDIR}")

# Optional dependencies required version
set(BFIO_REQUIRED_VERSION "20120425")
set(PFF_REQUIRED_VERSION "20120802")

# Check 64 bit
if( "${CMAKE_SIZEOF_VOID_P}" EQUAL 4 )
  set( HAVE_64_BIT 0 )
else( "${CMAKE_SIZEOF_VOID_P}" EQUAL 4 )
   if (WIN32)
       SET( HAVE_64_BIT 0 )
   else (WIN32)
       SET(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -DSWIGWORDSIZE64)
       SET( HAVE_64_BIT 1 )
   endif (WIN32)
endif( "${CMAKE_SIZEOF_VOID_P}" EQUAL 4 )

option(ENABLE_DEBUG "Compile using -g flag ? Useful for debugging" OFF)
add_definitions(-D__STDC_LIMIT_MACROS)
if(UNIX)
  if(ENABLE_DEBUG)
    add_definitions(-D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -g -Wall)
    message(STATUS "Will use -g for debugging -- yes")
  else(ENABLE_DEBUG)
#change flag here
    add_definitions(-D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -O2)
    message(STATUS "Will use -g for debugging -- no")
  endif(ENABLE_DEBUG)
endif(UNIX)
# $> cmake -DENABLE_DEBUG:BOOLEAN=OFF

# Set installation mode, include all items (*.py, ...) Default is development mode
option(INSTALL "Start installation mode ?" OFF)
IF(INSTALL)
  message(STATUS "Preparing installation mode")
ELSE(INSTALL)
  message(STATUS "Preparing development mode")
ENDIF(INSTALL)

option(WITH_IOSTAT "enable statistics on input / output comsumption ?" OFF)
if (WITH_IOSTAT)
  add_definitions(-DWITH_IOSTAT=1)
  message(STATUS "input / output stats enabled")
else (WITH_IOSTAT)
  message(STATUS "input / output stats disabled")
endif (WITH_IOSTAT)

option(WITH_TTT_DEBUG "Compile with two three tree debugging" OFF)
if (WITH_TTT_DEBUG)
  add_definitions(-DTWO_THREE_TREE_DEBUG=1)
  message(STATUS "Compile WITH TwoThreeTree debug information")
else (WITH_TTT_DEBUG)
  message(STATUS "Compile WITHOUT TwoThreeTree debug information")
endif (WITH_TTT_DEBUG)

IF (WIN32)
  option(WINALL "Package with windows Dependencies ?" OFF)
  IF(WINALL)
    message(STATUS "Packaging windows version with dependencies")
  ELSE(WINALL)
    message(STATUS "Packaging windows version without dependencies")
  ENDIF(WINALL)
ENDIF(WIN32)

## Swig
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

STRING (COMPARE LESS "${SWIG_VERSION}" "1.3.38" SWIGOK)

if (${SWIGOK})
  MESSAGE(FATAL_ERROR "Need SWIG version >= 1.3.38 (current version is ${SWIG_VERSION})")
endif (${SWIGOK})

if (ICU_DEP_PATH)
	if (WIN32)
		set(ICU_INCLUDE_PATH "${ICU_DEP_PATH}/include")
		set(ICU_LIBRARIES_PATH "${ICU_DEP_PATH}/lib")
		set(ICU_DYNLIB_PATH "${ICU_DEP_PATH}/bin")
	endif (WIN32)
endif (ICU_DEP_PATH)

find_package(ICU REQUIRED)
find_package(AFF)
find_package(BFIO)
find_package(EWF)
find_package(PFF)
find_package(TRE)
find_package(FFmpeg)

if (UNIX)
  find_package(UDEV)
  if (UDEV_FOUND)
    SET(HAVE_UDEV TRUE)
    message(STATUS "udev include and libraries: FOUND")
  endif (UDEV_FOUND)
endif(UNIX)


if (FFMPEG_FOUND)
  message(STATUS "FFmpeg includes and libraries found video module: ENABLED")
else ()
  message(STATUS "FFmpeg includes and libraries not found video module: DISABLED")
endif (FFMPEG_FOUND)


IF (TRE_FOUND)
   add_definitions(-DHAVE_TRE)
   include_directories(${TRE_INCLUDE_DIR})
   message(STATUS "TRE installed version: ${TRE_VERSION}
   approximative matching support : ${TRE_HAVE_APPROX}
   wide character support         : ${TRE_HAVE_WCHAR}
   multibyte character support    : ${TRE_HAVE_MULTIBYTE}")
ENDIF (TRE_FOUND)

if(PFF_FOUND)
   if("${PFF_VERSION}" VERSION_EQUAL "${PFF_REQUIRED_VERSION}" OR "${PFF_VERSION}" VERSION_GREATER "${PFF_REQUIRED_VERSION}")
     message(STATUS "PFF installed version: ${PFF_VERSION}
   >= ${PFF_REQUIRED_VERSION} -- yes")
   else("${PFF_VERSION}" VERSION_EQUAL "${PFF_REQUIRED_VERSION}" OR "${PFF_VERSION}" VERSION_GREATER "${PFF_REQUIRED_VERSION}")
     message(STATUS "PFF installed version: ${PFF_VERSION}
   >= ${PFF_REQUIRED_VERSION} -- no")
     unset(PFF_FOUND)
     unset(PFF_VERSION)
   endif("${PFF_VERSION}" VERSION_EQUAL "${PFF_REQUIRED_VERSION}" OR "${PFF_VERSION}" VERSION_GREATER "${PFF_REQUIRED_VERSION}")
endif(PFF_FOUND)

if(BFIO_FOUND)
   if("${BFIO_VERSION}" VERSION_EQUAL "${BFIO_REQUIRED_VERSION}" OR "${BFIO_VERSION}" VERSION_GREATER "${BFIO_REQUIRED_VERSION}")
     message(STATUS "BFIO installed version: ${BFIO_VERSION}
   >= ${BFIO_REQUIRED_VERSION} -- yes")
   else("${BFIO_VERSION}" VERSION_EQUAL "${BFIO_REQUIRED_VERSION}" OR "${BFIO_VERSION}" VERSION_GREATER "${BFIO_REQUIRED_VERSION}")
     message(STATUS "BFIO installed version: ${BFIO_VERSION}
   >= ${BFIO_REQUIRED_VERSION} -- no")
     unset(BFIO_FOUND)
     unset(BFIO_VERSION)
   endif("${BFIO_VERSION}" VERSION_EQUAL "${BFIO_REQUIRED_VERSION}" OR "${BFIO_VERSION}" VERSION_GREATER "${BFIO_REQUIRED_VERSION}")
endif(BFIO_FOUND)

IF (EWF_FOUND)
   message(STATUS "EWF installed version: ${EWF_VERSION}")
   message(STATUS "library: ${EWF_LIBRARY}")
ENDIF (EWF_FOUND)

if(AFF_FOUND)
  message(STATUS "AFF installed version: ${AFF_VERSION}")
endif(AFF_FOUND)

# Project-wide swig options
#SET(CMAKE_SWIG_FLAGS "-py3")

option(DISABLE_SWIG_THREADING "Wrap cpp code to python without -threads" OFF)
if(DISABLE_SWIG_THREADING)
  message(STATUS "Will we use swig -threads -- no")
else()
  #message(STATUS "Will we use swig -threads -- yes")
  #set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -O -threads)
  set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -threads)
endif(DISABLE_SWIG_THREADING)
# $> cmake -DDISABLE_SWIG_THREADING:BOOLEAN=ON

find_library(HAVE_FUSE NAMES fuse)
if(NOT HAVE_FUSE)
  message(STATUS "(Optional) fuse library not found; file system module 'fuse' will not be built")
endif(NOT HAVE_FUSE)


IF(WIN32)
  SET(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -DWIN32 -DSWIGWIN)
  add_definitions("/W3 /D_CRT_SECURE_NO_WARNINGS /wd4290 /nologo")
ENDIF(WIN32)


## Python check
FIND_PACKAGE(PythonInterp REQUIRED)
execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())" OUTPUT_VARIABLE PYTHON_SITE_PACKAGES_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_version; print(get_python_version())" OUTPUT_VARIABLE PYTHON_VERSION OUTPUT_STRIP_TRAILING_WHITESPACE)
if (UNIX)
  if (APPLE)
    execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_config_vars; print(get_config_vars()[\"PYTHONFRAMEWORKPREFIX\"] + \"/\" + get_config_vars()[\"LDLIBRARY\"])" OUTPUT_VARIABLE PYTHON_LIBRARIES OUTPUT_STRIP_TRAILING_WHITESPACE)
  else ()
    execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_config_vars; print(get_config_vars()[\"LIBDIR\"] + \"/\" + get_config_vars()[\"LDLIBRARY\"])" OUTPUT_VARIABLE PYTHON_LIBRARIES OUTPUT_STRIP_TRAILING_WHITESPACE)
  endif (APPLE)
  execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_python_inc; print(get_python_inc())" OUTPUT_VARIABLE PYTHON_INCLUDE_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
  execute_process ( COMMAND ${PYTHON_EXECUTABLE} -c "from distutils.sysconfig import get_config_vars; print(get_config_vars()[\"BINDIR\"])" OUTPUT_VARIABLE PYTHON_BIN_PATH OUTPUT_STRIP_TRAILING_WHITESPACE)
  if(NOT PYTHON_LIBRARIES)
    message(SEND_ERROR "No Python library found ; please install Python package, at least version 2.5.")
  else(NOT PYTHON_LIBRARIES)
    message(STATUS "Python library found: ${PYTHON_LIBRARIES}")
  endif(NOT PYTHON_LIBRARIES)
  if(NOT EXISTS ${PYTHON_INCLUDE_PATH}/Python.h)
    message(SEND_ERROR "No Python include/header file found; install Python development package.")
  else(NOT EXISTS ${PYTHON_INCLUDE_PATH}/Python.h)
    message(STATUS "Python header found: ${PYTHON_INCLUDE_PATH}")
  endif(NOT EXISTS ${PYTHON_INCLUDE_PATH}/Python.h)
else (UNIX)
  find_package(PythonLibs)
  find_package(PythonInterp)
  SET(PYTHON_BIN_PATH ${PYTHON_EXECUTABLE})
# FIXME for windows validate presence of Python.h in PYTHON_INCLUDE_PATH
endif(UNIX)

message(STATUS "Python in: ${PYTHON_BIN_PATH}")


FIND_PACKAGE(PythonLibrary REQUIRED)
FIND_PACKAGE(PyQt4 REQUIRED)
INCLUDE(PythonMacros)
IF (NOT MSVC)
  ADD_DEFINITIONS(-fPIC)
ENDIF ()
#FIND_PACKAGE(Qt4 REQUIRED)
#INCLUDE(${QT_USE_FILE})

if(UNIX)
# Search for gzip program, to compress manpage for Unix
  find_program(GZIP_TOOL
               NAMES gzip
               PATHS /bin
               /usr/bin
               /usr/local/bin)
  if(NOT GZIP_TOOL)
    message(FATAL_ERROR "Unable to find 'gzip' program")
  endif(NOT GZIP_TOOL)
endif(UNIX)

## Python-magic check for Unix only
if(UNIX)
  execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import magic; print magic.__file__" OUTPUT_VARIABLE PYTHON_MAGIC_PATH ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
  if(NOT PYTHON_MAGIC_PATH)
    message(STATUS "Python magic not found. Not needed at build step but mandatory to start DFF.")
  else(NOT PYTHON_MAGIC_PATH)
    message(STATUS "Python magic found: ${PYTHON_MAGIC_PATH}")
  endif(NOT PYTHON_MAGIC_PATH)
endif(UNIX)

## Python-QT bindings check
execute_process(COMMAND ${PYTHON_EXECUTABLE} -c "import PyQt4; print PyQt4.__path__[0]" OUTPUT_VARIABLE PYTHON_QT4_PATH ERROR_QUIET OUTPUT_STRIP_TRAILING_WHITESPACE)
if(NOT PYTHON_QT4_PATH)
  message(STATUS "Python QT4 bindings not found. Not needed at build step but mandatory to start DFF.")
else(NOT PYTHON_QT4_PATH)
  message(STATUS "Python QT4 libraries bindings found: ${PYTHON_QT4_PATH}")
endif(NOT PYTHON_QT4_PATH)

## PyQt linguist transalation updater check, to create or update translation
## files
find_program(PYTHON_QT4_LANGUAGE NAMES pylupdate4 PATHS	${CMAKE_SYSTEM_PROGRAM_PATH} ${PYTHON_QT4_PATH}/bin ${PYTHON_QT4_PATH})
if(PYTHON_QT4_LANGUAGE)
  message(STATUS "Python Qt4 linguist translation files updater found: ${PYTHON_QT4_LANGUAGE}")
else(PYTHON_QT4_LANGUAGE)
  message(STATUS "Python Qt4 linguist translation files updater not found, unable to check for new tranlatable strings.")
endif(PYTHON_QT4_LANGUAGE)

## QT .ts to .qm compiler, used by translator objects
find_program(QT_LANGUAGE_COMPILER NAMES lrelease lrelease-qt4 PATHS ${CMAKE_SYSTEM_PROGRAM_PATH} ${PYTHON_QT4_PATH}/bin ${PYTHON_QT4_PATH})
if(QT_LANGUAGE_COMPILER)
  message(STATUS "QT translation compiler found: ${QT_LANGUAGE_COMPILER}")
else(QT_LANGUAGE_COMPILER)
  message(ERROR "QT translation compiler not found.")
endif(QT_LANGUAGE_COMPILER)

## PyQt UI compiler check, to generate widgets
find_program(PYTHON_QT4_UIC NAMES pyuic4 pyuic4.bat PATHS ${CMAKE_SYSTEM_PROGRAM_PATH} ${PYTHON_QT4_PATH}/bin ${PYTHON_QT4_PATH})
if(PYTHON_QT4_UIC)
  message(STATUS "Python Qt4 user interface compiler found: ${PYTHON_QT4_UIC}")
else(PYTHON_QT4_UIC)
  message(SEND_ERROR "Python Qt4 user interface compiler not found.")
endif(PYTHON_QT4_UIC)

## PyQt resource compiler check, to generate icons
find_program(PYTHON_QT4_RCC NAMES pyrcc4 PATHS ${CMAKE_SYSTEM_PROGRAM_PATH} ${PYTHON_QT4_PATH}/bin ${PYTHON_QT4_PATH})
if(PYTHON_QT4_RCC)
  message(STATUS "Python Qt4 resource compiler found: ${PYTHON_QT4_RCC}")
else(PYTHON_QT4_RCC)
  message(SEND_ERROR "Python Qt4 resource compiler not found.")
endif(PYTHON_QT4_RCC)

# Backing up original install prefix, some files have to sit elsewhere than python path, see at the end of this file.
SET(CMAKE_INSTALL_ORIG_PREFIX ${CMAKE_INSTALL_PREFIX})
# Install prefix used by Python installer.
SET(CMAKE_INSTALL_PREFIX ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/)

## Main purpose of this macro if to copy Python files at install.
# It also deploys .py files in build directory if there is one.
LIST(APPEND PYC_FILES "")
FILE(WRITE "${CMAKE_BINARY_DIR}/installed_files.log" "")

macro(install_file target_name)
  foreach(file ${ARGN})
    # Be carreful:
    #  - SWiG generate .py files, which sits in builddir, so we have to check
    # if file exists in source dir before copying it.
    #  - Several files are configured at the cmake configure step, moving from
    # source to build dir, mostly to replace versions variables, so we have to
    # check if file is missing from build dir before copying it at build step.
    if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file} AND NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/${file})
      add_custom_target("builddeploy.${target_name}.${file}" ALL
	COMMAND ${CMAKE_COMMAND} -E copy_if_different
	  ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file}
	)
    endif(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file} AND NOT EXISTS ${CMAKE_CURRENT_BINARY_DIR}/${file})
    IF (INSTALL)
      add_custom_target("${target_name}.${file}" ALL)
      FILE(RELATIVE_PATH rel ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
	  IF ("${rel}" STREQUAL "")
	  	SET(ifile "${file}")
	  ELSE("${rel}" STREQUAL "")
		SET(ifile "${rel}/${file}")
	  ENDIF("${rel}" STREQUAL "")
	  FILE(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${ifile}\n")
      IF(NOT WIN32 AND UNIX)
		install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${file} DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/${rel})
	  ELSE(NOT WIN32 AND UNIX)
	    install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${file} DESTINATION /${CMAKE_PROJECT_NAME}/${rel})
		IF(${file} MATCHES "^.*\\.py$" AND NOT ${rel} STREQUAL "")
		# Store every .py files in a list, renaming each file to .pyc it
		# will handle Windows uninstall ; runtime created *.pyc are not
		# removed by uninstaller.
			STRING(REPLACE "\\" "\\\\" PYCFILE "${rel}/${file}c")
			STRING(REPLACE "/" "\\\\" PYCFILE ${PYCFILE})
			LIST(APPEND PYC_FILES "${PYCFILE}")
			SET(PYC_FILES "${PYC_FILES}" PARENT_SCOPE)
		ENDIF(${file} MATCHES "^.*\\.py$" AND NOT ${rel} STREQUAL "")
	  ENDIF(NOT WIN32 AND UNIX)
    ENDIF (INSTALL)
  endforeach(file ${ARGN}) 
endmacro(install_file target_name)

## Macro to copy lib at install
macro(install_lib target_name)
  FILE(RELATIVE_PATH rel ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
  IF ("${rel}" STREQUAL "")
	SET(ifile "${target_name}")
  ELSE("${rel}" STREQUAL "")
	SET(ifile "${rel}/${target_name}")
  ENDIF("${rel}" STREQUAL "")
  IF(NOT WIN32 AND UNIX)
	FILE(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${ifile}.so\n")	
    INSTALL (TARGETS ${target_name} DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}/${rel})
  ELSE(NOT WIN32 AND UNIX)
  	FILE(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${ifile}.pyd\n")
	INSTALL (TARGETS ${target_name} DESTINATION /${CMAKE_PROJECT_NAME}/${rel})
  ENDIF(NOT WIN32 AND UNIX)	
endmacro(install_lib)

if (APPLE)
  SET(CMAKE_SHARED_LIBRARY_SUFFIX ".so")
  SET(CMAKE_SHARED_MODULE_SUFFIX ".so")
endif(APPLE)

## Macro to convert XML ui files to Python Qt widget code
# We are unable to use pyuic4 with QTreeWidget as base class
# It is why <widget class="QWidget" name="useless" /> has to be appended to .ui
# files using QTreeWidget. Be carreful, QtDesigner place this second widget at
# the end of the .ui file ; which make pyuic4 fails to compile.
macro(uitopy_file target_name)
  foreach(UIFILE ${ARGN})
    string(REGEX REPLACE "^(.*)\\.ui$" "ui_\\1.py" PYUICFILE ${UIFILE})
    add_custom_target("${target_name}.${UIFILE}" ALL
      COMMAND ${PYTHON_QT4_UIC} -o ${CMAKE_CURRENT_BINARY_DIR}/${PYUICFILE} ${CMAKE_CURRENT_SOURCE_DIR}/${UIFILE}
      SOURCES ${CMAKE_CURRENT_SOURCE_DIR}/${UIFILE}
      )
  endforeach(UIFILE ${ui_dialog_files})
endmacro(uitopy_file)

#### Project install
SET(CPACK_SET_DESTDIR "ON")

SET(CPACK_PACKAGE_DESCRIPTION_SUMMARY "Digital Forensics Framework")
SET(CPACK_PACKAGE_VENDOR "ArxSys")
SET(CPACK_PACKAGE_DESCRIPTION_FILE "${CMAKE_CURRENT_SOURCE_DIR}/README")
SET(CPACK_RESOURCE_FILE_LICENSE "${CMAKE_CURRENT_SOURCE_DIR}/COPYRIGHT")
# In order to provide top-level setting of DFF version, three variables bellow
# must be used in those two files :
#  ui/gui/gui.py
#  ui/ui.py
# See corresponding CMakeLists.txt for CONFIGURE_FILE.
SET(CPACK_PACKAGE_VERSION_MAJOR "1") 
SET(CPACK_PACKAGE_VERSION_MINOR "3")
SET(CPACK_PACKAGE_VERSION_PATCH "1")
SET(CPACK_PACKAGE_INSTALL_DIRECTORY "DFF")

message(STATUS "DFF target version is ${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}")

#### Project API versionning
set(API_DEVICES_VERSION "0.4.0")
set(API_ENV_VERSION "1.1.0")
set(API_EXCEPTIONS_VERSION "1.0.0")
set(API_GUI_VERSION "1.1.0")
set(API_LOADER_VERSION "1.3.0")
set(API_MAGIC_VERSION "1.7.0")
set(API_MANAGER_VERSION "1.0.0")
set(API_MODULE_VERSION "1.0.0")
set(API_SEARCH_VERSION "1.0.0")
set(API_TASKMANAGER_VERSION "1.1.0")
set(API_TREE_VERSION "1.0.0")
set(API_TYPE_VERSION "1.0.0")
set(API_VARIANT_VERSION "1.0.0")
set(API_VFS_VERSION "2.7.0")
set(API_DATATYPE_VERSION "1.0.0")
set(API_EVENT_VERSION "1.0.0")

#### Project install for windows
IF(WIN32 AND NOT UNIX)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
	DESTINATION /${CMAKE_PROJECT_NAME}
	PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff-gui.py
	DESTINATION /${CMAKE_PROJECT_NAME}
	PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
	RENAME dff-gui.pyw)
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.ico
    DESTINATION /${CMAKE_PROJECT_NAME}/ressources/)

# Install docs and licenses
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/README ${CMAKE_CURRENT_SOURCE_DIR}/COPYRIGHT ${CMAKE_CURRENT_SOURCE_DIR}/LICENSE ${CMAKE_CURRENT_SOURCE_DIR}/LICENSE-THIRDPARTY
          DESTINATION /${CMAKE_PROJECT_NAME}/
          PERMISSIONS OWNER_READ GROUP_READ WORLD_READ)

  SET(CPACK_MONOLITHIC_INSTALL "ON")
	
  SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_BUNDLE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_NSIS_MUI_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
  SET(CPACK_NSIS_MUI_UNIICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
  SET(CPACK_NSIS_DISPLAY_NAME "Digital Forensics Framework")
  SET(CPACK_NSIS_HELP_LINK "http://www.digital-forensic.org/")
  SET(CPACK_NSIS_URL_INFO_ABOUT "http://www.arxsys.fr/")
  SET(CPACK_NSIS_CONTACT "contact@arxsys.fr")
  SET(CPACK_NSIS_MODIFY_PATH OFF)
  SET(CPACK_NSIS_COMPRESSOR "/SOLID lzma")
  SET(CPACK_GENERATOR "NSIS")
  
  SET(NSIS_GET_32_BITS_PATHES
	"
    !include \\\"x64.nsh\\\"
	Var /GLOBAL pypath
	Var /GLOBAL pyqtpath

	StrCpy \\\$pypath \\\"\\\"
	StrCpy \\\$pyqtpath \\\"\\\"
	\\\${If} \\\${RunningX64}
		ReadRegStr \\\$pypath HKLM \\\"SOFTWARE\\\\Wow6432Node\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
		ReadRegStr \\\$pyqtpath HKLM \\\"SOFTWARE\\\\Wow6432Node\\\\PyQt4\\\\Py2.7\\\\InstallPath\\\" \\\"\\\"
	\\\${Else}
		ReadRegStr \\\$pypath HKLM \\\"SOFTWARE\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
		ReadRegStr \\\$pyqtpath HKLM \\\"SOFTWARE\\\\PyQt4\\\\Py2.7\\\\InstallPath\\\" \\\"\\\"
	\\\${EndIf}
	")
	
  SET(NSIS_GET_64_BITS_PATHES
	"
	Var /GLOBAL pypath
	Var /GLOBAL pyqtpath

	StrCpy \\\$pypath \\\"\\\"
	StrCpy \\\$pyqtpath \\\"\\\"
	ReadRegStr \\\$pyqtpath HKLM \\\"SOFTWARE\\\\PyQt4\\\\Py2.7\\\" \\\"\\\"
	ReadRegStr \\\$pypath HKLM \\\"SOFTWARE\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
	")

  SET(NSIS_DEFAULT_LABELS
    "
    inst:
	    Var /GLOBAL installed_version
		StrCpy \\\$installed_version \\\"\\\"

		ReadRegStr \\\$R0 HKLM \\\"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\dff\\\" \\\"DisplayVersion\\\"
		ReadRegStr \\\$R1 HKLM \\\"Software\\\\Microsoft\\\\Windows\\\\CurrentVersion\\\\Uninstall\\\\dff\\\" \\\"UninstallString\\\"
		\\\${If} \\\$R0 != \\\"\\\"
			StrCpy \\\$installed_version \\\$R0
		\\\${ElseIf} \\\$R1 != \\\"\\\"
			StrCpy \\\$installed_version \\\$R1
		\\\${EndIf}
        \\\${If} \\\$installed_version != \\\"\\\"
			MessageBox MB_YESNO|MB_ICONQUESTION \\\"DFF version \\\$installed_version is already installed.\\\$\\\\n\\\$\\\\nClick 'YES' to uninstall it first, or 'NO' to overwrite already installed version.\\\" IDYES uninst
			Goto done
		\\\${Else}
			Goto cont		
        \\\${EndIf}

    end_with_errors:
        MessageBox MB_OK|MB_ICONEXCLAMATION \\\"Error uninstalling DFF version \\\$R0.\\\"	    
		Goto cont

	uninst:
        ClearErrors
        ExecWait '$R1 _?=$INSTDIR'
        IfErrors end_with_errors
	    MessageBox MB_OK|MB_ICONINFORMATION \\\"Uninstalling previous DFF version \\\$R0 done, continue with install.\\\"
		Goto cont

	cont:
        File /r \\\"\\\${INST_DIR}\\\\*.*\\\"
	
	done:
		
	")
	
  SET(CPACK_NSIS_EXTRA_INSTALL_COMMANDS       
    ${NSIS_GET_32_BITS_PATHES}
	"
    SetOutPath \\\"$INSTDIR\\\\dff\\\"
    CreateShortCut \\\"$DESKTOP\\\\DFF (shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\" 
    CreateShortCut \\\"$DESKTOP\\\\DFF (gui).lnk\\\" \\\"\\\$pypath\\\\pythonw.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
    CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
    CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (gui).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
    ")
	
	# *.pyc files are not deleted by installer, because they are created at
	# runtime. So, below, we force deletion of those files.
    FOREACH(PYCFILE ${PYC_FILES})
	  SET(CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS
	  "${CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS}
	  Delete \\\"$INSTDIR\\\\dff\\\\${PYCFILE}\\\"")
    ENDFOREACH(PYCFILE ${PYC_FILES})
  
	SET(CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS
    "
	${CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS}
	 Delete \\\"$DESKTOP\\\\DFF (shell).lnk\\\"
	 Delete \\\"$DESKTOP\\\\DFF (gui).lnk\\\"
	 Delete \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (shell).lnk\\\"
	 Delete \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (gui).lnk\\\"
	")
	
	#MESSAGE(STATUS ${CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS})
	
	
  if (WINALL)
    add_subdirectory (Prerequisites)
    message(STATUS "python installer: ${PYTHON_INSTALLER}")
    message(STATUS "pyqt installer: ${PYQT_INSTALLER}")
    message(STATUS "vcredist installer: ${VCREDIST_INSTALLER}")
	message(STATUS "apsw installer: ${APSW_INSTALLER}")
	message(STATUS "numpy installer: ${NUMPY_INSTALLER}")
	message(STATUS "matplotlib installer: ${MATPLOT_INSTALLER}")
	message(STATUS "PIL installer: ${PIL_INSTALLER}")
    if (WIN32)
      SET(CPACK_SYSTEM_NAME "win32_all_in_one")
    else(WIN32)
      SET(CPACK_SYSTEM_NAME "win64_all_in_one")
    endif(WIN32)
	SET(CPACK_NSIS_FULL_INSTALL ${CPACK_NSIS_FULL_INSTALL}
	${NSIS_DEFAULT_LABELS}
	"
    MessageBox MB_YESNO \\\"Install ${PYTHON_INSTALLER} ? \\\" /SD IDYES IDNO endPython
    ExecWait '\\\"msiexec\\\" /i \\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PYTHON_INSTALLER}\\\" /passive ALLUSERS=1'
    Goto endPython
    endPython:
        MessageBox MB_YESNO \\\"Install ${PYQT_INSTALLER} ? \\\" /SD IDYES IDNO endPyQt
        ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PYQT_INSTALLER}\\\"'
        Goto endPyQt
    endPyQt:
		MessageBox MB_YESNO \\\"Install ${APSW_INSTALLER}? \\\" /SD IDYES IDNO endAPSW
		ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${APSW_INSTALLER}\\\"'
		Goto endAPSW
	endAPSW:
		MessageBox MB_YESNO \\\"Install ${NUMPY_INSTALLER}? \\\" /SD IDYES IDNO endNumPy
		ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${NUMPY_INSTALLER}\\\"'
		Goto endNumPy
	endNumPy:
		MessageBox MB_YESNO \\\"Install ${MATPLOT_INSTALLER}? \\\" /SD IDYES IDNO endMatPlot
		ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${MATPLOT_INSTALLER}\\\"'
		Goto endMatPlot
	endMatPlot:
		MessageBox MB_YESNO \\\"Install ${PIL_INSTALLER}? \\\" /SD IDYES IDNO endPil
		ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PIL_INSTALLER}\\\"'
		Goto endPil
	endPil:
		MessageBox MB_YESNO \\\"Install Microsoft Visual Studio DLL dependencies ? \\\" /SD IDYES IDNO endVS
        ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${VCREDIST_INSTALLER}\\\" /q:a'
        Goto endVS
    endVS:
       RMDir /r \\\"$INSTDIR\\\\dff\\\\Prerequisites\\\"
	
    ")
  else(WINALL)
  	SET(CPACK_NSIS_FULL_INSTALL ${NSIS_GET_32_BITS_PATHES}
	"
	\\\${If} \\\$pypath == \\\"\\\"
		MessageBox MB_OK|MB_ICONEXCLAMATION \\\"Python 2.7 32 bits not found.\\\$\\\\nPlease install it before installing DFF.\\\"
		Goto done
	\\\${Else}
		Goto pyqt_check
	\\\${EndIf}
	pyqt_check:
		\\\${If} \\\$pyqtpath == \\\"\\\"
			MessageBox MB_OK|MB_ICONEXCLAMATION \\\"PyQt4 for Python 2.7 32 bits not found.\\\$\\\\nPlease install it before installing DFF.\\\"
			Goto done
		\\\${Else}
			Goto inst
		\\\${EndIf}
	"
	${NSIS_DEFAULT_LABELS}
	)
	
  endif(WINALL)
  SET(CPACK_SOURCE_GENERATOR "ZIP")
  
  SET(CMAKE_INSTALL_PREFIX "/dff/")
  
ELSE(WIN32 AND NOT UNIX)
  SET(CPACK_SOURCE_GENERATOR "TGZ")
#  SET(CPACK_SOURCE_IGNORE_FILES "") 
  SET(CPACK_GENERATOR "DEB" "RPM")
ENDIF(WIN32 AND NOT UNIX)

# Debian deb dependencies
#  python${PYTHON_VERSION} (>=${PYTHON_VERSION}.0), python-qt4 (>= 4.4.0), python-magic (>= 4.26)
# RedHat rpm dependencies
#  python >= ${PYTHON_VERSION}.0, PyQt4 >= 4.4.0, python-magic >= 4.26

install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
  DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}
  PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)

if (UNIX)
# Compress manpage
  add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz
                     COMMAND ${GZIP_TOOL} -c ${CMAKE_CURRENT_SOURCE_DIR}/docs/dff.1 > ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz
                     COMMENT "Building dff.1.gz")
  add_custom_target(manpage ALL DEPENDS ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz)
# Install man page
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz
          DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/share/man/man1
          PERMISSIONS OWNER_READ GROUP_READ WORLD_READ RENAME dff.1.gz)
# Install docs and licenses
  install(FILES README COPYRIGHT LICENSE LICENSE-THIRDPARTY
          DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/share/doc/${CMAKE_PROJECT_NAME}-${CPACK_PACKAGE_VERSION_MAJOR}.${CPACK_PACKAGE_VERSION_MINOR}.${CPACK_PACKAGE_VERSION_PATCH}
          PERMISSIONS OWNER_READ GROUP_READ WORLD_READ RENAME)
# Install binary  launcher, icons, shortcuts.
  #install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff
  #DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/bin
  #PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.png ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.xpm
  DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/share/pixmaps
  PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.desktop
  DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/share/applications
  PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)
endif(UNIX)

INCLUDE(CPack)
ENABLE_TESTING()
SUBDIRS(testsuite)

#### Deploying package file and DFF startup files
set(dff_scripts
  __init__.py
#  dff.py
#  dff-gui.py
)

#install_file(dff_launch ${dff_scripts})

# Override deployment of launcher to add proper Python binary prefix
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/dff.py ${CMAKE_CURRENT_BINARY_DIR}/dff.py)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/dff-gui.py ${CMAKE_CURRENT_BINARY_DIR}/dff-gui.py)

# Create launcher. Replace CMake variables in it, used after install.
#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ressources/linux_launcher.sh ${CMAKE_CURRENT_BINARY_DIR}/dff)

#### Subdirectories to recurse
add_subdirectory (dff)

if (WIN32)
	#
	FILE(COPY ${ICU_DYNLIB_PATH}/icuuc48.dll ${ICU_DYNLIB_PATH}/icudt48.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
	set (icu_dynlib
			icuuc48.dll
			icudt48.dll
		)
	install_file(icu ${icu_dynlib})
	if (FFMPEG_FOUND)
		FILE(COPY ${FFMPEG_ROOT}/bin/avcodec-54.dll ${FFMPEG_ROOT}/bin/avdevice-54.dll ${FFMPEG_ROOT}/bin/avfilter-3.dll ${FFMPEG_ROOT}/bin/avformat-54.dll ${FFMPEG_ROOT}/bin/avutil-51.dll ${FFMPEG_ROOT}/bin/postproc-52.dll ${FFMPEG_ROOT}/bin/swresample-0.dll ${FFMPEG_ROOT}/bin/swscale-2.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
		set (ffmpeg_dynlib
			avcodec-54.dll
			avdevice-54.dll
			avfilter-3.dll
			avformat-54.dll
			avutil-51.dll
			postproc-52.dll
			swresample-0.dll
			swscale-2.dll
			)
		install_file(ffmpeg ${ffmpeg_dynlib})
	endif (FFMPEG_FOUND)
	if (REGLOOKUP_PATH)
		message(STATUS "Reglookup/pyregfi path: ${REGLOOKUP_PATH}")
		file(COPY ${REGLOOKUP_PATH}/python/pyregfi DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
		add_subdirectory(pyregfi)
		file(COPY ${REGLOOKUP_PATH}/libiconv-2.dll ${REGLOOKUP_PATH}/libregfi.dll ${REGLOOKUP_PATH}/libtalloc.dll ${REGLOOKUP_PATH}/pthreadGC2.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
		set(reglookup_files
			libiconv-2.dll
			libregfi.dll
			libtalloc.dll
			pthreadGC2.dll
			)
		install_file(reglookup ${reglookup_files})
	else (REGLOOKUP_PATH)
		message(STATUS "Reglookup/pyregfi path not set")
	endif (REGLOOKUP_PATH)
endif (WIN32)

if (UNIX)
ADD_CUSTOM_COMMAND(
 	OUTPUT ${CMAKE_BINARY_DIR}/ctags
	COMMAND ctags --languages=+C++,+Python --exclude=[*.cxx,*wrap.h] --recurse=yes ${CMAKE_SOURCE_DIR}
	WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
)

ADD_CUSTOM_TARGET(tags DEPENDS ${CMAKE_BINARY_DIR}/ctags)
endif (UNIX)
