import ply.yacc as yacc
from lexer import tokens  # Import the lexer tokens

# Grammar Rules
def p_program(p):
    '''program : class_decl_list
               | main_function'''
    p[0] = p[1]  # AST root is a list of class declarations

def p_main_function(p):
    '''main_function : PUBLIC STATIC VOID MAIN LPAREN RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('main_function', p[6])  # 'main_function' -> body of main function

def p_class_decl_list(p):
    '''class_decl_list : class_decl
                       | class_decl_list class_decl'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_class_decl(p):
    '''class_decl : PUBLIC CLASS ID EXTENDS ID LBRACE method_decl_list RBRACE
                  | CLASS ID LBRACE method_decl_list RBRACE'''
    if len(p) == 9:  # class declaration with EXTENDS
        p[0] = ('class', p[2], p[4], p[6], p[8])  # ('class', access, class_name, extends_class, method_list)
    elif len(p) == 8:  # class declaration without PUBLIC
        p[0] = ('class', None, p[2], p[4], p[6])  # ('class', None, class_name, extends_class, method_list)

def p_method_decl_list(p):
    '''method_decl_list : method_decl method_decl_list
                        | method_decl'''
    if len(p) == 3:
        p[0] = [p[1]] + p[2]  # Add method to list
    else:
        p[0] = [p[1]]  # Only one method

def p_method_decl(p):
    '''method_decl : type ID LPAREN param_list RPAREN LBRACE statement_list RBRACE'''
    p[0] = ('method', p[1], p[2], p[4], p[6])  # (type, name, params, body)

def p_param(p):
    '''param : INT ID'''
    p[0] = ('param', p[1], p[2])  # Example for integer parameter

def p_param_list(p):
    '''param_list : param
                  | param_list COMMA param
                  | empty'''
    if len(p) == 2:  # Single parameter or empty
        p[0] = [p[1]] if p[1] is not None else []
    else:  # Multiple parameters
        p[0] = p[1] + [p[3]]


def p_statement(p):
    '''statement : assignment
                 | if_statement
                 | while_statement
                 | return_statement
                 | print_statement
                 | block'''
    p[0] = p[1]

def p_assignment(p):
    '''assignment : ID ASSIGN expression SEMICOLON'''
    p[0] = ('assign', p[1], p[3])

def p_if_statement(p):
    '''if_statement : IF LPAREN expression RPAREN statement
                     | IF LPAREN expression RPAREN statement ELSE statement'''
    if len(p) == 6:
        p[0] = ('if', p[3], p[5])  # If statement without an else clause
    else:
        p[0] = ('if', p[3], p[5], p[7])  # If statement with an else clause

def p_while_statement(p):
    '''while_statement : WHILE LPAREN expression RPAREN statement'''
    p[0] = ('while', p[3], p[5])

def p_return_statement(p):
    '''return_statement : RETURN expression SEMICOLON'''
    p[0] = ('return', p[2])

def p_print_statement(p):
    '''print_statement : PRINTLN LPAREN expression RPAREN SEMICOLON'''
    p[0] = ('print', p[3])

def p_block(p):
    '''block : LBRACE statement_list RBRACE'''
    p[0] = p[2]

def p_statement_list(p):
    '''statement_list : statement
                      | statement_list statement'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_type(p):
    '''type : INT
            | BOOL
            | STRING
            | VOID'''
    p[0] = p[1]


def p_expression(p):
    '''expression : expression PLUS expression
                  | expression MINUS expression
                  | expression TIMES expression
                  | expression LESS expression
                  | expression GREATER expression
                  | expression LEQ expression
                  | expression GEQ expression
                  | expression EQ expression
                  | expression NEQ expression
                  | expression AND expression
                  | NOT expression
                  | LPAREN expression RPAREN
                  | NUMBER
                  | ID
                  | TRUE
                  | FALSE
                  | NULL
                  | expression DOT ID LPAREN param RPAREN
                  | expression DOT LEN
                  | NEW ID LPAREN param RPAREN
                  | THIS
                  | expression LBRACKET expression RBRACKET'''

    if len(p) == 4:  # Binary operations (e.g., PLUS, MINUS, etc.)
        p[0] = (p[2], p[1], p[3])
    elif len(p) == 3:  # Unary operation (e.g., NOT)
        p[0] = ('not', p[2])
    elif len(p) == 2:  # Single token (NUMBER, ID, TRUE, FALSE, NULL)
        p[0] = p[1]
    elif len(p) == 5:  # Method call (expression DOT ID LPAREN param RPAREN)
        p[0] = ('method_call', p[1], p[3], p[4])  # p[3] is the method name (ID), p[4] is the argument list
    elif len(p) == 4:  # Array access (expression LBRACKET expression RBRACKET)
        p[0] = ('array_access', p[1], p[3])  # p[1] is the array, p[3] is the index
    elif len(p) == 3:  # Length access (expression DOT LEN)
        p[0] = ('length', p[1])  # p[1] is the array or string
    elif len(p) == 4:  # Object creation (NEW ID LPAREN param RPAREN)
        p[0] = ('new_object', p[2], p[4])  # p[2] is the class name, p[4] is the arguments
    elif len(p) == 2:  # 'this' refers to the current instance of the class
        p[0] = ('this')
    else:  # Parentheses for grouping
        p[0] = p[2]

def p_empty(p):
    '''empty :'''
    p[0] = None

# Other grammar rules for statements, expressions, etc.

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}') at line {p.lineno}")
    else:
        print("Syntax error at EOF")

# Your parser creation
parser = yacc.yacc()

def parse_input(tokens):
    """Function to parse the tokenized input."""
    return parser.parse(tokens)

