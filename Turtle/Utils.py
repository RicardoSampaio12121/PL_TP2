# Utils.py
# Author: Ricardo Sampaio
# Author: Cláudio Silva
# Date: 16/01/2021
 
import math

class Utils:

    def CalculatePos(self, x, y, degree, distance):
        x = x + distance * (math.cos(math.radians(degree)))

        y = y + distance * (math.sin(math.radians(degree)))
        return x, y

    def DrawLine(self, parser, x2, y2):
        parser.svg += "<line x1=\"" + str(parser.x1) + "\"  y1=\"" + str(parser.y1) + "\" x2=\"" + str(x2) + "\" y2=\"" + str(y2) + "\""
        parser.svg += " style=\"stroke: rgb" + str(parser.rgb) + ";" + " stroke-width: 1px\"/>\n"


    def CloseSvgMain(main_string):
        main_string += "</svg>"
        return main_string

        
  