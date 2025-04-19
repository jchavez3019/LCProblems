cmake_minimum_required(VERSION 3.26)
project(LeetCode)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

find_package(Python COMPONENTS Interpreter Development)

message("Python_FOUND:${Python_FOUND}")
message("Python_VERSION:${Python_VERSION}")
message("Python_Development_FOUND:${Python_Development_FOUND}")
message("Python_LIBRARIES:${Python_LIBRARIES}")


# Collect all problem subdirectories
file(GLOB problem_dirs RELATIVE ${CMAKE_SOURCE_DIR}/problems ${CMAKE_SOURCE_DIR}/problems/*)

# Add each problem as a subdirectory
foreach(problem ${problem_dirs})
    if(IS_DIRECTORY ${CMAKE_SOURCE_DIR}/problems/${problem})
        add_subdirectory(problems/${problem})
    endif()
endforeach()
