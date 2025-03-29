# lmaze_automate

Generates pseudoword distractors for L-Maze experiments using both
[Wuggy](https://github.com/WuggyCode/wuggy) and custom methods. Outputs are generated in format which is ready to use in PCIbex. Current language support for English, Japanese, and Russian.

- [lmaze\_automate](#lmaze_automate)
- [Requirements](#requirements)
- [Running an Example](#running-an-example)
- [Running With Your Items](#running-with-your-items)
  - [Description of Parameters](#description-of-parameters)
  - [Input File Format](#input-file-format)
- [Common Errors](#common-errors)


# Requirements
- [Python 3+](https://www.python.org/downloads/)
- Python packages listed in `requirements.txt`, installable via `pip`

To install all the necessary packages at once, use:

`pip install -r requirements.txt`

Before installing requirements, you may need to create a Python virtual environment. This acts as a container
that remembers what versions of Python packages you have. Ideally, each project you make with Python should therefore
have its own virtual environment. You may read more [here](https://docs.python.org/3/library/venv.html).

# Running an Example
First get the files by clicking the `Code` button on the top right of Github and selected `Download Zip`. Or, you may clone the Github repository to your local machine using `git clone https://github.com/devinj1121/lmaze_automate.git`. Install all required Python packages using the command given in the requirements section above. Before running, you may examine the included example outputs in the `examples` folder. Compare these with the corresponding input files to get an idea of how the program should work. 


To verify that the program runs correctly, after installing the required Python packages, open a terminal window and navigate to the folder where `l_maze.py` is located. Then type and run:

`python l_maze.py`

This runs the script with default parameters, meaning it will run the script on the included `example-en-in.txt` file. You should see the sentence outputs of the program in your terminal window. The output file should be named `example-en-out.txt`. 

# Running With Your Items
To run with custom parameters (i.e., your own items), use the following template:

````
python l_maze.py 
    -input_file [input file path] 
    -output_file [output file path] 
    -lang [lang identifier]
    -ja_shuffle [ja_shuffle]
````

Alternatively, you may edit and run the included Bash script:
````
chmod +x run.sh
./run.sh
````

These parameters are not mandatory, so if you just want to run with your items but keep the default output file name and lang "en", you can just specify the input file parameter.

## Description of Parameters
`input_file`: Provide a string of the full path to your input file. The program expects a .txt file in the format specified below.

`output_file`: Provide a string of the full path to the output file, which will be put in PCIbex format.

`lang`: Provide a string which specifies the language you need to create distractors for. Currently there are two options, "en" for English and "ja" for Japanese.

`ja_shuffle`: This tells the program what generation method to use for Japanese. Provide an int, either 0 or 1. If 0, each word (i.e., space-separated token in input) will be randomly shuffled to make a distractor. If 1, the final character of each word will be randomly swapped with another character in the word.


## Input File Format
Each line must be formatted as: 

```[condition];[item];[sentence]```

For example, if you have a 2x2 factorial design (four conditions - a,b,c,d), the first few lines may look like so:

```
exp1-a;1;blabla bla
exp1-b;1;blaaaa bla
exp1-c;1;blooo bla
exp1-d;1;blooombloa
exp1-a;2;blabla bla
exp1-b;2;blabla booo
exp1-c;2;blabla boomboom
exp1-d;2;blabla blooom
.....
.....
```

Keep the following in mind:

1. **File Type & Headings**: Your file must be a .txt file with no headings (e.g., like in CSV files).

1. **Words**: The program treats each space-separated token in the sentence as a word, generating a distractor for each. In English and Russian, this is intuitive. In the first line of the example above, "blabla" and "bla" would thus be two separate words. However, for Japanese, what is treated as a word is more flexible to the experiment design. For example, it may be reasonable to treat a string like `その学生が` as one word. This would mean participants would be presented with the choice between `その学生が` and a generated distractor such as `そのが学生`.

2. **Fixed Distractors**: Distractors are kept constant across the conditions of the same item. So, since item1 has "bla" in multiple conditions, the same distractor will be used. However, in item2, a new distractor for "bla" will be generated and used for any other instances of "bla" in item2.

# Common Errors
1. `Exception caught: Sequence ... was not found in lexicon orthographic_english`: This error means that Wuggy was not able to make a distractor for the given word. This can happen quite often. In this case, the program will insert the original word in CAPS to the output file. You will then need to replace these manually by searching with Ctrl+F for capital words in the output file.


2. `IndexError: list index out of range`: If you receive the error below, most likely you have empty lines in your input file. Make sure to delete any empty lines and that your file only contains lines with the proper formatting of `condition;item#;sentence`.

```
Traceback (most recent call last):
  File ".../l_maze.py", line 196, in <module>
    curr_item = int(line.split(";")[1])
                    ~~~~~~~~~~~~~~~^^^
IndexError: list index out of range
```