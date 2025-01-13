class GeradorCodigoMIPS:
    def __init__(self, arvore_sintatica):
        self.arvore_sintatica = arvore_sintatica
        self.codigo_mips = []  # Lista para armazenar as instruções MIPS
        self.registradores = {"$t0", "$t1", "$t2", "$t3", "$t4", "$t5", "$t6", "$t7"}  # Registradores temporários
        self.registrador_atual = 0  # Índice do próximo registrador temporário a ser usado
        self.variaveis = {}  # Mapeia variáveis para registradores ou memória
        self.rotulo_count = 0  # Contador para gerar rótulos únicos

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
        elif no.type == "CMD":
            self.visitar_cmd(no)
        elif no.type == "EXP":
            return self.visitar_exp(no)
        elif no.type == "CHAMADA_FUNCAO":
            return self.visitar_chamada_funcao(no)
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
        for filho in no.children:
            self.visitar(filho)
        self.codigo_mips.append("jr $ra")  # Retorna ao sistema operacional

    def visitar_var(self, no):
        """
        Visita o nó VAR (declaração de variável) e armazena no dicionário de variáveis.
        """
        nome_var = no.children[1].value  # O segundo filho é o nome da variável
        registrador = f"$t{self.registrador_atual}"
        self.registrador_atual += 1
        self.variaveis[nome_var] = registrador  # Armazena a variável no dicionário


    def gerar_label(self):
        """
        Gera um rótulo único para uso em desvios condicionais.
        """
        self.rotulo_count += 1
        return f"label{self.rotulo_count}"

    def visitar_cmd(self, no):
        """
        Visita o nó CMD (comando).
        """
        if no.children[0].value == "System.out.println":
            valor = self.visitar_exp(no.children[2])
            self.codigo_mips.append(f"li $v0, 1")  # Código para imprimir inteiro
            self.codigo_mips.append(f"move $a0, {valor}")
            self.codigo_mips.append("syscall")
            self.codigo_mips.append("li $v0, 11")  # Código para imprimir nova linha
            self.codigo_mips.append("li $a0, 10")
            self.codigo_mips.append("syscall")
        elif no.children[0].type == "IDENTIFIER":
            nome_var = no.children[0].value
            valor = self.visitar_exp(no.children[2])
            self.codigo_mips.append(f"move {self.variaveis[nome_var]}, {valor}")
        elif no.children[0].value == "if":
            # Gera código para o comando if
            registrador = self.visitar_exp(no.children[2])  # Avalia a condição do if
            label_else = self.gerar_label()  # Gera um rótulo para o bloco else
            label_fim = self.gerar_label()  # Gera um rótulo para o fim do if

            # Verifica a condição e pula para o bloco else se for falsa
            self.codigo_mips.append(f"beq $zero, {registrador}, {label_else}")

            # Gera código para o bloco then
            self.visitar_cmd(no.children[4])  # Visita o bloco then
            self.codigo_mips.append(f"j {label_fim}")  # Pula para o fim do if

            # Gera código para o bloco else
            self.codigo_mips.append(f"{label_else}:")
            if len(no.children) > 6:  # Verifica se há um bloco else
                self.visitar_cmd(no.children[6])  # Visita o bloco else

            # Rótulo para o fim do if
            self.codigo_mips.append(f"{label_fim}:")
        elif no.children[0].value == "return":
            # Gera código para o comando return
            registrador = self.visitar_exp(no.children[1])  # Avalia a expressão de retorno
            self.codigo_mips.append(f"move $v0, {registrador}")  # Move o resultado para $v0
            self.codigo_mips.append("jr $ra")  # Retorna ao chamador
        

    def visitar_classe(self, no):
        """
        Visita o nó CLASSE e gera código MIPS correspondente.
        """
        # Obtém o nome da classe (opcional, pode ser útil para depuração)
        nome_classe = no.children[1].value if len(no.children) > 1 else "UnnamedClass"
        print(f"Processando classe: {nome_classe}")  # Para depuração

        # Percorre os nós filhos da classe
        for filho in no.children:
            if filho.type == "METODO":
                self.visitar_metodo(filho)  # Processa métodos da classe
            elif filho.type == "VAR":
                self.visitar_var(filho)  # Processa variáveis da classe
            # Adicione mais casos conforme necessário (por exemplo, construtores)

    def visitar_metodo(self, no):
        """
        Visita o nó METODO e gera código MIPS correspondente.
        """
        # Obtém o nome do método
        nome_metodo = no.children[2].value  # O terceiro filho é o nome do método
        print(f"Processando método: {nome_metodo}")  # Para depuração

        # Adiciona o rótulo do método no código MIPS
        self.codigo_mips.append(f"{nome_metodo}:")

        # Aloca espaço na pilha para variáveis locais
        # Aqui, assumimos que cada variável local ocupa 4 bytes (ajuste conforme necessário)
        num_variaveis_locais = sum(1 for filho in no.children if filho.type == "VAR")
        espaco_pilha = num_variaveis_locais * 4
        if espaco_pilha > 0:
            self.codigo_mips.append(f"addiu $sp, $sp, -{espaco_pilha}")  # Aloca espaço na pilha

        # Processa os parâmetros do método (se houver)
        for filho in no.children:
            if filho.type == "PARAMS":
                for param in filho.children:
                    if param.type == "TIPO" and (param.children[0].type == "IDENTIFIER" or param.children[0].type == "RESERVED_WORD"):
                        nome_param = param.children[0].value
                        self.variaveis[nome_param] = f"{espaco_pilha}($sp)"  # Armazena o parâmetro na pilha

        # Processa as variáveis locais
        for filho in no.children:
            if filho.type == "VAR":
                nome_var = filho.children[1].value
                self.variaveis[nome_var] = f"{espaco_pilha}($sp)"  # Armazena a variável na pilha
                espaco_pilha -= 4  # Atualiza o offset da pilha

        # Processa os comandos do método
        for filho in no.children:
            if filho.type == "CMD":
                self.visitar_cmd(filho)

        # Desaloca espaço na pilha ao final do método
        if espaco_pilha > 0:
            self.codigo_mips.append(f"addiu $sp, $sp, {espaco_pilha}")

        # Adiciona a instrução de retorno
        self.codigo_mips.append("jr $ra")  # Retorna ao chamador

    def visitar_exp(self, no):
        if no.type == "EXP":
            return self.visitar_exp(no.children[0])  # Visita o filho REXP
        elif no.type == "REXP":
            return self.visitar_exp(no.children[0])  # Visita o filho AEXP
        elif no.type == "AEXP":
            return self.visitar_exp(no.children[0])  # Visita o filho MEXP
        elif no.type == "MEXP":
            return self.visitar_exp(no.children[0])  # Visita o filho SEXP
        elif no.type == "SEXP":
            return self.visitar_exp(no.children[0])  # Visita o filho PEXP
        elif no.type == "INTEGER":
            valor = no.value
            registrador = f"$t{self.registrador_atual}"
            self.registrador_atual += 1
            self.codigo_mips.append(f"li {registrador}, {valor}")
            self.variaveis['num'] = int(valor)
            return registrador
        elif no.type == "PEXP":
            if no.children[0].type == "INTEGER":
                valor = no.children[0].value
                registrador = f"$t{self.registrador_atual}"
                self.registrador_atual += 1
                self.codigo_mips.append(f"li {registrador}, {valor}")
                return registrador
            elif no.children[0].type == "IDENTIFIER":
                nome_var = no.children[0].value
                if nome_var in self.variaveis:
                    return self.variaveis[nome_var]  # Retorna o registrador da variável
                else:
                    # Variável não encontrada: gera um erro ou assume um valor padrão
                    raise ValueError(f"Variável '{nome_var}' não declarada.")
            elif no.children[0].type == "RESERVED_WORD" and no.children[0].value == "new":
                # Trata a criação de um novo objeto e a chamada de método
                registrador = f"$t{self.registrador_atual}"
                self.registrador_atual += 1

                # 1. Criação do objeto (simplificado)
                self.codigo_mips.append(f"li {registrador}, 1")  # Assume um valor padrão para o objeto

                # 2. Processa a chamada de método (ComputeFac)
                # Encontra o nó da chamada de método na AST
                metodo_chamada = None
                for filho in no.children:
                    if filho.type == "IDENTIFIER":
                        metodo_chamada = filho
                        break

                if metodo_chamada:
                    # Processa os argumentos da chamada de método
                    for filho in no.children:
                        if filho.type == "EXPS":
                            # Visita a expressão do argumento (no caso, INTEGER: 10)
                            arg_registrador = self.visitar_exp(filho.children[0])
                            self.codigo_mips.append(f"move $a0, {arg_registrador}")  # Passa o argumento para $a0

                    # Chama o método ComputeFac
                    self.codigo_mips.append(f"jal ComputeFac")  # Chama o método
                    self.codigo_mips.append(f"move {registrador}, $v0")  # Armazena o resultado no registrador

                return registrador
            elif no.children[0].type == "OPERATOR":
                esquerda = self.visitar_exp(no.children[1])
                direita = self.visitar_exp(no.children[2])
                registrador = f"$t{self.registrador_atual}"
                self.registrador_atual += 1
                if no.children[0].value == "+":
                    self.codigo_mips.append(f"add {registrador}, {esquerda}, {direita}")
                elif no.children[0].value == "-":
                    self.codigo_mips.append(f"sub {registrador}, {esquerda}, {direita}")
                elif no.children[0].value == "*":
                    self.codigo_mips.append(f"mul {registrador}, {esquerda}, {direita}")
                elif no.children[0].value == "/":
                    self.codigo_mips.append(f"div {esquerda}, {direita}")
                    self.codigo_mips.append(f"mflo {registrador}")
                return registrador
        return None

    def visitar_chamada_funcao(self, no):
        """
        Visita o nó CHAMADA_FUNCAO e gera código MIPS para chamadas de função.
        """
        nome_funcao = no.children[0].value
        argumentos = no.children[1].children if len(no.children) > 1 else []

        # Passa os argumentos para os registradores $a0, $a1, etc.
        for i, arg in enumerate(argumentos):
            valor = self.visitar_exp(arg)
            self.codigo_mips.append(f"move $a{i}, {valor}")

        # Chama a função
        self.codigo_mips.append(f"jal {nome_funcao}")

        # O resultado é retornado em $v0
        registrador = f"$t{self.registrador_atual}"
        self.registrador_atual += 1
        self.codigo_mips.append(f"move {registrador}, $v0")
        return registrador