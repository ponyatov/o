
import os,sys

def comment(s,l=80):
    print( '#'*(l-len(s)+1) + ' ' + s )
    sys.exit(-1)
# comment('system init')


############################################# Marvin Minsky's extended frame model

class Frame:
    def __init__(self,V):
        self.type = self.__class__.__name__.lower()
        self.val  = V
        self.slot = {}
        self.nest = []

    def __repr__(self):
        return self.dump()
    def dump(self,depth=0,prefix=''):
        tree = self.pad(depth) + self.head(prefix)
        # infty
        if not depth: Frame.dumped = []
        if self in Frame.dumped: return tree + ' _/'
        else: Frame.dumped.append(self)
        # slot{}
        for i in self.slot:
            tree += self.slot[i].dump(depth+1,prefix='%s = '%i)
        # nest[]
        idx = 0
        for j in self.nest:
            tree += j.dump(depth+1,prefix='%s = '%idx) ; idx += 1
        # subtree
        return tree
    def head(self,prefix=''):
        return '%s<%s:%s> @%x' % (prefix,self.type,self._val(),id(self))
    def pad(self,depth):
        return '\n' + '\t' * depth
    def _val(self): return str(self.val)

    def __getitem__(self,key):
        return self.slot[key]
    def __setitem__(self,key,that):
        self.slot[key] = that ; return self
    def __lshift__(self,that):
        return self.__setitem__(that.type,that)
    def __rshift__(self,that):
        return self.__setitem__(that.val,that)
    def __floordiv__(self,that):
        self.nest.append(that) ; return self

    def pop(self): return self.nest.pop()
    def top(self): return self.nest[-1]

################################################################## primitive types

class Primitive(Frame):
    def eval(self,env): env // self

class Symbol(Primitive): pass
class String(Primitive): pass
class Number(Primitive): pass
class Integer(Number): pass
class Hex(Integer): pass
class Bin(Integer): pass

################################################## EDS: executable data structures

class Active(Frame): pass

class VM(Active): pass

vm = VM('vm') ; vm << vm


############################################################ PLY: no-syntax parser

import ply.lex as lex

tokens = ['symbol','number','integer','hex','bin']

t_ignore         = ' \t\r\n'
t_ignore_comment = r'[\#\\].*'

def t_exp(t):
    r'[+\-]?[0-9]+(\.[0-9]*)?[eE][+\-]?[0-9]+'
    return Number(t.value)
def t_number(t):
    r'[+\-]?[0-9]+\.[0-9]*'
    return Number(t.value)

def t_hex(t):
    r'0x[0-9A-Fa-f]+'
    return Hex(t.value)
def t_bin(t):
    r'0b[01]+'
    return Bin(t.value)
def t_integer(t):
    r'[+\-]?[0-9]+'
    return Integer(t.value)

def t_symbol(t):
    r'[^ \t\r\n\#\\]+'
    return Symbol(t.value)

def t_ANY_error(t): raise SyntaxError(t)

lexer = lex.lex()


###################################################################### interpreter

def WORD(env):
    token = lexer.token()
    if token: env // token
    return token

def FIND(env):
    token = env.pop()
    try: env // env[token.val] ; return True
    except KeyError: env // token ; return False

def EVAL(env): env.pop().eval(env)

def INTERP(env):
    lexer.input(env.pop().val)
    while True:
        if not WORD(env): break
        if isinstance(env.top(),Symbol):
            if not FIND(env): raise SyntaxError(env)
        EVAL(env)
    print(env)


###################################################################### system init

if __name__ == '__main__':
    print(vm)
    for infile in sys.argv[1:]:
        with open(infile) as src:
            vm // String(src.read()) ; INTERP(vm)
