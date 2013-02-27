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

project (dff)

#### Basic Cmake definitions
cmake_minimum_required (VERSION 2.6)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake_modules/")

## Swig
find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

STRING (COMPARE LESS "${SWIG_VERSION}" "2.0.7" SWIGOK)

if (${SWIGOK})
  MESSAGE(FATAL_ERROR "Need SWIG version >= 2.0.7 (current version is ${SWIG_VERSION})")
endif (${SWIGOK})

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
    set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -DSWIGWORDSIZE32)
  else()
    set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} -DSWIGWORDSIZE64)
  endif()
  set( HAVE_64_BIT 1 )
endif( "${CMAKE_SIZEOF_VOID_P}" EQUAL 4 )

# Set installation mode, include all items (*.py, ...) Default is development mode
option(DEVELOP "Start installation mode ?" OFF)
IF(DEVELOP)
  message("          /==========================\\")
  message("          | Running development mode |")
  message("          \\==========================/")
ENDIF(DEVELOP)

IF (NOT ${CMAKE_BINARY_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR})
  SET(DEDICATED_BUILD_DIR 1)
  message(STATUS "Building project in dedicated build directory : ${CMAKE_BINARY_DIR}")
ENDIF (NOT ${CMAKE_BINARY_DIR} STREQUAL ${CMAKE_CURRENT_SOURCE_DIR})

option(BUILD_UNSUPPORTED "Build unsupported modules ?" OFF)

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

if (ICU_DEP_PATH)
  if (WIN32)
    if (HAVE_64_BIT)
      set(ICU_PATH_SUFFIX "64")
    else()
      set(ICU_PATH_SUFFIX "")
    endif()
    set(ICU_INCLUDE_PATH "${ICU_DEP_PATH}/include")
    set(ICU_LIBRARIES_PATH "${ICU_DEP_PATH}/lib${ICU_PATH_SUFFIX}")
    set(ICU_DYNLIB_PATH "${ICU_DEP_PATH}/bin${ICU_PATH_SUFFIX}")
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

#message("${CMAKE_INSTALL_ORIG_PREFIX}")

## Main purpose of this macro if to copy Python files at install.
# It also deploys .py files in build directory if there is one.
LIST(APPEND PYC_FILES "")
set_property(GLOBAL PROPERTY PYC_FILES)
FILE(WRITE "${CMAKE_BINARY_DIR}/installed_files.log" "")

FILE(APPEND "${CMAKE_BINARY_DIR}/targets" "")

LIST(APPEND CUSTOM_DEPENDENCIES "")
set_property(GLOBAL PROPERTY CUSTOM_DEPENDENCIES)

LIST(APPEND CREATED_TARGETS "")
set_property(GLOBAL PROPERTY CREATED_TARGET)

if (WIN32)
  set(INSTALL_FILE_DESTINATION "dff")
elseif (UNIX)
  set(INSTALL_FILE_DESTINATION ${PYTHON_SITE_PACKAGES_PATH})
endif (WIN32)

macro(log text)
  if (LOG_BUILD)
    message(${text})
  endif (LOG_BUILD)
endmacro(log text)

macro(SPLIT_PATH_FILE_EXTENSION item)
  file(TO_CMAKE_PATH ${item} path)
  string(FIND "${path}" "/" slash_rpos REVERSE)
  if (slash_rpos EQUAL -1)
    set(__FILE__ ${path})
    set(__PATH__ "")
  else()
    math(EXPR slash_rpos "${slash_rpos} + 1")
    string(SUBSTRING ${path} ${slash_rpos} -1 __FILE__)
    string(SUBSTRING ${path} 0 ${slash_rpos} __PATH__)
  endif()
  string(FIND "${__FILE__}" "." dot_rpos REVERSE)
  if (dot_rpos EQUAL -1)
    set(__EXTENSION__ "")
  else()
    math(EXPR dot_rpos "${dot_rpos} + 1")
    string(SUBSTRING ${__FILE__} ${dot_rpos} -1 __EXTENSION__)
  endif()
endmacro()

#split_path_file_extension("/usr/lib/pouet.py")
#message("path: ${__PATH__} -- file: ${__FILE__} -- extension: ${__EXTENSION__}")

#split_path_file_extension("/usr\\\\lib\\\\pouet.py")
#message("path: ${__PATH__} -- file: ${__FILE__} -- extension: ${__EXTENSION__}")

#split_path_file_extension("/usr/lib/pouet")
#message("path: ${__PATH__} -- file: ${__FILE__} -- extension: ${__EXTENSION__}")

#split_path_file_extension("pouet")
#message("path: ${__PATH__} -- file: ${__FILE__} -- extension: ${__EXTENSION__}")

#split_path_file_extension("pouet.py")
#message("path: ${__PATH__} -- file: ${__FILE__} -- extension: ${__EXTENSION__}")


macro(DFF_CPP_CONTEXT_INIT library_name)
  INCLUDE_DIRECTORIES(../include)

  list(APPEND arguments CPP_FILES SWIG_FILE LINK_LIBRARIES SWIG_FLAGS DEFINITIONS EXTRA_FILES INCLUDE_DIRS INCLUDE_FILES NO_SWIG_LIB_PREFIX)
  set(arglist "${ARGN}")
  foreach(argument ${arguments})
    list(REMOVE_ITEM arguments ${argument})
    string(FIND "${arglist}" ${argument} start_pos)
    if (NOT ${start_pos} EQUAL -1)
      string(LENGTH "${arglist}" end_pos)
      foreach(delim_arg ${arguments})
	string(FIND "${arglist}" ${delim_arg} idx)
	if (idx GREATER start_pos AND idx LESS end_pos)
	  set(end_pos ${idx})
	endif()
      endforeach()
      math(EXPR length "${end_pos} - ${start_pos}")
      string(SUBSTRING "${arglist}" ${start_pos} ${length} extracted)
      string(REPLACE "${extracted}" "" arglist "${arglist}")
      string(LENGTH "${argument}" val_start)
      string(SUBSTRING "${extracted}" ${val_start} -1 __${argument}__)
      string(STRIP "${__${argument}__}" __${argument}__)
      log("Values for ${argument} : ${__${argument}__}")
    else ()
      list(REMOVE_ITEM arguments ${argument})
    endif ()
  endforeach()
endmacro()


macro(VS_LIBRARY_PROPERTIES library_name extension)
  set_target_properties (${library_name} PROPERTIES
    SUFFIX "${extension}"
    RUNTIME_OUTPUT_DIRECTORY_RELEASE "${CMAKE_CURRENT_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_DEBUG "${CMAKE_CURRENT_BINARY_DIR}"
    RUNTIME_OUTPUT_DIRECTORY_RELWITHDEBINFO "${CMAKE_CURRENT_BINARY_DIR}"
    )
endmacro()

macro(DFF_COMPILE_HEAD)
  # setting default context when compiling CPP
  dff_cpp_context_init(library_name ${ARGN})


  # getting target from path
  path_to_target()

  #include(${SWIG_USE_FILE})
  include_directories(${PYTHON_INCLUDE_PATH})
  include_directories(${CMAKE_CURRENT_SOURCE_DIR})
  include_directories(${CMAKE_HOME_DIRECTORY}/dff/api/include)

  if (NOT "${__INCLUDE_DIRS__}" STREQUAL "")
    include_directories(${__INCLUDE_DIRS__})
  endif ()
  if (NOT "${__INCLUDE__}" STREQUAL "")
    include("${__INCLUDE__}")
  endif()

  if (NOT "${__DEFINITIONS__}" STREQUAL "")
    add_definitions(${__DEFINITIONS__})
  endif()

  if (NOT "${__SWIG_FLAGS__}" STREQUAL "")
    set(CMAKE_SWIG_FLAGS ${CMAKE_SWIG_FLAGS} ${__SWIG_FLAGS__})
  endif()
endmacro()

# Following macro is used to generate DFF's API and Python bindings libraries
#
# First argument to provide is the name of the library to create then
# 
# Mandatory arguments are :
#  - CPP_FILES followed by .cpp files
#  - SWIG_FILE followed by .i files
#
# Optional arguments are :
#  - LINK_LIBRARIES followed by needed library
#  - SWIG_FLAGS followed by needed flags
#  - DEFINITIONS followed by needed definitions
#  - EXTRA_FILES followed by extra files you need to install
#  - INCLUDE_DIRS followed by absolute path to include directories
#    By default following include dirs are managed 
#      * ${CMAKE_CURRENT_SOURCE_DIR}
#      * ${CMAKE_HOME_DIRECTORY}/dff/api/include
#      * ${PYTHON_INCLUDE_PATH}
#  - INCLUDE followed by files to include
#    By Default ${SWIG_USE_FILE} are included
#
# Ex: to create library foo which needs to be linked with
#     library 'bar'
#
# DFF_CPP_API(foo 
#   CPP_FILES foo.cpp 
#   SWIG_FILE libfoo.i
#   LINK_LIBRARIES bar
#   DEFINITIONS -D__STDC_LIMIT_MACROS
#   SWIG_FLAGS -threads -fvirtual -fastdispatch
#   EXTRA_FILES __init__.py
#   )
macro(DFF_CPP_API library_name)
  # Setting default context to compile cpp / swig libraries
  dff_compile_head(${ARGN})

  # General purpose DFF's library generation
  add_library(${library_name} SHARED ${__CPP_FILES__})
  target_link_libraries(${library_name} ${__LINK_LIBRARIES__})
  if ( CMAKE_GENERATOR MATCHES "Visual Studio")
    vs_library_properties(${library_name} ".dll")
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${rpath}/${library_name}.dll\n")
    install(TARGETS ${library_name} DESTINATION ${INSTALL_FILE_DESTINATION}/${rpath})
  elseif (UNIX)
    set_target_properties(${library_name} PROPERTIES
      LIBRARY_OUTPUT_DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/../"
      )
    install(TARGETS ${library_name} DESTINATION "${CMAKE_INSTALL_ORIG_PREFIX}/lib/dff/")    
  endif ()

  # Python's binding library generation
  if (${__NO_SWIG_LIB_PREFIX__})
    set(swig_lib_name "${library_name}")
  else()
    set(swig_lib_name "lib${library_name}")
  endif()
  set_source_files_properties(${__SWIG_FILE__} PROPERTIES CPLUSPLUS ON)
  swig_add_module(${swig_lib_name} python ${__SWIG_FILE__})
  swig_link_libraries(${swig_lib_name} ${PYTHON_LIBRARIES} ${library_name})
  if ( CMAKE_GENERATOR MATCHES "Visual Studio")
    vs_library_properties(${SWIG_MODULE_${swig_lib_name}_REAL_NAME} ".pyd")
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${rpath}/${SWIG_MODULE_${swig_lib_name}_REAL_NAME}.pyd\n")
    install (TARGETS ${SWIG_MODULE_${swig_lib_name}_REAL_NAME} DESTINATION ${INSTALL_FILE_DESTINATION}/${rpath})
  elseif (UNIX)
    set_target_properties(${SWIG_MODULE_${swig_lib_name}_REAL_NAME} PROPERTIES
      SKIP_BUILD_RPATH FALSE
      BUILD_WITH_INSTALL_RPATH FALSE
      INSTALL_RPATH "${CMAKE_INSTALL_ORIG_PREFIX}/lib/dff/"
      INSTALL_RPATH_USE_LINK_PATH TRUE
      )
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${rpath}/${SWIG_MODULE_${swig_lib_name}_REAL_NAME}.so\n")
    install(TARGETS ${SWIG_MODULE_${swig_lib_name}_REAL_NAME} DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${rpath})
  endif()

  # Final rules
  install_file("${swig_lib_name}.py" ${__EXTRA_FILES__})
  add_dependencies(${current_target} ${library_name} ${SWIG_MODULE_${library_name}_REAL_NAME})
endmacro()

macro(DFF_CPP_MODULE library_name)
  # Setting default context to compile cpp / swig libraries
  dff_compile_head(${ARGN})

  set_source_files_properties(${__SWIG_FILE__} PROPERTIES CPLUSPLUS ON)
  swig_add_module(${library_name} python ${__SWIG_FILE__} ${__CPP_FILES__})
  swig_link_libraries(${library_name} ${PYTHON_LIBRARIES} ${__LINK_LIBRARIES__})

  if ( CMAKE_GENERATOR MATCHES "Visual Studio")
    vs_library_properties(${SWIG_MODULE_${library_name}_REAL_NAME} ".pyd")
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${rpath}/${SWIG_MODULE_${library_name}_REAL_NAME}.pyd\n")
    install (TARGETS ${SWIG_MODULE_${library_name}_REAL_NAME} DESTINATION ${INSTALL_FILE_DESTINATION}/${rpath})
  elseif (UNIX)
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${rpath}/${SWIG_MODULE_${library_name}_REAL_NAME}.so\n")
    install(TARGETS ${SWIG_MODULE_${library_name}_REAL_NAME} DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${rpath})
  endif ( CMAKE_GENERATOR MATCHES "Visual Studio" )

  install_file("${library_name}.py" ${__EXTRA_FILES__})
  add_dependencies(${current_target} ${SWIG_MODULE_${library_name}_REAL_NAME})
endmacro()

macro(PATH_TO_TARGET)
  # Obtain relative path
  file(RELATIVE_PATH rpath ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
  # Replace all '/' with '.' resulting variable becomes current_target 
  string(REPLACE "/" "." current_target "${rpath}")
  # From current_target, extract the parent_target
  # parent_target completion depends on all its sub current_target
  string(FIND "${current_target}" "." dot_rpos REVERSE)
  if (${dot_rpos} EQUAL -1)
    set(parent_target "ALL")
  else (${dot_rpos} EQUAL -1)
    string(SUBSTRING ${current_target} 0 ${dot_rpos} parent_target)
  endif (${dot_rpos} EQUAL -1)
  log("[CONTEXT] :
  current target : ${current_target}
  parent target  : ${parent_target}
  relative path  : ${rpath}")
endmacro()

macro(install_rule file)
  if (NOT DEVELOP)
	split_path_file_extension(${file})
	if (NOT ${__PATH__} STREQUAL "")
		file(COPY ${file} DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
	endif()
    if("${rpath}" STREQUAL "")
      set(ifile "${__FILE__}")
    else("${rpath}" STREQUAL "")
      set(ifile "${rpath}/${__FILE__}")
    endif("${rpath}" STREQUAL "")
    file(APPEND "${CMAKE_BINARY_DIR}/installed_files.log" "${ifile}\n")
    if (${ifile} MATCHES "^.*\\.py$")
      string(REPLACE "\\" "\\\\" pyc_file "${ifile}")
      string(REPLACE "/" "\\\\" pyc_file "${pyc_file}")
      get_property(pyc_list GLOBAL PROPERTY PYC_FILES)
      list(APPEND pyc_list "${pyc_file}c")
      set_property(GLOBAL PROPERTY PYC_FILES ${pyc_list})
    endif (${ifile} MATCHES "^.*\\.py$")
	log("    install rule : ${CMAKE_CURRENT_BINARY_DIR}/${__FILE__} DESTINATION ${INSTALL_FILE_DESTINATION}/${rpath}")
	install(FILES ${CMAKE_CURRENT_BINARY_DIR}/${__FILE__} DESTINATION ${INSTALL_FILE_DESTINATION}/${rpath})
  endif (NOT DEVELOP)
endmacro()

macro(install_file)
  # Create empty strings which will contain all commands for the resulting current_target
  set(cmds "")
  path_to_target()
  # this loop iter on all files provided in ${ARGN} :
  #   * In install mode (default)
  #     - generate install rules
  #     - For windows targeted platfrom, generate all .py to .pyc to remove
  #       pyc files during desinstallation
  #   * all mode with build_dir != src_dir
  #     - create 'copy if different' command for each .py
  foreach(file ${ARGV})
    install_rule(${file})
    if (DEDICATED_BUILD_DIR)
      #message("Copying ${CMAKE_CURRENT_SOURCE_DIR}/${file} in ${CMAKE_CURRENT_BINARY_DIR}")
      # SWIG generated files are already present in CMAKE_CURRENT_BINARY_DIR
      if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
	if (cmds)
	  set(cmds ${cmds} &&)
	endif (cmds)
	set(cmds ${cmds} ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file})
      endif(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
    endif (DEDICATED_BUILD_DIR)
  endforeach(file ${ARGN})
  add_custom_target(${current_target} ALL ${cmds})
  set_target_properties(${current_target} PROPERTIES CREATED "true")
  get_property(created_targets GLOBAL PROPERTY CREATED_TARGETS)
  list(APPEND created_targets "${current_target}")
  set_property(GLOBAL PROPERTY CREATED_TARGETS ${created_targets})
  log("\n")
endmacro(install_file)


## Macro to copy lib at install
macro(install_lib target_name)
  file(RELATIVE_PATH rpath ${CMAKE_BINARY_DIR} ${CMAKE_CURRENT_BINARY_DIR})
  string(REPLACE "/" "." current_target ${rpath})
  # From current_target, extract the parent_target
  # parent_target completion depends on all its sub current_target
  string(FIND "${current_target}" "." dot_rpos REVERSE)
  if (${dot_rpos} EQUAL -1)
    set(parent_target "ALL")
  else (${dot_rpos} EQUAL -1)
    string(SUBSTRING ${current_target} 0 ${dot_rpos} parent_target)
  endif (${dot_rpos} EQUAL -1)
  log("[CONTEXT] :
  current target : ${current_target}
  parent target  : ${parent_target}
  relative path  : ${rpath}")

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
macro(gui_resources_files target_name)
  path_to_target()
  set(cmds "")
  foreach(file ${ARGV})
    string(FIND ${file} "." ext_pos REVERSE)
    math(EXPR ext_pos "${ext_pos} + 1")
    string(SUBSTRING ${file} ${ext_pos} -1 extension)
    if (extension STREQUAL "ui")
      string(REGEX REPLACE "^(.*)\\.ui$" "ui_\\1.py" PYUICFILE ${file})
      set(cmd ${PYTHON_QT4_UIC} -o ${CMAKE_CURRENT_BINARY_DIR}/${PYUICFILE} ${CMAKE_CURRENT_SOURCE_DIR}/${file})
      install_rule(${PYUICFILE})
    elseif (extension STREQUAL "qrc")
      string(REGEX REPLACE "^(.*)\\.qrc$" "\\1_rc.py" PY_QRC_FILE ${file})
      set(cmd ${PYTHON_QT4_RCC} ${CMAKE_CURRENT_SOURCE_DIR}/${file} -o ${CMAKE_CURRENT_BINARY_DIR}/${PY_QRC_FILE})
      install_rule(${PY_QRC_FILE})
    elseif (extension STREQUAL "py")
      if (DEDICATED_BUILD_DIR)
	if (EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
	  set(cmd ${CMAKE_COMMAND} -E copy_if_different ${CMAKE_CURRENT_SOURCE_DIR}/${file} ${CMAKE_CURRENT_BINARY_DIR}/${file})
	endif(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/${file})
      endif (DEDICATED_BUILD_DIR)
      install_rule(${file})
    endif ()
    if (cmds)
      set(cmds ${cmds} && ${cmd})
    else()
      set(cmds ${cmd})
    endif()
  endforeach()
  add_custom_target(${current_target} ALL ${cmds})
  set_target_properties(${current_target} PROPERTIES CREATED "true")
  get_property(created_targets GLOBAL PROPERTY CREATED_TARGETS)
  list(APPEND created_targets "${current_target}")
  set_property(GLOBAL PROPERTY CREATED_TARGETS ${created_targets})
endmacro()


# Override deployment of launcher to add proper Python binary prefix
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/dff.py ${CMAKE_CURRENT_BINARY_DIR}/dff.py)
configure_file(${CMAKE_CURRENT_SOURCE_DIR}/dff-gui.py ${CMAKE_CURRENT_BINARY_DIR}/dff-gui.py)

# Create launcher. Replace CMake variables in it, used after install.
#configure_file(${CMAKE_CURRENT_SOURCE_DIR}/ressources/linux_launcher.sh ${CMAKE_CURRENT_BINARY_DIR}/dff)

#### Subdirectories to recurse
add_subdirectory (dff)

if (WIN32)
  foreach (icu_dynlib ${ICU_DYN_LIBRARIES})
    install_rule(${icu_dynlib})
  endforeach()

  if (FFMPEG_FOUND)
    file(GLOB ffmpeg_dyn_libraries ${FFMPEG_ROOT}/bin/*.dll)
    foreach(ffmpeg_dynlib ${ffmpeg_dyn_libraries})
      install_rule(${ffmpeg_dynlib})
    endforeach()
  endif (FFMPEG_FOUND)

  if (REGLOOKUP_PATH)
    message(STATUS "Reglookup/pyregfi path: ${REGLOOKUP_PATH}")
    file(COPY ${REGLOOKUP_PATH}/python/pyregfi DESTINATION ${CMAKE_CURRENT_SOURCE_DIR})
    add_subdirectory(pyregfi)
    file(GLOB reglookup_dyn_libraries ${REGLOOKUP_PATH}/*.dll)
    foreach(reglookup_dynlib ${reglookup_dyn_libraries})
		install_rule(${reglookup_dynlib})
    endforeach()
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
SET(CPACK_PACKAGE_VERSION_PATCH "0")
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
  SET(CPACK_SET_DESTDIR "OFF")

  IF(CMAKE_CL_64)
	SET(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES64")
	SET(CPACK_NSIS_PACKAGE_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY} 64-bit")
	SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "${CPACK_PACKAGE_NAME} ${CPACK_PACKAGE_VERSION} 64-bit")
	SET(CPACK_NSIS_DISPLAY_NAME "Digital Forensics Framework 64-bit")
  ELSE(CMAKE_CL_64)
	SET(CPACK_NSIS_INSTALL_ROOT "$PROGRAMFILES")
	SET(CPACK_NSIS_PACKAGE_NAME "${CPACK_PACKAGE_INSTALL_DIRECTORY}")
	SET(CPACK_PACKAGE_INSTALL_REGISTRY_KEY "${CPACK_PACKAGE_NAME} ${CPACK_PACKAGE_VERSION}")
	SET(CPACK_NSIS_DISPLAY_NAME "Digital Forensics Framework")
  ENDIF(CMAKE_CL_64)
  
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
	DESTINATION ${CMAKE_PROJECT_NAME}
	PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff-gui.py
	DESTINATION ${CMAKE_PROJECT_NAME}
	PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
	RENAME dff-gui.pyw)
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.ico
    DESTINATION ${CMAKE_PROJECT_NAME}/ressources/)

# Install docs and licenses
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/README ${CMAKE_CURRENT_SOURCE_DIR}/COPYRIGHT ${CMAKE_CURRENT_SOURCE_DIR}/LICENSE ${CMAKE_CURRENT_SOURCE_DIR}/LICENSE-THIRDPARTY
          DESTINATION ${CMAKE_PROJECT_NAME}/
          PERMISSIONS OWNER_READ GROUP_READ WORLD_READ)

  SET(CPACK_MONOLITHIC_INSTALL "ON")
  
  SET(CPACK_PACKAGE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_BUNDLE_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\arxsys.bmp")
  SET(CPACK_NSIS_MUI_ICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
  SET(CPACK_NSIS_MUI_UNIICON "${CMAKE_CURRENT_SOURCE_DIR}\\\\ressources\\\\dff.ico")
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
	Var /GLOBAL py_hkcu_path
	Var /GLOBAL py_hklm_path

	StrCpy \\\$pypath \\\"\\\"
	StrCpy \\\$py_hkcu_path \\\"\\\"
	StrCpy \\\$py_hklm_path \\\"\\\"
	StrCpy \\\$pyqtpath \\\"\\\"
    
	\\\${If} \\\${RunningX64}
		SetRegView 64
	\\\${EndIf}
		
	ReadRegStr \\\$py_hkcu_path HKCU \\\"SOFTWARE\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
	ReadRegStr \\\$py_hklm_path HKLM \\\"SOFTWARE\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
	ReadRegStr \\\$pyqtpath HKLM \\\"SOFTWARE\\\\PyQt4\\\\Py2.7\\\\InstallPath\\\" \\\"\\\"
	\\\${If} \\\$py_hklm_path != \\\"\\\"
		StrCpy \\\$pypath \\\$py_hklm_path
	\\\${Else}
		StrCpy \\\$pypath \\\$py_hkcu_path
	\\\${EndIf}
	"
	)
	
  SET(NSIS_GET_64_BITS_PATHES
	"
	Var /GLOBAL pypath
	Var /GLOBAL pyqtpath

	StrCpy \\\$pypath \\\"\\\"
	StrCpy \\\$pyqtpath \\\"\\\"
	ReadRegStr \\\$pyqtpath HKLM \\\"SOFTWARE\\\\PyQt4\\\\Py2.7\\\" \\\"\\\"
	ReadRegStr \\\$pypath HKLM \\\"SOFTWARE\\\\Python\\\\PythonCore\\\\2.7\\\\InstallPath\\\" \\\"\\\"
	"
	)

  SET(NSIS_DEFAULT_LABELS
    "
	!include \\\"x64.nsh\\\"
	\\\${If} \\\${RunningX64}
		SetRegView 64
	\\\${EndIf}
	
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
		
	"
	)
	
	SET(CPACK_NSIS_EXTRA_INSTALL_COMMANDS       
	"
    SetOutPath \\\"$INSTDIR\\\\dff\\\"
	!include \\\"x64.nsh\\\"
	\\\${If} \\\${RunningX64}
	    CreateShortCut \\\"$DESKTOP\\\\DFF (64-bit shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\" 
		CreateShortCut \\\"$DESKTOP\\\\DFF (64-bit gui).lnk\\\" \\\"\\\$pypath\\\\pythonw.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
		CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework 64-bit\\\\DFF (shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
		CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework 64-bit\\\\DFF (gui).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
	\\\${Else}
		CreateShortCut \\\"$DESKTOP\\\\DFF (shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\" 
		CreateShortCut \\\"$DESKTOP\\\\DFF (gui).lnk\\\" \\\"\\\$pypath\\\\pythonw.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
		CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (shell).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff.py\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
		CreateShortCut \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (gui).lnk\\\" \\\"\\\$pypath\\\\python.exe\\\" \\\"\\\$\\\\\\\"$INSTDIR\\\\dff\\\\dff-gui.pyw\\\$\\\\\\\"\\\" \\\"$INSTDIR\\\\dff\\\\ressources\\\\dff.ico\\\"  
	\\\${EndIf}
    "
	)
	
#	# *.pyc files are not deleted by installer, because they are created at
#	# runtime. So, below, we force deletion of those files.
    get_property(pyc_list GLOBAL PROPERTY PYC_FILES)
    foreach (pyc_file ${pyc_list})
      set(CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS
	"${CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS}
	  Delete \\\"$INSTDIR\\\\dff\\\\${pyc_file}\\\""
	)
    endforeach (pyc_file ${pyc_list})
  
	SET(CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS
    "
	${CPACK_NSIS_EXTRA_UNINSTALL_COMMANDS}
	 Delete \\\"$DESKTOP\\\\DFF (shell).lnk\\\"
	 Delete \\\"$DESKTOP\\\\DFF (gui).lnk\\\"
	 Delete \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (shell).lnk\\\"
	 Delete \\\"$SMPROGRAMS\\\\Digital Forensics Framework\\\\DFF (gui).lnk\\\"
	"
	)
	
	
  if (WINALL)
    add_subdirectory (prerequisites)
    message(STATUS "python installer: ${PYTHON_INSTALLER}")
    message(STATUS "pyqt installer: ${PYQT_INSTALLER}")
    message(STATUS "vcredist installer: ${VCREDIST_INSTALLER}")
    message(STATUS "apsw installer: ${APSW_INSTALLER}")
    message(STATUS "numpy installer: ${NUMPY_INSTALLER}")
    message(STATUS "matplotlib installer: ${MATPLOTLIB_INSTALLER}")
    message(STATUS "PIL installer: ${PIL_INSTALLER}")
    IF(CMAKE_CL_64)
      SET(CPACK_SYSTEM_NAME "win64_all_in_one")
    ELSE(CMAKE_CL_64)
      SET(CPACK_SYSTEM_NAME "win32_all_in_one")
    ENDIF(CMAKE_CL_64)
	SET(CPACK_NSIS_FULL_INSTALL ${CPACK_NSIS_FULL_INSTALL}
	${NSIS_DEFAULT_LABELS}
	"
    MessageBox MB_YESNO \\\"Install ${PYTHON_INSTALLER} ? \\\" /SD IDYES IDNO InstPyQt
    ExecWait '\\\"msiexec\\\" /i \\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PYTHON_INSTALLER}\\\" /passive ALLUSERS=1'
    Goto InstPyQt
    InstPyQt:
        MessageBox MB_YESNO \\\"Install ${PYQT_INSTALLER} ? \\\" /SD IDYES IDNO InstAPSW
        ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PYQT_INSTALLER}\\\"'
        Goto InstAPSW
    InstAPSW:
	MessageBox MB_YESNO \\\"Install ${APSW_INSTALLER}? \\\" /SD IDYES IDNO InstPil
	ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${APSW_INSTALLER}\\\"'
	Goto InstPil
    InstPil:
	MessageBox MB_YESNO \\\"Install ${PIL_INSTALLER}? \\\" /SD IDYES IDNO InstVcredist
	ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${PIL_INSTALLER}\\\"'
	Goto InstVcredist
	")
    if (BUILD_UNSUPPORTED)
      set(CPACK_NSIS_FULL_INSTALL ${CPACK_NSIS_FULL_INSTALL}
	"
    InstVcredist:
	MessageBox MB_YESNO \\\"Install Microsoft Visual Studio DLL dependencies ? \\\" /SD IDYES IDNO InstNumpy
        ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${VCREDIST_INSTALLER}\\\" /q:a'
	Goto InstNumpy
    InstNumpy:
	MessageBox MB_YESNO \\\"Install ${NUMPY_INSTALLER}? \\\" /SD IDYES IDNO InstMatplotlib
	ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${NUMPY_INSTALLER}\\\"'
	Goto InstMatplotlib
    IntMatplotlib:
	MessageBox MB_YESNO \\\"Install ${MATPLOTLIB_INSTALLER}? \\\" /SD IDYES IDNO InstEnd
	ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${MATPLOTLIB_INSTALLER}\\\"'
	Goto InstEnd
	")
    else()
      set(CPACK_NSIS_FULL_INSTALL ${CPACK_NSIS_FULL_INSTALL}
	"
    InstVcredist:
	MessageBox MB_YESNO \\\"Install Microsoft Visual Studio DLL dependencies ? \\\" /SD IDYES IDNO InstEnd
        ExecWait '\\\"$INSTDIR\\\\dff\\\\Prerequisites\\\\${VCREDIST_INSTALLER}\\\" /q:a'
	Goto InstEnd
	")      
    endif()
          set(CPACK_NSIS_FULL_INSTALL ${CPACK_NSIS_FULL_INSTALL}
	    "
    InstEnd:
       RMDir /r \\\"$INSTDIR\\\\dff\\\\Prerequisites\\\"	
    " ${NSIS_GET_32_BITS_PATHES})
  else(WINALL)
	if (HAVE_64_BIT)
	else()
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
	endif()
  endif(WINALL)
  SET(CPACK_SOURCE_GENERATOR "ZIP")
  
  SET(CMAKE_INSTALL_PREFIX "")
  
ELSE(WIN32 AND NOT UNIX)
  SET(CPACK_SOURCE_GENERATOR "TGZ")
#  SET(CPACK_SOURCE_IGNORE_FILES "") 
  SET(CPACK_GENERATOR "DEB" "RPM")
ENDIF(WIN32 AND NOT UNIX)

# Debian deb dependencies
#  python${PYTHON_VERSION} (>=${PYTHON_VERSION}.0), python-qt4 (>= 4.4.0), python-magic (>= 4.26)
# RedHat rpm dependencies
#  python >= ${PYTHON_VERSION}.0, PyQt4 >= 4.4.0, python-magic >= 4.26


if (UNIX)
# Compress manpage
  add_custom_command(OUTPUT ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz
                     COMMAND ${GZIP_TOOL} -c ${CMAKE_CURRENT_SOURCE_DIR}/doc/man/dff.1 > ${CMAKE_CURRENT_BINARY_DIR}/dff.1.gz
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
  PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
  install(FILES ${CMAKE_CURRENT_SOURCE_DIR}/ressources/dff.desktop
  DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/share/applications
  PERMISSIONS OWNER_READ OWNER_WRITE GROUP_READ WORLD_READ)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
    DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/bin/
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    RENAME dff)
  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff-gui.py
    DESTINATION ${CMAKE_INSTALL_ORIG_PREFIX}/bin/
    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE
    RENAME dff-gui)
#else (UNIX)
#  install(FILES ${CMAKE_CURRENT_BINARY_DIR}/dff.py
#    DESTINATION ${PYTHON_SITE_PACKAGES_PATH}/${CMAKE_PROJECT_NAME}
#    PERMISSIONS OWNER_READ OWNER_WRITE OWNER_EXECUTE GROUP_READ GROUP_EXECUTE WORLD_READ WORLD_EXECUTE)
endif(UNIX)

INCLUDE(CPack)
ENABLE_TESTING()
SUBDIRS(testsuite)


function(CHECK_ORPHANED_PARENT_DEPENDENCIES target)
  set(dot_pos 0)
  set(tmp ${target})
  list(APPEND prefixes "")
  set(current_target ${target})
  while((NOT ${dot_pos} EQUAL -1) AND (NOT ${tmp} STREQUAL "dff"))
    string(FIND ${tmp} "." dot_pos REVERSE)
    string(SUBSTRING ${tmp} 0 ${dot_pos} tmp)
    list(APPEND prefixes ${tmp})
  endwhile()
  list(REVERSE prefixes)
  set(parent_target "")
  foreach(prefix ${prefixes})
    get_target_property(prop ${prefix} CREATED)
    if (NOT prop STREQUAL "true")
      log("Target <${prefix}> does not exist")
      add_custom_target("${prefix}" ALL DEPENDS ${parent_target})
      log("  custom target created with DEPENDS setted to ${parent_target}")
      set_target_properties(${prefix} PROPERTIES CREATED "true")
    endif()
    set(parent_target ${prefix})
  endforeach()
endfunction()

get_property(created_targets GLOBAL PROPERTY CREATED_TARGETS)
foreach(current_target ${created_targets})
  string(FIND ${current_target} "." dot_pos REVERSE)
  string(SUBSTRING ${current_target} 0 ${dot_pos} parent_target)
  log("Making build dependencies between ${current_target} and its parent ${parent_target}")
  if (NOT ${current_target} STREQUAL "dff")
    check_orphaned_parent_dependencies(${current_target})
    add_dependencies(${parent_target} ${current_target})
  endif()
endforeach()


log("
   ==========================================
   | .pyc files to be uninstalled with NSIS |
   ==========================================\n")
get_property(pyc_list GLOBAL PROPERTY PYC_FILES)
foreach (pyc_file ${pyc_list})
  log("${pyc_file}")
endforeach (pyc_file ${pyc_list})
