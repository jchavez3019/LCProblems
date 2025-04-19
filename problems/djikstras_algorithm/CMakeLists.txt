cmake_minimum_required(VERSION 3.26)

add_executable(djikstras_algorithm main.cpp)
#target_link_libraries(djikstras_algorithm ${Python_LIBRARIES})
target_link_libraries(djikstras_algorithm PRIVATE Python::Python)
