import re
import sys

lines = [] # [lineNumber, operand, comment]
infile = []

filename = sys.argv[1]

with open(filename, 'r') as input_file, open(f"formatted_{filename}", 'w') as outfile:
    for line in input_file:
        infile.append(line)

    for lineNumber, line in enumerate(infile, 1):
        # remove all line breaks
        line = line.rstrip(" \t\n")
        operand = ""
        comment = ""

        # handle comments
        if ";" in line:
            index = line.index(";")
            comment = line[index:]            
            line = line[:index]
            line = line

        line = line.upper()
       
       # handle labels
        if ":" in line:
            index = line.index(":")
            operand = line[:index+1].lstrip(" \t")
            line = line[index+1:]
            counter = len(operand)
            # if label and mnemonic on one line, seperate onto two
            if line != "":
                infile.insert(lineNumber, line)
                line = ""
        
        # left are mnemonic (with operand), directives, symbol
        line = line.strip(" \t")
        if line != "":
            line = re.sub(r'\s+', ' ', line)

            if line[0] == "." or "=" in line:
                operand = line
            else:
                operand = "\t\t\t\t" + line.strip(" \t")
            counter = len(operand) + 4
        
        # padd out comments to col 30
        if comment and operand:
            while True:
                expanded = len(operand.expandtabs(2))
                if expanded == 30:
                    break
                else:
                    operand += "\t"

        lines.append([lineNumber, operand, comment])
    
    for line in lines:
        line = line[1] + line[2]
        outfile.write(f"{line}\n")
