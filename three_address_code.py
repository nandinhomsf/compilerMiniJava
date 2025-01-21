class ThreeAddressCodeGenerator:
    def __init__(self):
        self.temp_counter = 0
        self.code = []
        self.params = []
        self.dic = {}

    def new_temp(self):
        temp_name = f"t{self.temp_counter}"
        self.temp_counter += 1
        return temp_name

    def generate_code(self, node):
        if node.type == "PROG":
            for child in node.children:
                self.generate_code(child)
        elif node.type == "MAIN":
            nome_classe = self.generate_code(node.children[1])
            self.code.append(f"{nome_classe}:")
            self.generate_code(node.children[14])
        elif node.type == "CLASSE":
            nome_classe = node.children[1].value
            self.code.append(f"{nome_classe}:")
            for child in node.children[2:]:
                self.generate_code(child)
        elif node.type == "METODO":
            method_name = node.children[2].value
            self.code.append(f"{method_name}:")
            for child in node.children[3:]:
                print(child.type)
                self.generate_code(child)
            self.code.append("}")
        elif node.type == "PARAMS":
            param_name = node.children[1].value
            self.dic[param_name] = self.params[0]
            for i in range(3, len(node.children), 3):
                param_name = node.children[i].value
                self.dic[param_name] = self.params[i//3]
        elif node.type == "TIPO":
            return self.generate_code(node.children[0])
        elif node.type == "IDENTIFIER":
            if node.value in self.dic:
                return self.dic[node.value]
            return node.value
        elif node.type == "CMD":
            valor =""
            for child in node.children:
                if child.type == "IDENTIFIER":
                    valor+=self.new_temp() + " = "
                    continue
                aux = self.generate_code(child)
                if aux!=None:   valor+=aux
            if len(node.children)==7 and node.children[5].value == "else":  valor+="end_else"
            elif node.children[0] == "if":  valor+="end_if"
            elif node.children[0] == "while":  valor+="end_while"
            if valor!="":
                self.code.append(valor)
        elif node.value == "if":
            self.generate_if()
        elif node.value == "else":
            self.generate_else()
        elif node.value == "while":
            self.code.append("while:")
        elif node.value == "new":
            return self.generate_new()
        elif node.value == "System.out.println":
            return self.generate_print()
        elif node.value == "this":
            return node.value
        elif node.type == "INTEGER":    
            return node.value
        elif node.type == "EXPS":
            valor = ""
            for child in node.children:
                temp = self.new_temp()
                self.code.append(f"{temp} = {self.generate_code(child)}")
                self.params.append(temp)
                valor += temp + ", "
            valor = valor[:-2]
            return valor
        elif node.type == "EXP":
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            else:
                left_temp = self.generate_code(node.children[0])
                right_temp = self.generate_code(node.children[2])
                temp = self.new_temp()
                self.code.append(f"{temp} = {left_temp} {node.children[1].value} {right_temp}")
                return temp
        elif node.type == "REXP":
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            else:
                left_temp = self.generate_code(node.children[0])
                right_temp = self.generate_code(node.children[2])
                temp = self.new_temp()
                self.code.append(f"{temp} = {left_temp} {node.children[1].value} {right_temp}")
                return temp
        elif node.type == "AEXP":
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            elif node.value!=None: return node.value
            else:
                left_temp = self.generate_code(node.children[0])
                for i in range(0,len(node.children)-2,2):
                    right_temp = self.generate_code(node.children[i+2])
                    temp = self.new_temp()
                    self.code.append(f"{temp} = {left_temp} {node.children[i+1].value} {right_temp}")
                    left_temp = temp
                return temp
        elif node.type == "MEXP":
            if len(node.children) == 1:
                return self.generate_code(node.children[0])
            elif node.value!=None: return node.value
            else:
                left_temp = self.generate_code(node.children[0])
                for i in range(0,len(node.children)-2,2):
                    right_temp = self.generate_code(node.children[i+2])
                    temp = self.new_temp()
                    self.code.append(f"{temp} = {left_temp} {node.children[i+1].value} {right_temp}")
                    left_temp = temp
                return temp
        elif node.type == "SEXP":
            if len(node.children) == 1:
                if node.value!=None:
                    return node.value
                return self.generate_code(node.children[0])
            else:
                temp = self.new_temp()
                self.code.append(f"{temp} = {node.children[0].value} {self.generate_code(node.children[1])}")
                return temp
        elif node.type == "PEXP":
            if len(node.children) == 1:
                if node.children[0].type == "IDENTIFIER":
                    if node.children[0].value in self.dic:
                        return self.dic[node.children[0].value]
                    return self.new_temp()                 
                return node.value
            else:
                valor =""
                cont = 0
                for child in node.children:
                    if child.value == "(":
                        valor+=child.value
                        cont=1
                    elif cont>=2 or child.value == ")":
                        if child.value == ")":
                            valor+=child.value
                            cont = 0
                        else: cont=1
                        temp = self.new_temp()
                        self.code.append(f"{temp} = {valor}")
                        valor = temp
                    elif child.value == ".":
                        valor+=child.value
                    else:
                        cont+=1
                        valor+=self.generate_code(child)
                return temp

    def generate_if(self):
        self.code.append("if:")
    def generate_else(self):
        self.code.append("end_if")
        self.code.append("else:")
    def generate_print(self):
        return "print "
    def generate_new(self):
        return "new "

    def get_code(self):
        return "\n".join(self.code)