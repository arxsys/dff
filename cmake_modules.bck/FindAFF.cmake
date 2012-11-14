# - Find AFF
# This module finds an installed AFF.  It sets the following variables:
#  AFF_FOUND - set to true if AFF is found
#  AFF_LIBRARY - dynamic libraries for aff
#  AFF_INCLUDE_DIR - the path to the include files
#  AFF_VERSION   - the version number of the aff library
#

SET(AFF_FOUND FALSE)

FIND_LIBRARY(AFF_LIBRARY afflib)

IF (AFF_LIBRARY)
   FIND_PATH(AFF_INCLUDE_DIR afflib)
   IF (AFF_INCLUDE_DIR)
   	  IF (CMAKE_GENERATOR MATCHES "Visual Studio")
		STRING(REPLACE "afflib.lib" "" AFF_DYN_LIB_PATH "${AFF_LIBRARY}")
		SET(AFF_LIBRARY Ws2_32;${AFF_DYN_LIB_PATH}/afflib.lib;${AFF_DYN_LIB_PATH}/libeay32.lib;${AFF_DYN_LIB_PATH}/ssleay32.lib;${AFF_DYN_LIB_PATH}/zlib.lib)
		SET(AFF_DYN_LIBRARIES ${AFF_DYN_LIB_PATH}/afflib.dll;${AFF_DYN_LIB_PATH}/zlib.dll)
		FILE(COPY ${AFF_DYN_LIBRARIES} DESTINATION ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/Debug/)
	  ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
      FILE(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/affversion.c
      "#include <afflib/afflib.h>
       #include <stdio.h>
       int main()
       {
	 const char*   version;

  	 version = af_version();
  	 printf(\"%s\", version);
	 return 1;
       }")
       IF (UNIX)
       	  SET (COMP_DEF "-DHAVE_INTTYPES_H")
       ENDIF (UNIX)
      TRY_RUN(AFF_RUN_RESULT AFF_COMP_RESULT
	${CMAKE_BINARY_DIR}
     	${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/affversion.c
	CMAKE_FLAGS -DINCLUDE_DIRECTORIES:STRING=${AFF_INCLUDE_DIR} "-DLINK_LIBRARIES:STRING=${AFF_LIBRARY}"
	COMPILE_DEFINITIONS ${COMP_DEF}
	COMPILE_OUTPUT_VARIABLE COMP_OUTPUT
	RUN_OUTPUT_VARIABLE RUN_OUTPUT)
      #message(STATUS ${AFF_COMP_RESULT})
      #message(STATUS ${COMP_OUTPUT})
      #message(STATUS ${RUN_OUPUT})
      #message(STATUS ${AFF_RUN_RESULT})
      IF (AFF_COMP_RESULT)
      	 IF (AFF_RUN_RESULT)
	    set(AFF_FOUND TRUE)
	    SET(AFF_VERSION ${RUN_OUTPUT})
	    SET(AFFVERSION ${AFF_VERSION})
     	    STRING(REGEX REPLACE "^([0-9]+)\\.[0-9]+\\.[0-9]+.*" "\\1" AFF_VERSION_MAJOR "${AFFVERSION}")
    	    STRING(REGEX REPLACE "^[0-9]+\\.([0-9])+\\.[0-9]+.*" "\\1" AFF_VERSION_MINOR "${AFFVERSION}")
    	    STRING(REGEX REPLACE "^[0-9]+\\.[0-9]+\\.([0-9]+).*" "\\1" AFF_VERSION_PATCH "${AFFVERSION}")
	 ENDIF (AFF_RUN_RESULT)
      ELSE (AFF_COMP_RESULT)
      	   message(STATUS "${COMP_OUTPUT}")
      ENDIF (AFF_COMP_RESULT)
   ENDIF (AFF_INCLUDE_DIR)
ENDIF (AFF_LIBRARY)