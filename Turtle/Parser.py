# Parser.py
import sys
import ply.yacc as yacc
from Lexer import Lexer
from Command import Command
from random import Random
import Utils
import SVG
import operator


class Parser:
    tokens = Lexer.tokens

    precedence = (
        ("left", '+', '-'),
        ("left", '*', '/'),
    )

    def __init__(self):
        self.parser = None
        self.lexer = None
        self.rgb = (0, 0, 0)
        self.x1 = 1
        self.y1 = 1
        self.angle = 0
        self.penstate = True
        self.svg = "<svg viewBox=\"0 0 500.00 500.00\" xmlns=\"http://www.w3.org/2000/svg\">\n"
        # Tabela de Simbolos (symbol table)
        self.vars = {}
        self.funcs = {}
        self.random = Random()


    #returns a valid value, be it a variable or a dictionary
    def eval(self, value):
        operations = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}


        if type(value) == int or type(value) == float:
            return value
        
        if type(value) == str:
            if value in self.vars:
                return self.vars[value]
            else:
                print("Variável não inicializada: {value}", file=sys.stderr)
                self.vars[value] = 0
                return self.vars[value] 

        if type(value) == dict:
            left = self.eval(value['left'])
            right = self.eval(value['right'])
            return operations[value['op']](left, right)
            

    def Parse(self, input, **kwargs):
        self.lexer = Lexer()
        self.lexer.Build(input, **kwargs)
        self.parser = yacc.yacc(module=self, **kwargs)
        program = self.parser.parse(lexer=self.lexer.lexer)
        self.execute(program)

    def execute(self, program): #execute program
        for command in program:
            command.run(self)

    def p_error(self, t):
        print("Syntax error", file=sys.stderr)
        next_token = self.parser.token()
        if next_token:
            print(f"Got unexpected token {next_token}", file=sys.stderr)
        exit(1)

    def p_program0(self, p):
        """  program  :   command  """
        p[0] = [p[1]]

    def p_program1(self, p):
        """  program  :  program command  """
        lst = p[1]
        lst.append(p[2])
        p[0] = lst

    def p_varlist_0(self, p):
        """  varlist : VAR  """
        p[0] = [p[1]]

    def p_varlist_1(self, p):
        """  varlist  : varlist VAR """

        p[0] = p[1]
        p[0].append(p[2])

    
    #defines a function
    def p_command_def_func(self, p):
        """  command  :  to ':' VAR '(' varlist ')' '[' program ']' """
        p[0] = Command("def", {"name": p[3], "varlist": p[5], "code": p[8]})

    #variables of the function
    def p_valuelist_0(self, p):
        """  valuelist : value  """
        p[0] = [p[1]]

    def p_valuelist_1(self, p):
        """  valuelist  : valuelist value """
        p[0] = p[1] 
        p[0].append(p[2])

    #to use a function
    def p_command_use_func(self, p):
        """   command  :  VAR '(' valuelist ')'  """
        p[0] = Command("call", {"name": p[1], "values": p[3]})

    #make a variable
    def p_command_attrib(self, p):
        """ command  :  make '"' VAR value 
                     |  make '"' VAR value ARTH value """  
        
        if(len(p) == 5):
            p[0] = Command("attrib", {"target": p[3], "value": p[4]})  
        else:
            p[0] = Command("attrib", {"target": p[3], "op": p[5],"left": p[4], "right": p[6]})  

    #moves forward
    def p_command0(self, p):
        """ command   :  forward value
                      |  fd value """
               
        p[0] = Command("draw_line", {"distance": p[len(p) - 1], "ahead": True})
                 
    #moves backwards
    def p_command1(self, p):
        """ command   :  back value
                      |  bk value    """

        p[0] = Command("draw_line", {"distance": p[len(p) - 1], "ahead": False})
        
    #rotates left
    def p_command2(self, p):
        """ command   :  left value
                      |  lt value """

        p[0] = Command("lt_angle", {"angle": p[len(p) - 1]})

    #rotates right
    def p_command3(self, p):
        """ command   :  right value
                      |  rt value """

        p[0] = Command("rt_angle", {"angle": p[len(p) - 1]})

    #moves to a certain xy position
    def p_command4(self, p):
        """ command   :  setpos '[' value value ']'  """ 

        p[0] = Command("draw_line_xy", {"x2": p[3], "y2": p[4]})
        
    #moves to a certain xy position
    def p_command5(self, p):
        """ command   :  setxy '[' value value ']'  """ 

        p[0] = Command("draw_line_xy", {"x2": p[3], "y2": p[4]})
        
    #moves x to a certain position
    def p_command6(self, p):
        """ command  :  setx value """
       
        p[0] = Command("draw_line_x", {"x2": p[len(p) - 1]})

    #moves y to a certain position
    def p_command7(self, p):
        """  command  :  sety value """
        p[0] = Command("draw_line_y", {"y2": p[len(p) - 1]})

    #moves to the initial position
    def p_command8(self, p):
        """  command  :  home  """
        p[0] = Command("draw_line_hm", {})

    #paint mode off
    def p_command9(self, p):
        """  command  :  pendown
                      |  pd       """
        p[0] = Command("pndn", {})

    #paint mode on
    def p_command10(self, p):
        """  command  :  penup
                      |  pu       """
        p[0] = Command("pnup", {})

    #changes the color of the lines
    def p_command11(self, p):
        """  command  :  setpencolor '[' value value value ']' """

        p[0] = Command("change_rgb", {"r": p[3], "g": p[4], "b": p[5]})

        
    #defines a cicle
    def p_command12(self, p):
        """  command  :  while '[' ':' VAR SIGNAL value ']' '[' program ']' """
        p[0] = Command("while", {
                           "var": p[4],
                           "signal": p[5],
                           "value": p[6],
                           "commands": p[9]
                       })

    #defines a if/ifelse condition
    def p_command13(self, p):
        """ command  :  if '[' ':' VAR SIGNAL value ']' '[' program ']' 
            command  :  if '[' ':' VAR SIGNAL value ']' '[' program ']' else '[' program ']' """
        
        if(len(p) == 11):
            p[0] = Command("if", {"var": p[4], "signal": p[5], "value": p[6], "commands": p[9]})
        else:
            p[0] = Command("ifelse", {"var": p[4], "signal": p[5], "value": p[6], "ifCommands": p[9], "elseCommands": p[13]})

    #repeats a series of commands
    def p_command14(self, p):
        """ command  :  repeat value '[' program ']' """

        p[0] = Command("repeat", {"value": p[2], "commands": p[4]})


    def p_value1(self, p):
        """  value : INT  
                   | FLOAT """
        p[0] = p[1]

    def p_value2(self, p):
        """  value : VAR  """
        p[0] = p[1]

    def p_value3(self, p): 
        """  value :  value '+' value
                   |  value '-' value
                   |  value '*' value
                   |  value '/' value """
        p[0] = {"left": p[1], "right": p[3], "op": p[2]}

    def p_value4(self, p):
        """  value : '(' value ')' """
        p[0] = p[2]

    def p_value5(self, p):
        """  value : ':' value """
        p[0] = p[2]

    def p_value6(self, p):
        """ value  : '"' VAR """

