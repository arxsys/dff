# - Find EWF
# This module finds an installed EWF.  It sets the following variables:
#  EWF_FOUND - set to true if EWF is found
#  EWF_LIBRARY - dynamic libraries for aff
#  EWF_INCLUDE_DIR - the path to the include files
#  EWF_VERSION   - the version number of the aff library
#

SET(EWF_FOUND FALSE)

FIND_LIBRARY(EWF_LIBRARY ewf)

IF (EWF_LIBRARY)
   FIND_FILE(EWF_INCLUDE_FILE libewf.h)
   IF (EWF_INCLUDE_FILE)
	  IF (CMAKE_GENERATOR MATCHES "Visual Studio")
		STRING(REPLACE "libewf.lib" "" EWF_DYN_LIB_PATH "${EWF_LIBRARY}")
      ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
      STRING(REPLACE "libewf.h" "" EWF_INCLUDE_DIR "${EWF_INCLUDE_FILE}")
      #message(STATUS "LIBEWF include path found ${EWF_INCLUDE_DIR}")
	  #message(STATUS "${EWF_DYN_LIB_PATH}")
  	  IF (CMAKE_GENERATOR MATCHES "Visual Studio")
	  	  SET (EWF_DYN_LIBRARIES ${EWF_DYN_LIB_PATH}/libewf.dll;${EWF_DYN_LIB_PATH}/zlib.dll)
	  	  FILE(COPY ${EWF_DYN_LIBRARIES} DESTINATION ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/Debug/)
      ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
	  #message(STATUS "${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}")
      FILE(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/ewfversion.c
      "#ifdef WIN32
			#if _MSC_VER >= 1600
				#include <stdint.h>
			#else
				#include <wstdint.h>
			#endif
	   #endif
	   #include <libewf.h>
       #include <stdio.h>
       int main()
       {
	 const char*   version;

	 version = libewf_get_version();
  	 printf(\"%s\", version);
	 return 1;
       }")
     IF (UNIX)
	   SET(COMP_EWF_DEF "-DHAVE_STDINT_H -DHAVE_INTTYPES_H -D_LIBEWF_TYPES_H_INTEGERS")
	 ENDIF (UNIX)
      TRY_RUN(EWF_RUN_RESULT EWF_COMP_RESULT
	${CMAKE_BINARY_DIR}
      	${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/ewfversion.c
	CMAKE_FLAGS -DINCLUDE_DIRECTORIES:STRING=${EWF_INCLUDE_DIR} -DLINK_LIBRARIES:STRING=${EWF_LIBRARY}
	COMPILE_DEFINITIONS ${COMP_EWF_DEF}
	COMPILE_OUTPUT_VARIABLE COMP_OUTPUT
	RUN_OUTPUT_VARIABLE RUN_OUTPUT)
    IF (EWF_COMP_RESULT)
      	IF (EWF_RUN_RESULT)
			SET(EWF_FOUND TRUE)
			SET(EWF_VERSION ${RUN_OUTPUT})
		ENDIF (EWF_RUN_RESULT)
    ELSE (EWF_COMP_RESULT)
      	message(STATUS "${COMP_OUTPUT}")
    ENDIF (EWF_COMP_RESULT)
   ENDIF (EWF_INCLUDE_FILE)
ENDIF (EWF_LIBRARY)