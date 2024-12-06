import ply.lex as lex

# ID, numero
# +, -, *, &&, !
# <, >, <=, >=, ==, !=
# [, ], (, ), {, }
# ;, ,, ., =
tokens = [
    'ID', 'NUMBER', 
    'PLUS', 'MINUS', 'TIMES', 'AND', 'NOT', 
    'LESS', 'GREATER', 'LEQ', 'GEQ', 'EQ', 'NEQ', 
    'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'LBRANCE', 'RBRANCE', 
    'SEMICOLON', 'COMMA', 'DOT', 'ASSIGN' 
]

reserved = {
    'boolean': 'BOOL',
    'class' : 'CLASS',
    'extends': 'EXTENDS',
    'public': 'PUBLIC',
    'static': 'STATIC',
    'void': 'VOID',
    'main': 'MAIN',
    'String': 'STRING',
    'return': 'RETURN',
    'int': 'INT',
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'System.out.println': 'PRINTLN',
    'length': 'LEN',
    'true': 'TRUE',
    'false': 'FALSE',
    'this': 'THIS',
    'new': 'NEW',
    'null': 'NULL'
}

tokens = tokens + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'\-'
t_TIMES = r'\*'
t_AND = r'&&'
t_NOT = r'\!'
t_LESS = r'\<'
t_GREATER = r'\>'
t_LEQ = r'<='
t_GEQ = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRANCE = r'\{'
t_RBRANCE = r'\}'
t_SEMICOLON = r'\;'
t_COMMA = r'\,'
t_DOT = r'\.'
t_ASSIGN = r'\='

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_COMMENT(t):
    r'//.*|/\*[\s\S]*?\*/'
    pass

def t_NEWLINE(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

t_ignore  = ' \t'


lexer = lex.lex()

# Test it out
data = '''
class Factorial{
    public static void main(String[] a){
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    public int ComputeFac(int num){
        int num_aux;
        if (num < 1)
            num_aux = 1;
        else
            num_aux = num * (this.ComputeFac(num-1));
    return num_aux ;
    }
}

'''


lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)