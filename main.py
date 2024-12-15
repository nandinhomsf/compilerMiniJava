from lexer import AnalisadorLexico
from parser import Parser
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


    lexer = AnalisadorLexico(data)
    tokens = lexer.tokenize()
    parser = Parser(tokens)
    ast = parser.parse()

 
    print("Árvore Sintática:")
    print(ast)


    print("Gerando a visualização da Árvore Sintática...")
    graph = visualize_ast(ast)
    graph.render('arvore_sintatica', view=True)
    print("Árvore Sintática salva como 'arvore_sintatica.png', exibindo...")