import re

class AnalisadorLexico:
    def __init__(self, code):
        self.code = code
        self.tokens = []
        self.current_pos = 0

        self.token_patterns = [
            ("WHITESPACE", r"[ \n\t\r\f]+"),
            ("COMMENT_LINE", r"//.*"),
            ("COMMENT_BLOCK", r"/\*.*?\*/"),
            ("RESERVED_WORD", r"\b(boolean|class|extends|public|static|void|main|String|return|int|if|else|while|System\.out\.println|length|true|false|this|new|null)\b"),
            ("IDENTIFIER", r"[a-zA-Z][a-zA-Z0-9_]*"),
            ("INTEGER", r"\b\d+\b"),
            ("OPERATOR", r"\+|\-|\*|&&|!|==|!=|<=|>=|<|>|="),
            ("PUNCTUATION", r"[\(\)\[\]\{\};\.,]"),
        ]

        self.master_pattern = re.compile(
            "|".join(f"(?P<{name}>{pattern})" for name, pattern in self.token_patterns), re.DOTALL
        )

    def tokenize(self):
        while self.current_pos < len(self.code):
            match = self.master_pattern.match(self.code, self.current_pos)
            if match:
                token_type = match.lastgroup
                token_value = match.group(token_type)

                if token_type in ("WHITESPACE", "COMMENT_LINE", "COMMENT_BLOCK"):
                    pass
                else:
                    self.tokens.append((token_type, token_value))

                self.current_pos = match.end()
            else:
                unrecognized = self.code[self.current_pos]
                raise ValueError(f"Token não reconhecido: {unrecognized} na posição {self.current_pos}")

        return self.tokens

# Example usage
if __name__ == "__main__":
    code = """
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
            return num_aux;
        }
    }
    """

    lexer = AnalisadorLexico(code)
    try:
        tokens = lexer.tokenize()
        for token in tokens:
            print(token)
    except ValueError as e:
        print(e)