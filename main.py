from keys import *
from AST import *


class Token:

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f"Token({self.type}:{self.value})"


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
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
            self.error()

        return Token(EOF, EOF)


class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception("Syntax Error")

    def eat(self, type):
        print(f"type: {type}")
        print(f"current token type: {self.current_token.type}")
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


class Interpreter(NodeVisitor):

    def __init__(self, tree):
        self.tree = tree
        self.visit(tree)

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
if __name__ == "__main__":
    text = input("calc>")
    lexer = Lexer(text)
    pars = Parser(lexer).expr()
    interpreter = Interpreter(pars).visit_BinOp(pars)
    print(interpreter)