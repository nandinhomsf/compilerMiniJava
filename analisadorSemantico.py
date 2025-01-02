from parser import Node


class TabelaSimbolos:
    def __init__(self):
        self.tabela = {}

    def adicionar(self, nome_variavel, tipo):
        if nome_variavel in self.tabela:
            raise Exception(f"Variável '{nome_variavel}' já foi declarada.")
        self.tabela[nome_variavel] = tipo

    def verificar(self, nome_variavel):
        if nome_variavel not in self.tabela:
            raise Exception(f"Erro semântico: Variável '{nome_variavel}' utilizada antes de ser declarada.")



class AnalisadorSemantico:
    def __init__(self):
        self.tabela_simbolos = TabelaSimbolos()

    def analisar(self, ast:Node):
        if ast.type=="VAR":
            self.declarar(ast.children[1])
        elif ast.type == "PARAMS":
            self.declarar(ast.children[1])
        elif ast.type == "CMD" and isinstance(ast.children[0],Node) and ast.children[0].type=="IDENTIFIER":
            self.tabela_simbolos.verificar(ast.children[0].value)
        elif ast.type == "PEXP" and isinstance(ast.children[0],Node) and ast.children[0].type=="IDENTIFIER":
            self.tabela_simbolos.verificar(ast.children[0].value)
        elif ast.type == "AEXP":
            aux = self.substituiAexp(ast)
            if aux!=None: ast = aux
        for child in ast.children:
            self.analisar(child)
        return ast
    
    def declarar(self,no:Node):
        self.tabela_simbolos.adicionar(no.value,no.type)

    def substituiExp(self,sast:Node):
        return self.substituiRexp(sast.children[0])
    
    def substituiRexp(self,sast:Node):
        return self.substituiAexp(sast.children[0])
        
    def substituiAexp(self,sast: Node):
        if len(sast.children)>=3:
            left_child = self.substituiMexp(sast.children[0])
            if left_child==None: return sast
            right_child = self.substituiMexp(sast.children[2])
            #print(sast.children)
            #print((left_child.value))
            #print((sast.children[1].value))
            #print((right_child.value))
            self.executeAexp(sast.children[1].value,left_child.value,right_child.value)
            sast.children[2] = Node(left_child.type,self.executeAexp(sast.children[1].value,left_child.value,right_child.value))
            sast.children = sast.children[2:]
            while len(sast.children)!=1:
                #print(sast.children)
                left_child = sast.children[0]
                right_child = self.substituiMexp(sast.children[2])
                #print((left_child.value))
                #print((sast.children[1].value))
                #print((right_child.value))
                self.executeAexp(sast.children[1].value,left_child.value,right_child.value)
                sast.children[2] = Node(left_child.type,self.executeAexp(sast.children[1].value,left_child.value,right_child.value))
                sast.children = sast.children[2:]
            sast.value=sast.children[0].value
            return sast
        return self.substituiMexp(sast.children[0])
    def substituiMexp(self,sast:Node):
        #print(sast.children)
        if len(sast.children)>=3:
            #print(9999999999999999999999)
            left_child = self.substituiSexp(sast.children[0])
            if left_child==None:
                #print(33333333333333)
                return sast
            right_child = self.substituiSexp(sast.children[2])
            l = int(left_child.value)
            r = int(right_child.value)
            sast.children[2] = Node(left_child.type,l*r)
            sast.children = sast.children[2:]
            #print(sast.children)
            while len(sast.children )!=1: 
                #print(8888888888)
                left_child = sast.children[0]
                right_child = self.substituiSexp(sast.children[2])
                l = int(left_child.value)
                r = int(right_child.value)
                sast.children[2] = Node(left_child.type,l*r)
                sast.children = sast.children[2:]
            #print(sast)
            sast.value = sast.children[0].value
            return sast
        return self.substituiSexp(sast.children[0])
    def substituiSexp(self,sast:Node):
        if sast.children[0].type == "PUNCTUATION":
            #print(55555555)
            return self.substituiExp(sast.children[1])
        return self.substituiPexp(sast.children[0])
    def substituiPexp(self,sast:Node):
        if sast.type == "INTEGER":
            return sast
    @staticmethod
    def executeAexp(op, x, y):
        x,y=int(x),int(y)
        if op == '+':
            return x + y
        elif op == '-':
            return x - y
        else:
            raise ValueError("Operador inválido para Aexp.")


        

        '''
        if isinstance(ast, Declaracao):
            # Adiciona a variável na tabela de símbolos
            self.tabela_simbolos.adicionar(ast.nome, ast.tipo)
        elif isinstance(ast, UsoVariavel):
            # Verifica se a variável foi declarada
            self.tabela_simbolos.verificar(ast.nome)
        elif isinstance(ast, Operacao):
            # Avalia subexpressões constantes
            valor = avaliar_expressao_constante(ast)
            if valor is not None:
                # Substitui a operação pela constante calculada
                return Numero(valor)
        # Percorre os filhos da árvore sintática
        for filho in ast.filhos:
            self.analisar(filho)
    def avaliar_expressao_constante(expr):
        if isinstance(expr, ):  # Se a expressão for um número literal
            return expr.valor
        elif isinstance(expr, Operacao):  # Se for uma operação
            # Avalia as duas subexpressões
            valor_esquerda = avaliar_expressao_constante(expr.esquerda)
            valor_direita = avaliar_expressao_constante(expr.direita)
            if valor_esquerda is not None and valor_direita is not None:
                if expr.operador == '+':
                    return valor_esquerda + valor_direita
                elif expr.operador == '-':
                    return valor_esquerda - valor_direita
                elif expr.operador == '*':
                    return valor_esquerda * valor_direita
                elif expr.operador == '/':
                    return valor_esquerda / valor_direita
        return None  # Se não for uma expressão constante
        '''