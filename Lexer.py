from token import Token


class Lexer:

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_token = None
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception("Invalid Parse")

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.error()

    def skip_white_space(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

