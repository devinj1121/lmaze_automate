
with open("stims_lmaze_ibex.txt", "r", encoding="utf-8") as f:
    regular = False
    fake = False
    good = True

    regular_s = ""
    fake_s = ""

    for line in f:
        for i, char in enumerate(line):

            if char == "s" and line[i+1] == ":":
                regular = True
                fake = False

            if char == "a" and line[i+1] == ":":
                regular = False
                fake = True

            if char == "}":
                
                if len(regular_s.split()) != len(fake_s.split()):
                    good = False
                    print(regular_s.split())
                    print(fake_s.split())
                    print()

                regular_s = ""
                fake_s = ""
                regular = False
                fake = False

            if regular:
                regular_s += char
            
            if fake:
                fake_s += char

    if good:
        print("Checks successful - all lines proper length.")