# License: Apache 2.0. See LICENSE file in root directory.
# Copyright(c) 2019 Intel Corporation. All Rights Reserved.
#  minimum required cmake version: 3.1.0
cmake_minimum_required(VERSION 3.1.0)

project(RealsenseExamplesAlignCapture)

add_executable(rs-align-capture rs-align-capture.cpp)
set_property(TARGET rs-align-capture PROPERTY CXX_STANDARD 11)
target_link_libraries(rs-align-capture ${DEPENDENCIES})
include_directories(rs-align-capture ../../common ../../third-party ../../third-party/tclap/include)
set_target_properties (rs-align-capture PROPERTIES FOLDER "Examples")
install(TARGETS rs-align-capture RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR})
