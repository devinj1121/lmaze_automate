with open("data.txt", "r") as f:
    for line in f.readlines():
        import re
        split_line = re.split('a:|s:|{|}',line)
        
        s = split_line[2].replace("\"","").replace(".", "").replace("?", "").replace(",", "")
        a = split_line[3].replace("\"","").replace(".", "")
        
        if len(s.split()) != len(a.split()):
            print(s)
            print(a)