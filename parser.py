class Node:
    def __init__(self, type, value=None):
        self.type = type
        self.value = value
        self.children = []

    def __repr__(self, level=0):
        ret = "\t" * level + repr(self.type) + (f": {self.value}" if self.value else "") + "\n"
        for child in self.children:
            ret += child.__repr__(level + 1)
        return ret

class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.current_pos = 0

    def parse(self):
        return self.prog()

    def prog(self):
        node = Node("PROG")
        node.children.append(self.main())
        while self.current_token()[1] == "class":
           node.children.append(self.classe())
        return node

    def main(self):
        node = Node("MAIN")
        node.children.append(self.match("RESERVED_WORD", "class"))
        node.children.append(self.match("IDENTIFIER"))
        node.children.append(self.match("PUNCTUATION", "{"))
        node.children.append(self.match("RESERVED_WORD", "public"))
        node.children.append(self.match("RESERVED_WORD", "static"))
        node.children.append(self.match("RESERVED_WORD", "void"))
        node.children.append(self.match("RESERVED_WORD", "main"))
        node.children.append(self.match("PUNCTUATION", "("))
        node.children.append(self.match("RESERVED_WORD", "String"))
        node.children.append(self.match("PUNCTUATION", "["))
        node.children.append(self.match("PUNCTUATION", "]"))
        node.children.append(self.match("IDENTIFIER"))
        node.children.append(self.match("PUNCTUATION", ")"))
        node.children.append(self.match("PUNCTUATION", "{"))
        node.children.append(self.cmd())
        node.children.append(self.match("PUNCTUATION", "}"))
        node.children.append(self.match("PUNCTUATION", "}"))
        return node

    def classe(self):
        node = Node("CLASSE")
        node.children.append(self.match("RESERVED_WORD", "class"))
        node.children.append(self.match("IDENTIFIER"))
        if self.current_token()[1] == "extends":
            node.children.append(self.match("RESERVED_WORD", "extends"))
            node.children.append(self.match("IDENTIFIER"))
        node.children.append(self.match("PUNCTUATION", "{"))
        while self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] in ["int", "boolean",]:
            node.children.append(self.var())
        while self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "public":
            node.children.append(self.metodo())
        node.children.append(self.match("PUNCTUATION", "}"))
        return node

    def var(self):
        node = Node("VAR")
        node.children.append(self.tipo())
        node.children.append(self.match("IDENTIFIER",self.current_token()[1]))
        node.children.append(self.match("PUNCTUATION", ";"))
        return node

    def metodo(self):
        node = Node("METODO")
        node.children.append(self.match("RESERVED_WORD", "public"))
        node.children.append(self.tipo())
        node.children.append(self.match("IDENTIFIER"))
        node.children.append(self.match("PUNCTUATION", "("))
        if self.current_token()[0] != "PUNCTUATION" or self.current_token()[1] != ")":
            node.children.append(self.params())
        node.children.append(self.match("PUNCTUATION", ")"))
        node.children.append(self.match("PUNCTUATION", "{"))
        while self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] in ["int", "boolean", "String"]:
            node.children.append(self.var())
        while self.current_token()[0] in ["RESERVED_WORD", "IDENTIFIER", "PUNCTUATION"] and self.current_token()[1] != "return":
            node.children.append(self.cmd())
        node.children.append(self.match("RESERVED_WORD", "return"))
        node.children.append(self.exp())
        node.children.append(self.match("PUNCTUATION", ";"))
        node.children.append(self.match("PUNCTUATION", "}"))
        return node

    def params(self):
        node = Node("PARAMS")
        node.children.append(self.tipo())
        node.children.append(self.match("IDENTIFIER",self.current_token()[1]))
        while self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == ",":
            node.children.append(self.match("PUNCTUATION", ","))
            node.children.append(self.tipo())
            node.children.append(self.match("IDENTIFIER"))
        return node

    def tipo(self):
        node = Node("TIPO")
        if self.current_token()[1] == "int":
            node.children.append(self.match("RESERVED_WORD", "int"))
            if self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "[":
                node.children.append(self.match("PUNCTUATION", "["))
                node.children.append(self.match("PUNCTUATION", "]"))
        elif self.current_token()[1] == "boolean":
            node.children.append(self.match("RESERVED_WORD", "boolean"))
        elif self.current_token()[0] == "IDENTIFIER":
            node.children.append(self.match("IDENTIFIER"))
        else:
            raise ValueError(f"Token inesperado: {self.current_token()} na posição {self.current_pos}")
        return node

    def cmd(self):
        node = Node("CMD")
        if self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "{":
            node.children.append(self.match("PUNCTUATION", "{"))
            while self.current_token()[0] in ["RESERVED_WORD", "IDENTIFIER", "PUNCTUATION"]:
                node.children.append(self.cmd())
            node.children.append(self.match("PUNCTUATION", "}"))
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "if":
            node.children.append(self.match("RESERVED_WORD", "if"))
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.exp())
            node.children.append(self.match("PUNCTUATION", ")"))
            node.children.append(self.cmd())
            if self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "else":
                node.children.append(self.match("RESERVED_WORD", "else"))
                node.children.append(self.cmd())
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "while":
            node.children.append(self.match("RESERVED_WORD", "while"))
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.exp())
            node.children.append(self.match("PUNCTUATION", ")"))
            node.children.append(self.cmd())
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "System.out.println":
            node.children.append(self.match("RESERVED_WORD", "System.out.println"))
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.exp())
            node.children.append(self.match("PUNCTUATION", ")"))
            node.children.append(self.match("PUNCTUATION", ";"))
        elif self.current_token()[0] == "IDENTIFIER":
            node.children.append(self.match("IDENTIFIER",self.current_token()[1]))
            if self.current_token()[0] == "OPERATOR" and self.current_token()[1] == "=":
                node.children.append(self.match("OPERATOR", "="))
                node.children.append(self.exp())
                node.children.append(self.match("PUNCTUATION", ";"))
            elif self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "[":
                node.children.append(self.match("PUNCTUATION", "["))
                node.children.append(self.exp())
                node.children.append(self.match("PUNCTUATION", "]"))
                node.children.append(self.match("OPERATOR", "="))
                node.children.append(self.exp())
                node.children.append(self.match("PUNCTUATION", ";"))
        else:
            raise ValueError(f"Token inesperado: {self.current_token()} na posição {self.current_pos}")
        return node

    def exp(self):
        node = Node("EXP")
        node.children.append(self.rexp())
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] == "&&":
            node.children.append(self.match("OPERATOR", "&&"))
            node.children.append(self.rexp())
        return node

    def rexp(self):
        node = Node("REXP")
        node.children.append(self.aexp())
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["<", "==", "!="]:
            node.children.append(self.match("OPERATOR", self.current_token()[1]))
            node.children.append(self.aexp())
        return node

    def aexp(self):
        node = Node("AEXP")
        node.children.append(self.mexp())
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["+", "-"]:
            node.children.append(self.match("OPERATOR", self.current_token()[1]))
            node.children.append(self.mexp())
        return node

    def mexp(self):
        node = Node("MEXP")
        node.children.append(self.sexp())
        while self.current_token()[0] == "OPERATOR" and self.current_token()[1] == "*":
            node.children.append(self.match("OPERATOR", "*"))
            node.children.append(self.sexp())
        return node

    def sexp(self):
        node = Node("SEXP")
        if self.current_token()[0] == "OPERATOR" and self.current_token()[1] in ["!", "-"]:
            node.children.append(self.match("OPERATOR", self.current_token()[1]))
            node.children.append(self.sexp())
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] in ["true", "false", "null"]:
            node.children.append(self.match("RESERVED_WORD", self.current_token()[1]))
        elif self.current_token()[0] == "INTEGER":
            node.children.append(self.match("INTEGER"))
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "new":
            if self.current_token()[1] == "int":
                node.children.append(self.match("RESERVED_WORD", "new"))
                node.children.append(self.match("RESERVED_WORD", "int"))
                node.children.append(self.match("PUNCTUATION", "["))
                node.children.append(self.exp())
                node.children.append(self.match("PUNCTUATION", "]"))
            else:
                node.children.append(self.pexp())
        elif self.current_token()[0] == "IDENTIFIER":
            node.children.append(self.pexp())
            if self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == ".":
                node.children.append(self.match("PUNCTUATION", "."))
                node.children.append(self.match("RESERVED_WORD", "length"))
            elif self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "[":
                node.children.append(self.match("PUNCTUATION", "["))
                node.children.append(self.exp())
                node.children.append(self.match("PUNCTUATION", "]"))
        elif self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "(":
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.exp())
            node.children.append(self.match("PUNCTUATION", ")"))
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "this":
            node.children.append(self.pexp())
        else:
            raise ValueError(f"Token inesperado: {self.current_token()} na posição {self.current_pos}")
        return node

    def pexp(self):
        node = Node("PEXP")
        if self.current_token()[0] == "IDENTIFIER":
            node.children.append(self.match("IDENTIFIER",self.current_token()[1]))
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "this":
            node.children.append(self.match("RESERVED_WORD", "this"))
        elif self.current_token()[0] == "RESERVED_WORD" and self.current_token()[1] == "new":
            node.children.append(self.match("RESERVED_WORD", "new"))
            node.children.append(self.match("IDENTIFIER"))
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.match("PUNCTUATION", ")"))
        elif self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "(":
            node.children.append(self.match("PUNCTUATION", "("))
            node.children.append(self.exp())
            node.children.append(self.match("PUNCTUATION", ")"))
        else:
            raise ValueError(f"Token inesperado: {self.current_token()} na posição {self.current_pos}")

        while self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == ".":
            node.children.append(self.match("PUNCTUATION", "."))
            node.children.append(self.match("IDENTIFIER"))
            if self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == "(":
                node.children.append(self.match("PUNCTUATION", "("))
                if self.current_token()[0] != "PUNCTUATION" or self.current_token()[1] != ")":
                    node.children.append(self.exps())
                node.children.append(self.match("PUNCTUATION", ")"))
        return node

    def exps(self):
        node = Node("EXPS")
        node.children.append(self.exp())
        while self.current_token()[0] == "PUNCTUATION" and self.current_token()[1] == ",":
            node.children.append(self.match("PUNCTUATION", ","))
            node.children.append(self.exp())
        return node

    def match(self, token_type, token_value=None):
        if self.current_pos < len(self.tokens):
            token = self.tokens[self.current_pos]
            if token[0] == token_type and (token_value is None or token[1] == token_value):
                self.current_pos += 1
                return Node(token_type, token[1])
            else:
                raise ValueError(f"Token inesperado: {token} na posição {self.current_pos}")
        else:
            raise ValueError(f"Fim inesperado dos tokens na posição {self.current_pos}")

    def current_token(self):
        if self.current_pos < len(self.tokens):
            return self.tokens[self.current_pos]
        else:
            return ("EOF", "EOF")