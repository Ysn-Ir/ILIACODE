#!/bin/bash

# Directly add the virtual environment's binaries to your path
export PATH="$PWD/../ILIACODE/Scripts:$PATH"

# Force the prompt to show you are in the environment
export VIRTUAL_ENV="$PWD/../ILIACODE"
export PS1="(ILIACODE) ${PS1}"

# Keep the shell open
$SHELL