from parser import Node
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
            self.visitar_cmd(no.children[4])  # Verifica o bloco do if
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
                '''tipo_var = self.tabela_simbolos[nome_var]["tipo"]
                tipo_exp =''' 
                self.visitar_exp(no.children[2])  # Verifica o tipo da expressão
                if len(no.children) > 4:
                    self.visitar_exp(no.children[5])
                '''if tipo_var != tipo_exp:
                    self.erros.append(f"Erro semântico: tipo incompatível na atribuição de '{nome_var}'.")'''

    def visitar_exp(self, no):
        """
        Visita o nó EXP (expressão) e retorna o valor da expressão ou o tipo da variável.
        """
        for child in no.children:
            no.value = self.visitar_rexp(child)
            return no.value
        
        #return None
    def visitar_rexp(self, no):
        if len(no.children)==3:
            self.visitar_rexp(no.children[0])
            self.visitar_aexp(no.children[2])
        else: no.value = self.visitar_aexp(no.children[0])
        return no.value

    def visitar_aexp(self, no):
        j = 0
        if len(no.children)>=3:
            i=0
            nfilhos = len(no.children)
            left = self.visitar_mexp(no.children[i])
            while left == None or type(left)!=int:
                i+=2
                if i>nfilhos:
                    break
                left = self.visitar_mexp(no.children[i])
            j=i
            i+=2
            while i<nfilhos:
                right = self.visitar_mexp(no.children[i])
                if right == None or type(right)!=int:
                    aux = Node("AEXP",no.value)
                    aux.children.extend(no.children[j:i-1])
                    no.children[j:i-1] = [aux]
                    j+=2
                    i=j+2
                    nfilhos = len(no.children)
                    left = 0
                else:
                    no.value = self.executeAexp(no.children[i-1].value, left, right)
                    left = no.value
                    i+=2
            if j>0: no.value = None
            return no.value
        else:
            no.value = self.visitar_mexp(no.children[0])
        return no.value
    def visitar_mexp(self, no):
        j=0
        if len(no.children)>=3:
            i=0
            nfilhos = len(no.children)
            left = self.visitar_sexp(no.children[i])
            while left == None or type(left)!=int:
                    i+=2
                    if i>nfilhos:
                        break
                    left = self.visitar_sexp(no.children[i])
            i+=2
            while i<nfilhos:
                right = self.visitar_sexp(no.children[i])
                if right == None:
                    i+=2
                elif type(right)!=int:
                    aux = Node("MEXP",no.value)
                    aux.children.extend(no.children[j:i-1])
                    no.children[j:i-1] = [aux]
                    j+=2
                    i=j+2
                    nfilhos = len(no.children)
                    left = 1
                else:
                    no.value = left * right
                    left = no.value
                    i+=2
            if j>0: no.value = None
            return no.value
        else :
            no.value = self.visitar_sexp(no.children[0])
            return no.value
    def visitar_sexp(self, no):
        if no.children[0].type == "PEXP":
            self.visitar_pexp(no.children[0])
            no.value = no.children[0].value
            return no.value
        elif no.type == "INTEGER":
            return no.value
        elif no.children[0].type == "INTEGER":
            no.value = int(no.children[0].value)
            return no.value
        elif no.children[0].type == "PUNCTUATION":
            no.value = self.visitar_exp(no.children[1])
            return no.value
    def visitar_pexp(self, no):
        if no.children[0].type == "INTEGER":
            no.value = int(no.children[0].value)
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            if nome_var not in self.tabela_simbolos:
                self.erros.append(f"Erro semântico: variável '{nome_var}' não declarada.")
            no.value = nome_var


    def executeAexp(self,op, x, y):
        x,y=int(x),int(y)
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        else:
            raise ValueError("Operador inválido para Aexp.")
