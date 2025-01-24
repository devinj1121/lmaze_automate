# lmaze_automate

Generates pseudoword distractors for L-Maze experiments using both
[Wuggy](https://github.com/WuggyCode/wuggy) and custom methods. Outputs are generated in format which is ready to use in PCIbex. Current language support for English and Japanese.

## Requirements
- [Python 3+](https://www.python.org/downloads/)
- Packages required by [Wuggy](https://github.com/WuggyCode/wuggy) (available via pip)

## Running an Example
First, open a terminal window and navigate to the folder where `l_maze.py` is located. Then type and run:

`python l_maze.py`

This runs the script with default parameters, meaning it will run the script on the included `example-en.txt` file. You should see the sentence outputs of the program in your terminal window.

## Running With Your Items
To run with custom parameters (i.e., your own items), use the following template:

````
python l_maze.py 
    -input_file [input file path] 
    -output_file [output file path] 
    -lang [lang identifier]
    -ja_shuffle [ja_shuffle]
````

These parameters are not mandatory, so if you just want to run with your items but keep the default output file name and lang "en", you can just specify the input file parameter.

### Description of Parameters
`input_file`: Provide a string of the full path to your input file. The program expects a .txt file in the format specified below.

`output_file`: Provide a string of the full path to the output file, which will be put in PCIbex format.

`lang`: Provide a string which specifies the language you need to create distractors for. Currently there are two options, "en" for English and "ja" for Japanese.

`ja_shuffle`: This tells the program what generation method to use for Japanese. Provide an int, either 0 or 1. If 0, each word (i.e., space-separated token in input) will be randomly shuffled to make a distractor. If 1, the final character of each word will be randomly swapped with another character in the word.


### Input File Format
Each line must be formatted as: 

```[condition];[item];[sentence]```

For example, if you have a 2x2 factorial design, the first few lines may look like so:

```
condition-a;item1;blabla bla
condition-b;item1;blaaaa bla
condition-c;item1;blooo bla
condition-d;item1;blooombloa
condition-a;item2;blabla bla
.....
.....
```

Keep the following in mind:

1. **File Type & Headings**: Your file must be a .txt file with no headings (e.g., like in CSV files).

1. **Words**: The program treats each space-separated token in the sentence as a word, generating a distractor for each. In English, this is intuitive. In the first line of the example above, "blabla" and "bla" would thus be two separate words. However, for Japanese, what is treated as a word is more flexible to the experiment design. For example, it may be reasonable to treat a string like `その学生が` as one word. This would mean participants would be presented with the choice between `その学生が` and a generated distractor such as `そのが学生`.

2. **Fixed Distractors**: Distractors are kept constant across the conditions of the same item. So, since item1 has "bla" in multiple conditions, the same distractor will be used. However, in item2, a new distractor for "bla" will be generated and used for any other instances of "bla" in item2.