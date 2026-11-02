class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line {self.line})"

class SSIError(Exception):
    def __init__(self, message, line):
        super().__init__(f"{message} (line {line})")
        self.line = line