#!/bin/bash
eval "$(conda shell.bash hook)" # Initialize conda for bash subsheells see: https://github.com/conda/conda/issues/7980
# Activate the conda environment
conda activate connect_env

# install the latest version of the app
pip install -e .

# Run pyinstaller with the specified options
pyinstaller script.py --onefile --add-data="connect4app/assets/*:connect4app/assets/" --paths ./connect4app/ --name "Connect4"

# --icon "connect4app/assets/ico4.ico" # only supported on windows and macOS