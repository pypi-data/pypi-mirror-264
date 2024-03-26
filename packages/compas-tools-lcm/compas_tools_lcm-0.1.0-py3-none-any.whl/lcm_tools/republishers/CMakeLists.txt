cmake_minimum_required(VERSION 3.15)

if(CMAKE_BUILD_TYPE STREQUAL DEBUG)
    project(republishers)
else()
    project(${POD_NAME}_republishers)
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

    # calibrated_ahrs
    pods_install_python_script(${TARG_NAME}_ahrs calibrated_ahrs/corrected_ahrs.py)

    # lass_republisher
    pods_install_python_packages(lass_republisher/lass_republisher_oi)
    pods_install_python_packages(lass_republisher/lass_republisher_bot_core)
    pods_install_python_script(${TARG_NAME}_lass_ins lass_republisher/ins_republisher.py)
    pods_install_python_script(${TARG_NAME}_prosilica lass_republisher/prosilica_republisher.py)

endif()
##################################################

# Install config files
set(CONFIG_FILES
config/config_ahrs_calibration.json
)
install(FILES ${CONFIG_FILES} DESTINATION config)