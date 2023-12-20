from extra_modules.results import ParseResult
from extra_modules.position import *
from extra_modules.Tokens import *
from extra_modules.Nodes import *
import extra_modules.Errors as err
import extra_modules.Warnings as wrn

# Parser

class Parser:
    def __init__(self, tokens):
        self.tokens: list[Token] = tokens
        self.tok_idx = -1
        self.advance()

    def advance(self):
        self.tok_idx += 1
        self.update_current_tok()
        #print(self.current_tok)
        return self.current_tok

    def reverse(self, amount=1):
        self.tok_idx -= amount
        self.update_current_tok()
        return self.current_tok
    
    def update_current_tok(self):
        if self.tok_idx >= 0 and self.tok_idx < len(self.tokens):
            self.current_tok = self.tokens[self.tok_idx]

    def parse(self):
        res = self.statements()
        if not res.error and self.current_tok.type != TT_EOF:
            print(self.current_tok.type, self.current_tok.value)
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '+', '-', '*' or '/'"
            ))
        return res
    
    ################
    
    def statements(self):
        res = ParseResult()
        statements = []
        pos_start = self.current_tok.pos_start.copy()

        while self.current_tok.type == TT_NEWLINE:
            res.register_adv()
            self.advance()

        statement = res.register(self.statement())
        if res.error: return res
        statements.append(statement)

        more_statements = True
        while True:
            newline_count = 0
            while self.current_tok.type == TT_NEWLINE:
                res.register_adv()
                self.advance()
                newline_count += 1
            
            if newline_count == 0:
                more_statements = False

            if not more_statements: break
            statement = res.try_register(self.statement())
            if not statement:
                self.reverse(res.to_reverse_count)
                more_statements = False
                continue
            statements.append(statement)

        return res.success(IterArrayNode(
            statements,
            pos_start,
            self.current_tok.pos_end.copy()
        ))
    
    def statement(self):
        res = ParseResult()
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.matches(TT_KEYWORD, 'return'):
            res.register_adv()
            self.advance()

            expr = res.try_register(self.expr())
            if not expr:
                self.reverse(res.to_reverse_count)
            return res.success(ReturnNode(expr, pos_start, self.current_tok.pos_start.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, 'continue'):
            res.register_adv()
            self.advance()
            return res.success(ContinueNode(pos_start, self.current_tok.pos_start.copy()))
        
        if self.current_tok.matches(TT_KEYWORD, 'break'):
            res.register_adv()
            self.advance()
            return res.success(BreakNode(pos_start, self.current_tok.pos_start.copy()))

        expr = res.register(self.expr())
        if res.error: return res.failure(err.InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected int, float, identifier, var, mut, const, 'return', 'continue', 'break', 'if', 'for', 'while', 'func', '+', '-', '(', '[', '{' or 'not'"
            ))
        
        return res.success(expr)

    def if_expr(self):
        res = ParseResult()
        all_cases = res.register(self.if_expr_cases('if'))
        if res.error: return res
        cases, else_case = all_cases
        return res.success(IfNode(cases, else_case))
    
    def if_expr_b(self):
        return self.if_expr_cases('elif')
    
    def if_expr_c(self):
        res = ParseResult()
        else_case = None

        if self.current_tok.matches(TT_KEYWORD, 'else'):
            res.register_adv()
            self.advance()

            if self.current_tok.type == TT_NEWLINE:
                res.register_adv()
                self.advance()

                statements = res.register(self.statements())
                if res.error: return res
                else_case = (statements, True)

                if self.current_tok.matches(TT_KEYWORD, 'end'):
                    res.register_adv()
                    self.advance()
                else:
                    return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'end'"
                    ))
            else:
                expr = res.register(self.statement())
                if res.error: return res
                else_case = (expr, False)

        return res.success(else_case)
    
    def if_expr_b_or_c(self):
        res = ParseResult()
        cases, else_case = [], None

        if self.current_tok.matches(TT_KEYWORD, 'elif'):
            all_cases = res.register(self.if_expr_b())
            if res.error: return res
            cases, else_case = all_cases
        else:
            else_case = res.register(self.if_expr_c())
            if res.error: return res
        
        return res.success((cases, else_case))

    def if_expr_cases(self, case_keyword):
        res = ParseResult()
        cases = []
        else_case = None

        if not self.current_tok.matches(TT_KEYWORD, case_keyword):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '{case_keyword}'"
            ))
        
        res.register_adv()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_adv()
            self.advance()

            statements = res.register(self.statements())
            if res.error: return res
            cases.append((condition, statements, True))

            if self.current_tok.matches(TT_KEYWORD, 'end'):
                res.register_adv()
                self.advance()
            else:
                all_cases = res.register(self.if_expr_b_or_c())
                if res.error: return res
                new_cases, else_case = all_cases
                cases.extend(new_cases)
        else:
            expr = res.register(self.statement())
            if res.error: return res
            cases.append((condition, expr, False))

            all_cases = res.register(self.if_expr_b_or_c())
            if res.error: return res
            new_cases, else_case = all_cases
            cases.extend(new_cases)
        
        return res.success((cases, else_case))

    def for_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'for'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'for'"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected identifier"
            ))
        
        var_name = self.current_tok
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_EQ:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected '='"
            ))
        
        res.register_adv()
        self.advance()

        start_value = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'to'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'to'"
            ))
        
        res.register_adv()
        self.advance()

        end_value = res.register(self.expr())
        if res.error: return res
        
        if self.current_tok.matches(TT_KEYWORD, 'step'):
            res.register_adv()
            self.advance()
            
            step_value = res.register(self.expr())
            if res.error: return res
        else:
            step_value = None

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_adv()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))
            
            res.register_adv()
            self.advance()

            return res.success(ForNode(var_name, start_value, end_value, step_value, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(ForNode(var_name, start_value, end_value, step_value, body, False))
    
    def while_expr(self):
        res = ParseResult()

        if not self.current_tok.matches(TT_KEYWORD, 'while'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'while'"
            ))
        
        res.register_adv()
        self.advance()

        condition = res.register(self.expr())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'then'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                f"Expected 'then'"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_NEWLINE:
            res.register_adv()
            self.advance()

            body = res.register(self.statements())
            if res.error: return res

            if not self.current_tok.matches(TT_KEYWORD, 'end'):
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    f"Expected 'end'"
                ))
            
            res.register_adv()
            self.advance()

            return res.success(WhileNode(condition, body, True))

        body = res.register(self.statement())
        if res.error: return res

        return res.success(WhileNode(condition, body, False))

    def power(self):
        return self.bin_op(self.reassign_expr, (TT_POW,), self.factor)

    def reassign_expr(self):
        res = ParseResult()
        primary = res.register(self.primary())
        if res.error: return res
        '''
        res.register_adv()
        self.advance()
        '''

        if self.current_tok.type == TT_EQ: # INEFFICIENT AST IN-PLACE EDITING BLACK MAGIC
            res.register_adv()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            
            if isinstance(primary, VarAccessNode): # Base case (case 1/4)
                primary.value_node = expr
                primary.pos_end = self.current_tok.pos_end

            elif isinstance(primary, ArrayViewNode): # Uh-oh case (case 2/4)
                primary.value_node = expr
                primary.pos_end = self.current_tok.pos_end

            elif isinstance(primary, MemberAccessNode): #Uh-oh case (case 3/4)
                primary.value_node = expr
                primary.pos_end = self.current_tok.pos_end
                
            else: # Error case (case 4/4)
                return res.failure(err.InvalidSyntaxError(
                    primary.pos_start, primary.pos_end,
                    "Invalid assignment target"
                ))
        '''
        elif self.current_tok.type == TT_COLON:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Type of a variable cannot be edited"
            ))
        '''
        
        #print(self.current_tok.type)
        return res.success(primary)
    
    def primary(self):
        res = ParseResult()

        highest = res.register(self.atom())
        if res.error: return res

        while self.current_tok.type in (TT_LPAREN, TT_LSQUARE, TT_DOT):
            if self.current_tok.type == TT_LPAREN:
                res.register_adv()
                self.advance()
                arg_nodes = []

                if self.current_tok.type == TT_RPAREN:
                    res.register_adv()
                    self.advance()
                else:
                    arg_nodes.append(res.register(self.expr()))
                    if res.error:
                        return res.failure(err.InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ')', int, float, identifier, var, mut, const, 'if', 'for', 'while', 'fun', '+', '-', '(', '[' or 'not'"
                        ))
                    
                    while self.current_tok.type == TT_COMMA:
                        res.register_adv()
                        self.advance()

                        arg_nodes.append(res.register(self.expr()))
                        if res.error: return res

                    if self.current_tok.type != TT_RPAREN:
                        return res.failure(err.InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ',' or ')'"
                        ))
                    
                    res.register_adv()
                    self.advance()

                highest = CallNode(highest, arg_nodes)
            elif self.current_tok.type == TT_LSQUARE:
                index_nodes = [None, None, None] # (idx 0):(idx 1):(idx 2)
                highest_index = -1
                while self.current_tok.type != TT_RSQUARE:
                    res.register_adv()
                    self.advance()
                    if highest_index == 2:
                        return res.failure(err.InvalidSyntaxError(
                                self.current_tok.pos_start, self.current_tok.pos_end,
                                "Too many splicing arguments (maximum is 3)"
                            ))
                    
                    highest_index += 1

                    index_nodes[highest_index] = res.register(self.comp_expr())
                    if res.error: return res

                    if self.current_tok.type == TT_RSQUARE:
                        if highest_index == 0:
                            res.register_adv()
                            self.advance()
                            pos_end = self.current_tok.pos_end
                            return res.success(ArrayViewNode(highest, index_nodes[0], pos_end))      
                        elif highest_index < 2:
                            return res.failure(err.InvalidSyntaxError(
                                self.current_tok.pos_start, self.current_tok.pos_end,
                                "Expected ':'"
                            ))

                pos_end = self.current_tok.pos_end
                res.register_adv()
                self.advance()

                highest = ArraySpliceNode(highest, index_nodes, pos_end)
            elif self.current_tok.type == TT_DOT:
                res.register_adv()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier (member name)"
                    ))
                member_name_tok = self.current_tok
                res.register_adv()
                self.advance()
                
                highest = MemberAccessNode(highest, member_name_tok)
        
        return res.success(highest)
    
    def atom(self):
        res = ParseResult()
        tok: Token = self.current_tok

        # INTS
        if tok.type == TT_INT:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'i'))
        
        elif tok.type == TT_LONGINT:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'l'))
        
        elif tok.type == TT_BIGINT:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'b'))
        
        # FLOATS
        elif tok.type == TT_HALF:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'h'))
        
        elif tok.type == TT_FLOAT:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'f'))
        
        elif tok.type == TT_DOUBLE:
            res.register_adv()
            self.advance()
            return res.success(NumberNode(tok, 'd'))
        
        # OTHERS
        elif tok.type == TT_STRING:
            res.register_adv()
            self.advance()
            return res.success(StringNode(tok))
        
        elif tok.type == TT_IDENTIFIER: 
            var_name_tok = tok
            res.register_adv()
            self.advance()
            return res.success(VarAccessNode(var_name_tok))
        
        elif tok.type == TT_LPAREN:
            res.register_adv()
            self.advance()
            expr = res.register(self.expr())
            if res.error: return res
            if self.current_tok.type == TT_RPAREN:
                res.register_adv()
                self.advance()
                return res.success(expr)
            else:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ')'"
                ))

        elif tok.type == TT_LSQUARE:
            iterarray_expr = res.register(self.iterarray_expr())
            if res.error: return res
            return res.success(iterarray_expr)
        
        elif tok.type == TT_LBRACE:
            numarray_expr = res.register(self.matrix_expr())
            if res.error: return res
            return res.success(numarray_expr)
        
        elif tok.matches(TT_KEYWORD, 'if'):
            if_expr = res.register(self.if_expr())
            if res.error: return res
            return res.success(if_expr)
        
        elif tok.matches(TT_KEYWORD, 'for'):
            for_expr = res.register(self.for_expr())
            if res.error: return res
            return res.success(for_expr)
        
        elif tok.matches(TT_KEYWORD, 'while'):
            while_expr = res.register(self.while_expr())
            if res.error: return res
            return res.success(while_expr)

        elif tok.matches(TT_KEYWORD, 'func'):
            func_def = res.register(self.func_def())
            if res.error: return res
            return res.success(func_def)

        return res.failure(err.InvalidSyntaxError(
            tok.pos_start, tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[', if', 'for', 'while' or 'func'"
        ))

    def iterarray_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LSQUARE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '['"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_RSQUARE:
            res.register_adv()
            self.advance()
        else:
            element_nodes.append(res.register(self.expr()))
            if res.error:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ']', int, float, identifier, var, mut, const, 'if', 'for', 'while', 'fun', '+', '-', '(', or 'not'"
                ))
            
            while self.current_tok.type == TT_COMMA:
                res.register_adv()
                self.advance()

                element_nodes.append(res.register(self.expr()))
                if res.error: return res

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected ',' or ']'"
                ))
            
            res.register_adv()
            self.advance()

        return res.success(IterArrayNode(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))
    
    def matrix_expr(self):
        res = ParseResult()
        subvector_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '{'"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_RBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Matrix must have a nesting depth of exactly 2"
            ))
        
        subvector_nodes.append(res.register(self.matrix_subvector_expr()))
        if res.error: return res

        while self.current_tok.type == TT_COMMA:
            res.register_adv()
            self.advance()

            subvector_nodes.append(res.register(self.matrix_subvector_expr()))
            if res.error: return res

        if self.current_tok.type != TT_RBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ',' or '}'"
            ))
        elif not all(map(lambda vn: len(vn.element_nodes) == len(subvector_nodes[0].element_nodes), subvector_nodes)):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "All subvectors in a matrix must have the same length"
            ))

        res.register_adv()
        self.advance()

        return res.success(MatrixNode(
            subvector_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def matrix_subvector_expr(self):
        res = ParseResult()
        element_nodes = []
        pos_start = self.current_tok.pos_start.copy()

        if self.current_tok.type != TT_LBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Matrix must have a nesting depth of exactly 2"
            ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_RBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Subvectors of a matrix cannot be empty"
            ))
        
        element_nodes.append(res.register(self.expr()))
        if res.error:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '}', int, float, identifier, var, mut, const, 'if', 'for', 'while', 'fun', '+', '-', '(', or 'not'"
            ))
        
        while self.current_tok.type == TT_COMMA:
            res.register_adv()
            self.advance()

            element_nodes.append(res.register(self.expr()))
            if res.error: return res

        if self.current_tok.type != TT_RBRACE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ',' or '}'"
            ))
        
        res.register_adv()
        self.advance()

        return res.success(MatrixSubvectorContainer(
            element_nodes,
            pos_start,
            self.current_tok.pos_end.copy()
        ))

    def factor(self):
        res = ParseResult()
        tok = self.current_tok

        if tok.type in (TT_PLUS, TT_MINUS, TT_COMPLEMENT):
            res.register_adv()
            self.advance()
            factor = res.register(self.factor())
            if res.error: return res
            return res.success(UnaryOpNode(tok, factor))

        return self.power()

    def term(self):
        return self.bin_op(self.factor, (TT_MUL, TT_MATMUL, TT_DIV))
    
    def arith_expr(self):
        return self.bin_op(self.term, (TT_PLUS, TT_MINUS))

    def comp_expr(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'not'):
            op_tok = self.current_tok
            res.register_adv()
            self.advance()

            node = res.register(self.comp_expr())
            if res.error: return res
            return res.success(UnaryOpNode(op_tok, node))
        
        node = res.register(self.bin_op(self.bitwise_expr, (TT_EE, TT_NE, TT_LT, TT_GT, TT_LTE, TT_GTE)))
        #print(None if not res.error else res.error.as_str())
        if res.error: return res.failure(err.InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected int, float, identifier, '+', '-', '(', '[' or 'not'"
        ))

        return res.success(node)
    
    def bitwise_expr(self):
        return self.bin_op(self.shift_expr, (TT_BITWISEAND, TT_BITWISEOR, TT_BITWISEXOR))
    
    def shift_expr(self):
        return self.bin_op(self.arith_expr, (TT_LEFTSHIFT, TT_RIGHTSHIFT))

    def expr(self):
        res = ParseResult()

        if (
            self.current_tok.matches(TT_KEYWORD, 'var')
            or self.current_tok.matches(TT_KEYWORD, 'mut')
            or self.current_tok.matches(TT_KEYWORD, 'const')
        ):
            var_def = res.register(self.var_def())
            if res.error: return res
            return res.success(var_def)
        
        elif self.current_tok.matches(TT_KEYWORD, 'typeof'):
            res.register_adv()
            self.advance()

            pos_start = self.current_tok.pos_start.copy()
            expr = res.register(self.expr())
            if res.error: return res 

            return res.success(TypifyNode(expr, pos_start, self.current_tok.pos_start.copy()))
        
        elif self.current_tok.matches(TT_KEYWORD, 'struct'):
            struct_def = res.register(self.struct_def())
            if res.error: return res
            return res.success(struct_def)
        
        elif self.current_tok.matches(TT_KEYWORD, 'del'):
            res.register_adv()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            
            var_name = self.current_tok
            res.register_adv()
            self.advance()
            
            if res.error: return res
            return res.success(VarRmNode(var_name))
        
        if self.current_tok.matches(TT_KEYWORD, 'protect'):
            res.register_adv()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier"
                ))
            
            var_name = self.current_tok
            res.register_adv()
            self.advance()
            
            if res.error: return res
            return res.success(VarProtectNode(var_name))

        node = res.register(self.bin_op(self.comp_expr, ((TT_KEYWORD, "and"), (TT_KEYWORD, "or"))))

        if res.error: return res.failure(err.InvalidSyntaxError(
            self.current_tok.pos_start, self.current_tok.pos_end,
            "Expected int, float, identifier, var, mut, const, 'if', 'for', 'while', 'func', '+', '-', '(', '[' or 'not'"
            ))
        return res.success(node)
    
    def var_def(self):
        res = ParseResult()

        if self.current_tok.matches(TT_KEYWORD, 'const'): 
            res.register_adv()
            self.advance()

            if not self.current_tok.matches(TT_KEYWORD, 'var'):
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected var"
                ))
            
            mode = 0
        elif self.current_tok.matches(TT_KEYWORD, 'mut'):
            res.register_adv()
            self.advance()

            if not self.current_tok.matches(TT_KEYWORD, 'var'):
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected var"
                ))
            
            mode = 1
        elif self.current_tok.matches(TT_KEYWORD, 'var'): mode = 2
        else:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected var, mut, or const"
            ))
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier"
            ))
        
        var_name = self.current_tok
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_COLON:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected colon"
            ))
        res.register_adv()
        self.advance()

        type_container = res.register(self.type_container([TT_EQ]))
        if res.error: return res
        
        res.register_adv()
        self.advance()
        expr = res.register(self.expr())
        if res.error: return res
        return res.success(VarAssignNode(var_name, expr, mode, type_container))

    def func_def(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, 'func'):
            return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'func'"
                ))
        
        res.register_adv()
        self.advance()

        if self.current_tok.type == TT_IDENTIFIER:
            var_name_tok = self.current_tok
            res.register_adv()
            self.advance()
        else:
            var_name_tok = None
            
        if self.current_tok.type != TT_LPAREN:
            return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '('"
                ))
            
        res.register_adv()
        self.advance()
        arg_prototypes = []

        if self.current_tok.type == TT_IDENTIFIER:
            arg_name = self.current_tok
            res.register_adv()
            self.advance()

            if self.current_tok.type != TT_COLON:
                return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ':'"
                    ))
            
            res.register_adv()
            self.advance()
            
            arg_type = res.register(self.type_container([TT_COMMA, TT_RPAREN]))
            if res.error: return res

            arg_prototypes.append((arg_name, arg_type)) #(arg_name, arg_type)

            while self.current_tok.type == TT_COMMA:
                res.register_adv()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(err.InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected identifier"
                        ))
                
                arg_name = self.current_tok
                res.register_adv()
                self.advance()

                if self.current_tok.type != TT_COLON:
                    return res.failure(err.InvalidSyntaxError(
                            self.current_tok.pos_start, self.current_tok.pos_end,
                            "Expected ':'"
                        ))
                
                res.register_adv()
                self.advance()
                
                arg_type = res.register(self.type_container([TT_COMMA, TT_RPAREN]))
                if res.error: return res

                arg_prototypes.append((arg_name, arg_type)) #(arg_name, arg_type)

            if self.current_tok.type != TT_RPAREN:
                return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ',' or ')'"
                    ))
        else:
            if self.current_tok.type != TT_RPAREN:
                return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier or ')'"
                    ))
            
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_ARROW:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected '->'"
            ))
        
        res.register_adv()
        self.advance()

        res_type_container = res.register(self.type_container([TT_COLON, TT_NEWLINE]))
        #print(self.current_tok.type, self.current_tok.value)
        if res.error: return res

        if self.current_tok.type == TT_COLON:
            res.register_adv()
            self.advance()
            body = res.register(self.expr())
            print(self.current_tok.type, self.current_tok.value, self.current_tok.pos_start)
            if res.error: return res

            return res.success(FuncDefNode(
                var_name_tok,
                arg_prototypes,
                res_type_container,
                body,
                True
            ))
        
        if self.current_tok.type != TT_NEWLINE:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected ':' or NEWLINE"
            ))
        
        res.register_adv()
        self.advance()

        body = res.register(self.statements())
        if res.error: return res

        if not self.current_tok.matches(TT_KEYWORD, 'end'):
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected 'end'"
            ))
        
        res.register_adv()
        self.advance()

        return res.success(FuncDefNode(
            var_name_tok,
            arg_prototypes,
            res_type_container,
            body,
            False
        )) 

    def struct_def(self):
        res = ParseResult()
        
        if not self.current_tok.matches(TT_KEYWORD, 'struct'):
            return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected 'struct'"
                ))
        
        pos_start = self.current_tok.pos_start.copy()
        
        res.register_adv()
        self.advance()

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier (structure name)"
                ))
        
        struct_name_tok = self.current_tok

        res.register_adv()
        self.advance()
        if self.current_tok.type != TT_LSQUARE:
            return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected '['"
                ))
            
        res.register_adv()
        self.advance()
        field_toks = []

        if self.current_tok.type == TT_IDENTIFIER:
            field_name_tok = self.current_tok
            res.register_adv()
            self.advance()

            if self.current_tok.type != TT_COLON:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected colon"
                ))
            res.register_adv()
            self.advance()

            field_type_node = res.register(self.type_container([TT_RSQUARE, TT_COMMA]))
            if res.error: return res

            field_toks.append([field_name_tok, field_type_node])

            while self.current_tok.type == TT_COMMA:
                res.register_adv()
                self.advance()

                if self.current_tok.type != TT_IDENTIFIER:
                    return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier (field name)"
                    ))
                
                field_name_tok = self.current_tok
                res.register_adv()
                self.advance()

                if self.current_tok.type != TT_COLON:
                    return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected colon"
                    ))
                res.register_adv()
                self.advance()
                
                field_type_node = res.register(self.type_container([TT_RSQUARE, TT_COMMA]))
                if res.error: return res

                field_toks.append([field_name_tok, field_type_node])

            if self.current_tok.type != TT_RSQUARE:
                return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected ',' or ']'"
                    ))
            pos_end = self.current_tok.pos_end.copy()
        else:
            if self.current_tok.type != TT_RSQUARE:
                return res.failure(err.InvalidSyntaxError(
                        self.current_tok.pos_start, self.current_tok.pos_end,
                        "Expected identifier or ']'"
                    ))
            pos_end = self.current_tok.pos_end.copy()
            wrn.StructureWarning(pos_start, pos_end, 'Structure does not have any fields')
            
        res.register_adv()
        self.advance()

        return res.success(
            StructAssignNode(
                struct_name_tok,
                field_toks,
                pos_start,
                pos_end
            )
        )

    def type_container(self, end_tok_types):
        res = ParseResult()

        type_toks = []

        if self.current_tok.type != TT_IDENTIFIER:
            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                "Expected identifier (type)"
            ))
                 
        type_toks.append(self.current_tok)
        res.register_adv()
        self.advance()

        while self.current_tok.type not in end_tok_types+[TT_EOF]:
            if self.current_tok.type != TT_BITWISEOR:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected bitwise OR"
                ))
            
            res.register_adv()
            self.advance()

            if self.current_tok.type != TT_IDENTIFIER:
                return res.failure(err.InvalidSyntaxError(
                    self.current_tok.pos_start, self.current_tok.pos_end,
                    "Expected identifier (type)"
                ))
                   
            type_toks.append(self.current_tok)
            res.register_adv()
            self.advance()

        if self.current_tok.type == TT_EOF:
            err_msg = f"Expected {', '.join([TOKEN_TYPE_TO_STRING[end_tok_type] for end_tok_type in end_tok_types[:-1]])}" if len(end_tok_types) > 1 else f"Expected {TOKEN_TYPE_TO_STRING[end_tok_types[0]]}"
            if len(end_tok_types) > 1: err_msg += f"or {TOKEN_TYPE_TO_STRING[end_tok_types[-1]]}"

            return res.failure(err.InvalidSyntaxError(
                self.current_tok.pos_start, self.current_tok.pos_end,
                err_msg
            ))

        return res.success(TypeContainerNode(type_toks))

    def bin_op(self, func_a, ops, func_b=None):
        if func_b == None: func_b = func_a

        res = ParseResult()
        left = res.register(func_a())
        if res.error: return res

        while self.current_tok.type in ops or (self.current_tok.type, self.current_tok.value) in ops:
            op_tok = self.current_tok
            res.register_adv()
            self.advance()
            right = res.register(func_b())
            if res.error: return res
            left = BinOpNode(left, op_tok, right)
            
        return res.success(left)