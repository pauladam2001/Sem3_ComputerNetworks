cmake_minimum_required(VERSION 3.17)
project(Pb10_Lab1 C)

set(CMAKE_C_STANDARD 99)

link_libraries(ws2_32 wsock32)

add_executable(Pb10_Lab1 Server.c)