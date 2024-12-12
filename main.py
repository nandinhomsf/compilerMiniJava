from lexer import AnalisadorLexico
from parser import Parser

data = '''
class Factorial {
    public static void main(String[] a) {
        System.out.println(new Fac().ComputeFac(10));
    }
}

class Fac {
    public int ComputeFac(int num) {
        int num_aux;
        if (num < 1)
            num_aux = 1;
        else
            num_aux = num * (this.ComputeFac(num-1));
        return num_aux;
    }
}
'''

lexer = AnalisadorLexico(data)
tokens = lexer.tokenize()
#print("Tokens:", tokens)
parser = Parser(tokens)
ast = parser.parse()
print("Árvore Sintática:")
print(ast)