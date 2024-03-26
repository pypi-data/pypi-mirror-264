# Test plan for nvidia-stub

## Goals

The goals of tests for nvidia-stub is to ensure that nvidia-stub is robust on the plethora of platforms, Python versions, and environments NVIDIA users may try to install software on. We want to make sure that the user gets the right software when they should, or at least gets a clear, actionable error message when we cannot reach our Python Package Index.

## Scope

The main actions being tested are installation and package generation using the nvidia-stub build backend.

## Use cases

- Installation on supported platforms using the right version of Python
- Installation on an unsupported operating system/architecture
- Installation on an unsupported Python versions

## Functional tests

1. Verify sdist/wheel selection priority in pip
   - Should pull wheel with extra index url
   - Should pull sdist without
2. Function with/without network
   - Error without network
   - Download and install correct wheel with network
3. Error text should work both with and without CUDA available
4. Test install works on supported platforms
   - OS
   - Arch
   - Python ABI

## Negative tests

1. Test installation where there is no supported wheel for user OS/Arch/Python on NVIDIA index
2. Invalid input wheel for package generation

## Method and Environment

Tests will be run with pytest, and use docker containers to enable manipulation of networking in the testing environment.

Unit and integration tests will run against the wheel selection code and sdist generation code.
