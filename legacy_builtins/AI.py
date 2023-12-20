# Initalise

try:
    x = []
    x.append(MathBuiltInFunction)
    x.append(VecMathBuiltInFunction)
    x.append(MatMathBuiltInFunction)
    x.append(nNumArray)
    x.append(nnNumArray)
    x.append(math_c)
except NameError:
    del x
    raise err.RequiredModuleNotLoaded('"math" module is required for this module')
else:
    del x

to_be_pushed = []

global AIBuiltInFunction
global ActivationAIBuiltInFunction
global DActivationAIBuiltInFunction
global LossAIBuiltInFunction
global DLossAIBuiltInFunction
global AI_c

AI_c = ctypes.CDLL(os.path.dirname(os.path.abspath(__file__)) + '/legacy_builtins/AI.so')

AI_c.ai_freeM.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_int]
AI_c.d_softmax.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.POINTER(ctypes.c_double), ctypes.c_int]
AI_c.d_softmax.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_double))

# Define funcs & variables

class AIBuiltInFunction(BaseFunction):
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
        copy = AIBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<AI built-in function {self.name}>"
    
    # EXEC

    def execute_ai_math_map(self, exec_ctx):
        narray = exec_ctx.symbol_table.get_var('narray')
        func = exec_ctx.symbol_table.get_var('func')

        global r
        global ctx
        ctx = exec_ctx
        r = RTResult()

        if not isinstance(func, BaseFunction):
            return r.failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a function',
                        ctx
                    ))

        def x(i):
            global r
            global ctx
            return_value = r.register(func.execute([i])).set_pos(self.pos_start, self.pos_end).set_context(ctx)
            if r.should_return(): return r
            if not isinstance(return_value, Number):
                return r.failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Function must always return a number',
                        ctx
                    ))
            return Number(float(return_value))

        if isinstance(narray, nNumArray):
            mapped = list(map(x, narray.elements))

            if r.should_return(): return r
            return r.success(nNumArray(mapped))
        if isinstance(iterarray, nnNumArray):
            mapped = [IterArray(list(map(x, row.elements))) for row in narray.elements]

            if r.should_return(): return r
            return r.success(nnNumArray(mapped))

        return r.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nnNumArray or a nNumArray',
                exec_ctx
            ))
        
    execute_ai_math_map.arg_names = ['func', 'narray']

    def execute_ai_make_nna_zeroes(self, exec_ctx):
        _len = exec_ctx.symbol_table.get_var('len')

        if not isinstance(_len, Number) or not type(_len.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number (integer)',
                        ctx
                    ))
        
        return RTResult().success(nNumArray([Number(0.0)]*_len.value))

    execute_ai_make_nna_zeroes.arg_names = ['len']

    def execute_ai_make_nnna_zeroes(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        return RTResult().success(nnNumArray([IterArray([Number(0.0)]*c.value) for _ in range(r.value)]))

    execute_ai_make_nnna_zeroes.arg_names = ['rows', 'columns']

    def execute_ai_rand_uniform_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        minval = exec_ctx.symbol_table.get_var('minval')
        maxval = exec_ctx.symbol_table.get_var('maxval')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(minval, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (minimum value) must be a number (if in doubt, use -0.05)',
                        ctx
                    ))
        
        if not isinstance(maxval, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Fourth argument (maximum value) must be a number (if in doubt, use 0.05)',
                        ctx
                    ))
        
        return RTResult().success(nnNumArray([IterArray([Number(random.uniform(minval.value, maxval.value)) for _ in range(c.value)]) for _ in range(r.value)]))

    execute_ai_rand_uniform_init.arg_names = ['rows', 'columns', 'minval', 'maxval']

    def execute_ai_rand_normal_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        mean = exec_ctx.symbol_table.get_var('mean')
        stddev = exec_ctx.symbol_table.get_var('stddev')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(mean, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (mean) must be a number (if in doubt, use 0)',
                        ctx
                    ))
        
        if not isinstance(stddev, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Fourth argument (standard deviation) must be a number (if in doubt, use 0.05)',
                        ctx
                    ))
        
        return RTResult().success(nnNumArray([IterArray([Number(random.normalvariate(mean.value, stddev.value)) for _ in range(c.value)]) for _ in range(r.value)]))

    execute_ai_rand_normal_init.arg_names = ['rows', 'columns', 'mean', 'stddev']

    def execute_ai_glorot_uniform_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        n_inputs = exec_ctx.symbol_table.get_var('n_inputs')
        n_outputs = exec_ctx.symbol_table.get_var('n_outputs')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_inputs, Number) or not type(n_inputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (number of inputs) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_outputs, Number) or not type(n_outputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Fourth argument (number of outputs) must be a number (integer)',
                        ctx
                    ))
        
        limit = math.sqrt(6/(n_inputs.value + n_outputs.value))

        return RTResult().success(nnNumArray([[Number(random.uniform(-limit, limit)) for _ in range(c.value)] for _ in range(r.value)]))

    execute_ai_glorot_uniform_init.arg_names = ['rows', 'columns', 'n_inputs', 'n_outputs']

    def execute_ai_glorot_normal_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        n_inputs = exec_ctx.symbol_table.get_var('n_inputs')
        n_outputs = exec_ctx.symbol_table.get_var('n_outputs')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_inputs, Number) or not type(n_inputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (number of inputs) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_outputs, Number) or not type(n_outputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Fourth argument (number of outputs) must be a number (integer)',
                        ctx
                    ))
        
        stddev = math.sqrt(2/(n_inputs.value + n_outputs.value))

        return RTResult().success(nnNumArray([[Number(random.normalvariate(0, stddev)) for _ in range(c.value)] for _ in range(r.value)]))

    execute_ai_glorot_normal_init.arg_names = ['rows', 'columns', 'n_inputs', 'n_outputs']

    def execute_ai_he_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        n_inputs = exec_ctx.symbol_table.get_var('n_inputs')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_inputs, Number) or not type(n_inputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (number of inputs) must be a number (integer)',
                        ctx
                    ))
        
        stddev = math.sqrt(2/n_inputs.value)

        return RTResult().success(nnNumArray([[Number(random.normalvariate(0, stddev)) for _ in range(c.value)] for _ in range(r.value)]))

    execute_ai_he_init.arg_names = ['rows', 'columns', 'n_inputs', 'n_outputs']

    def execute_ai_lecun_init(self, exec_ctx):
        r = exec_ctx.symbol_table.get_var('rows')
        c = exec_ctx.symbol_table.get_var('columns')
        n_inputs = exec_ctx.symbol_table.get_var('n_inputs')

        if not isinstance(r, Number) or not type(r.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (rows) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(c, Number) or not type(c.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (columns) must be a number (integer)',
                        ctx
                    ))
        
        if not isinstance(n_inputs, Number) or not type(n_inputs.value) is int:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Third argument (number of inputs) must be a number (integer)',
                        ctx
                    ))
        
        stddev = math.sqrt(1/n_inputs.value)

        return RTResult().success(nnNumArray([[Number(random.normalvariate(0, stddev)) for _ in range(c.value)] for _ in range(r.value)]))

    execute_ai_lecun_init.arg_names = ['rows', 'columns', 'n_inputs', 'n_outputs']

class ActivationAIBuiltInFunction(BaseFunction): #TODO: OPTIMISE!!!!!
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
        copy = ActivationAIBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Activation AI built-in function {self.name}>"
    
    # EXEC

    def execute_ai_sigmoid_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        return RTResult().success(Number(1/(1 + math.exp(-(x.value)))))

    execute_ai_sigmoid_single.arg_names = ['x']

    def execute_ai_sigmoid_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))

        outarray = [IterArray([Number(1/(1 + math.exp(-(x.value)))) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))
    
    execute_ai_sigmoid_map.arg_names = ['nnnarray']
    
    def execute_ai_tanh_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        return RTResult().success(Number(math.tanh(x.value)))

    execute_ai_tanh_single.arg_names = ['x']

    def execute_ai_tanh_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))

        outarray = [IterArray([Number(math.tanh(x.value)) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_tanh_map.arg_names = ['nnnarray']

    def execute_ai_relu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        return RTResult().success(Number(max(0.0, float(x.value))))

    execute_ai_relu_single.arg_names = ['x']

    def execute_ai_relu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))

        outarray = [IterArray([Number(max(0.0, x.value)) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_relu_map.arg_names = ['nnnarray']

    def execute_ai_leaky_relu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (input) must be a number',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (if in doubt, choose 0.01, 0.2 (for shallow networks), and 0.3 (for deeper networks))',
                        ctx
                    ))
        
        return RTResult().success(Number(max(float(alpha.value*x.value), float(x.value))))

    execute_ai_leaky_relu_single.arg_names = ['x', 'alpha']

    def execute_ai_leaky_relu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (if in doubt, choose 0.01, 0.2 (for shallow networks), and 0.3 (for deeper networks))',
                        ctx
                    ))

        outarray = [IterArray([Number(max(alpha.value*x.value, x.value)) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_leaky_relu_map.arg_names = ['nnnarray', 'alpha']

    def execute_ai_elu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (input) must be a number',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (if in doubt, choose 1 (for deep networks), 0.1 (for shallow networks in some cases), and 0.3 (for small datasets in some cases))',
                        ctx
                    ))
        
        return RTResult().success(Number(alpha.value * (math.exp(x.value)-1) if float(x.value) < 0.0 else float(x.value)))

    execute_ai_elu_single.arg_names = ['x', 'alpha']

    def execute_ai_elu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (if in doubt, choose 1 (for deep networks), 0.1 (for shallow networks in some cases), and 0.3 (for small datasets in some cases))',
                        ctx
                    ))
        outarray = [IterArray([Number(alpha.value * (math.exp(x.value)-1) if x.value < 0.0 else x.value) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_elu_map.arg_names = ['nnnarray', 'alpha']

    def execute_ai_softplus_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        return RTResult().success(Number(math_c.ln(float(1 + math.exp(x.value)))))

    execute_ai_softplus_single.arg_names = ['x']

    def execute_ai_softplus_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        outarray = [IterArray([Number(math_c.ln(float(1 + math.exp(x.value)))) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_softplus_map.arg_names = ['nnnarray']

    def execute_ai_softmax_map(self, exec_ctx):
        nnarray = exec_ctx.symbol_table.get_var('nnarray')

        if not isinstance(nnarray, nNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nNumArray (vector)',
                        ctx
                    ))

        exp_x = list(map(lambda x: math.exp(x.value), nnarray.elements))

        sum_exp_x = sum(exp_x)

        outarray = [Number(i / sum_exp_x) for i in exp_x]

        return RTResult().success(nNumArray(outarray))

    execute_ai_softmax_map.arg_names = ['nnarray']

class DActivationAIBuiltInFunction(BaseFunction): #TODO: FIX!!!!!
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
        copy = DActivationAIBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Derived Activation AI built-in function {self.name}>"
    
    # EXEC

    def execute_ai_d_sigmoid_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        sig = lambda x: 1/(1 + math.exp(-(x.value)))

        return RTResult().success(Number(sig(x) * (1 - sig(x))))

    execute_ai_d_sigmoid_single.arg_names = ['x']

    def execute_ai_d_sigmoid_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        sig = lambda x: 1/(1 + math.exp(-(x.value)))

        outarray = [IterArray([Number(sig(x) * (1 - sig(x))) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))
    
    execute_ai_d_sigmoid_map.arg_names = ['nnnarray']
    
    def execute_ai_d_tanh_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        return RTResult().success(Number(math.tanh(x.value)**2))

    execute_ai_d_tanh_single.arg_names = ['x']

    def execute_ai_d_tanh_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))

        outarray = [IterArray([Number(math.tanh(x.value)**2) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_d_tanh_map.arg_names = ['nnnarray']

    def execute_ai_d_relu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
        
        return RTResult().success(Number(0.0 if float(x.value) < 0.0 else 1.0))

    execute_ai_d_relu_single.arg_names = ['x']

    def execute_ai_d_relu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))

        outarray = [IterArray([Number(0.0 if float(x.value) < 0.0 else 1.0) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_d_relu_map.arg_names = ['nnnarray']

    def execute_ai_d_leaky_relu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (input) must be a number',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (same as the normal function\'s alpha)',
                        ctx
                    ))
        
        return RTResult().success(Number(float(alpha.value) if float(x.value) < 0.0 else 1.0))

    execute_ai_d_leaky_relu_single.arg_names = ['x', 'alpha']

    def execute_ai_d_leaky_relu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (same as the normal function\'s alpha)',
                        ctx
                    ))

        outarray = [IterArray([Number(float(alpha.value) if float(x.value) < 0.0 else 1.0) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_d_leaky_relu_map.arg_names = ['nnnarray', 'alpha']

    def execute_ai_d_elu_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (input) must be a number',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (same as the normal function\'s alpha)',
                        ctx
                    ))
        return RTResult().success(Number(alpha.value*math.exp(x.value) if x.value < 0.0 else 1.0))

    execute_ai_d_elu_single.arg_names = ['x', 'alpha']

    def execute_ai_d_elu_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')
        alpha = exec_ctx.symbol_table.get_var('alpha')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        if not isinstance(alpha, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (alpha) must be a number (same as the normal function\'s alpha)',
                        ctx
                    ))

        outarray = [IterArray([Number(alpha.value*math.exp(x.value) if x.value < 0.0 else 1.0) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_d_elu_map.arg_names = ['nnnarray', 'alpha']

    def execute_ai_d_softplus_single(self, exec_ctx):
        x = exec_ctx.symbol_table.get_var('x')

        if not isinstance(x, Number):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a number',
                        ctx
                    ))
    
        return RTResult().success(Number(math_c.ln(1/(1 + math.exp(-(x.value))))))

    execute_ai_d_softplus_single.arg_names = ['x']

    def execute_ai_d_softplus_map(self, exec_ctx):
        nnnarray = exec_ctx.symbol_table.get_var('nnnarray')

        if not isinstance(nnnarray, nnNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Argument must be a nnNumArray (matrix)',
                        ctx
                    ))
        
        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        outarray = [IterArray([Number(math_c.ln(1/(1 + math.exp(-(x.value))))) for x in row]) for row in nnnarray.elements]

        return RTResult().success(nnNumArray(outarray))

    execute_ai_d_softplus_map.arg_names = ['nnnarray']

    def execute_ai_d_softmax_map(self, exec_ctx):
        vecin = exec_ctx.symbol_table.get_var('vecin')
        vecout = exec_ctx.symbol_table.get_var('vecout')

        if not isinstance(vecin, nNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument (input nNumArray) must be a nNumArray (vector)',
                        ctx
                    ))
        
        if not isinstance(vecout, nNumArray):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument (output nNumArray) must be a nNumArray (vector)',
                        ctx
                    ))
        
        if len(vecin) != len(vecout):
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First and second argument must have the same length (check if both nNumArrays are inputs and outputs of the same softmax function)',
                        ctx
            ))

        c_vecin = (ctypes.c_double * len(vecin))(*vecin.elements)
        c_vecout = (ctypes.c_double * len(vecout))(*vecout.elements)
        c_res = AI_c.d_softmax(c_vecin, c_vecout, len(vecin))
        result = [IterArray([Number(c_res[i][j]) for j in range(len(vecin))]) for i in range(len(vecin))]
        AI_c.ai_freeM(c_res, len(vecin))

        return RTResult().success(nnNumArray(result))

    execute_ai_d_softmax_map.arg_names = ['vecin', 'vecout']

class LossAIBuiltInFunction(BuiltInFunction): #TODO: add loss and regularisation
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
        copy = LossAIBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Loss AI built-in function {self.name}>"

    # EXEC

    def execute_ai_sse(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))

        error_vec, e = y_pred.sub_by(y_actual)
        if e: return res.failure(e)
        sse, e = error_vec.mult_by(error_vec)
        if e: return res.failure(e)

        return res.success(sse)

    execute_ai_sse.arg_names = ['y_pred', 'y_actual']
    
    def execute_ai_mse(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))

        error_vec, e = y_pred.sub_by(y_actual)
        if e: return res.failure(e)
        mse, e = error_vec.mult_by(error_vec)
        if e: return res.failure(e)
        mse, e = mse.div_by(len(y_actual))
        if e: return res.failure(e)

        return r.success(mse)

    execute_ai_mse.arg_names = ['y_pred', 'y_actual']

    def execute_ai_bin_ce(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, Number) or not (y_pred.value >= 0.0 and y_pred.value <= 1.0):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a number between the range of 0 to 1 (inclusive of 0 and 1) (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, Number) or not float(y_actual.value) in [0.0, 1.0]:
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a number that is either 0 or 1 (y_actual)',
                ctx
            ))

        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        return res.success(Number(-(y_actual * math_c.ln(float(y_pred)) + (1 - y_actual) * math_c.ln(float(1 - y_pred)))))

    execute_ai_bin_ce.arg_names = ['y_pred', 'y_actual']

    def execute_ai_cat_ce(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))
        
        if not all(map(lambda x: x >= 0.0 and x <= 1.0, y_pred)):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must only contain numbers between the range of 0 to 1 (inclusive of 0 and 1)',
                ctx
            ))
        
        if not all(map(lambda x: x in [0.0, 1.0], y_actual)):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must only contain numbers that are either 0 or 1',
                ctx
            ))

        math_c.ln.argtypes = [ctypes.c_double]
        math_c.ln.restype = ctypes.c_double

        loss = 0
        for i in range(len(y_pred)):
            loss -= y_actual.elements[i].value * math_c.ln(y_pred[i].value)
        return res.success(Number(loss))

    execute_ai_cat_ce.arg_names = ['y_pred', 'y_actual']

class DLossAIBuiltInFunction(BuiltInFunction): #TODO: add loss and regularisation
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
        copy = LossAIBuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<Derived Loss AI built-in function {self.name}>"

    # EXEC

    def execute_ai_d_sse(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))

        ds = []
        for ya, yp in zip(y_actual, y_pred):
            ds.append(Number(2 * (yp.value - ya.value)))

        return res.success(Number(ds))

    execute_ai_d_sse.arg_names = ['y_pred', 'y_actual']
    
    def execute_ai_d_mse(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))

        ds = []
        for ya, yp in zip(y_actual, y_pred):
            ds.append(Number(yp.value - ya.value))

        return r.success(nNumArray(ds))

    execute_ai_d_mse.arg_names = ['y_pred', 'y_actual']

    def execute_ai_d_bin_ce(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, Number) or not (y_pred.value >= 0.0 and y_pred.value <= 1.0):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a number between the range of 0 to 1 (inclusive of 0 and 1) (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, Number) or not float(y_actual.value) in [0.0, 1.0]:
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a number that is either 0 or 1 (y_actual)',
                ctx
            ))

        ds = []
        for ya, yp in zip(y_actual, y_pred):
            ds.append(Number((-ya.value / yp.value) + ((1 - ya.value) / (1 - yp.value))))

        return res.success(nNumArray(ds))

    execute_ai_d_bin_ce.arg_names = ['y_pred', 'y_actual']

    def execute_ai_d_cat_ce(self, exec_ctx):
        y_pred = exec_ctx.symbol_table.get_var('y_pred')
        y_actual = exec_ctx.symbol_table.get_var('y_actual')
        res = RTResult()

        if not isinstance(y_pred, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must be a nNumArray (y_pred)',
                ctx
            ))
        
        if not isinstance(y_actual, nNumArray):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'Second argument must be a nNumArray (y_actual)',
                ctx
            ))
        
        if len(y_pred) != len(y_actual):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First and second argument must have the same length',
                ctx
            ))
        
        if not all(map(lambda x: x >= 0.0 and x <= 1.0, y_pred)):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must only contain numbers between the range of 0 to 1 (inclusive of 0 and 1)',
                ctx
            ))
        
        if not all(map(lambda x: x in [0.0, 1.0], y_actual)):
            return res.failure(err.RTError(
                self.pos_start, self.pos_end,
                'First argument must only contain numbers that are either 0 or 1',
                ctx
            ))

        ds = []
        for ya, yp in zip(y_actual, y_pred):
            ds.append(Number(-ya.value/yp.value))
        return res.success(nNumArray(ds))

    execute_ai_d_cat_ce.arg_names = ['y_pred', 'y_actual']

#TODO: add regularisation!

to_be_pushed.append(('ai_math_map', AIBuiltInFunction('ai_math_map')))
to_be_pushed.append(('ai_make_nna_zeroes', AIBuiltInFunction('ai_make_nna_zeroes')))
to_be_pushed.append(('ai_make_nnna_zeroes', AIBuiltInFunction('ai_make_nnna_zeroes')))
to_be_pushed.append(('ai_rand_uniform_init', AIBuiltInFunction('ai_rand_uniform_init')))
to_be_pushed.append(('ai_rand_normal_init', AIBuiltInFunction('ai_rand_normal_init')))
to_be_pushed.append(('ai_glorot_uniform_init', AIBuiltInFunction('ai_glorot_uniform_init')))
to_be_pushed.append(('ai_glorot_normal_init', AIBuiltInFunction('ai_glorot_normal_init')))
to_be_pushed.append(('ai_he_init', AIBuiltInFunction('ai_he_init')))
to_be_pushed.append(('ai_lecun_init', AIBuiltInFunction('ai_lecun_init')))

to_be_pushed.append(('ai_sigmoid_single', ActivationAIBuiltInFunction('ai_sigmoid_single')))
to_be_pushed.append(('ai_sigmoid_map', ActivationAIBuiltInFunction('ai_sigmoid_map')))
to_be_pushed.append(('ai_tanh_single', ActivationAIBuiltInFunction('ai_tanh_single')))
to_be_pushed.append(('ai_tanh_map', ActivationAIBuiltInFunction('ai_tanh_map')))
to_be_pushed.append(('ai_relu_single', ActivationAIBuiltInFunction('ai_relu_single')))
to_be_pushed.append(('ai_relu_map', ActivationAIBuiltInFunction('ai_relu_map')))
to_be_pushed.append(('ai_leaky_relu_single', ActivationAIBuiltInFunction('ai_leaky_relu_single')))
to_be_pushed.append(('ai_leaky_relu_map', ActivationAIBuiltInFunction('ai_leaky_relu_map')))
to_be_pushed.append(('ai_elu_single', ActivationAIBuiltInFunction('ai_elu_single')))
to_be_pushed.append(('ai_elu_map', ActivationAIBuiltInFunction('ai_elu_map')))
to_be_pushed.append(('ai_softplus_single', ActivationAIBuiltInFunction('ai_softplus_single')))
to_be_pushed.append(('ai_softplus_map', ActivationAIBuiltInFunction('ai_softplus_map')))
to_be_pushed.append(('ai_softmax_map', ActivationAIBuiltInFunction('ai_softmax_map')))

to_be_pushed.append(('ai_d_sigmoid_single', ActivationAIBuiltInFunction('ai_d_sigmoid_single')))
to_be_pushed.append(('ai_d_sigmoid_map', ActivationAIBuiltInFunction('ai_d_sigmoid_map')))
to_be_pushed.append(('ai_d_tanh_single', ActivationAIBuiltInFunction('ai_d_tanh_single')))
to_be_pushed.append(('ai_d_tanh_map', ActivationAIBuiltInFunction('ai_d_tanh_map')))
to_be_pushed.append(('ai_d_relu_single', ActivationAIBuiltInFunction('ai_d_relu_single')))
to_be_pushed.append(('ai_d_relu_map', ActivationAIBuiltInFunction('ai_d_relu_map')))
to_be_pushed.append(('ai_d_leaky_relu_single', ActivationAIBuiltInFunction('ai_d_leaky_relu_single')))
to_be_pushed.append(('ai_d_leaky_relu_map', ActivationAIBuiltInFunction('ai_d_leaky_relu_map')))
to_be_pushed.append(('ai_d_elu_single', ActivationAIBuiltInFunction('ai_d_elu_single')))
to_be_pushed.append(('ai_d_elu_map', ActivationAIBuiltInFunction('ai_d_elu_map')))
to_be_pushed.append(('ai_d_softplus_single', ActivationAIBuiltInFunction('ai_d_softplus_single')))
to_be_pushed.append(('ai_d_softplus_map', ActivationAIBuiltInFunction('ai_d_softplus_map')))
to_be_pushed.append(('ai_d_softmax_map', ActivationAIBuiltInFunction('ai_d_softmax_map')))

to_be_pushed.append(('ai_sse', LossAIBuiltInFunction('ai_sse')))
to_be_pushed.append(('ai_mse', LossAIBuiltInFunction('ai_mse')))
to_be_pushed.append(('ai_bin_ce', LossAIBuiltInFunction('ai_bin_ce')))
to_be_pushed.append(('ai_cat_ce', LossAIBuiltInFunction('ai_cat_ce')))

to_be_pushed.append(('ai_d_sse', DLossAIBuiltInFunction('ai_d_sse')))
to_be_pushed.append(('ai_d_mse', DLossAIBuiltInFunction('ai_d_mse')))
to_be_pushed.append(('ai_d_bin_ce', DLossAIBuiltInFunction('ai_d_bin_ce')))
to_be_pushed.append(('ai_d_cat_ce', DLossAIBuiltInFunction('ai_d_cat_ce')))

# Load funcs & variables
for symbol_table in SymbolTable.get_global_instances():
    for name, value in to_be_pushed:
        symbol_table.set_sys_var(name, value)