# Imports
from extra_modules.execution_components.position import Position
from extra_modules.execution_components.results import RTResult
from extra_modules.execution_components.context_and_datatypes import *
from extra_modules.execution_components.Tokens import *
from extra_modules.execution_components.Nodes import *
import extra_modules.errors_and_warnings.Errors as err
import extra_modules.c_apis.linalg as linalg
import extra_modules.errors_and_warnings.Warnings as wrn

# Interpreter

class Interpreter:
    def visit(self, node, context):
        method_name = f'visit_{type(node).__name__}'
        method = getattr(self, method_name, self.no_visit_method)
        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f'No visit_{type(node).__name__} method defined')

    ################

    def visit_NumberNode(self, node: NumberNode, context):
        number_type = node.type
        match number_type:
            # INTS
            case 'i':
                int_value = int(node.tok.value)
                if int_value > 2147483647:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}i is above the upper 32-bit integer limit of 2147483647",
                            context
                        )
                    )
                elif int_value < -2147483648:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}i is below the lower 32-bit integer limit of -2147483648",
                            context
                        )
                    )
                return RTResult().success(Int32(int_value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'l':
                int_value = int(node.tok.value)
                if int_value > 9223372036854775807:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}l is above the upper 64-bit integer limit of 9223372036854775807",
                            context
                        )
                    )
                elif int_value < -9223372036854775808:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}l is below the lower 64-bit integer limit of -9223372036854775808",
                            context
                        )
                    ) 
                return RTResult().success(Int64(int_value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'ui':
                int_value = int(node.tok.value)
                if int_value > 4294967295:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}ui is above the upper unsigned 32-bit integer limit of 4294967295",
                            context
                        )
                    )
                elif int_value < 0:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}ui is below the lower unsigned 32-bit integer limit of 0",
                            context
                        )
                    )
                return RTResult().success(UInt32(int_value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'ul':
                int_value = int(node.tok.value)
                if int_value > 18446744073709551615:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}ul is above the upper unsigned 64-bit integer limit of 18446744073709551615",
                            context
                        )
                    )
                elif int_value < 0:
                    return RTResult().failure(
                        err.IntegerOverflowError(
                            node.pos_start, node.pos_end,
                            f"{int_value}ul is below the lower unsigned 64-bit integer limit of 0",
                            context
                        )
                    )
                return RTResult().success(UInt64(int_value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'b':
                return RTResult().success(Integer(int(node.tok.value)).set_context(context).set_pos(node.pos_start, node.pos_end))
            # FLOATS
            case 'h':
                return RTResult().success(Float16(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'f':
                return RTResult().success(Float32(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
            case 'd':
                return RTResult().success(Float64(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
            # ERROR HANDLING
            case _:
                return RTResult().failure(
                    err.UnknownRTError(
                        node.pos_start, node.pos_end,
                        f"'{number_type}' is not a valid number type",
                        context
                    )
                )
    
    def visit_StringNode(self, node, context):
        return RTResult().success(String(node.tok.value).set_context(context).set_pos(node.pos_start, node.pos_end))
    
    def visit_IterArrayNode(self, node, context):
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): 
                return res

        return res.success(
            IterArray(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_MatrixNode(self, node, context):
        res = RTResult()

        subvectors = []
        subvector_types = [] #To check inputs

        for subvector_node in node.subvector_nodes:
            container_res = res.register(self.visit(subvector_node, context))

            if res.should_return(): 
                return res

            subvectors.append(container_res[0])
            subvector_types.append(container_res[1])
        matrix_type = subvector_types[0]
            
        if not all(map(lambda x: x == matrix_type, subvector_types)):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                "All elements in a matrix must be of the same type",
                context
            ))

        try:
            match matrix_type:
                case 'Float16':
                    matrix = Float16Matrix(linalg.f16_matrix(subvectors))
                case 'Float32':
                    matrix = Float32Matrix(linalg.f32_matrix(subvectors))
                case 'Float64':
                    matrix = Float64Matrix(linalg.f64_matrix(subvectors))
                case 'Int32':
                    matrix = Int32Matrix(linalg.i32_matrix(subvectors))
                case 'Int64':
                    matrix = Int64Matrix(linalg.i64_matrix(subvectors))
                case _:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"Invalid matrix type '{matrix_type}'",
                        context
                    ))
        except ValueError as e:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                e,
                context
            ))

        return res.success(
            matrix.set_context(context).set_pos(node.pos_start, node.pos_end)
        )

    def visit_MatrixSubvectorContainer(self, node, context): #TODO
        res = RTResult()
        elements = []

        for element_node in node.element_nodes:
            elements.append(res.register(self.visit(element_node, context)))
            if res.should_return(): 
                return res
        
        if not all(map(lambda x: x.type == elements[0].type, elements)):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                "All elements in a matrix must be of the same type",
                context
            ))

        return res.success((elements, elements[0].type))

    def visit_VarAccessNode(self, node: VarAccessNode, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value

        if node.value_node:
            var_name = node.var_name_tok.value
            value = res.register(self.visit(node.value_node, context))
            if res.should_return(): return res

            return context.symbol_table.ra_var(node, context, var_name, value)
        elif node.value:
            var_name = node.var_name_tok.value
            value = node.value

            return context.symbol_table.ra_var(node, context, var_name, value)
            
        value = context.symbol_table.get_var(var_name)
        if value == None:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(value)
    
    def visit_MemberAccessNode(self, node: MemberAccessNode, context: Context):
        res = RTResult()
        parent = res.register(self.visit(node.parent, context))
        if res.should_return(): return res

        if isinstance(parent, Structure):
            if node.value_node and not parent.isinstance:
                return res.failure(err.RTError(
                    node.pos_start, node.pos_end,
                    f"{parent} is not a structure instance",
                    context
                ))
        elif isinstance(parent, Namespace):
            if node.value_node:
                return res.failure(err.RTError(
                    node.pos_start, node.pos_end,
                    f"{parent} is not a structure instance",
                    context
                ))
        else:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"{parent} is not a structure or namespace (and hence has no members)",
                context
            )) 
        
        if node.member_name_tok.type != TT_IDENTIFIER:
            return res.failure(err.RTError(
                node.member_name_tok.pos_start, node.member_name_tok.pos_end,
                f"Expected identifier",
                context
            ))
        member_name = node.member_name_tok.value

        if member_name in parent.elements:
            if node.value_node:
                value = res.register(self.visit(node.value_node, context))
                if res.should_return(): return res

                typenamified_types = [t.typename for t in parent.elements[member_name][0]]
                
                if Type.Any.typename not in typenamified_types and value.type not in typenamified_types:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"Type of '{value}' ({Type(value.type)}) is not accepted by the type of the field '{member_name}' ({"|".join(typenamified_types)})",
                        context
                    ))
                
                parent.elements[member_name][1] = value
                node.parent.value = parent

                res.register(self.visit(node.parent, context))
                if res.should_return(): return res
            elif node.value:
                value = node.value
                
                typenamified_types = [t.typename for t in parent.elements[member_name][0]]
                
                if Type.Any.typename not in typenamified_types and value.type not in typenamified_types:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"Type of '{value}' ({Type(value.type)}) is not accepted by the type of the field '{member_name}' ({"|".join(typenamified_types)})",
                        context
                    ))
                
                parent.elements[member_name][1] = value
                node.parent.value = parent

                res.register(self.visit(node.parent, context))
                if res.should_return(): return res
            else:
                value = parent.elements[member_name] if isinstance(parent, Namespace) else parent.elements[member_name][1]
        else:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{member_name}' (member) is not defined in {parent}",
                context
            ))

        return res.success(value)
    
    def visit_ArrayViewNode(self, node: ArrayViewNode, context: Context): #TODO: add x[y][z] support!
        res = RTResult()
        to_view = res.register(self.visit(node.node_to_view, context))
        if res.should_return(): return res

        match bool(node.value_node):
            case False:
                if not getattr(to_view, '__getitem__', None):
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"'{to_view}' is not subscriptable",
                        context
                    ))
                index = res.register(self.visit(node.index_node, context))
                if res.should_return(): return res

                if getattr(index, 'value', None) == None:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"'{index}' is an invalid index",
                        context
                    ))
                
                value = to_view[index.value]
                
                if value == None:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"{index.value} is not a valid {'key' if to_view.index_type == INDEX_TYPE_KEY else 'index'} of '{to_view}'",
                        context
                    ))
                
                return res.success(value)
            case True:
                if not getattr(to_view, '__getitem__', None):
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"'{to_view}' is not subscriptable",
                        context
                    ))
                elif not getattr(to_view, '__setitem__', None):
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"'{to_view}' is not editable",
                        context
                    ))
                
                index = res.register(self.visit(node.index_node, context))
                if res.should_return(): return res

                if not getattr(index, 'value', None):
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"'{index}' is an invalid index",
                        context
                    ))
                
                value = res.register(self.visit(node.value_node, context))

                set_result = to_view.__setitem__(index.value, value)
                
                if set_result == False:
                    return res.failure(err.RTError(
                        node.pos_start, node.pos_end,
                        f"{index.value} is not a valid {'key' if to_view.index_type == INDEX_TYPE_KEY else 'index'} of {to_view}",
                        context
                    ))
                
                return res.success(value)
            
    def visit_VarAssignNode(self, node: VarAssignNode, context: Context):
        '''
        Modes:
        0 -> const var
        1 -> mut var
        2 -> var
        '''

        res = RTResult()
        var_name = node.var_name_tok.value
        _type = node.type
        value = res.register(self.visit(node.value_node, context))
        if res.should_return(): return res

        types = res.register(self.visit(node.type_container, context))
        if res.should_return(): return res
        
        return context.symbol_table.set_var(node, context, var_name, types, value, _type==1, _type>0)
    
    def visit_VarRmNode(self, node, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value
        vis = context.symbol_table.chk_var_in_symbols(var_name)

        if not vis:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined in current scope",
                context
            ))
        
        res.register(context.symbol_table.rm_var(var_name, node, context))
        if res.should_return(): return res
        return res.success(Null.null)
        
    def visit_VarProtectNode(self, node, context):
        res = RTResult()
        var_name = node.var_name_tok.value
        vis = context.symbol_table.chk_var_in_symbols(var_name)

        if not vis:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not defined",
                context
            ))
        
        res.register(context.symbol_table.protect_var(var_name, node, context))
        if res.should_return(): return res

        return res.success(Null.null)
    
    def visit_TypeContainerNode(self, node: TypeContainerNode, context):
        res = RTResult()
        wrap_field_type_tok = lambda tok: VarAccessNode(tok)
        types = [res.register(self.visit(wrap_field_type_tok(tok), context)) for tok in node.type_toks]
        if res.should_return(): return res

        if not all(map(lambda x: isinstance(x, Type), types)):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"Some items in '{types}' are not 'Type's",
                context
            ))
        
        if Type.Any.typename in map(lambda x: x.typename, types) and len(types) > 1 and context.strict_mode:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"(strict mode) 'Any' is an arbitrary type and must be alone",
                context
            ))
        
        return res.success(types)

    def visit_StructAssignNode(self, node: StructAssignNode, context: Context):
        res = RTResult()
        var_name = node.var_name_tok.value

        ''' DEPRECATED SNIPPET 1
        wrap_field_type_tok = lambda tok: VarAccessNode(tok)
        get_field_type = lambda tok: res.register(self.visit(wrap_field_type_tok(tok), context))
        fields = [[field_name_tok.value, get_field_type(field_type_tok)] for field_name_tok, field_type_tok in node.field_toks]
        if res.should_return(): return res
        '''

        ''' DEPRECATED SNIPPET 2
        wrap_field_type_tok = lambda tok: VarAccessNode(tok)
        get_field_types = lambda types_node: [res.register(self.visit(wrap_field_type_tok(tok), context)) for tok in types_node.type_toks]

        fields = [[field_name_tok.value, get_field_types(field_type_node)] for field_name_tok, field_type_node in node.field_toks]
        if res.should_return(): return res

        if not all(map(lambda x: isinstance(x[1], Type), fields)):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{var_name}' is not a Type",
                context
            ))
        '''

        context.symbol_table.set_sys_var(f"{var_name}_Struct", Type(f"{var_name}_Struct"))

        fields = [[field_name_tok.value, res.register(self.visit(field_type_node, context))] for field_name_tok, field_type_node in node.field_toks]
        if res.should_return(): return res

        structure = Structure(var_name, {field_name: [field_types, Null.null] for field_name, field_types in fields})

        res.register(context.symbol_table.set_struct(node, context, var_name, structure))
        if res.should_return(): return res
        
        return res.success(structure)

    def visit_ArraySpliceNode(self, node: ArraySpliceNode, context: Context):
        res = RTResult()
        to_splice = res.register(self.visit(node.node_to_splice, context))
        if res.should_return(): return res
        if not getattr(to_splice, '__getitem__', None):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{to_splice}' is not subscriptable",
                context
            ))
        elif to_splice.index_type != INDEX_TYPE_INT:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"'{to_splice}' is not splicable",
                context
            ))
        
        idx_nodes = [res.register(self.visit(node, context)) for node in node.index_nodes]
        if res.should_return(): return res
        elif not all(map(lambda x: isinstance(x, Integer) or x==None, idx_nodes)):
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"All indices must be Integers or nonexistant", #TODO: Improve comment
                context
            ))
        
        slicify_idx = lambda idx: None if idx == None else idx.value

        slice_idxs = slice(slicify_idx(idx_nodes[0]), slicify_idx(idx_nodes[1]), slicify_idx(idx_nodes[2]))

        value = to_splice[slice_idxs]

        stringify_idxs = ['XXXX' if idx == None else str(idx) for idx in [slice_idxs.start, slice_idxs.stop, slice_idxs.step]]
                
        if value == None:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                f"{stringify_idxs} are not valid splice indices of {to_splice}",
                context
            ))
        
        return res.success(value)
    
    def visit_BinOpNode(self, node, context):
        res = RTResult()
        left = res.register(self.visit(node.left_node, context))
        if res.should_return(): return res
        right = res.register(self.visit(node.right_node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_PLUS:
            result, error = left.add_by(right)
        elif node.op_tok.type == TT_MINUS:
            result, error = left.sub_by(right)
        elif node.op_tok.type == TT_MUL:
            result, error = left.mult_by(right)
        elif node.op_tok.type == TT_MATMUL:
            result, error = left.matmult_by(right)
        elif node.op_tok.type == TT_DIV:
            result, error = left.div_by(right)
        elif node.op_tok.type == TT_POW:
            result, error = left.pow_by(right)
        elif node.op_tok.type == TT_EE:
            result, error = left.get_comparison_eq(right)
        elif node.op_tok.type == TT_NE:
            result, error = left.get_comparison_ne(right)
        elif node.op_tok.type == TT_LT:
            result, error = left.get_comparison_lt(right)
        elif node.op_tok.type == TT_GT:
            result, error = left.get_comparison_gt(right)
        elif node.op_tok.type == TT_LTE:
            result, error = left.get_comparison_lte(right)
        elif node.op_tok.type == TT_GTE:
            result, error = left.get_comparison_gte(right)
        elif node.op_tok.type == TT_BITWISEAND:
            result, error = left.bitwise_and_by(right)
        elif node.op_tok.type == TT_BITWISEOR:
            result, error = left.bitwise_or_by(right)
        elif node.op_tok.type == TT_BITWISEXOR:
            result, error = left.bitwise_xor_by(right)
        elif node.op_tok.type == TT_LEFTSHIFT:
            result, error = left.left_shift_by(right)
        elif node.op_tok.type == TT_RIGHTSHIFT:
            result, error = left.right_shift_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'and'):
            result, error = left.and_by(right)
        elif node.op_tok.matches(TT_KEYWORD, 'or'):
            result, error = left.or_by(right)
        
        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    def visit_UnaryOpNode(self, node, context):
        res = RTResult()
        number = res.register(self.visit(node.node, context))
        if res.should_return(): return res

        if node.op_tok.type == TT_MINUS:
            number, error = number.neg()
        elif node.op_tok.type == TT_COMPLEMENT:
            number, error = number.complement()
        elif node.op_tok.matches(TT_KEYWORD, 'not'):
            number, error = number.not_()

        if error:
            return res.failure(error)
        else:

            return res.success(number.set_pos(node.pos_start, node.pos_end).set_context(context))
        
    def visit_IfNode(self, node, context):
        res = RTResult()

        for condition, expr, should_return_null in node.cases:
            condition_value = res.register(self.visit(condition, context))
            if res.should_return(): return res

            if condition_value.is_true():
                expr_value = res.register(self.visit(expr, context))
                if res.should_return(): return res
                return res.success(Null.null if should_return_null else expr_value)

        if node.else_case:
            expr, should_return_null = node.else_case
            else_value = res.register(self.visit(expr, context))
            if res.should_return(): return res
            return res.success(Null.null if should_return_null else else_value)

        return res.success(Null.null)
    
    def visit_ForNode(self, node, context):
        res = RTResult()
        elements = []

        start_value = res.register(self.visit(node.start_value_node, context))
        if res.should_return(): return res

        end_value = res.register(self.visit(node.end_value_node, context))
        if res.should_return(): return res

        if node.step_value_node:
            step_value = res.register(self.visit(node.step_value_node, context))
            if res.should_return(): return res
        else:
            step_value = Integer(1)

        i = start_value.value

        if step_value.value > 0:
            condition = lambda: i < end_value.value
        elif step_value.value < 0:
            condition = lambda: i > end_value.value
        else:
            return res.failure(err.RTError(
                node.step_value_node.pos_start, node.step_value_node.pos_end,
                f"Step value must not be zero",
                context
            ))
        
        one_loop_done = False
        while condition():
            if not one_loop_done:
                context.symbol_table.set_var(node, context, node.var_name_tok.value, [Type.Integer], Integer(i), True, True)
            else:
                context.symbol_table.ra_var(node, context, node.var_name_tok.value, Integer(i))
            
            i += step_value.value
            
            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            if res.loop_should_continue:
                continue
            if res.loop_should_break: 
                break

            elements.append(value)
            one_loop_done = True

        return res.success(
            Null.null if node.should_return_null else 
            IterArray(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )   
    
    def visit_WhileNode(self, node, context):
        res = RTResult()
        elements = []

        while True:
            condition = res.register(self.visit(node.condition_node, context))
            if res.should_return(): return res
            
            if not condition.is_true(): break

            value = res.register(self.visit(node.body_node, context))
            if res.should_return() and res.loop_should_continue == False and res.loop_should_break == False: return res
            if res.loop_should_continue: continue
            if res.loop_should_break: break

            elements.append(value)
        
        return res.success(
            Null.null if node.should_return_null else
            IterArray(elements).set_context(context).set_pos(node.pos_start, node.pos_end)
        )
    
    def visit_FuncDefNode(self, node: FuncDefNode, context:Context): #TODO
        res = RTResult()

        func_name = node.var_name_tok.value if node.var_name_tok else None
        body_node = node.body_node
        arg_prototypes = [(arg_name.value, res.register(self.visit(arg_types, context))) for arg_name, arg_types in node.arg_prototypes]
        if res.should_return(): return res
        res_types = res.register(self.visit(node.res_type_container, context))
        if res.should_return(): return res

        func_value = Function(func_name, body_node, arg_prototypes, res_types, node.should_auto_return).set_context(context).set_pos(node.pos_start, node.pos_end)

        if node.var_name_tok:
            res.register(context.symbol_table.set_var(node, context, func_name, [Type.Function], func_value, False, True))
            if res.should_return(): return res

        return res.success(func_value)
    
    def visit_CallNode(self, node: CallNode, context):
        res = RTResult()
        args = []

        value_to_call = res.register(self.visit(node.node_to_call, context))
        if res.should_return(): return res

        if isinstance(value_to_call, BaseFunction):
            value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end).set_context(context)

            for arg_node in node.arg_nodes:
                args.append(res.register(self.visit(arg_node, context)))
                if res.should_return(): return res

            return_value = res.register(value_to_call.execute(node, args))
            if res.should_return(): return res
            return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
            return res.success(return_value)
        elif isinstance(value_to_call, Structure) and not value_to_call.isinstance:
            value_to_call = value_to_call.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
            if len(node.arg_nodes) != 0:
                return res.failure(err.RTError(
                    node.pos_start, node.pos_end,
                    f"Structure cannot be instantiated with arguments",
                    context
                ))

            ins = value_to_call.make_instance(node.pos_start, node.pos_end)
            return RTResult().success(ins)
        
        return res.failure(err.RTError(
            node.pos_start, node.pos_end,
            f"Can't call or instantiate {value_to_call}",
            context
        ))
    
    def visit_ReturnNode(self, node, context):
        res = RTResult()

        if node.node_to_return:
            value = res.register(self.visit(node.node_to_return, context))
            if res.should_return(): return res
        else:
            value = Null.null

        return res.success_return(value)
    
    def visit_TypifyNode(self, node, context): 
        res = RTResult()
        value = res.register(self.visit(node.node_to_typify, context))
        if res.should_return(): return res

        return res.success(Type(value.type))

    def visit_CopyNode(self, node, context):
        res = RTResult()
        value = res.register(self.visit(node.node_to_copy, context))
        if res.should_return(): return res

        copied_value = value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        if res.should_return(): return res

        return res.success(copied_value)
    
    def visit_ContinueNode(self, node, context):
        return RTResult().success_continue()

    def visit_BreakNode(self, node, context):
        return RTResult().success_break()