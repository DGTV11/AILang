# Initalise

to_be_pushed = []

global MathBuiltInFunction
global VecMathBuiltInFunction
global MatMathBuiltInFunction
global nNumArray
global nnNumArray
global math_c
math_c = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + '/legacy_builtins/math.so')

## C VECTORS
math_c.freeV.argtypes = [ctypes.POINTER(ctypes.c_double)]
math_c.addV2V.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
math_c.addV2V.restype = ctypes.POINTER(ctypes.c_double)
math_c.subVfV.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
math_c.subVfV.restype = ctypes.POINTER(ctypes.c_double)
math_c.mulVbV.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
math_c.mulVbV.restype = ctypes.c_double
math_c.mulNbV.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.c_double), ctypes.c_int]
math_c.mulNbV.restype = ctypes.POINTER(ctypes.c_double)

## C MATRICES
math_c.freeM.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.c_int]
math_c.gettranspose.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int)]
math_c.gettranspose.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
math_c.addM2M.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int)]
math_c.addM2M.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
math_c.subMfM.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int)]
math_c.subMfM.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
math_c.mulMbM.argtypes = [ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.POINTER(ctypes.c_int))]
math_c.mulMbM.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))
math_c.mulNbM.argtypes = [ctypes.c_double, ctypes.POINTER(ctypes.POINTER(ctypes.c_double)), ctypes.POINTER(ctypes.c_int)]
math_c.mulNbM.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

# Define funcs & variables

import math
import os

class nNumArray(Value): 
    def __init__(self, elements):
        super().__init__()
        self.elements = elements
    
    def add_by(self, other):
        if isinstance(other, nNumArray):
            self_elements = list(map(lambda x: x.value, self.elements))
            other_elements = list(map(lambda x: x.value, other.elements))
            new_len = max(len(self_elements), len(other_elements))
            while new_len > len(self_elements): self_elements.append(0.0)
            while new_len > len(other_elements): other_elements.append(0.0)

            c_vec1 = (ctypes.c_double * new_len)(*self_elements)
            c_vec2 = (ctypes.c_double * new_len)(*other_elements)
            c_res = math_c.addV2V(c_vec1, c_vec2, new_len)
            result = [Number(c_res[i]) for i in range(new_len)]
            math_c.freeV(c_res)

            return nNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        elif isinstance(other, nnNumArray):
            if other.get_shape()[1] != len(self.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            self_hdf = self.trans_to_nnNumArray()
            self_hdf.elements = self_hdf.elements[0] * other.get_shape()[0]
            return self_hdf.add_by(other), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def sub_by(self, other):
        if isinstance(other, nNumArray):
            self_elements = list(map(lambda x: x.value, self.elements))
            other_elements = list(map(lambda x: x.value, other.elements))
            new_len = max(len(self_elements), len(other_elements))
            while new_len > len(self_elements): self_elements.append(0.0)
            while new_len > len(other_elements): other_elements.append(0.0)

            c_vec1 = (ctypes.c_double * new_len)(*self_elements)
            c_vec2 = (ctypes.c_double * new_len)(*other_elements)
            c_res = math_c.subVfV(c_vec1, c_vec2, new_len)
            result = [Number(c_res[i]) for i in range(new_len)]
            math_c.freeV(c_res)

            return nNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        elif isinstance(other, nnNumArray):
            if other.get_shape()[1] != len(self.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            self_hdf = self.trans_to_nnNumArray()
            self_hdf.elements = self_hdf.elements[0] * other.get_shape()[0]
            return self_hdf.sub_by(other), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def mult_by(self, other): #snek ∫ (idk why I put this here)
        if isinstance(other, nNumArray):
            if len(self.elements) != len(self.elements): return None, Value.illegal_operation(self.pos_start, other.pos_end)
            self_elements = list(map(lambda x: x.value, self.elements))
            other_elements = list(map(lambda x: x.value, other.elements))
            _len = len(self.elements)

            c_vec1 = (ctypes.c_double * _len)(*self_elements)
            c_vec2 = (ctypes.c_double * _len)(*other_elements)
            c_res = math_c.mulVbV(c_vec1, c_vec2, _len)
            result = float(c_res)

            return Number(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        
        elif isinstance(other, nnNumArray):
            if other.get_shape()[0] != len(self.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            #Get dot of vector and matrix (turn to matrix then dot it)
            self_hdf = self.trans_to_nnNumArray()
            x, y = self_hdf.mult_by(other)
            return x, y
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def is_true(self):
        return len(self.elements) > 0
    
    def copy(self):
        copy = nNumArray(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def trans_to_nnNumArray(self):
        mat = nnNumArray(IterArray([self.elements]))
        mat.set_pos(self.pos_start, self.pos_end)
        mat.set_context(self.context)
        return mat
    
    def __str__(self):
        return f'nNumArray([{", ".join([str(x) for x in self.elements])}])'

    def __repr__(self):
        return f'nNumArray([{", ".join([str(x) for x in self.elements])}])'
    
    def __len__(self):
        return len(self.elements)
    
class nnNumArray(Value): #TODO: PLUG MEMORY LEAKS IF ANY AND REFACTOR SOON
    '''
    columns ->
    rows
    |
    V
    '''
    def __init__(self, elements):
        super().__init__()
        self.elements = elements

    def convert_to_c(self):
        elements       = self.get_elements()
        len_rows       = len(elements)
        len_columns    = len(elements[0])

        c_mat_init = (ctypes.c_double * len_columns * len_rows)()
        for i in range(len_rows):
            for j in range(len_columns):
                c_mat_init[i][j] = elements[i][j]

        c_mat = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))()
        c_mat.contents = (ctypes.POINTER(ctypes.c_double) * len_rows)(*c_mat_init)

        return c_mat, len_rows, len_columns
    
    def pad_n_convert(self, other):
        self_elements       = self.get_elements()
        other_elements      = other.get_elements()
        self_len_rows       = len(self_elements)
        self_len_columns    = len(self_elements[0])
        other_len_rows      = len(other_elements)
        other_len_columns   = len(other_elements[0])
        new_len_rows        = max(self_len_rows, other_len_rows)
        new_len_columns     = max(self_len_columns, other_len_columns)

        while new_len_columns > len(self_elements[0]): 
            for row in self_elements: row.append(0.0)
        while new_len_columns > len(other_elements[0]):
            for row in other_elements: row.append(0.0)

        while new_len_rows > len(self_elements): 
            self_elements.append([0.0]*new_len_columns)
        while new_len_rows > len(other_elements): 
            other_elements.append([0.0]*new_len_columns)

        c_mat1_init = (ctypes.c_double * new_len_columns * new_len_rows)()
        for i in range(new_len_rows):
            for j in range(new_len_columns):
                c_mat1_init[i][j] = self_elements[i][j]

        c_mat2_init = (ctypes.c_double * new_len_columns * new_len_rows)()
        for i in range(new_len_rows):
            for j in range(new_len_columns):
                c_mat2_init[i][j] = other_elements[i][j]

        c_mat1 = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))()
        c_mat1.contents = (ctypes.POINTER(ctypes.c_double) * self_len_rows)(*c_mat1_init)

        c_mat2 = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))()
        c_mat2.contents = (ctypes.POINTER(ctypes.c_double) * other_len_rows)(*c_mat2_init)

        c_dims = (ctypes.c_int * 2)(*[new_len_rows, new_len_columns])

        return c_mat1, c_mat2, c_dims, new_len_rows, new_len_columns

    def get_mat_transpose(self):
        c_mat, len_rows, len_columns = self.convert_to_c()
        c_dims = (ctypes.c_int * 2)(*[len_rows, len_columns])

        c_res = math_c.gettranspose(c_mat, c_dims)
        result = [IterArray([Number(c_res[i][j]) for j in range(len_rows)]) for i in range(len_columns)]
        math_c.freeM(c_res, len_columns)

        return nnNumArray(result).set_context(self.context).set_pos(self.pos_start, self.pos_end)

    def add_by(self, other): 
        if isinstance(other, nnNumArray):
            c_mat1, c_mat2, c_dims, new_len_rows, new_len_columns = self.pad_n_convert(other)

            c_res = math_c.addM2M(c_mat1, c_mat2, c_dims)
            result = [IterArray([Number(c_res[i][j]) for j in range(new_len_columns)]) for i in range(new_len_rows)]
            math_c.freeM(c_res, new_len_rows)

            return nnNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        elif isinstance(other, nNumArray):
            if self.get_shape()[1] != len(other.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            other_hdf = other.trans_to_nnNumArray()
            other_hdf.elements = other_hdf.elements[0] * self.get_shape()[0]
            return self.add_by(other_hdf), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def sub_by(self, other): 
        if isinstance(other, nnNumArray):
            c_mat1, c_mat2, c_dims, new_len_rows, new_len_columns = self.pad_n_convert(other)

            c_res = math_c.subMfM(c_mat1, c_mat2, c_dims)
            result = [IterArray([Number(c_res[i][j]) for j in range(new_len_columns)]) for i in range(new_len_rows)]
            math_c.freeM(c_res, new_len_rows)

            return nnNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        elif isinstance(other, nNumArray):
            if self.get_shape()[1] != len(other.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            other_hdf = other.trans_to_nnNumArray()
            other_hdf.elements = other_hdf.elements[0] * self.get_shape()[0]
            return self.sub_by(other_hdf), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def mult_by(self, other): #USE ZE DOT
        if isinstance(other, nnNumArray):
            self_elements       = self.get_elements()
            other_elements      = other.get_elements()
            self_len_rows       = len(self)[0]
            self_len_columns    = len(self)[1]
            other_len_rows      = len(other)[0]
            other_len_columns   = len(other)[1]

            if self_len_rows != other_len_columns: return None, Value.illegal_operation(self.pos_start, other.pos_end)

            c_mat1_init = (ctypes.c_double * self_len_columns * self_len_rows)()
            for i in range(self_len_rows):
                for j in range(self_len_columns):
                    c_mat1_init[i][j] = self_elements[i][j]

            c_mat2_init = (ctypes.c_double * other_len_columns * other_len_rows)()
            for i in range(other_len_rows):
                for j in range(other_len_columns):
                    c_mat2_init[i][j] = other_elements[i][j]

            c_mat1 = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))()
            c_mat1.contents = (ctypes.POINTER(ctypes.c_double) * self_len_rows)(*c_mat1_init)

            c_mat2 = (ctypes.POINTER(ctypes.POINTER(ctypes.c_double)))()
            c_mat2.contents = (ctypes.POINTER(ctypes.c_double) * other_len_rows)(*c_mat2_init)

            c_dims_init = (ctypes.c_int * 2 * 2)(*[[self_len_rows, self_len_columns], [other_len_rows, other_len_columns]])
            c_dims = (ctypes.POINTER(ctypes.POINTER(ctypes.c_int)))()
            c_dims.contents = (ctypes.POINTER(ctypes.c_int) * 2)(*c_dims_init)

            c_res = math_c.mulMbM(c_mat1, c_mat2, c_dims)
            result = [IterArray([Number(c_res[i][j]) for j in range(other_len_columns)]) for i in range(self_len_rows)]
            math_c.freeM(c_res, self_len_rows)

            return nnNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        elif isinstance(other, nNumArray):
            if self.get_shape()[1] != len(other.elements): 
                return None, Value.illegal_operation(self.pos_start, other.pos_end)
            other_hdf = other.trans_to_nnNumArray().get_mat_transpose()
            x, y = self.mult_by(other_hdf)
            return x, y
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def div_by(self, other):
        if isinstance(other, Number):
            number = float(1 / other.value)
            c_mat, len_rows, len_columns = self.convert_to_c()
                    
            c_dims = (ctypes.c_int * 2)(*[len_rows, len_columns])
            c_res = math_c.mulNbM(number, c_mat, c_dims)
            result = [IterArray([Number(c_res[i][j]) for j in range(len_columns)]) for i in range(len_rows)]
            math_c.freeM(c_res, len_rows)

            return nnNumArray(result).set_context(self.context).set_pos(self.pos_start, other.pos_end), None
        else:
            return None, Value.illegal_operation(self.pos_start, other.pos_end)
        
    def get_elements(self):
        return list(map(lambda row: list(map(lambda x: x.value, row.elements)), self.elements))

    def is_true(self):
        return len(self.elements) or len(self.elements[0])
    
    def copy(self):
        copy = nnNumArray(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        max_digits = max(
            [max([len(str(number)) for number in row.elements]) 
             for row in self.elements
            ]
        )
        

        formatted_rows = [f"[{', '.join([str(number).rjust(max_digits) for number in row.elements])}]" for row in self.elements]
        x = ',\n'
        return f"nnNumArray([\n{x.join(formatted_rows)}])"

    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return [len(self.elements), len(self.elements[0])] #rows, columns
    
    def get_shape(self):
        return [len(self.elements), len(self.elements[0])] #rows, columns

class MathBuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
        #frame = inspect.currentframe().f_back
        #info = inspect.getframeinfo(frame)
        #print(f'Object {self} created in file {info.filename} at line {info.lineno} function {info.function}')
    
    def execute(self, node, args):
        res = RTResult()
        self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method) 

        res.register(self.check_and_populate_args(node, method.arg_names, args))
        if res.should_return(): return res

        return_value = res.register(method(self.exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, exec_ctx):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = MathBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<mathematical built-in function {self.name}>"
    
    #EXECS
    
    def execute_math_ln(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        if number.value <= 0:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Value outside of domain',
                    exec_ctx
                ))
        
        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        return RTResult().success(Number(float(math_c.ln(float(number.value)))))

    execute_math_ln.arg_names = ['number']

    def execute_math_log(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        base = exec_ctx.symbol_table.get_var('base')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a number',
                    exec_ctx
                ))
        if number.value <= 0:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Value outside of domain',
                    exec_ctx
                ))

        if not isinstance(base, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Second argument must be a number',
                    exec_ctx
                ))
        if base.value <= 0:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Base outside of domain',
                    exec_ctx
                ))
        
        math_c.log_b.argtypes = [ctypes.c_double, ctypes.c_double]
        math_c.log_b.restype = ctypes.c_double
        
        return RTResult().success(Number(float(math_c.log_b(float(number.value), float(base.value)))))
    execute_math_log.arg_names = ['number', 'base']

    def execute_math_sin(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        return RTResult().success(Number(math.sin(number.value)))
    execute_math_sin.arg_names = ['number']

    def execute_math_cos(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        return RTResult().success(Number(math.cos(number.value)))
    execute_math_cos.arg_names = ['number']

    def execute_math_tan(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(math.tan(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'tan(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
    execute_math_tan.arg_names = ['number']

    def execute_math_csc(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(1/math.sin(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'csc(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
    execute_math_csc.arg_names = ['number']

    def execute_math_sec(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(1/math.cos(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'sec(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
    execute_math_sec.arg_names = ['number']

    def execute_math_cot(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(1/math.cot(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'cot(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
    execute_math_cot.arg_names = ['number']

    def execute_math_asin(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(math.asin(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'asin(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
        except ValueError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'asin(x) is undefined at {number.value}',
                    exec_ctx
                )
    execute_math_asin.arg_names = ['number']

    def execute_math_acos(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(math.acos(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'acos(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
        except ValueError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'acos(x) is undefined at {number.value}',
                    exec_ctx
                )
    execute_math_acos.arg_names = ['number']

    def execute_math_atan(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        return RTResult().success(Number(math.atan(number.value)))
    execute_math_atan.arg_names = ['number']

    def execute_math_sinh(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(math.sinh(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'sinh(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
    execute_math_sinh.arg_names = ['number']
        
    def execute_math_cosh(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(math.cosh(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'cosh(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
        except ValueError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'cosh(x) is undefined at {number.value}',
                    exec_ctx
                )
    execute_math_cosh.arg_names = ['number']

    def execute_math_tanh(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        return RTResult().success(Number(math.tanh(number.value)))
    execute_math_tanh.arg_names = ['number']
    
    def execute_math_csch(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(1/math.sinh(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'csch(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
        except ValueError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'csch(x) is undefined at {number.value}',
                    exec_ctx
                )
    execute_math_csch.arg_names = ['number']

    def execute_math_sech(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        return RTResult().success(Number(1/math.cosh(number.value)))
    execute_math_sech.arg_names = ['number']

    def execute_math_coth(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a number',
                    exec_ctx
                ))
        
        try:
            return RTResult().success(Number(1/math.tanh(number.value)))
        except ZeroDivisionError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'coth(x) has a vertical asymptote at {number.value}',
                    exec_ctx
                )
        except ValueError:
            return None, err.RTError(
                    self.pos_start, self.pos_end,
                    f'coth(x) is undefined at {number.value}',
                    exec_ctx
                )
    execute_math_coth.arg_names = ['number']

class VecMathBuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, node, args):
        res = RTResult()
        self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method) 

        res.register(self.check_and_populate_args(node, method.arg_names, args))
        if res.should_return(): return res

        return_value = res.register(method(self.exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

    def no_visit_method(self, exec_ctx):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = VecMathBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Vector mathematical built-in function {self.name}>"
    
    # EXEC

    def execute_math_ia2nna(self, exec_ctx):
        iterarray = exec_ctx.symbol_table.get_var('iterarray')
        if not isinstance(iterarray, IterArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be an IterArray',
                    exec_ctx
                ))
        
        for t in map(type, iterarray.elements):
            if t is not Number:
                return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument cannot be converted to an nNumArray (Non-numerical item found in elements)',
                    exec_ctx
                ))
        
        for n in iterarray.elements: n.value = float(n.value)
        return RTResult().success(nNumArray(iterarray.elements))
    execute_math_ia2nna.arg_names = ['iterarray']

    def execute_math_n2nna(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        repeats = exec_ctx.symbol_table.get_var('repeats')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a number',
                    exec_ctx
                ))
        if not isinstance(repeats, Number) or repeats.value <= 0:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Second argument must be a positive number',
                    exec_ctx
                ))
            
        return RTResult().success(nNumArray([number]*repeats.value))
    execute_math_n2nna.arg_names = ['number', 'repeats']

    def execute_math_nna2ia(self, exec_ctx):
        nnarray = exec_ctx.symbol_table.get_var('nnarray')
        if not isinstance(nnarray, nNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a nNumArray',
                    exec_ctx
                ))
        
        return RTResult().success(IterArray(nnarray.elements))
    execute_math_nna2ia.arg_names = ['nnarray']

    def execute_math_nna2nnna(self, exec_ctx):
        nnarray = exec_ctx.symbol_table.get_var('nnarray')
        if not isinstance(nnarray, nNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a nNumArray',
                    exec_ctx
                ))
        
        return RTResult().success(nnNumArray(IterArray([nnarray.elements])))
    execute_math_nna2nnna.arg_names = ['nnarray']

    def execute_math_mul_n_by_nna(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        nnarray = exec_ctx.symbol_table.get_var('nnarray')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a number',
                    exec_ctx
                ))
        if not isinstance(nnarray, nNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Second argument must be a nNumArray (vector)',
                    exec_ctx
                ))
        
        number = float(number.value)
        elements = [float(x.value) for x in nnarray.elements]
        c_vec = (ctypes.c_double * len(elements))(*elements)
        c_res = math_c.mulNbV(number, c_vec, len(elements))
        result = [Number(c_res[i]) for i in range(len(elements))]
        math_c.freeV(c_res)
            
        return RTResult().success(nNumArray(result))
    execute_math_mul_n_by_nna.arg_names = ['number', 'nnarray']

class MatMathBuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
    
    def execute(self, node, args):
        res = RTResult()
        self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method) 

        res.register(self.check_and_populate_args(node, method.arg_names, args))
        if res.should_return(): return res

        return_value = res.register(method(self.exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)

        '''
        VECTOR:
        res = RTResult()
        self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method) 

        res.register(self.check_and_populate_args(node, method.arg_names, args))
        if res.should_return(): return res

        return_value = res.register(method(self.exec_ctx))
        if res.should_return(): return res
        return res.success(return_value)
        '''

    def no_visit_method(self, exec_ctx):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = MatMathBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Matrix mathematical built-in function {self.name}>"
    
    # EXEC

    def execute_math_ia2nnna(self, exec_ctx):
        iterarray = exec_ctx.symbol_table.get_var('iterarray')
        if not isinstance(iterarray, IterArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be an IterArray',
                    exec_ctx
                ))
        
        x = None
        for t in iterarray.elements:
            if type(t) is IterArray:
                if x and x != len(t):
                    return RTResult().failure(err.RTError(
                            self.pos_start, self.pos_end,
                            'Argument cannot be converted to an nNumArray (Inconsistent row lengths)',
                            exec_ctx
                        ))
                x = len(t)
                for y in map(type, t.elements):
                    if y is not Number:
                        return RTResult().failure(err.RTError(
                            self.pos_start, self.pos_end,
                            'Argument cannot be converted to an nNumArray (Non-numerical item found in columns)',
                            exec_ctx
                        ))
            else:
                return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument cannot be converted to an nNumArray (IterArray not found in elements)',
                    exec_ctx
                ))
        
        for r in iterarray.elements: 
            for c in r.elements: 
                c.value = float(c.value)

        return RTResult().success(nnNumArray(iterarray.elements))
    execute_math_ia2nnna.arg_names = ['iterarray']

    def execute_math_n2nnna(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        repeats = exec_ctx.symbol_table.get_var('dims')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a number',
                    exec_ctx
                ))
        if not isinstance(repeats, IterArray) or len(repeats.elements) != 2:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Second argument must be an IterArray with two elements ([rows, columns])',
                    exec_ctx
                ))
            
        return RTResult().success(nnNumArray([IterArray([[number]*repeats.elements[1].value]) for _ in repeats.elements[0].value]))
    execute_math_n2nnna.arg_names = ['number', 'dims']

    def execute_math_nnna2nna(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a nnNumArray',
                    exec_ctx
                ))
        
        if len(nnnarray.elements) != 1:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must have only one row',
                    exec_ctx
                ))

        return RTResult().success(nNumArray(nnnarray.elements[0].elements))
    execute_math_nnna2nna.arg_names = ['nnnarray']

    def execute_math_nnna2ia(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a nnNumArray',
                    exec_ctx
                ))
        
        return RTResult().success(IterArray(nnnarray.elements))
    execute_math_nnna2ia.arg_names = ['nnnarray']

    def execute_math_mul_n_by_nnna(self, exec_ctx):
        number = exec_ctx.symbol_table.get_var('number')
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        if not isinstance(number, Number):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a number',
                    exec_ctx
                ))
        
        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Second argument must be a nnNumArray (matrix)',
                    exec_ctx
                ))
        
        number = float(number.value)
        c_mat, len_rows, len_columns = nnnarray.convert_to_c()
                
        c_dims = (ctypes.c_int * 2)(*[len_rows, len_columns])
        c_res = math_c.mulNbM(number, c_mat, c_dims)
        result = [IterArray([Number(c_res[i][j]) for j in range(len_columns)]) for i in range(len_rows)]
        math_c.freeM(c_res, len_rows)
            
        return RTResult().success(nnNumArray(result))
    execute_math_mul_n_by_nnna.arg_names = ['number', 'nnnarray']

    def execute_math_get_nnna_transp(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a nnNumArray (matrix)',
                    exec_ctx
                ))
        
        return RTResult().success(nnnarray.get_mat_transpose())
    execute_math_get_nnna_transp.arg_names = ['nnnarray']

    '''
TODO:
Determinant of a matrix
Inverse of a matrix
Adjugate of a matrix
Eigenvalues and eigenvectors of a matrix
Cofactors of a matrix
...
    '''

to_be_pushed.append(('math_ln', MathBuiltInFunction('math_ln')))
to_be_pushed.append(('math_log', MathBuiltInFunction('math_log')))
to_be_pushed.append(('math_sin', MathBuiltInFunction('math_sin')))
to_be_pushed.append(('math_cos', MathBuiltInFunction('math_cos')))
to_be_pushed.append(('math_tan', MathBuiltInFunction('math_tan')))
to_be_pushed.append(('math_csc', MathBuiltInFunction('math_tan')))
to_be_pushed.append(('math_sec', MathBuiltInFunction('math_sec')))
to_be_pushed.append(('math_cot', MathBuiltInFunction('math_cot')))
to_be_pushed.append(('math_asin', MathBuiltInFunction('math_asin')))
to_be_pushed.append(('math_acos', MathBuiltInFunction('math_acos')))
to_be_pushed.append(('math_atan', MathBuiltInFunction('math_atan')))
to_be_pushed.append(('math_sinh', MathBuiltInFunction('math_sinh')))
to_be_pushed.append(('math_cosh', MathBuiltInFunction('math_cosh')))
to_be_pushed.append(('math_tanh', MathBuiltInFunction('math_tanh')))
to_be_pushed.append(('math_csch', MathBuiltInFunction('math_csch')))
to_be_pushed.append(('math_sech', MathBuiltInFunction('math_sech')))
to_be_pushed.append(('math_coth', MathBuiltInFunction('math_coth')))

to_be_pushed.append(('math_ia2nna', VecMathBuiltInFunction('math_ia2nna')))
to_be_pushed.append(('math_n2nna', VecMathBuiltInFunction('math_n2nna')))
to_be_pushed.append(('math_nna2ia', VecMathBuiltInFunction('math_nna2ia')))
to_be_pushed.append(('math_nna2nnna', VecMathBuiltInFunction('math_nna2nnna')))
to_be_pushed.append(('math_mul_n_by_nna', VecMathBuiltInFunction('math_mul_n_by_nna')))

to_be_pushed.append(('math_ia2nnna', MatMathBuiltInFunction('math_ia2nnna')))
to_be_pushed.append(('math_n2nnna', MatMathBuiltInFunction('math_n2nnna')))
to_be_pushed.append(('math_nnna2ia', MatMathBuiltInFunction('nnna2ia')))
to_be_pushed.append(('math_nnna2nna', MatMathBuiltInFunction('nnna2nna')))
to_be_pushed.append(('math_mul_n_by_nnna', MatMathBuiltInFunction('math_mul_n_by_nnna')))
to_be_pushed.append(('math_get_nnna_transp', MatMathBuiltInFunction('math_get_nnna_transp')))

to_be_pushed.append(('math_pi', Number(math.pi)))
to_be_pushed.append(('math_e', Number(math.e)))

# Load funcs & variables
for symbol_table in SymbolTable.get_global_instances():
    for name, value in to_be_pushed:
        symbol_table.set_sys_var(name, value)