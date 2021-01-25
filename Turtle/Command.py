# Commands.py
# Author: Ricardo Sampaio
# Author: Cláudio Silva
# Date: 16/01/2021

import sys
import Utils
import operator
 
operations = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


def do_make_var(command, parser):
    var_name = command.args['target']

    if (len(command.args) == 2):
        var_value = parser.eval(command.args['value'])
    else:
        var_value = parser.eval({'left': command.args['left'], 'right': command.args['right'], 'op': command.args['op']})

    parser.vars[var_name] = var_value


def do_line(command, parser):


    if(command.args['ahead'] == False):
        distance = 0 - parser.eval(command.args['distance'])
    else:
        distance = parser.eval(command.args['distance'])

   
    x2, y2 = Utils.Utils.CalculatePos(None, parser.x1, parser.y1, parser.angle, distance)

    if(parser.penstate == True):
        Utils.Utils.DrawLine(None, parser, x2, y2)
    
    parser.x1 = x2
    parser.y1 = y2



def do_line_x(command, parser):

    x2 = parser.eval(command.args['x2'])

    if(parser.penstate == True):
        Utils.Utils.DrawLine(None, parser, x2, parser.y1)
    
    parser.x1 = x2  

def do_line_y(command, parser):

    y2 = parser.eval(command.args['y2'])

    if(parser.penstate == True):
        Utils.Utils.DrawLine(None, parser, parser.x1, y2)
    
    parser.y1 = y2


def do_line_xy(command, parser):
    x2 = parser.eval(command.args['x2'])
    y2 = parser.eval(command.args['y2'])

    if(parser.penstate == True):
        Utils.Utils.DrawLine(None, parser, x2, y2)

    parser.x1 = x2
    parser.y1 = y2


def do_line_hm(command, parser):
    
    if(parser.penstate == True):
        Utils.Utils.DrawLine(None, parser, 1, 1)

    parser.x1 = 1
    parser.y1 = 1


def do_rt_angle(command, parser):
    parser.angle += parser.eval(command.args['angle'])

def do_lt_angle(command, parser):
    parser.angle -= parser.eval(command.args['angle'])


def do_pnup(command, parser):
    parser.penstate = False

def do_pndn(command, parser):
    parser.penstate = True

def do_rgb(command, parser):
    
    rgb = (parser.eval(command.args['r']), parser.eval(command.args['g']), parser.eval(command.args['b']))

    parser.rgb = rgb


def do_while(command, parser):
    var_name = command.args['var']

    value = parser.eval(command.args['value'])
    
    if(command.args['signal'] == '>'):
        while parser.vars[var_name] > value:
            parser.execute(command.args['commands'])

    elif(command.args['signal'] == '<'):
        while parser.vars[var_name] < value:
            parser.execute(command.args['commands'])



    
def do_if(command, parser):
    var_name = command.args['var']

    value = parser.eval(command.args['value'])

    if(command.args['signal'] == '>'):
        if(parser.vars[var_name] > value):
            parser.execute(command.args['commands'])
    
    elif(command.args['signal'] == '<'):
        if(parser.vars[var_name] < value):
            parser.execute(command.args['commands'])

    else:
        if(parser.vars[var_name] == value):
            parser.execute(command.args['commands'])



def do_if_else(command, parser):
    var_name = command.args['var']

    value = parser.eval(command.args['value'])

    if(command.args['signal'] == '>'):
        if(parser.vars[var_name] > value):
            parser.execute(command.args['ifCommands'])
        else:
            parser.execute(command.args['elseCommands'])
  
    elif(command.args['signal'] == '<'):
        if(parser.vars[var_name] < value):
            parser.execute(command.args['ifCommands'])
        else:
            parser.execute(command.args['elseCommands'])
  
    elif(command.args['signal'] == '='):
        if(parser.vars[var_name] == value):
            parser.execute(command.args['ifCommands'])
        else:
            parser.execute(command.args['elseCommands'])


def do_repeat(command, parser):
    i = parser.eval(command.args["value"])

    while(i != 0):
        i -= 1
        parser.execute(command.args['commands'])
   

def do_def(command, parser):
    parser.funcs[command.args["name"]] = {"varlist": command.args["varlist"], "code": command.args["code"]}
    print(parser.funcs)


def do_call(command, parser):
    
    funcname = command.args['name']
    
    if funcname not in parser.funcs:
        print(f"Undefined function call {funcname}", file=sys.stderr)
        exit(1)
    varlist = parser.funcs[funcname]["varlist"]
    code = parser.funcs[funcname]["code"]
    if len(varlist) != len(command.args["values"]):
        print(f"Function {funcname} call with mismatched umber of parameters ({len(varlist)} vs {len(command.args['values'])})")
        exit(1)
    # save state before function
    tmp_vars = parser.vars.copy()

    # atribuir valores às variáveis da função
    for var, value in zip(varlist, command.args["values"]):
        parser.vars[var] = value
    
       
    # executar a função
    parser.execute(code)
    
    parser.vars = tmp_vars.copy()


class Command:
    dispatch_table = {
        "attrib": do_make_var,
        "while": do_while,
        "if": do_if,
        "ifelse": do_if_else,
        "repeat": do_repeat,
        "def": do_def,
        "call": do_call,
        "draw_line": do_line,
        "draw_line_x": do_line_x,
        "draw_line_y": do_line_y,
        "draw_line_hm": do_line_hm,
        "draw_line_xy": do_line_xy,
        "lt_angle": do_lt_angle,
        "rt_angle": do_rt_angle,
        "pnup": do_pnup,
        "pndn": do_pndn,
        "change_rgb": do_rgb,
    }

    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __repr__(self):
        return f"{self.name} => {self.args}"

    def run(self, parser):
        self.dispatch_table[self.name](self, parser)
