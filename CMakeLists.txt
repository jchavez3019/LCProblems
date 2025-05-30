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

# Collect only problem subdirectories that have a CMakeLists.txt
file(GLOB cmake_files RELATIVE ${CMAKE_SOURCE_DIR}/problems ${CMAKE_SOURCE_DIR}/problems/*/CMakeLists.txt)

# Add each problem as a subdirectory
foreach(cmake_file ${cmake_files})
    # Get the directory name (e.g., "problem1/CMakeLists.txt" -> "problem1")
    get_filename_component(problem_dir ${cmake_file} DIRECTORY)
    add_subdirectory(problems/${problem_dir})
    message("Compiling problem: ${problem_dir}")
endforeach()