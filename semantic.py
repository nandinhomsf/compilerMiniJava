class AnalisadorSemantico:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.tabela_simbolos = {}  # Para armazenar classes, variáveis e métodos
        self.erros = []  # Para armazenar erros semânticos encontrados
        self.classe_atual = None  # Para rastrear a classe atual

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
            self.visitar_exp(no)
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
        # Verifica se o método main está corretamente declarado
        if no.children[0].value != "class":
            self.erros.append("Erro semântico: declaração de classe inválida no método main.")
        # Verifica outros aspectos do método main
        for filho in no.children:
            self.visitar(filho)

    def visitar_classe(self, no):
        nome_classe = no.children[1].value
        self.tabela_simbolos[nome_classe] = {"tipo": "classe", "variaveis": {}, "metodos": {}}
        self.classe_atual = nome_classe  # Define a classe atual

        # Verifica se a classe estende outra classe
        if len(no.children) > 2 and no.children[2].value == "extends":
            classe_pai = no.children[3].value
            if classe_pai not in self.tabela_simbolos:
                self.erros.append(f"Erro semântico: classe pai '{classe_pai}' não encontrada.")

        # Visita variáveis e métodos da classe
        for filho in no.children:
            self.visitar(filho)

    def visitar_var(self, no):
        tipo = no.children[0].value
        nome_var = no.children[1].value

        # Verifica se a variável já foi declarada na classe atual
        if nome_var in self.tabela_simbolos[self.classe_atual]["variaveis"]:
            self.erros.append(f"Erro semântico: variável '{nome_var}' já declarada.")
        else:
            self.tabela_simbolos[self.classe_atual]["variaveis"][nome_var] = {"tipo": tipo}

    def visitar_metodo(self, no):
        nome_metodo = no.children[2].value
        tipo_retorno = no.children[1].value

        # Verifica se a chave 'metodos' existe na tabela de símbolos
        if "metodos" not in self.tabela_simbolos:
            self.tabela_simbolos["metodos"] = {}

        # Verifica se o método já foi declarado
        if nome_metodo in self.tabela_simbolos["metodos"]:
            self.erros.append(f"Erro semântico: método '{nome_metodo}' já declarado.")
        else:
            self.tabela_simbolos["metodos"][nome_metodo] = {"tipo_retorno": tipo_retorno, "parametros": []}

        # Visita parâmetros e comandos do método
        for filho in no.children:
            self.visitar(filho)

    def visitar_cmd(self, no):
        if no.children[0].value == "if":
            self.visitar_exp(no.children[2])  # Verifica a expressão do if
            self.visitar(no.children[4])  # Verifica o bloco do if
            if len(no.children) > 5 and no.children[5].value == "else":
                self.visitar(no.children[6])  # Verifica o bloco do else
        elif no.children[0].value == "while":
            self.visitar_exp(no.children[2])  # Verifica a expressão do while
            self.visitar(no.children[4])  # Verifica o bloco do while
        elif no.children[0].value == "System.out.println":
            self.visitar_exp(no.children[2])  # Verifica a expressão do println
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            # Verifica se a chave 'variaveis' existe na classe atual
            if self.classe_atual is None or "variaveis" not in self.tabela_simbolos[self.classe_atual]:
                self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
            else:
                if nome_var not in self.tabela_simbolos[self.classe_atual]["variaveis"]:
                    self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
                else:
                    tipo_var = self.tabela_simbolos[self.classe_atual]["variaveis"][nome_var]["tipo"]
                    tipo_exp = self.visitar_exp(no.children[2])  # Verifica o tipo da expressão
                    if tipo_var != tipo_exp:
                        self.erros.append(f"Erro semântico: tipo incompatível na atribuição de '{nome_var}'.")

    def visitar_exp(self, no):
        """
        Visita o nó EXP (expressão) e retorna o tipo da expressão.
        """
        if no.children[0].type == "INTEGER":
            return "int"
        elif no.children[0].type == "RESERVED_WORD" and no.children[0].value in ["true", "false"]:
            return "boolean"
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            if nome_var not in self.tabela_simbolos.get("variaveis", {}):
                self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
                return None
            else:
                return self.tabela_simbolos["variaveis"][nome_var]["tipo"]
        # Adicione mais casos conforme necessário
        return None