class GeradorCodigoMIPS:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.codigo_mips = []  # Lista para armazenar as instruções MIPS
        self.variaveis = []  # Mapeia variáveis para registradores ou memória
        self.if_count,self.while_count,self.exp_count = 0,0,0
        self.pexp_count = [0]  # Para rastrear a classe atual durante a geração de código
        self.chamada = []  # Para rastrear o método atual durante a geração de código
        self.params_count=0
        self.var_count = 0

    def gerar_codigo(self):
        """
        Inicia a geração de código MIPS.
        """
        self.visitar(self.arvore_sintatica)
        return "\n".join(self.codigo_mips)

    def visitar(self, no):
        """
        Visita um nó da árvore sintática e gera código MIPS correspondente.
        """
        if no.type == "PROG":
            self.visitar_prog(no)
        elif no.type == "MAIN":
            self.visitar_main(no)
        elif no.type == "VAR":
            self.visitar_var(no)
        elif no.type == "PARAMS":
            self.visitar_params(no)
        elif no.type == "CMD":
            self.visitar_cmd(no)
        elif no.type == "EXP":
            return self.visitar_exp(no)
        elif no.type == "CLASSE":
            self.visitar_classe(no)  # Adicionado suporte para nó CLASSE
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
        self.codigo_mips.append(".text")
        self.codigo_mips.append(".globl main")
        self.codigo_mips.append("main:")
        self.visitar(no.children[14])
        self.codigo_mips.append('li $v0, 10')
        self.codigo_mips.append('syscall')

    def visitar_var(self, no):
        """
        Visita o nó VAR (declaração de variável) e armazena no dicionário de variáveis.
        """
        nome_var = no.children[1].value  # O segundo filho é o nome da variável
        self.variaveis.append(nome_var)  # Adiciona a variável à lista de variáveis
        self.codigo_mips.append("addi $sp, $sp, -4")
        self.var_count+=1


    def visitar_cmd(self, no):
        """
        Visita o nó CMD (comando).
        """
        if no.children[0].value == "System.out.println":
            self.visitar_exp(no.children[2])
            self.codigo_mips.append(f"li $v0, 1")  # Código para imprimir inteiro
            self.codigo_mips.append(f"move $a0, $t0")
            self.codigo_mips.append("syscall")
            self.codigo_mips.append("li $v0, 11")  # Código para imprimir nova linha
            self.codigo_mips.append("li $a0, 10")
            self.codigo_mips.append("syscall")
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            pos = 4*(len(self.variaveis) - self.variaveis.index(nome_var) - 1)
            self.visitar_exp(no.children[2])
            if len(no.children) > 4:
                self.codigo_mips.append(f"sll $t2, $t0, 2")
                self.codigo_mips.append(f"addi $sp, $t2, {pos})")
                self.visitar_exp(no.children[5])
            self.codigo_mips.append(f"sw $t0, {pos}($sp)")
        elif no.children[0].value == "if":
            # Gera código para o comando if
            self.visitar_exp(no.children[2])  # Avalia a expressão do if
            self.codigo_mips.append(f"bne $t0, $zero, if{self.if_count}")  # Pula para o bloco else se a condição for falsa

            if len(no.children) > 5:
                self.visitar_cmd(no.children[6])  # Visita o bloco else
            self.codigo_mips.append(f"j fim{self.if_count}")  # Pula para o fim do if
            self.codigo_mips.append(f"if{self.if_count}:")
            self.visitar_cmd(no.children[4])  # Visita o bloco then
            self.codigo_mips.append(f"fim{self.if_count}:")
            self.if_count+=1

        elif no.children[0].value == "while":
            
            self.codigo_mips.append(f"loop{self.while_count}:")
            self.visitar_exp(no.children[2])
            self.codigo_mips.append(f"bne $t0, $zero, loop{self.while_count}")
            self.while_count+=1
        

    def visitar_classe(self, no):
        """
        Visita o nó CLASSE e gera código MIPS correspondente.
        """
        # Obtém o nome da classe (opcional, pode ser útil para depuração)
        nome_classe = no.children[1].value
        #print(f"Processando classe: {nome_classe}")  # Para depuração
        self.codigo_mips.append(f"{nome_classe}:")  # Adiciona o rótulo da classe no código MIPS
        # Percorre os nós filhos da classe

        for filho in no.children[2:]:
            if filho.type == "VAR":
                self.visitar_var(filho)  # Processa variáveis da classe
            # Adicione mais casos conforme necessário (por exemplo, construtores)
        self.codigo_mips.append("jr $ra")  # Retorna ao chamador
        for filho in no.children[2:]:
            if filho.type == "METODO":
                self.visitar_metodo(filho)  # Processa métodos da classe
                self.codigo_mips.append("jr $ra")  # Retorna ao chamador

    def visitar_metodo(self, no):
        """
        Visita o nó METODO e gera código MIPS correspondente.
        """
        # Obtém o nome do método
        nome_metodo = no.children[2].value  # O terceiro filho é o nome do método

        # Adiciona o rótulo do método no código MIPS
        self.codigo_mips.append(f"{nome_metodo}:")
        for child in no.children[3:]:
            self.visitar(child)
        self.codigo_mips.append(f"addi $sp, $sp, {4*(self.params_count + self.var_count) }")  # Salva o parâmetro na pilha
        self.var_count = 0
        self.params_count = 0


    def visitar_params(self, no):
        """
        Visita o nó PARAMS e gera código MIPS correspondente.
        """
        # Percorre os parâmetros do método
        for i in range(1, len(no.children), 3):
            nome_param = no.children[i].value
            self.variaveis.append(nome_param)  # Adiciona o parâmetro à lista de variáveis
        self.params_count = ((len(no.children)+1) // 3)
        self.codigo_mips.append(f"addi $sp, $sp, {-4*self.params_count }")  # Salva o parâmetro na pilha

    def visitar_exp(self, no):
        if no.value != None:
            if no.value in self.variaveis:
                pos = 4*(len(self.variaveis) - self.variaveis.index(no.value) - 1)
                self.codigo_mips.append(f"lw $t0, {pos}($sp)")
            elif no.value == 'true':
                self.codigo_mips.append("li $t0, 1")
            elif no.value == 'false' or no.value == 'null':
                self.codigo_mips.append("li $t0, 0")
            elif no.type !="PUNCTUATION": self.codigo_mips.append(f"li $t0, {no.value}")
            return no.value
        elif no.type == "EXP":
            if len(no.children) == 1:
                return self.visitar_exp(no.children[0])
            self.visitar_exp(no.children[0])
            self.codigo_mips.append("move $t1, $t0")
            for i in range(2,len(no.children),2):
                self.visitar_exp(no.children[i])
                self.codigo_mips.append("and $t1, $t0, $t1")
            self.codigo_mips.append("move $t0, $t1")
        elif no.type == "REXP":
            if len(no.children) == 1:
                return self.visitar_exp(no.children[0])
            self.visitar_exp(no.children[0])
            self.codigo_mips.append("move $t1, $t0")
            for i in range(2,len(no.children),2):
                self.visitar_exp(no.children[i])
                if no.children[i-1].value == '<':
                    self.codigo_mips.append("slt $t1, $t1, $t0")
                elif no.children[i-1].value == '==':
                    self.codigo_mips.append("seq $t1, $t0, $t1")
                elif no.children[i-1].value == '!=':
                    self.codigo_mips.append("seq $t1, $t0, $t1")
                    self.codigo_mips.append("xori $t1, $t1, 1")
                self.codigo_mips.append(f"beq $t1, $zero, fim_exp{self.exp_count}")
            self.codigo_mips.append(f"fim_exp{self.exp_count}:")
            self.codigo_mips.append("move $t0, $t1")
            self.exp_count+=1
        elif no.type == "AEXP":
            if len(no.children) == 1:
                return self.visitar_exp(no.children[0])
            self.visitar_exp(no.children[0])
            self.codigo_mips.append("move $t2, $t0")
            for i in range(2,len(no.children),2):
                self.visitar_exp(no.children[i])
                if no.children[i-1].value == '+':
                    self.codigo_mips.append("add $t2, $t2, $t0")
                elif no.children[i-1].value == '-':
                    self.codigo_mips.append("sub $t2, $t2, $t0")
            self.codigo_mips.append("move $t0, $t2")
        elif no.type == "MEXP":
            if len(no.children) == 1:
                return self.visitar_exp(no.children[0])
            self.visitar_exp(no.children[0])
            self.codigo_mips.append("move $t1, $t0")
            for i in range(2,len(no.children),2):
                self.visitar_exp(no.children[i])
                self.codigo_mips.append("mul $t1, $t0, $t1")
            self.codigo_mips.append("move $t0, $t1")
        elif no.type == "SEXP":
            if len(no.children) == 1:
                return self.visitar_exp(no.children[0])
            if no.children[0].value == '!':
                self.visitar_exp(no.children[1])
                self.codigo_mips.append("xori $t0, $t0, 1")
            elif no.children[0].value == '(':
                self.visitar_exp(no.children[1])
            else:
                self.visitar_exp(no.children[0])
                if no.children[1].value == '.':
                    pass
                else:
                    self.codigo_mips.append("move $t1, $t0")
                    self.visitar_exp(no.children[2])
                    self.codigo_mips.append("sll $t0, $t0, 2")
                    self.codigo_mips.append("add $t1, $t0, $t1")
                    self.codigo_mips.append("lw $t2, 0($t1)")
                    self.codigo_mips.append("move $t0, $t1")

        elif no.type == "PEXP":
            self.pexp_count.append(0)
            for child in no.children:
                if child.type == "IDENTIFIER":
                    if child.value in self.variaveis:
                        pos = 4*(len(self.variaveis) - self.variaveis.index(no.children[0].value) - 1)
                        self.codigo_mips.append(f"lw $t0, {pos}($sp)")
                    else:
                        self.chamada.append("sw $ra, -4($sp)\nsw $t1, -8($sp)\nsw $t2, -12($sp)")
                        self.chamada.append("addi $sp, $sp, -12")
                        self.chamada.append(f"jal {child.value}")
                        self.chamada.append("addi $sp, $sp, 12")
                        self.chamada.append("lw $ra, -4($sp)\nlw $t1, -8($sp)\nlw $t2, -12($sp)")
                        self.pexp_count[-1]+=5
                elif child.type == "EXPS":
                    self.visitar_exps(child)
                elif child.type == "EXP":
                    self.visitar_exp(child)
            self.codigo_mips.extend(self.chamada[:self.pexp_count[-1]])
            self.pexp_count.pop()
            self.chamada = self.chamada[:self.pexp_count[-1]]

    def visitar_exps(self,no):
        i = -12
        for child in no.children:
            if child.type=="EXP":
                i-=4
                self.visitar_exp(child)
                self.codigo_mips.append(f"sw $t0, {i}($sp)")