class AnalisadorSemantico:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_simbolos = {}  # Para armazenar variáveis, funções e seus parâmetros
        self.erros = []  # Para armazenar erros semânticos encontrados
        self.funcao_atual = None  # Para rastrear a função atual durante a análise

    def analisar(self):
        """
        Inicia a análise semântica.
        """
        self.visitar(self.arvore_sintatica)
        return self.erros

    def visitar(self, no):
        """
        Visita um nó da árvore sintática e realiza as verificações semânticas.
        """
        if no.type == "PROG":
            self.visitar_prog(no)
        elif no.type == "MAIN":
            self.visitar_main(no)
        elif no.type == "CLASSE":
            self.visitar_classe(no)
        elif no.type == "VAR":
            self.visitar_var(no)
        elif no.type == "METODO":
            self.visitar_metodo(no)
        elif no.type == "CMD":
            self.visitar_cmd(no)
        elif no.type == "EXP":
            return self.visitar_exp(no)
        elif no.type == "CHAMADA_FUNCAO":
            print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA")
            return self.visitar_chamada_funcao(no)
        # Adicione mais casos conforme necessário

    def visitar_prog(self, no):
        """
        Visita o nó PROG (programa principal).
        """
        for filho in no.children:
            self.visitar(filho)

    def visitar_main(self, no):
        """
        Visita o nó MAIN (método principal).
        """
        for filho in no.children:
            self.visitar(filho)

    def visitar_classe(self, no):
        """
        Visita o nó CLASSE.
        """
        for filho in no.children:
            self.visitar(filho)
        self.tabela_simbolos = {}  # Reseta a tabela de símbolos após visitar a classe

    def visitar_var(self, no):
        """
        Visita o nó VAR (declaração de variável).
        """
        tipo = no.children[0].value
        nome_var = no.children[1].value

        # Verifica se a variável já foi declarada
        if nome_var in self.tabela_simbolos:
            self.erros.append(f"Erro semântico: variável '{nome_var}' já declarada.")
        else:
            self.tabela_simbolos[nome_var] = {"tipo": tipo}

    def visitar_metodo(self, no):
        """
        Visita o nó METODO (declaração de método).
        """
        nome_metodo = no.children[2].value
        tipo_retorno = no.children[1].value
        tabela_classe = self.tabela_simbolos.copy()

        # Verifica se o método já foi declarado
        if nome_metodo in self.tabela_simbolos:
            self.erros.append(f"Erro semântico: método '{nome_metodo}' já declarado.")
        else:
            # Armazena o método na tabela de símbolos
            self.tabela_simbolos[nome_metodo] = {
                "tipo_retorno": tipo_retorno,
                "parametros": [],  # Lista de parâmetros
            }
            self.funcao_atual = nome_metodo  # Define a função atual

            # Visita os parâmetros do método
            if no.children[4].type == "PARAMS":
                pars = no.children[4].children
                for i in range(0,len(pars),3):
                    print("99999",i)
                    tipo_param = pars[i].value
                    nome_param = pars[i+1].value
                    self.tabela_simbolos[nome_param] = {"tipo": tipo_param}
                    self.tabela_simbolos[nome_metodo]["parametros"].append(
                        {"nome": nome_param, "tipo": tipo_param}
                    )

            # Visita o corpo do método
            for filho in no.children[5:]:
                self.visitar(filho)

            self.funcao_atual = None  # Reseta a função atual após visitar o método
            self.tabela_simbolos = tabela_classe.copy()  # Restaura a tabela de símbolos da classe

    def visitar_cmd(self, no):
        """
        Visita o nó CMD (comando).
        """
        if no.children[0].value == "if":
            self.visitar_exp(no.children[2])  # Verifica a expressão do if
            self.visitar(no.children[4])  # Verifica o bloco do if
            if len(no.children) > 5 and no.children[5].value == "else":
                self.visitar(no.children[6])  # Verifica o bloco do else
        elif no.children[0].value == "while":
            self.visitar_exp(no.children[2])  # Verifica a expressão do while
            self.visitar(no.children[4])  # Verifica o bloco do while
        elif no.children[0].value == "System.out.println":
            resultado = self.visitar_exp(no.children[2])  # Verifica a expressão do println
            if resultado is not None:
                print(f"Resultado da expressão: {resultado}")  # Exibe o resultado da expressão
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            if nome_var not in self.tabela_simbolos:
                self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
            else:
                tipo_var = self.tabela_simbolos[nome_var]["tipo"]
                tipo_exp = self.visitar_exp(no.children[2])  # Verifica o tipo da expressão
                if tipo_var != tipo_exp:
                    self.erros.append(f"Erro semântico: tipo incompatível na atribuição de '{nome_var}'.")

    def visitar_exp(self, no):
        """
        Visita o nó EXP (expressão) e retorna o valor da expressão ou o tipo da variável.
        """
        if no.children[0].type == "INTEGER":
            return int(no.children[0].value)  # Retorna o valor numérico da constante
        elif no.children[0].type == "RESERVED_WORD" and no.children[0].value in ["true", "false"]:
            return no.children[0].value  # Retorna o valor booleano
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            if nome_var not in self.tabela_simbolos:
                self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
                return None
            else:
                return self.tabela_simbolos[nome_var]["tipo"]  # Retorna o tipo da variável
        elif no.children[0].type == "OPERATOR":
            # Avalia expressões aritméticas ou lógicas
            valor_esquerda = self.visitar_exp(no.children[1])
            valor_direita = self.visitar_exp(no.children[2])
            if valor_esquerda is not None and valor_direita is not None:
                if no.children[0].value == "+":
                    return valor_esquerda + valor_direita
                elif no.children[0].value == "-":
                    return valor_esquerda - valor_direita
                elif no.children[0].value == "*":
                    return valor_esquerda * valor_direita
                elif no.children[0].value == "/":
                    return valor_esquerda / valor_direita
                elif no.children[0].value == "&&":
                    return valor_esquerda and valor_direita
                elif no.children[0].value == "||":
                    return valor_esquerda or valor_direita
        elif no.children[0].type == "CHAMADA_FUNCAO":
            return self.visitar_chamada_funcao(no)
        return None

    def visitar_chamada_funcao(self, no):
        """
        Visita o nó CHAMADA_FUNCAO e verifica os parâmetros passados.
        """
        nome_funcao = no.children[0].value

        # Verifica se a função foi declarada
        if nome_funcao not in self.tabela_simbolos:
            self.erros.append(f"Erro semântico: função '{nome_funcao}' não declarada.")
            return None

        # Obtém os parâmetros esperados da função
        parametros_esperados = self.tabela_simbolos[nome_funcao]["parametros"]

        # Verifica se a quantidade de argumentos passados corresponde aos parâmetros esperados
        argumentos_passados = no.children[1].children if len(no.children) > 1 else []
        if len(argumentos_passados) != len(parametros_esperados):
            self.erros.append(
                f"Erro semântico: número incorreto de argumentos para a função '{nome_funcao}'. "
                f"Esperados: {len(parametros_esperados)}, fornecidos: {len(argumentos_passados)}."
            )
            return None

        # Verifica se os tipos dos argumentos correspondem aos tipos dos parâmetros
        for i, (arg, param) in enumerate(zip(argumentos_passados, parametros_esperados)):
            tipo_arg = self.visitar_exp(arg)
            tipo_param = param["tipo"]
            if tipo_arg != tipo_param:
                self.erros.append(
                    f"Erro semântico: tipo incompatível no argumento {i + 1} da função '{nome_funcao}'. "
                    f"Esperado: {tipo_param}, fornecido: {tipo_arg}."
                )

        # Retorna o tipo de retorno da função
        return self.tabela_simbolos[nome_funcao]["tipo_retorno"]