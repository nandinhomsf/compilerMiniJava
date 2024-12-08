import ply.lex as lex

# ID, numero
# +, -, *, &&, !
# <, >, <=, >=, ==, !=
# [, ], (, ), {, }
# ;, ,, ., =


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

tokens = [
    'ID', 'NUMBER', 
    'PLUS', 'MINUS', 'TIMES', 'AND', 'NOT', 
    'LESS', 'GREATER', 'LEQ', 'GEQ', 'EQ', 'NEQ', 
    'LBRACKET', 'RBRACKET', 'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 
    'SEMICOLON', 'COMMA', 'DOT', 'ASSIGN',
    # Add reserved keywords dynamically
] + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_AND = r'&&'
t_NOT = r'!'
t_LESS = r'<'
t_GREATER = r'>'
t_LEQ = r'<='
t_GEQ = r'>='
t_EQ = r'=='
t_NEQ = r'!='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
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

def t_error(t):
    print(f"Problema no caracter '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

t_ignore  = ' \t'

# Create the lexer
lexer = lex.lex()

def tokenize(data):
    """Tokenize the input data string."""
    lexer.input(data)  # Pass the raw data string to the lexer
    tokens = []
    while True:
        tok = lexer.token()
        if not tok: 
            break  # No more input
        tokens.append(tok)
    return tokens