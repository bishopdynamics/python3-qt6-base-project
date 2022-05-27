#!/bin/bash
# transform the .ui files from QT Designer into python modules

# Created 2022 by James Bishop (james@bishopdynamics.com)

VENV_NAME='venv'

function bail() {
	echo "An unexpected error occurred"
	exit 1
}

# create venv if missing
if [ ! -d "$VENV_NAME" ]; then
  ./setup-venv.sh
fi

# need venv to bake
source "${VENV_NAME}/bin/activate" || bail

# Baking syntax
# pyuic6 -o <output.py> <input.ui>

# main window
echo "Baking MainWindow"
pyuic6 -o MainWindow.py MainWindow.ui || bail

echo "Baking DialogContractExplorer"
pyuic6 -o DialogContractExplorer.py DialogContractExplorer.ui || bail


# clean up
deactivate

echo "done baking ui"
