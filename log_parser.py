import os
import csv

logs = os.listdir("./Logs")

import re
import ast
import struct

def parse_csv_line(line):
    # Split the line into fields considering byte strings
    pattern = re.compile(r"(b'.*?')|([^,]+)")
    matches = pattern.findall(line)
    fields = [m[0] or m[1].strip() for m in matches if any(m)]
    
    processed = []
    for field in fields:
        field = field.strip()
        if field.startswith('b'):
            # Convert string representation of bytes to actual bytes
            try:
                byte_data = ast.literal_eval(field)
                if len(byte_data) == 8:
                    # Convert bytes to double (big-endian)
                    num = struct.unpack('>d', byte_data)[0]
                    processed.append(num)
                else:
                    # Handle unexpected byte length
                    processed.append(field)
            except:
                processed.append(field)
        else:
            # Convert regular numbers to float or int
            try:
                processed.append(float(field) if '.' in field else int(field))
            except ValueError:
                processed.append(field)
    
    return processed

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
