# lmaze_automate

Generates pseudoword distractors for L-Maze experiments using
[Wuggy](https://github.com/WuggyCode/wuggy) in Python. Outputs are generated in format
which is ready to use in PCIbex.

## Requirements
- [Python 3+](https://www.python.org/downloads/)

## Running an Example
First, open a terminal window and navigate to the folder where `l_maze.py` is located. Then type and run:

`python l_maze.py`

This runs the script with default parameters, meaning it will run the script on the included `example.txt` file.
You should see the sentence outputs of the program in your terminal window.

## Running With Your Items
To run with custom parameters (i.e., your items), use the following template:

`python l_maze.py -input_file [input_file] -output_file [output_file] -lang [lang]`

The parameters serve the following functions:

- input_file (default = ./example.txt): String specifying where script will take input from (txt). 
- output_file (default = ./items_ibex.txt/): String specifying where output will be stored.
- lang (default = EN): String specifying input language. Only English is functioning at the moment.

These parameters are not mandatory, so if you just want to run with your items but keep the default output file name and
lang EN, you can just specify the input file parameter.

 **NOTE** each line must be formatted as: 

```[condition];[item];[sentence]```


For example, if you have a 2x2 factorial experiment, the first few lines may look like so:

```
condition-a;item1;blabla bla
condition-b;item1;blaaaa bla
condition-c;item1;blooo bla
condition-d;item1;blooombloa
condition-a;item2;fooofaaa
.....
.....
```

In addition, your file **must have no headings**.
