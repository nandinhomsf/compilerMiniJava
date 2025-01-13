from lexer import AnalisadorLexico
from parser import Parser
from semantic import AnalisadorSemantico
from generator import GeradorCodigoMIPS
from graphviz import Digraph

def visualize_ast(node, graph=None, parent_id=None):
    if graph is None:
        graph = Digraph(format='png')
        graph.attr(rankdir="TB")

    current_id = str(id(node))

    label = node.type
    if node.value is not None:
        label += f": {node.value}"


    graph.node(current_id, label=label)


    if parent_id is not None:
        graph.edge(parent_id, current_id)


    for child in node.children:
        visualize_ast(child, graph, current_id)

    return graph

def main():
    # 1. Leitura do arquivo de entrada
    nome_arquivo = "entrada.txt"  # Substitua pelo nome do seu arquivo de entrada
    with open(nome_arquivo, "r") as arquivo:
        codigo_fonte = arquivo.read()

    # 2. Análise léxica
    lexer = AnalisadorLexico(codigo_fonte)
    tokens = lexer.tokenize()

    # 3. Análise sintática
    parser = Parser(tokens)
    ast = parser.parse()

    print("\nÁrvore sintática gerada:")
    print(ast)

    # 4. Análise semântica
    analisador_semantico = AnalisadorSemantico(ast)  # Passa a AST para o analisador semântico
    erros_semanticos = analisador_semantico.analisar()  # Executa a análise semântica

    if erros_semanticos:
        print("\nErros semânticos encontrados:")
        for erro in erros_semanticos:
            print(erro)
    else:
        print("\nAnálise semântica concluída sem erros.")

    # 5. Geração de código MIPS
    if not erros_semanticos:  # Só gera código se não houver erros semânticos
        generator = GeradorCodigoMIPS(ast)
        mips_code = generator.gerar_codigo()

        print("\nCódigo MIPS gerado:")
        print(mips_code)

        # 6. Salvar o código MIPS em um arquivo (opcional)
        with open("saida.asm", "w") as f:
            f.write(mips_code)

if __name__ == "__main__":
    main()