from keys import *
from AST import *


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}:{self.value})"


class Lexer:

    reserved_words = {
        "LET": Token(LET, LET),
        "AND": Token(AND, AND),
        "OR": Token(OR, OR),
        "IF": Token(IF, IF),
        "END": Token(END, END)
    }

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char:str = self.text[self.pos]

    def error(self):
        raise Exception("Invalid Parse")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def id(self):
        name = ""
        while self.current_char is not None and self.current_char.isalnum():
            name += self.current_char
            self.advance()
        return self.reserved_words.get(name.upper(), Token(ID, name))

    def number(self):
        number = ""
        while self.current_char is not None and self.current_char.isdigit():
            number += self.current_char
            self.advance()
        return int(number)

    def get_next_token(self):

        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_white_space()

            if self.current_char.isdigit():
                return Token(CONST_INTEGER, self.number())

            if self.current_char.isalnum():
                return self.id()

            if self.current_char == "+":
                self.advance()
                return Token(PLUS, "+")

            if self.current_char == "-":
                self.advance()
                return Token(MINUS, "-")

            if self.current_char == "*":
                self.advance()
                return Token(MULTIPLICATION, "*")

            if self.current_char == "/":
                self.advance()
                return Token(DIVISION, "/")

            if self.current_char == "(":
                self.advance()
                return Token(OPEN_PARENTHESES, '(')

            if self.current_char == ")":
                self.advance()
                return Token(CLOSE_PARENTHESES, ')')

            if self.current_char == ">":
                self.advance()
                return Token(MORE_THAN, '>')

            if self.current_char == "<":
                self.advance()
                return Token(LESS_THAN, '<')

            if self.current_char == "=":
                self.advance()
                return Token(ASSIGN, '=')

            if self.current_char == ",":
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == ":":
                self.advance()
                return Token(COLON, ':')

            self.error()

        return Token(EOF, EOF)


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Syntax Error")

    def eat(self, type):
        if self.current_token.type == type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        if self.current_token.type == CONST_INTEGER:
            token = self.current_token
            self.eat(CONST_INTEGER)
            return Num(token)

        elif self.current_token.type == OPEN_PARENTHESES:
            self.eat(OPEN_PARENTHESES)
            node = self.expr()
            self.eat(CLOSE_PARENTHESES)
            return node

    def term(self):

        node = self.factor()

        while self.current_token.type in (MULTIPLICATION, DIVISION):

            token = self.current_token
            if token.type is MULTIPLICATION:
                self.eat(MULTIPLICATION)

            if token.type is DIVISION:
                self.eat(DIVISION)

            node = BinOp(token, node, self.factor())

        return node

    def expr(self):

        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)

            if token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(token, node, self.term())
        return node

    def factor_expr(self):
        left = self.expr()
        op = self.current_token
        if op.type == MORE_THAN:
            self.eat(MORE_THAN)
        elif op.type == LESS_THAN:
            self.eat(LESS_THAN)
        right = self.expr()
        return Cond(left, op, right)

    def term_expr(self):
        node = self.factor_expr()
        while self.current_token.type in (AND, OR):
            token = self.current_token
            if token.type == AND:
                self.eat(AND)
            elif token.type == OR:
                self.eat(OR)
            node = CondOp(node, token, self.factor_expr())

        return node

    def cond_expr(self):

        node = self.term_expr()

        while self.current_token.type in (MORE_THAN, LESS_THAN):
            token = self.current_token
            if token.type == MORE_THAN:
                self.eat(MORE_THAN)
            elif token.type == LESS_THAN:
                self.eat(LESS_THAN)

            node = CondOp(node, token, self.term_expr())

        return node

    def program(self):
        return self.statements_list()

    def statements_list(self):
        statements_list = []

        while self.current_token.type in (IF, LET):
            token = self.current_token
            if token.type == IF:
                statements_list.append(self.selection_statement())

            if token.type == LET:
                statements_list.append(self.declaration_statement())

        return Program(statements_list)

    def declaration_statement(self):
        self.eat(LET)
        vdl = VarDecList()
        while self.current_token.type == ID:
            name = self.current_token.value
            self.eat(ID)
            self.eat(ASSIGN)
            node = VarDec(Var(name, self.current_token.value))
            self.eat(CONST_INTEGER)
            vdl.children.append(node)
            if self.current_token.type == COMMA:
                self.eat(COMMA)
                self.eat(LET)
        return vdl

    def selection_statement(self):
        self.eat(IF)
        cond = self.cond_expr()
        self.eat(COLON)
        statements_list = self.statements_list()

        return Selction(cond, statements_list)


class Interpreter(NodeVisitor):

    GLOBAL_SCOPE = dict()

    def __init__(self, tree):
        self.tree = tree
        self.visit_Program(tree)

    def visit_Program(self, tree):
        for node in tree.statements:
            self.visit(node)

    def visit_Selction(self, node):
        if self.visit(node.cond):
            self.visit(node.statements)

    def visit_BinOp(self, node):
        if node.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)

        if node.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)

        if node.type == MULTIPLICATION:
            return self.visit(node.left) * self.visit(node.right)

        if node.type == DIVISION:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, token):
        return token.value

    def visit_Cond(self, node):
        op = node.op
        if op.type == MORE_THAN:
            return True if self.visit(node.left) > self.visit(node.right) else False

    def visit_CondOp(self, node):
        if node.op.type == AND:
            if self.visit(node.left) and self.visit(node.right):
                return True
            else:
                return False
        elif node.op.type == OR:
            if self.visit(node.left) or self.visit(node.right):
                return True
            else:
                return False

    def visit_VarDecList(self, node):
        for dec in node.children:
            self.visit(dec)

    def visit_VarDec(self, node):
        self.GLOBAL_SCOPE[node.name] = node.value


if __name__ == "__main__":
    text = open("code.txt", "r").read()
    lexer = Lexer(text)
    pars = Parser(lexer).program()
    interpreter = Interpreter(pars)
    print(interpreter.GLOBAL_SCOPE)