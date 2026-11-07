class Token:
    def __init__(self, type, value, line):
        self.type = type
        self.value = value
        self.line = line

    def __repr__(self):
        return f"Token({self.type}, {self.value!r}, line {self.line})"

class SSIError(Exception):
    def __init__(self, message, line=-1):
        super().__init__(f"{message} (line {line if line > 0 else '-Internal-'})")
        self.line = line

class Empty():
    def __init__(self):
        pass

class Scope:
    def __init__(self, parent= None):
        self.variables = dict()
        self.parent = parent

    def get(self, name, line):
        if name in self.variables:
            return self.variables.get(name)
        if self.parent is not None:
            return self.parent.get(name)
        raise SSIError(f"Undefined variable {name}", line)
        
    def set(self, name, value, line=-1):
        self.variables[name] = value



def parse_output(i, t=None):
    res = None
    def r_t(nt):
        nonlocal t
        if t == None and not isinstance(t, nt):
            t = nt

    if isinstance(i, str):
        if str(i) == "True":
            r_t(str)
            res =  "true"
        if str(i) == "False":
            r_t(str)
            res =  "false"
    if isinstance(i, float):
        if i.is_integer():
            r_t(int)
            res =  round(i)
            
    if not res:
        res = i
    try:
        return t(res)
    except:
        return res

p_o = parse_output