# CMAKE generated file: DO NOT EDIT!
# Generated by "MinGW Makefiles" Generator, CMake Version 3.17

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

SHELL = cmd.exe

# The CMake executable.
CMAKE_COMMAND = "C:\Program Files\JetBrains\CLion 2020.3.2\bin\cmake\win\bin\cmake.exe"

# The command to remove a file.
RM = "C:\Program Files\JetBrains\CLion 2020.3.2\bin\cmake\win\bin\cmake.exe" -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/Pb2_Lab1.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/Pb2_Lab1.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/Pb2_Lab1.dir/flags.make

CMakeFiles/Pb2_Lab1.dir/Server.c.obj: CMakeFiles/Pb2_Lab1.dir/flags.make
CMakeFiles/Pb2_Lab1.dir/Server.c.obj: ../Server.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/Pb2_Lab1.dir/Server.c.obj"
	C:\Qt\Tools\mingw810_64\bin\gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles\Pb2_Lab1.dir\Server.c.obj   -c "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\Server.c"

CMakeFiles/Pb2_Lab1.dir/Server.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/Pb2_Lab1.dir/Server.c.i"
	C:\Qt\Tools\mingw810_64\bin\gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\Server.c" > CMakeFiles\Pb2_Lab1.dir\Server.c.i

CMakeFiles/Pb2_Lab1.dir/Server.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/Pb2_Lab1.dir/Server.c.s"
	C:\Qt\Tools\mingw810_64\bin\gcc.exe $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\Server.c" -o CMakeFiles\Pb2_Lab1.dir\Server.c.s

# Object files for target Pb2_Lab1
Pb2_Lab1_OBJECTS = \
"CMakeFiles/Pb2_Lab1.dir/Server.c.obj"

# External object files for target Pb2_Lab1
Pb2_Lab1_EXTERNAL_OBJECTS =

Pb2_Lab1.exe: CMakeFiles/Pb2_Lab1.dir/Server.c.obj
Pb2_Lab1.exe: CMakeFiles/Pb2_Lab1.dir/build.make
Pb2_Lab1.exe: CMakeFiles/Pb2_Lab1.dir/linklibs.rsp
Pb2_Lab1.exe: CMakeFiles/Pb2_Lab1.dir/objects1.rsp
Pb2_Lab1.exe: CMakeFiles/Pb2_Lab1.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug\CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable Pb2_Lab1.exe"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles\Pb2_Lab1.dir\link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/Pb2_Lab1.dir/build: Pb2_Lab1.exe

.PHONY : CMakeFiles/Pb2_Lab1.dir/build

CMakeFiles/Pb2_Lab1.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles\Pb2_Lab1.dir\cmake_clean.cmake
.PHONY : CMakeFiles/Pb2_Lab1.dir/clean

CMakeFiles/Pb2_Lab1.dir/depend:
	$(CMAKE_COMMAND) -E cmake_depends "MinGW Makefiles" "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1" "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1" "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug" "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug" "C:\Users\paula\CLionProjects\COMPUTER NETWORKS\Pb2_Lab1\cmake-build-debug\CMakeFiles\Pb2_Lab1.dir\DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/Pb2_Lab1.dir/depend

