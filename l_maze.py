"""
Generate L-maze items in ibex format from standard-formatted text file of stimuli.
Author: Devin Johnson, 2022
"""

import argparse
import random
import re
from wuggy import WuggyGenerator


def parse_args():
    """
    Parse all command line arguments
    Parameters:
        - None
    Returns:
        - args (argparse.Namespace): The list of arguments passed in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_file",type=str, help = "Full path to input file (txt).", default = "example.txt")
    parser.add_argument("-out_file",type=str, help = "Full path to desired output file (l-maze/ibex format)", default = "./items_ibex.txt")
    parser.add_argument("-lang",type=str, help = "Language of input/pseudowords", default = "EN")
    args = parser.parse_args()
    
    return args


def get_pseudowords(line):
    real_words = line.split(";")[2].split()
    pseudowords = []

    for word in real_words:   
        try:
            # Try to get pseudoword
            query_term = re.sub(",|\.|\?", "", word).lower()
            results = g.generate_classic([query_term])

            # Append a random pseudoword from the results
            if results != None and len(results) > 0:
                n = random.randint(0, len(results)-1)
                pseudoword = results[n]['pseudoword']

                # If real word had first letter caps, pseudoword should
                if word[0].isupper():
                    pseudoword = pseudoword.capitalize()

                # If real word had punctuation, pseudoword should
                if pseudoword[-1] not in [".", ",", "?", "!"] and word[-1] in [".", ",", "?", "!"]:
                    pseudoword += word[-1]
                
                pseudowords.append(pseudoword)
            else:
                pseudowords.append(word.upper())

        except Exception as e:
            if "not found in lexicon" in str(e):
                pseudowords.append(word.upper())      
            print("Exception: " + str(e))
    
    # If you want first distractor to be x-x-x instead of pseudoword, uncomment.
    # pseudowords[0] = "x-x-x"

    # Python check
    if len(pseudowords) != len(real_words):
        print("ERROR-PY Length of pseudowords not the same as length of real words for lines:")
        print(pseudoword)
        print(real_words)
        exit()

    # Ibex Javascript check
    merged_pseudo = " ".join(pseudowords)
    merged_real = " ".join(real_words)

    x = re.sub(r"\s*[\r\n]\s*", r" \r ", merged_pseudo).split(r"[ \t]+")
    y = re.sub(r"\s*[\r\n]\s*", r" \r ", merged_real).split(r"[ \t]+")

    if len(x) != len(y):
        print("ERROR-JS Length of pseudowords not the same as length of real words for lines:")
        print(x)
        print(y)
        exit()

    return pseudowords


def output_ibex(out_file, lines):
    with open(out_file, "w", encoding="utf-8") as f:
        for line in lines:
            s = line.split(";")
            condition  = s[0]
            item_num = s[1]
            real_sentence = s[2]
            distractor_sentence = s[3]

            f.write((f"[[\"{condition}\", {item_num}], \"Maze\", {{s:\"{real_sentence}\", a:\"{distractor_sentence}\"}}],\n"))


if __name__ == '__main__':

    args = parse_args()
    g = WuggyGenerator()
    if args.lang == "EN":
        g.load("orthographic_english")
    else:
        print("Error: Currently no support for non-English - stopping the program.")
        quit()

    new_lines = []
    with open(args.input_file, "r", encoding="utf-8-sig") as f:
        # Check that the line is right format.
        # NOTE: This is not a comprehensive format check - please check that your lines are formatted as such: condition;item#;sentence
        lines = f.readlines()
        if len(lines[0].split(";")) != 3:
            print("Error: Improper stimuli formatting. Please format sentences as follows and ensure no headings on text file. condition;item#;sentence")
            quit()
        
        # Get pseudowords for each item set
        last_item = 0
        last_pseudo = []
        for line in lines:

            # Want pseudowords to be same for all conditions of an item
            curr_item = int(line.split(";")[0])

            # If it's a new item, generate, otherwise use last pseudowords
            if curr_item != last_item:
                curr_pseudo = get_pseudowords(line)
            else:
                curr_pseudo = last_pseudo

            # Make the line for txt output
            line = line.strip() + ";" + " ".join(curr_pseudo).strip()
            new_lines.append(line)
            print(line)

            # Update "last" variables
            last_pseudo = curr_pseudo
            last_item = curr_item
        
    # Output to Ibex format
    output_ibex(args.out_file, new_lines)