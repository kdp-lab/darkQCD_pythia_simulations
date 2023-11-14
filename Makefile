# Makefile is a part of the PYTHIA event generator.
# Copyright (C) 2022 Torbjorn Sjostrand.
# PYTHIA is licenced under the GNU GPL v2 or later, see COPYING for details.
# Please respect the MCnet Guidelines, see GUIDELINES for details.
# Author: Philip Ilten, September 2014.
#
# This is is the Makefile used to build PYTHIA examples on POSIX systems.
# Example usage is:
#     make main01
# For help using the make command please consult the local system documentation,
# i.e. "man make" or "make --help".

################################################################################
# VARIABLES: Definition of the relevant variables from the configuration script.
################################################################################

# Set the shell.
SHELL=/usr/bin/env bash

# make bin dir
MKDIR_BIN=mkdir -p $(PWD)/bin

# Include the configuration.
-include Makefile.inc

# Check distribution (use local version first, then installed version).
ifneq ("$(wildcard ../lib/libpythia8.*)","")
  PREFIX_LIB=/home/abadea/pythia8307/lib
  PREFIX_INCLUDE=/home/abadea/pythia8307/include
endif
CXX_COMMON:=-I$(PREFIX_INCLUDE) $(CXX_COMMON) $(GZIP_LIB)
CXX_COMMON+= -L$(PREFIX_LIB) -Wl,-rpath,$(PREFIX_LIB) -lpythia8 -ldl
PYTHIA=$(PREFIX_LIB)/libpythia8$(LIB_SUFFIX)


# Fix missing runtime paths from RIVET.
ifeq ($(RIVET_USE),true)
  COMMA=,
  RIVET_LPATH=$(filter -L%,$(shell $(RIVET_BIN)$(RIVET_CONFIG) --ldflags))
  RIVET_RPATH=$(subst -L,-Wl$(COMMA)-rpath$(COMMA),$(RIVET_LPATH))
endif

################################################################################
# RULES: Definition of the rules used to build the PYTHIA examples.
################################################################################

# Rules without physical targets (secondary expansion for specific rules).
.SECONDEXPANSION:
.PHONY: all clean

all: mkdirBin higgsPortal
mkdirBin:
	$(MKDIR_BIN)

# PYTHIA library.
$(PYTHIA):
	$(error Error: PYTHIA must be built, please run in the top PYTHIA directory)

# ROOT (turn off all warnings for readability).
higgsPortal: $(PYTHIA) src/$$@.cc 
ifeq ($(ROOT_USE),true)
	$(CXX) src/$@.cc -o bin/$@.exe -w $(CXX_COMMON) $(ROOT_LIB)\
	 `$(ROOT_CONFIG) --cflags --glibs`
else
	$(error Error: $@ requires ROOT)
endif

# # ROOT (turn off all warnings for readability).
# %: $(PYTHIA) %.cc
# ifeq ($(ROOT_USE),true)
# 	$(CXX) $*.cc -o $@ -w $(CXX_COMMON) $(ROOT_LIB)\
# 	 `$(ROOT_CONFIG) --cflags --glibs`
# else
# 	$(error Error: $@ requires ROOT)
# endif

# Clean.
clean:
	rm -f *~
	rm -f \#*.*#
	rm -f $(PWD)/include/#*.*#
	rm -f $(PWD)/include/*~
	rm -f $(PWD)/src/#*.*#
	rm -f $(PWD)/src/*~
	rm -f $(PWD)/bin/*.exe
	rmdir bin
