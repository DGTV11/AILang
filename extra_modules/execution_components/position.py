class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        self.idx += 1
        self.col += 1

        if current_char == '\n':
            self.ln += 1
            self.col = 0

        return self
    
    def copy(self):
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
    
    def __str__(self):
        if '\n' in self.ftxt:
            ftxt = self.ftxt.split('\n')[self.ln]
            if self.ln == 0:
                return f"Position(idx={self.idx}, ln={self.ln}, col={self.col}, fn={self.fn}, ftxt=... {ftxt})"
            return f"Position(idx={self.idx}, ln={self.ln}, col={self.col}, fn={self.fn}, ftxt=... {ftxt} ...)"
        return f"Position(idx={self.idx}, ln={self.ln}, col={self.col}, fn={self.fn}, ftxt={self.ftxt})"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash((self.idx, self.ln, self.col, self.fn))
Position.system_pos = Position(-1, 0, -1, '<System>', '<UNREADABLE>')