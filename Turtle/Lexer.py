# Lexer.py
import ply.lex as lex
import sys

class Lexer:
    literals = "x:;,[]=()+-/*\""
    t_ignore = " \n\t"
    
    tokens = ("FLOAT", "INT", "fd", "forward", "bk", "back", "lt",
              "left", "rt", "right", "setpos", "setxy", "setx", "sety", "home", "pendown"
              , "pd", "penup", "pu", "setpencolor", "make", "if", "else", "repeat", "while", "to"
              , "VAR", "ARTH", "SIGNAL")

    def t_COMMAND(self, t):
        r"""f(orwar)?d|b(ac)?k|l(ef)?t|r(igh)?t|set(pos)?(xy)?(x)?(y)?(pencolor)?|home|
             p((en)?(d(own)?)?(u(p)?)?)|make|if|else|repeat|while|to|ENDFOR """
        t.type = t.value
        return t

    def t_SIGNAL(self, t):
        r"[\< | \> | \= ]"
        return t

    def t_DOTS(self, t):
        r"\.\."
        return t

    def t_VAR(self, t):
        r"[a-z][a-z0-9]*"
        return t

    def t_ARTH(self, t):
        r"[+-\/*]"
        return t

    def t_FLOAT (self, t):
        r"[0-9]+\.[0-9]+"
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r"[0-9]+"
        t.value = int(t.value)
        return t

    def t_error(self, t):
        print(f"Parser error. Unexpected char: {t.value[0]}", file=sys.stderr)
        exit(1)

    def __init__(self):
        self.lexer = None

    def Build(self, input, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)
        self.lexer.input(input)