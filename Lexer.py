from token import Token
from keys import *


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
        return number

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
                return Token(OPEN_PARENTHESES)

            if self.current_char == ")":
                self.advance()
                return Token(CLOSE_PARENTHESES)


        return Token(EOF, EOF)
if __name__ == "__main__":
    lexer = Lexer("132 + 100")
    print(lexer.get_next_token())
    print(lexer.get_next_token())
    print(lexer.get_next_token())
    print(lexer.get_next_token())
    print(lexer.get_next_token())