from lexer import AnalisadorLexico
from parser import Parser
from semantic import AnalisadorSemantico

if __name__ == "__main__":
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


    # Análise léxica
    lexer = AnalisadorLexico(data)
    tokens = lexer.tokenize()

    # Análise sintática
    parser = Parser(tokens)
    ast = parser.parse()

    # Análise semântica
    semantic_analyzer = AnalisadorSemantico(ast)  # Passa a AST para o analisador semântico
    erros = semantic_analyzer.analisar()  # Executa a análise semântica

    # Verifica se houve erros semânticos
    if erros:
        print("Erros semânticos encontrados:")
        for erro in erros:
            print(erro)
    else:
        print("Análise semântica concluída sem erros.")

    # Exibe a árvore sintática (opcional)
    #print("\nÁrvore Sintática:")
    #print(ast)