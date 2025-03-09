import os
import csv

logs = os.listdir("./Logs")

import ast
import struct

for log in logs:
    new_lines = []
    with open("./Logs/" + log, "r") as f:
        lines = f.read().splitlines()
        for line in lines:
            data = line.split(',')
            if len(data) != 5:
                continue
            new_line = [str(data[0]), str(struct.unpack('d', ast.literal_eval(data[1]))[0]), str(struct.unpack('d', ast.literal_eval(data[2]))[0]), str(struct.unpack('d', ast.literal_eval(data[3]))[0]), str(data[4])]
            new_lines.append(",".join(new_line))
    with open("./Parsed_Logs/" + log, "a") as f:
        for line in new_lines:
            f.write(line + '\n')
