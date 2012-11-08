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
		FILE(COPY ${TRE_DYN_LIBRARIES} DESTINATION ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/Debug/)
	  ENDIF (CMAKE_GENERATOR MATCHES "Visual Studio")
      FILE(WRITE ${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/treconfig.c
      "#ifdef _MSC_VER
      	   typedef int size_t;
       #endif
	   #include \"tre/tre.h\"
       #include <stdio.h>
       int main()
       {
	 char*   version;
	 int	 approx;
	 int	 wchar;
	 int	 mbs;

	 tre_config(TRE_CONFIG_VERSION, &version);
	 tre_config(TRE_CONFIG_APPROX, &approx);
	 tre_config(TRE_CONFIG_WCHAR, &wchar);
	 tre_config(TRE_CONFIG_MULTIBYTE, &mbs);
	 printf(\"%s--%d--%d--%d\", version, approx, wchar, mbs);
	 return 1;
       }")
       IF (WIN32)
       	  SET (COMP_TRE_DEF "-DTRE_EXPORTS -DHAVE_CONFIG_H")
       ENDIF (WIN32)
      TRY_RUN(TRE_RUN_RESULT TRE_COMP_RESULT
	${CMAKE_BINARY_DIR}
      	${CMAKE_BINARY_DIR}${CMAKE_FILES_DIRECTORY}/CMakeTmp/treconfig.c
	CMAKE_FLAGS -DINCLUDE_DIRECTORIES:STRING=${TRE_INCLUDE_DIR} -DLINK_LIBRARIES:STRING=${TRE_LIBRARY}
	COMPILE_DEFINITIONS ${COMP_DEF}
	COMPILE_OUTPUT_VARIABLE COMP_OUTPUT
	RUN_OUTPUT_VARIABLE RUN_OUTPUT)
      IF (TRE_COMP_RESULT)
      	 IF (TRE_RUN_RESULT)
       	    STRING(REGEX REPLACE "([0-9]+\\.[0-9]+\\.[0-9]+)--[0-1]+--[0-1]+--[0-1]+.*" "\\1" TRE_VERSION "${RUN_OUTPUT}")
       	    STRING(REGEX REPLACE "[0-9]+\\.[0-9]+\\.[0-9]+--([0-1]+)--[0-1]+--[0-1]+.*" "\\1" TRE_HAVE_APPROX "${RUN_OUTPUT}")
       	    STRING(REGEX REPLACE "[0-9]+\\.[0-9]+\\.[0-9]+--[0-1]+--([0-1]+)--[0-1]+.*" "\\1" TRE_HAVE_WCHAR "${RUN_OUTPUT}")
       	    STRING(REGEX REPLACE "[0-9]+\\.[0-9]+\\.[0-9]+--[0-1]+--[0-1]+--([0-1]+).*" "\\1" TRE_HAVE_MULTIBYTE "${RUN_OUTPUT}")
	    SET(TRE_FOUND TRUE)
	 ENDIF (TRE_RUN_RESULT)
      ELSE (TRE_COMP_RESULT)
      	   message(STATUS "${COMP_OUTPUT}")
      ENDIF (TRE_COMP_RESULT)
   ENDIF (TRE_INCLUDE_PATH)
ENDIF (TRE_LIBRARY)