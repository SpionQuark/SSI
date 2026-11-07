from modules.helpers import Token
from modules.tokens import KEYWORDS
from modules.tokens import OPERATORS as special_keywords
from modules.helpers import SSIError

class Lexer:
    
    def __init__(self, source_code):
        self.KEYWORDS = KEYWORDS
        self.source_code = source_code
        self.position = 0
        self.line = 1
        self.current_char = self.source_code[self.position] if self.source_code else None

    def advance(self, steps=1):
        self.position += steps
        if self.position < len(self.source_code):
            self.current_char = self.source_code[self.position]
        else:
            self.current_char = None

    def peek(self):
        peek_pos = self.position + 1
        if peek_pos < len(self.source_code):
            return self.source_code[peek_pos]

    def skip_comment(self):
        while self.current_char is not None and self.current_char != '\n':
            self.advance()

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            if self.current_char == '\n':
                self.line += 1
            self.advance()

    def get_next_token(self):
        self.skip_whitespace()
        if self.current_char is None:
            return None

        if special_keywords.get(self.current_char) == "STRING":
            return self.read_string()

        if self.current_char in special_keywords or (self.peek() is not None and self.current_char + self.peek() in special_keywords):
            return self.read_operator()

        if self.current_char.isalpha() or self.current_char == '_':
            return self.read_word()
        
        if self.current_char.isdigit():
            return self.read_number()
        
        raise SSIError(f"Unexpected character {self.current_char!r}", self.line)
    
    def read_string(self):
        quote_char = self.current_char
        self.advance()
        start = self.position
        while self.current_char is not None:
            if self.current_char == quote_char:
                self.advance()
                return Token('STRING', self.source_code[start:self.position-1], self.line)
            if self.current_char == '\n':
                raise SSIError(f"Unterminated string literal", self.line)
            self.advance()
        if self.current_char != quote_char:
            raise SSIError(f"Unterminated (not closed) string literal", self.line)
        return Token('STRING', self.source_code[start:self.position], self.line)

    def read_operator(self):
        if self.peek() is not None and self.current_char + self.peek() in special_keywords:
            if self.current_char + self.peek() == "//":
                self.skip_comment()
                return None
            operator = self.current_char + self.peek()
            line = self.line
            self.advance(2)
            return Token(special_keywords[operator], operator, line)
        if self.current_char in special_keywords:
            operator = self.current_char
            self.advance()
            return Token(special_keywords[operator], operator, self.line)
        raise SSIError(f"Unknown operator {self.current_char}")


    def read_word(self):
        start = self.position
        while self.current_char is not None and (self.current_char.isalnum() or self.current_char == '_'):
            self.advance()
        word = self.source_code[start:self.position]
        print(word)
        if word in self.KEYWORDS:
            return Token(self.KEYWORDS[word], word, self.line)
        return Token('IDENTIFIER', word, self.line)

    def read_number(self):
        start = self.position
        seen_dot = False
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                if seen_dot:
                    raise SSIError("Invalid number: second decimal point", self.line)
                nxt = self.peek()
                if nxt is None or not nxt.isdigit():
                    raise SSIError("Invalid number: digit expected after decimal point", self.line)
                seen_dot = True
            self.advance()

        if self.current_char is not None and (self.current_char.isalpha() or self.current_char == '_'):
            raise SSIError("Invalid number: unexpected letter after digits", self.line)

        return Token('NUMBER', self.source_code[start:self.position], self.line)

    def tokenize(self, debug=False):
        tokens = []
        try:
            while self.current_char is not None:
                token = self.get_next_token()
                if token is not None:
                    tokens.append(token)
            tokens.append(Token('EOF', None, self.line))
            return tokens
        except SSIError as e:
            raise SSIError(f"Syntax error: {e}", e.line)
        