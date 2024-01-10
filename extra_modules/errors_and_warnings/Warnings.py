class Warning:
    def __init__(self, pos_start, pos_end, warning_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.warning_name = warning_name
        self.details = details

    def warn(self):
        result  = f'In File {self.pos_start.fn}, {"line" if (x:=self.pos_start.ln == self.pos_end.ln) else "lines"} {self.pos_start.ln + 1} {"to %s"%(self.pos_end.ln + 1) if not x else ""}:'
        result += f' {self.warning_name}: {self.details}'
        print('\n' + result + '\n')

def StructureWarning(pos_start, pos_end, details): Warning(pos_start, pos_end, 'Structure-Related Warning', details).warn()
def MultiFloatConstTableWarning(pos_start, pos_end, details): Warning(pos_start, pos_end, 'Float Constant Table Warning', details).warn()
def CopyWarning(pos_start, pos_end, details): Warning(pos_start, pos_end, 'Copy Warning', details).warn()