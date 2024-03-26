cmake_minimum_required(VERSION 3.15)

if(CMAKE_BUILD_TYPE STREQUAL DEBUG)
    project(logtools)
else()
    project(${POD_NAME}_logtools)
endif()

# Imports CMake addons from root folder to work with python
set(POD_NAME ${PROJECT_NAME})
include("${CMAKE_SOURCE_DIR}/cmake/pods.cmake")
include("${CMAKE_SOURCE_DIR}/cmake/venv.cmake")

# Sets target name
set(TARG_NAME
    "${GLOBAL_BINARY_PREFIX}${PROJECT_NAME}"
)

# If building standalone, install to ./build
if(CMAKE_BUILD_TYPE STREQUAL DEBUG)
set(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/build)
endif()

############## Python target #####################
set(PYTHON_TARGET ON)
# Install python scripts, if available
if (${PYTHON_TARGET})
    # First check if a virtual environment is active and install packages if so.
    if(DEFINED ENV{VIRTUAL_ENV})
        python_install_requirements()
    endif()

    # Install python scripts
    pods_install_python_script(${TARG_NAME}_log2pkl log2pkl/log2pkl.py)
    pods_install_python_script(${TARG_NAME}_img2log img2log/img2log.py)
    pods_install_python_script(${TARG_NAME}_imgt2img imgt2img/imgt2img.py)

endif()
##################################################

# Install config files -- Not needed for now
# set(CONFIG_FILES
# config/somefile.yaml
# )
# install(FILES ${CONFIG_FILES} DESTINATION config)