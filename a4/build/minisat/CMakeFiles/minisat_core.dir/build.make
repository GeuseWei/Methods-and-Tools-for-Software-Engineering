# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.26

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

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:
.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CMake.app/Contents/bin/cmake

# The command to remove a file.
RM = /Applications/CMake.app/Contents/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /Users/geuse/Desktop/a4/z29wei1

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /Users/geuse/Desktop/a4/z29wei1/build

# Include any dependencies generated for this target.
include minisat/CMakeFiles/minisat_core.dir/depend.make
# Include any dependencies generated by the compiler for this target.
include minisat/CMakeFiles/minisat_core.dir/compiler_depend.make

# Include the progress variables for this target.
include minisat/CMakeFiles/minisat_core.dir/progress.make

# Include the compile flags for this target's objects.
include minisat/CMakeFiles/minisat_core.dir/flags.make

minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o: minisat/CMakeFiles/minisat_core.dir/flags.make
minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o: /Users/geuse/Desktop/a4/z29wei1/minisat/minisat/core/Main.cc
minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o: minisat/CMakeFiles/minisat_core.dir/compiler_depend.ts
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/Users/geuse/Desktop/a4/z29wei1/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o"
	cd /Users/geuse/Desktop/a4/z29wei1/build/minisat && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -MD -MT minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o -MF CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o.d -o CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o -c /Users/geuse/Desktop/a4/z29wei1/minisat/minisat/core/Main.cc

minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/minisat_core.dir/minisat/core/Main.cc.i"
	cd /Users/geuse/Desktop/a4/z29wei1/build/minisat && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /Users/geuse/Desktop/a4/z29wei1/minisat/minisat/core/Main.cc > CMakeFiles/minisat_core.dir/minisat/core/Main.cc.i

minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/minisat_core.dir/minisat/core/Main.cc.s"
	cd /Users/geuse/Desktop/a4/z29wei1/build/minisat && /Library/Developer/CommandLineTools/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /Users/geuse/Desktop/a4/z29wei1/minisat/minisat/core/Main.cc -o CMakeFiles/minisat_core.dir/minisat/core/Main.cc.s

# Object files for target minisat_core
minisat_core_OBJECTS = \
"CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o"

# External object files for target minisat_core
minisat_core_EXTERNAL_OBJECTS =

minisat/minisat_core: minisat/CMakeFiles/minisat_core.dir/minisat/core/Main.cc.o
minisat/minisat_core: minisat/CMakeFiles/minisat_core.dir/build.make
minisat/minisat_core: minisat/libminisat.a
minisat/minisat_core: /Library/Developer/CommandLineTools/SDKs/MacOSX13.1.sdk/usr/lib/libz.tbd
minisat/minisat_core: minisat/CMakeFiles/minisat_core.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/Users/geuse/Desktop/a4/z29wei1/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable minisat_core"
	cd /Users/geuse/Desktop/a4/z29wei1/build/minisat && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/minisat_core.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
minisat/CMakeFiles/minisat_core.dir/build: minisat/minisat_core
.PHONY : minisat/CMakeFiles/minisat_core.dir/build

minisat/CMakeFiles/minisat_core.dir/clean:
	cd /Users/geuse/Desktop/a4/z29wei1/build/minisat && $(CMAKE_COMMAND) -P CMakeFiles/minisat_core.dir/cmake_clean.cmake
.PHONY : minisat/CMakeFiles/minisat_core.dir/clean

minisat/CMakeFiles/minisat_core.dir/depend:
	cd /Users/geuse/Desktop/a4/z29wei1/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /Users/geuse/Desktop/a4/z29wei1 /Users/geuse/Desktop/a4/z29wei1/minisat /Users/geuse/Desktop/a4/z29wei1/build /Users/geuse/Desktop/a4/z29wei1/build/minisat /Users/geuse/Desktop/a4/z29wei1/build/minisat/CMakeFiles/minisat_core.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : minisat/CMakeFiles/minisat_core.dir/depend

