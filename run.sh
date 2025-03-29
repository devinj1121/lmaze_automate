#!/bin/bash
# You can edit/run this script if you don't feel like calling Python directly.

LMAZE_DIR='./'
VENV_DIR= './'

# Activate a virtual environment
source ${VENV_DIR}/venv/bin/activate

pip install -r ${LMAZE_DIR}/requirements.txt

python3 ${LMAZE_DIR}/l_maze.py\
 -input_file examples/example-en-in.txt\
 -output_file examples/example-en-out.txt\
 -lang en
#  -ja_shuffle 0
