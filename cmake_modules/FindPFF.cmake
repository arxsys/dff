# - Find PFF
# This module finds an installed PFF.  It sets the following variables:
#  PFF_FOUND - set to true if PFF is found
#  PFF_LIBRARY - dynamic libraries for aff
#  PFF_INCLUDE_DIR - the path to the include files
#  PFF_VERSION   - the version number of the aff library
#

SET(PFF_FOUND FALSE)

FIND_LIBRARY(PFF_LIBRARY pff)

IF (PFF_LIBRARY)
   FIND_FILE(PFF_INCLUDE_FILE libpff.h)
   IF (PFF_INCLUDE_FILE)
	  IF (CMAKE_GENERATOR MATCHES "Visual Studio")
		STRING(REPLACE "libpff.h" "" PFF_INCLUDE_DIR "${PFF_INCLUDE_FILE}")
		STRING(REPLACE "libpff.lib" "" PFF_DYN_LIB_PATH "${PFF_LIBRARY}")
		SET (PFF_DYN_LIBRARIES ${PFF_DYN_LIB_PATH}/libpff.dll)
		FILE(COPY ${BFIO_DYN_LIBRARIES} ${PFF_DYN_LIBRARIES} DESTINATION ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/Debug/)
	  ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
      FILE(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/pffversion.c
      "#ifdef WIN32
			#if _MSC_VER >= 1600
				#include <stdint.h>
			#else
				#include <wstdint.h>
			#endif
	   #endif
	   #include <libpff.h>
       #include <stdio.h>
       int main()
       {
	 const char*   version;

	 version = libpff_get_version();
  	 printf(\"%s\", version);
	 return 1;
       }")
     IF (UNIX)
	   SET(COMP_PFF_DEF "-DHAVE_STDINT_H -DHAVE_INTTYPES_H -D_LIBPFF_TYPES_H_INTEGERS")
	 ENDIF (UNIX)
      TRY_RUN(PFF_RUN_RESULT PFF_COMP_RESULT
	${CMAKE_BINARY_DIR}
      	${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/pffversion.c
	CMAKE_FLAGS -DINCLUDE_DIRECTORIES:STRING=${PFF_INCLUDE_DIR} -DLINK_LIBRARIES:STRING=${PFF_LIBRARY}
	COMPILE_DEFINITIONS ${COMP_PFF_DEF}
	COMPILE_OUTPUT_VARIABLE COMP_OUTPUT
	RUN_OUTPUT_VARIABLE RUN_OUTPUT)
      IF (PFF_COMP_RESULT)
      	 IF (PFF_RUN_RESULT)
	    SET(PFF_FOUND TRUE)
	    SET(PFF_VERSION ${RUN_OUTPUT})
	 ENDIF (PFF_RUN_RESULT)
      ELSE (PFF_COMP_RESULT)
      	   message(STATUS "${COMP_OUTPUT}")
      ENDIF (PFF_COMP_RESULT)
   ENDIF (PFF_INCLUDE_FILE)
ENDIF (PFF_LIBRARY)