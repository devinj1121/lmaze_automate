"""
Generate L-maze items in ibex format from standard-formatted text file of stimuli.
Author: Devin Johnson, 2022
"""

import argparse
import random
import re
from wuggy import WuggyGenerator

language = None
ja_shuffle = None

def parse_args():
    """
    Parse all command line arguments
    Parameters:
        - None
    Returns:
        - args (argparse.Namespace): The list of arguments passed in
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-input_file",type=str, help = "Full path to input file (txt).", default = "example-en.txt")
    parser.add_argument("-output_file",type=str, help = "Full path to desired output file (l-maze/ibex format)", default = "./items_ibex.txt")
    parser.add_argument("-lang",type=str, help = "Language of input; en for English; ja for Japanese.", default = "en", choices=["en","ja"])
    parser.add_argument("-ja_shuffle",type=int, help = "Types of pseudoword generations (only valid for Japanese); 0 for random shuffle of each token; 1 for random shift of end-of-phrase particle (like が・は, etc.) ", default = 0, choices=[0,1])

    args = parser.parse_args()

    global language
    language = args.lang.lower()
    
    global ja_shuffle
    ja_shuffle = args.ja_shuffle

    return args

def get_pseudowords(line, item_dict):
    # Let a word be defined as a space-separated token in the input
    # Ex. "I like pizza" has three words; 「その学生が　ピザを　食べた。」also has three words.
    real_words = line.split(";")[2].split()
    pseudowords = []

    for real_word in real_words:

        # If already generated a pseudoword for this word (i.e., still on the same item), just use that one
        if real_word in item_dict:
            pseudowords.append(item_dict[real_word])
        else:
            if language == "en":
                try:
                    # Try to get pseudoword
                    query_term = re.sub(r",|\.|\?", "", real_word).lower()
                    results = g.generate_classic([query_term])
     
                    if len(results) > 0:
                        # Append a random pseudoword from the results                    
                        n = random.randint(0, len(results)-1)
                        pseudoword = results[n]['pseudoword']

                        #  Handle punctuation and caps
                        if real_word[0].isupper():
                            pseudoword = pseudoword.capitalize()
                        if pseudoword[-1] not in [".", ",", "?", "!"] and real_word[-1] in [".", ",", "?", "!"]:
                            pseudoword += real_word[-1]
                        
                        pseudowords.append(pseudoword)
                        item_dict[real_word] = pseudoword
                    # Can return empty, for example, on 1 letter words
                    else: 
                        pseudowords.append(real_word.upper())   
                        item_dict[real_word] = real_word.upper()   

                except Exception as e:
                    if "not found in lexicon" in str(e):
                        pseudowords.append(real_word.upper())   
                        item_dict[real_word] = real_word.upper()   
                    print("Exception caught: " + str(e))
                    
            if language == "ja":
                # Handle ending punctuation
                end_punctuation = ""

                if "。" in real_word or "？" in real_word:
                    end_punctuation = real_word[-1]
                    pseudoword = list(real_word)[0:-1]
                else:
                    pseudoword = list(real_word)
                
                # Random shuffle mode
                if ja_shuffle == 0:
                    word_c = pseudoword.copy()
                    while(word_c == pseudoword): 
                        random.shuffle(word_c)
                        pseudoword = word_c
                    
                # Move end particle mode
                elif ja_shuffle == 1:
                    if len(pseudoword) <= 2:
                        temp = pseudoword[0]
                        pseudoword[0] = pseudoword[-1]
                        pseudoword[-1] = temp
                    else:
                        targeti = random.randint(0, len(pseudoword)-2)
                        temp = pseudoword[targeti]
                        pseudoword[targeti] = pseudoword[-1]
                        pseudoword[-1] = temp

                pseudoword = "".join(pseudoword) + end_punctuation
                pseudowords.append(pseudoword)
                item_dict[real_word] = pseudoword 
                
    # Python check
    if len(pseudowords) != len(real_words):
        print("ERROR-PY Length of pseudowords not the same as length of real words for lines:")
        print(pseudowords)
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

    return pseudowords, item_dict

def output_ibex(output_file, lines):
    with open(output_file, "w", encoding="utf-8") as f:
        for line in lines:
            s = line.split(";")
            condition  = s[0]
            item_num = s[1]
            real_sentence = s[2]
            distractor_sentence = s[3]

            f.write((f"[[\"{condition}\", \'{item_num}\'], \"Maze\", {{s:\"{real_sentence}\", a:\"{distractor_sentence}\"}}],\n"))

if __name__ == '__main__':

    args = parse_args()
    g = WuggyGenerator()
    if args.lang.lower() == "en":
        g.load("orthographic_english")
    elif args.lang.lower() == "ja":
        pass
    else:
        print("Error: Current support only for English (en) and Japanese (ja).")
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
        item_dict = {}
        for line in lines:

            # Want distractors to be same for all conditions of an item (except at manipulated regions)
            curr_item = int(line.split(";")[1])
            
            # Upon new item, reset dict and generate all new
            if curr_item != last_item:
                item_dict = {}
            curr_pseudo, item_dict = get_pseudowords(line, item_dict)
            last_item = curr_item
                
            # Make the line for txt output
            line = line.strip() + ";" + " ".join(curr_pseudo).strip()
            new_lines.append(line)
            print(line)
        
    # Output to Ibex format
    output_ibex(args.output_file, new_lines)