#!/usr/local/bin/python3.12

# Credit to CodePulse and his videos! Base code here: https://github.com/davidcallanan/py-myopl-code

# Imports

from extra_modules.execution_components.context_and_datatypes import *
from extra_modules.execution_components.Lexer import Lexer
from extra_modules.execution_components.Parser import Parser
from extra_modules.execution_components.Interpreter import Interpreter

# import resource
import os
import sys
# import time
# import inspect #debug
    
# Load path

def load_path(progpath: str):
    out_path = []
    AILang_path = os.path.dirname(os.path.abspath(__file__))

    for f in os.listdir(AILang_path + '/builtins'):
        if (f.endswith(".ail") or f.endswith(".py")) and not f.startswith("."):
            out_path.append(AILang_path + '/builtins/' + f)
        elif os.path.isdir(AILang_path + '/builtins/' + f) and os.path.isfile(AILang_path + '/builtins/' + f + '/init.py'):
            out_path.append(AILang_path + '/builtins/' + f)

    for f in os.listdir(AILang_path + '/user_modules'):
        if (f.endswith(".ail") or f.endswith(".py")) and not f.startswith("."):
            out_path.append(AILang_path + '/user_modules/' + f)
        elif os.path.isdir(AILang_path + '/user_modules/' + f) and os.path.isfile(AILang_path + '/user_modules/' + f + '/init.py'):
            out_path.append(AILang_path + '/user_modules/' + f)

    if progpath is not None:
        for f in os.listdir(os.path.dirname(os.path.abspath(progpath))):
            if (f.endswith(".ail") or f.endswith(".py")) and not f.startswith("."):
                out_path.append(os.path.dirname(os.path.abspath(progpath)) + '/' + f)
            elif os.path.isdir(os.path.dirname(os.path.abspath(progpath)) + '/' + f) and os.path.isfile(os.path.dirname(os.path.abspath(progpath)) + '/' + f + '/init.py'):
                out_path.append(os.path.dirname(os.path.abspath(progpath)) + '/' + f)

    return out_path

# Run

global_symbol_table = SymbolTable()

# Types
global_symbol_table.set_sys_var('Any',                      Type.Any)
global_symbol_table.set_sys_var('Type',                     Type.Type)
global_symbol_table.set_sys_var('NullType',                 Type.Null)
global_symbol_table.set_sys_var('Integer',                  Type.Integer)
global_symbol_table.set_sys_var('Int32',                    Type.Int32)
global_symbol_table.set_sys_var('Int64',                    Type.Int64)
global_symbol_table.set_sys_var('UInt32',                   Type.UInt32)
global_symbol_table.set_sys_var('UInt64',                   Type.UInt64)
global_symbol_table.set_sys_var('Float16',                  Type.Float16)
global_symbol_table.set_sys_var('Float32',                  Type.Float32)
global_symbol_table.set_sys_var('Float64',                  Type.Float64)
global_symbol_table.set_sys_var('Float16Matrix',            Type.Float16Matrix)
global_symbol_table.set_sys_var('Float32Matrix',            Type.Float32Matrix)
global_symbol_table.set_sys_var('Float64Matrix',            Type.Float64Matrix)
global_symbol_table.set_sys_var('Int32Matrix',              Type.Int32Matrix)
global_symbol_table.set_sys_var('Int64Matrix',              Type.Int64Matrix)
global_symbol_table.set_sys_var('UInt32Matrix',             Type.UInt32Matrix)
global_symbol_table.set_sys_var('UInt64Matrix',             Type.UInt64Matrix)
global_symbol_table.set_sys_var('String',                   Type.String)
global_symbol_table.set_sys_var('IterArray',                Type.IterArray)
global_symbol_table.set_sys_var('Namespace',                Type.Namespace)
global_symbol_table.set_sys_var('Function',                 Type.Function)
global_symbol_table.set_sys_var('BuiltInFunction',          Type.BuiltInFunction)

# Null
global_symbol_table.set_sys_var('null',                     Null.null)

# Integers
global_symbol_table.set_sys_var('true',                     Integer.true)
global_symbol_table.set_sys_var('false',                    Integer.false)

# Built-in functions
global_symbol_table.set_sys_var('print',                    BuiltInFunction.print)
global_symbol_table.set_sys_var('stringify',                BuiltInFunction.stringify)
global_symbol_table.set_sys_var('print_without_end',        BuiltInFunction.print_without_end)
global_symbol_table.set_sys_var('get_float_sci_str',        BuiltInFunction.get_float_sci_str)
global_symbol_table.set_sys_var('input',                    BuiltInFunction.input)
global_symbol_table.set_sys_var('input_int',                BuiltInFunction.input_int)
global_symbol_table.set_sys_var('clear',                    BuiltInFunction.clear)
global_symbol_table.set_sys_var('terminal_prompt',          BuiltInFunction.terminal_prompt)
global_symbol_table.set_sys_var('exit',                     BuiltInFunction.exit)
global_symbol_table.set_sys_var('quit',                     BuiltInFunction.quit)
global_symbol_table.set_sys_var('push',                     BuiltInFunction.push)
global_symbol_table.set_sys_var('pop',                      BuiltInFunction.pop)
global_symbol_table.set_sys_var('len',                      BuiltInFunction.len)
global_symbol_table.set_sys_var('exec_prog',                BuiltInFunction.exec_prog)
global_symbol_table.set_sys_var('load_module',              BuiltInFunction.load_module)
global_symbol_table.set_sys_var('range',                    BuiltInFunction.range)
global_symbol_table.set_sys_var('map',                      BuiltInFunction.map)
global_symbol_table.set_sys_var('numerical_cast',           BuiltInFunction.numerical_cast)
global_symbol_table.set_sys_var('matrix_cast',              BuiltInFunction.matrix_cast)
global_symbol_table.set_sys_var('matrix_fill',              BuiltInFunction.matrix_fill)
global_symbol_table.set_sys_var('row_vector_to_matrix',     BuiltInFunction.row_vector_to_matrix)
global_symbol_table.set_sys_var('column_vector_to_matrix',  BuiltInFunction.column_vector_to_matrix)
global_symbol_table.set_sys_var('transpose_matrix',         BuiltInFunction.transpose_matrix)

def interpret(ast, progpath = None, st:SymbolTable = global_symbol_table, is_strict:bool = True):
    # Promote st
    st.promote()

    # Run prog
    _path = load_path(progpath)
    st.set_sys_var('__path__', IterArray(_path))
    interpreter = Interpreter()
    context = Context('<program>', strict_mode=is_strict)
    context.symbol_table = global_symbol_table
    result = interpreter.visit(ast.node, context)

    return result.value, result.error

def run(fn, text, progpath = None, st:SymbolTable = global_symbol_table, is_strict:bool = True):         
    # Generate tokens
    lexer = Lexer(fn, text)
    tokens, error = lexer.make_tokens()
    if error: return None, error

    # Generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error: return None, ast.error

    # Interpret
    return interpret(ast, progpath, st, is_strict)

def shell(strict_mode=True):
    print(f'Official AILang Shell (Python Implementation) ({"" if not strict_mode else "strict mode"})')
    while True:
        text = input('SHELL > ')
        if text.strip() == '': continue
        result, error = run('<stdin>', text, is_strict=strict_mode)

        if error: print(error.as_str())
        elif result:
            if len(result.elements) == 1:
                print(repr(result.elements[0]))
            else:
                print(repr(result))

'''
if __name__ == "__main__":
    fn = "/Volumes/Data stuffs/Python/AILang/Tests/test.ail"
    try:

            script = f.read()
    except Exception as e:
        raise IOError(f'Failed to load script "{fn}"\n' + str(e))
    
    _, error = run(fn, script, fn)

    if error:
        raise RuntimeError(f'Failed to finish executing script "{fn}"\n' + error.as_str())
    
'''
if __name__ == "__main__": #TODO: find way to add CLI decorators
    sys.set_int_max_str_digits(0)
    if len(sys.argv) == 1:
        shell()
    elif len(sys.argv) == 2:
        fn = sys.argv[1]
        try:
            with open(fn, 'r') as f:
                script = f.read()
        except Exception as e:
            raise IOError(f'Failed to load script "{fn}"\n' + str(e))
        
        _, error = run(fn, script, fn)

        if error:
            raise RuntimeError(f'Failed to finish executing script "{fn}"\n' + error.as_str())
        
    else:
        raise IndexError(f'Too many arguments (0 or 1 argument(s) expected, {len(sys.argv) - 1} given)')
