# lmaze_automate

Generates pseudoword distractors for the Lmaze experimental methodology using
[Wuggy](https://github.com/WuggyCode/wuggy) in Python. Outputs are generated in format
which is ready to use in PCIbex.

## Requirements
- [Python 3+](https://www.python.org/downloads/)

## Running an Example
First, open a terminal window and navigate to the folder where `l_maze.py` is located. Then type and run:

`python l_maze.py`

This runs the script with default parameters, meaning it will run the script on the included `example.txt` file.
You should see teh sentence outputs of the program in your terminal window.

## Running With Your Items
To run with custom parameters (i.e., your items), use the following template:

`python l_maze.py -input_file [input_file] -output_file [output_file] -lang [lang]`

The parameters serve the following functions:

- input_file (default = ./example.txt): String specifying where script will take input from (txt). 
- output_file (default = ./items_ibex.txt/): String specifying where output will be stored.
- lang (default = EN): String specifying input language. Only English is functioning at the moment.

NOTE: Your input must be formatted as condition;item#;sentence. In addition, your file must have no headings. Refer to the example provided as reference.
