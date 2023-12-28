# Interpreter
import sys
from lex_core import *

try:
    file = open(sys.argv[1])
except IndexError:
    file = open('tryme.txt')

lines = file.readlines()
num_line = 0

for line in lines:
    num_line += 1

    sublines = line.split(";")
    for subline in sublines:
        try:
            result = execute(subline)
            if result:
                print(result, end=" ")
        except Exception as error:
            print(f"\n{type(error).__name__} on line {num_line}: {error}")