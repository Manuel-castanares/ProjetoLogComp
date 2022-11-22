from abc import abstractmethod
import abc
from ast import Num
import enum
import sys


reservados = ["Serve", "Rally", "Deuce", "In", "Out", "i32", "String", "ace", "return", "Court"]

class SymbolTable():
    def __init__(self):
        self.variaveis = {}
    def getIdentifier(self, ident):
        if(ident in self.variaveis.keys()):
            return self.variaveis[ident]
        else:
            raise Exception
    
    def setIdentifier(self, ident, value):
        if(ident in self.variaveis.keys()):
            if(value[0] == self.variaveis[ident][0]):
                temp = list(self.variaveis[ident])
                temp[1] = value[1]
                temp = tuple(temp)
                self.variaveis[ident] = temp
            else:
                raise Exception
        else:
            raise Exception

    def createIdentifier(self, type, ident):
        if(ident not in self.variaveis.keys()):
            self.variaveis[ident] = (type, None)
        else:
            raise Exception

class FuncTable():
    funcoes = {}
    def getFunc(ident):
        if(ident in FuncTable.funcoes.keys()):
            return FuncTable.funcoes[ident]
        else:
            raise Exception

    def createFunc(ident, type, funcao):
        if(ident not in FuncTable.funcoes.keys()):
            FuncTable.funcoes[ident] = (type, funcao)
        else:
            raise Exception

class Node():
    def __init__(self, value, children):
        pass

    def Evaluate(self):
        pass

class BinOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    def Evaluate(self, ST):
        primeiro = self.children[0].Evaluate(ST)
        segundo = self.children[1].Evaluate(ST)
        if(primeiro[0] == segundo[0]):
            if(self.value == "+"):
                result = ("i32",primeiro[1] + segundo[1])
            elif(self.value == "-"):
                result = ("i32",primeiro[1] - segundo[1])
            elif(self.value == "*"):
                result = ("i32",primeiro[1] * segundo[1])
            elif(self.value == "/"):
                result = ("i32",primeiro[1] // segundo[1])
            elif(self.value == "=="):
                result = ("i32", int(primeiro[1] == segundo[1]))
            elif(self.value == "<"):
                result = ("i32",int(primeiro[1] < segundo[1]))
            elif(self.value == ">"):
                result = ("i32",int(primeiro[1] > segundo[1]))
            elif(self.value == "&&"):
                result = ("i32",int(primeiro[1] and segundo[1]))
            elif(self.value == "||"):
                result = ("i32",int(primeiro[1] or segundo[1]))
            elif(self.value == "."):
                result = ("String",str(primeiro[1]) + str(segundo[1]))
        else:
            if(self.value == "."):
                result = ("String",str(primeiro[1]) + str(segundo[1]))
            else:
                raise Exception
        return result

class UnOp(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        result = 0
        if(self.value == "+"):
            result += self.children.Evaluate(ST)[1]
        elif(self.value == "-"):
            result -= self.children.Evaluate(ST)[1]
        elif(self.value == "!"):
            result = not self.children.Evaluate(ST)[1]
        return ("i32",result)

class IntVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = None
    
    def Evaluate(self, ST=None):
        return ("i32", self.value)

class StrVal(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = None
    
    def Evaluate(self, ST=None):
        return ("String", self.value)

class Assignment(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        ST.setIdentifier(self.children[0].value, self.children[1].Evaluate(ST))

class VarDec(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        i = 0
        while(i < len(self.children)):
            ST.createIdentifier(self.value, self.children[i].value)
            i += 1

class FuncCall(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    def Evaluate(self, StOriginal):
        funcao = FuncTable.getFunc(self.value)[1]
        if(len(funcao.children) != (len(self.children)+2)):
            raise Exception
        ST = SymbolTable()
        i = 0
        while(i < len(self.children)):
            funcao.children[i+1].Evaluate(ST)
            for child in funcao.children[i+1].children:
                a = self.children[i].Evaluate(StOriginal)
                ST.setIdentifier(child.value, a)
                i += 1
        result = funcao.children[-1].Evaluate(ST)
        return result


class FuncDec(Node):
    def __init__(self, children, type):
        self.value = "funcao"
        self.children = children
        self.type = type
    
    def Evaluate(self, ST=None):
        FuncTable.createFunc(self.children[0], self.type, self)

class Identifier(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = None
    
    def Evaluate(self, ST):
        return ST.getIdentifier(self.value)

class NoOp(Node):  
    def __init__(self, value, children):
        self.value = None
        self.children = None
    
    def Evaluate(self, ST=None):
        pass

class Print(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        print(self.children.Evaluate(ST)[1])

class Return(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        return self.children.Evaluate(ST)

class IfNode(Node):
    def __init__(self, value, children):
        self.value = None
        self.children = children
    
    def Evaluate(self, ST):
        if(self.children[0].Evaluate(ST)[1] == 1):
            self.children[1].Evaluate(ST)
        elif(len(self.children) == 3):
            self.children[2].Evaluate(ST)

class WhileNode(Node):
    def __init__(self, value, children):
        self.value = None
        self.children = children

    def Evaluate(self,ST):
        while(self.children[0].Evaluate(ST)[1] == 1):
            self.children[1].Evaluate(ST)

class Read(Node):
    def __init__(self, value, children):
        self.value = None
        self.children = None

    def Evaluate(self, ST=None):
        result = int(input())
        return ("i32",result)

class Block(Node):
    def __init__(self, value, children):
        self.value = value
        self.children = children
    
    def Evaluate(self, ST):
        for i in range(0, len(self.children)):
            if(self.children[i].value == "return"):
                return self.children[i].Evaluate(ST)
            else:
                self.children[i].Evaluate(ST)


class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

class PrePro:
    def filter(expressao):
        counter=0
        expressaonova = ""
        a = 0
        contador = 0
        checker = False
        final = 0
        for i in range(0, len(expressao)):
            if(counter != 2):
                if(expressao[i] == "/"):
                    counter+=1
                else:
                    counter=0
            else:
                a = i-2
                checker = True
                counter = 0
            if(expressao[i] == "\n" and checker):
                expressaonova += expressao[contador:a]
                contador = i
                checker = False
            if(expressao[i] == "}"):
                final = i
        expressaonova += expressao[contador:final+1]
        return expressaonova

class Tokenizer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.next = None
    
    def selectNext(self):
        if(self.position > len(self.source)-1):
            self.next = Token("EOF", "EOF")
        else:
            while(self.source[self.position] == "\n"):
                self.position += 1
            if(self.source[self.position] == " "):
                while(self.source[self.position] == " " or self.source[self.position] == "\n"):
                    self.position += 1
            if(self.source[self.position] == "+"):
                self.next = Token("PLUS", "+")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "-" and self.source[self.position+1] == ">"):
                self.next = Token("FLECHA", "->")
                self.position += 2
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "-"):
                self.next = Token("MINUS", "-")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "*"):
                self.next = Token("MULT", "*")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "/"):
                self.next = Token("DIV", "/")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "!"):
                self.next = Token("NOT", "!")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "<"):
                self.next = Token("SMALLER", "<")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == ">"):
                self.next = Token("GREATER", ">")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "."):
                self.next = Token("CONCAT", ".")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == ","):
                self.next = Token("COMMA", ",")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == ":"):
                self.next = Token("COLON", ":")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "("):
                self.next = Token("PARLEFT", "(")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == ")"):
                self.next = Token("PARRIGHT", ")")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position].isdigit()):
                numero = ""
                if self.source[self.position].isdigit():
                    while((self.position < len(self.source)) and self.source[self.position].isdigit()):
                        numero += self.source[self.position]
                        self.position += 1
                    while((self.position < len(self.source)) and self.source[self.position] == " "):
                        self.position += 1
                else:
                    while((self.position < len(self.source)) and self.source[self.position] == " "):
                        self.position += 1
                    while((self.position < len(self.source)) and self.source[self.position].isdigit()):
                        numero += self.source[self.position]
                        self.position += 1
                self.next = Token("INT", int(numero))
            elif(self.source[self.position] == '"'):
                palavra = ""
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] != '"'):
                    palavra += self.source[self.position]
                    self.position += 1
                self.position += 1
                self.next = Token("STRINGVALUE", palavra)
            elif(self.source[self.position].isalpha()):
                identificador = ""
                while((self.position < len(self.source)) and (self.source[self.position].isdigit() or self.source[self.position].isalpha() or self.source[self.position] == "_") and self.source[self.position] != ":"):
                        identificador += self.source[self.position]
                        self.position += 1
                if(identificador in reservados):
                    self.next = Token(identificador, identificador)
                else:
                    self.next = Token("identificador", identificador)
            elif(self.source[self.position] == "{"):
                self.next = Token("ABRECHAVE", "{")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "}"):
                self.next = Token("FECHACHAVE", "}")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == ";"):
                self.next = Token("PONTOEVIRGULA", ";")
                self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "|" and self.source[self.position+1] == "|"):
                self.next = Token("OR", "||")
                self.position += 2
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "&" and self.source[self.position+1] == "&"):
                self.next = Token("AND", "&&")
                self.position += 2
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            elif(self.source[self.position] == "="):
                if(self.source[self.position+1] == "="):
                    self.position += 2
                    self.next = Token("IGUALIGUAL", "==")
                else:
                    self.next = Token("IGUAL", "=")
                    self.position += 1
                while((self.position < len(self.source)) and self.source[self.position] == " "):
                    self.position += 1
            else:
                raise Exception

            

class Parser:
    tokenizer = None
    def RelExpression():
        result = 0
        result = Parser.parseExpression()
        while(Parser.tokenizer.next.type == "IGUALIGUAL" or Parser.tokenizer.next.type == "GREATER" or Parser.tokenizer.next.type == "SMALLER" or Parser.tokenizer.next.type == "CONCAT"):
            if(Parser.tokenizer.next.type == "IGUALIGUAL"):
                Parser.tokenizer.selectNext()
                num=Parser.parseExpression()
                result = BinOp("==", [result, num])
            elif(Parser.tokenizer.next.type == "GREATER"):
                Parser.tokenizer.selectNext()
                num=Parser.parseExpression()
                result = BinOp(">", [result, num])
            elif(Parser.tokenizer.next.type == "SMALLER"):
                Parser.tokenizer.selectNext()
                num=Parser.parseExpression()
                result = BinOp("<", [result, num])
            elif(Parser.tokenizer.next.type == "CONCAT"):
                Parser.tokenizer.selectNext()
                num=Parser.parseExpression()
                result = BinOp(".", [result, num])
        return result

    def parseExpression():
        result = 0
        result = Parser.parseTerm()
        while(Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "OR"):
            if(Parser.tokenizer.next.type == "PLUS"):
                Parser.tokenizer.selectNext()
                num=Parser.parseTerm()
                result = BinOp("+", [result, num])
            elif(Parser.tokenizer.next.type == "MINUS"):
                Parser.tokenizer.selectNext()
                num=Parser.parseTerm()
                result = BinOp("-", [result, num])
            elif(Parser.tokenizer.next.type == "OR"):
                Parser.tokenizer.selectNext()
                num=Parser.parseTerm()
                result = BinOp("||", [result, num])
        return result

    def parseTerm():
        result = 0
        result = Parser.parseFactor()
        while(Parser.tokenizer.next.type == "MULT" or Parser.tokenizer.next.type == "DIV" or Parser.tokenizer.next.type == "AND"):
            if(Parser.tokenizer.next.type == "MULT"):
                Parser.tokenizer.selectNext()
                num=Parser.parseFactor()
                result = BinOp("*", [result, num])
            elif(Parser.tokenizer.next.type == "DIV"):
                Parser.tokenizer.selectNext()
                num=Parser.parseFactor()
                result = BinOp("/", [result, num])
            elif(Parser.tokenizer.next.type == "AND"):
                Parser.tokenizer.selectNext()
                num=Parser.parseFactor()
                result = BinOp("&&", [result, num])
        return result

    def parseFactor():
        result = 0
        if(Parser.tokenizer.next.type == "INT"):
            result = IntVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
        elif(Parser.tokenizer.next.type == "STRINGVALUE"):
            result = StrVal(Parser.tokenizer.next.value, None)
            Parser.tokenizer.selectNext()
        elif(Parser.tokenizer.next.type == "identificador"):
            ident = Parser.tokenizer.next.value
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                childs = []
                while(Parser.tokenizer.next.type != "PARRIGHT"):
                    Expression = Parser.RelExpression()
                    childs.append(Expression)
                    if(Parser.tokenizer.next.type == "COMMA"):
                        Parser.tokenizer.selectNext()
                Parser.tokenizer.selectNext()
                result = FuncCall(ident, childs)
            else:
                result = Identifier(ident, None)
        elif(Parser.tokenizer.next.type == "Rally"):
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                if(Parser.tokenizer.next.type == "PARRIGHT"):
                    Parser.tokenizer.selectNext()
                    result = Read(None, None)
                else:
                    raise Exception
            else:
                raise Exception
        elif(Parser.tokenizer.next.type == "PLUS" or Parser.tokenizer.next.type == "MINUS" or Parser.tokenizer.next.type == "NOT" or Parser.tokenizer.next.type == "PARLEFT"):
            if(Parser.tokenizer.next.type == "PLUS"):
                Parser.tokenizer.selectNext()
                num = Parser.parseFactor()
                result = UnOp("+", num)
            elif(Parser.tokenizer.next.type == "MINUS"):
                Parser.tokenizer.selectNext()
                num = Parser.parseFactor()
                result = UnOp("-", num)
            elif(Parser.tokenizer.next.type == "NOT"):
                Parser.tokenizer.selectNext()
                num = Parser.parseFactor()
                result = UnOp("!", num)
            elif(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                result = Parser.RelExpression()
                if(Parser.tokenizer.next.type != "PARRIGHT"):
                    raise Exception
                Parser.tokenizer.selectNext()
        else:
            raise Exception
        return result

    def parseProgram():
        result = 0
        childs = []
        while(Parser.tokenizer.next.type != "EOF"):
            childs.append(Parser.declaration())
        mainNode = FuncCall("Main", [])
        childs.append(mainNode)
        result = Block("BLOCK", childs)
        return result

    def declaration():
        result = 0
        childs = []
        tipo = None
        if(Parser.tokenizer.next.type == "Court"):
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "identificador"):
                childs.append(Parser.tokenizer.next.value)
                Parser.tokenizer.selectNext()
                if(Parser.tokenizer.next.type == "PARLEFT"):
                    Parser.tokenizer.selectNext()
                    idents = []
                    while(Parser.tokenizer.next.type == "identificador"):
                        idents.append(Parser.tokenizer.next)
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.next.type == "COMMA"):
                            Parser.tokenizer.selectNext()
                        elif(Parser.tokenizer.next.type == "COLON"):
                            Parser.tokenizer.selectNext()
                            temp = VarDec(Parser.tokenizer.next.type, idents)
                            childs.append(temp)
                            idents = []
                            Parser.tokenizer.selectNext()
                            if(Parser.tokenizer.next.type == "COMMA"):
                                Parser.tokenizer.selectNext()
                        else:
                            raise Exception
                    if(Parser.tokenizer.next.type == "PARRIGHT"):
                        Parser.tokenizer.selectNext()
                        if(Parser.tokenizer.next.type == "FLECHA"):
                            Parser.tokenizer.selectNext()
                            tipo = Parser.tokenizer.next.type
                            Parser.tokenizer.selectNext()
                        childs.append(Parser.parseBlock())
                        result = FuncDec(childs, tipo)
                    else:
                        raise Exception
            else:
                raise Exception
        else:
            raise Exception
        return result


    def parseBlock():
        result = 0
        if(Parser.tokenizer.next.type == "ABRECHAVE"):
            Parser.tokenizer.selectNext()
            childs = []
            #Parser.tokenizer.selectNext()
            while(Parser.tokenizer.next.type != "FECHACHAVE"):
                childs.append(Parser.statement())
                #Parser.tokenizer.selectNext()
            result = Block("BLOCK", childs)
        else:
            raise Exception
        Parser.tokenizer.selectNext()
        return result

    def statement():
        if(Parser.tokenizer.next.type == "identificador"):
            leftnode = Parser.tokenizer.next
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "IGUAL"):
                Parser.tokenizer.selectNext()
                Expression = Parser.RelExpression()
                result = Assignment("=", [leftnode, Expression])
            elif(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                childs = []
                while(Parser.tokenizer.next.type != "PARRIGHT"):
                    Expression = Parser.RelExpression()
                    childs.append(Expression)
                    if(Parser.tokenizer.next.type == "COMMA"):
                        Parser.tokenizer.selectNext()
                Parser.tokenizer.selectNext()
                result = FuncCall(leftnode.value, childs)
        elif(Parser.tokenizer.next.type == "Serve"):
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                Expression = Parser.RelExpression()
                result = Print("Serve", Expression)
                if(Parser.tokenizer.next.type != "PARRIGHT"):
                    raise Exception
                else:
                    Parser.tokenizer.selectNext()
        elif(Parser.tokenizer.next.type == "ace"):
            Parser.tokenizer.selectNext()
            childs = []
            while(Parser.tokenizer.next.type == "identificador"):
                childs.append(Parser.tokenizer.next)
                Parser.tokenizer.selectNext()
                if(Parser.tokenizer.next.type == "COMMA"):
                    Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "COLON"):
                Parser.tokenizer.selectNext()
            else:
                raise Exception
            result = VarDec(Parser.tokenizer.next.type, childs)
            Parser.tokenizer.selectNext()
        elif(Parser.tokenizer.next.type == "return"):
            Parser.tokenizer.selectNext()
            Expression = Parser.RelExpression()
            result = Return("return", Expression)
        elif(Parser.tokenizer.next.type == "Deuce"):
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                Expression = Parser.RelExpression()
                if(Parser.tokenizer.next.type != "PARRIGHT"):
                    raise Exception
                else:
                    Parser.tokenizer.selectNext()
                    Statement = Parser.statement() #Chama block
                    result = WhileNode(None, [Expression, Statement])
                    return result
        elif(Parser.tokenizer.next.type == "In"):
            Parser.tokenizer.selectNext()
            if(Parser.tokenizer.next.type == "PARLEFT"):
                Parser.tokenizer.selectNext()
                Expression = Parser.RelExpression()
                if(Parser.tokenizer.next.type != "PARRIGHT"):
                    raise Exception
                else:
                    Parser.tokenizer.selectNext()
                    Statement = Parser.statement()
                    if(Parser.tokenizer.next.type == "Out"):
                        Parser.tokenizer.selectNext()
                        Statement_Else = Parser.statement()
                        result = IfNode(None, [Expression, Statement, Statement_Else])
                        return result
                    result = IfNode(None, [Expression, Statement])
                    return result
        elif(Parser.tokenizer.next.type == "PONTOEVIRGULA"):
            result = NoOp(None, None)
            Parser.tokenizer.selectNext()
            return result
        else:
            result = Parser.parseBlock()
            return result
        #Parser.tokenizer.selectNext()
        if(Parser.tokenizer.next.type == "PONTOEVIRGULA"):
            Parser.tokenizer.selectNext()
            return result
        else:
            raise Exception


    def run(code):
        Parser.tokenizer = Tokenizer(code)
        Parser.tokenizer.selectNext()
        result = Parser.parseProgram()
        if(Parser.tokenizer.next.type != "EOF"):
            raise Exception
        return result

def main():
    argumento = sys.argv[1]
    f = open("{0}".format(argumento), "r")
    line = f.read()
    f.close()
    argumentonovo = PrePro.filter(line)
    result = Parser.run(argumentonovo)
    St = SymbolTable()
    result.Evaluate(St)

if __name__ == "__main__":
    main()