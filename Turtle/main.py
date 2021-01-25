# main.py
import sys

import SVG
from Utils import Utils
from Parser import Parser


#open file
with open("LogoFiles/" + sys.argv[1], mode="r") as fh: 
    contents = fh.read()


parser = Parser()
parser.Parse(contents)


parser.svg = Utils.CloseSvgMain(parser.svg)

print(parser.vars)

#write file
with open("SVG/teste.svg", mode="w") as fh:
    fh.write(parser.svg)


