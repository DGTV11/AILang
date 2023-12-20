# Nodes

class NumberNode:
    def __init__(self, tok, _type):
        self.tok = tok
        self.type = _type

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'
    
class StringNode:
    def __init__(self, tok):
        self.tok = tok

        self.pos_start = self.tok.pos_start
        self.pos_end = self.tok.pos_end
    
    def __repr__(self):
        return f'{self.tok}'
    
class IterArrayNode:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end
    
    def __repr__(self):
        return f'{self.tok}'
    
class MatrixNode:
    def __init__(self, subvector_nodes, pos_start, pos_end):
        self.subvector_nodes = subvector_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

class MatrixSubvectorContainer:
    def __init__(self, element_nodes, pos_start, pos_end):
        self.element_nodes = element_nodes

        self.pos_start = pos_start
        self.pos_end = pos_end

class VarAccessNode:
    def __init__(self, var_name_tok, value_node=None, value=None):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.value = value

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class MemberAccessNode:
    def __init__(self, parent, member_name_tok, value_node=None, value=None):
        self.parent = parent
        self.member_name_tok = member_name_tok
        self.value_node = value_node
        self.value = value

        self.pos_start = self.parent.pos_start
        self.pos_end = self.member_name_tok.pos_end

class TypeContainerNode:
    def __init__(self, type_toks):
        self.type_toks = type_toks

        self.pos_start = self.type_toks[0].pos_start
        self.pos_end = self.type_toks[-1].pos_end

'''
class MemberAccessNode:
    def __init__(self, hierarchy: list, value_node=None):
        self.hierarchy = hierarchy
        self.value_node = value_node

        self.pos_start = self.hierarchy[0].pos_start
        self.pos_end = self.hierarchy[-1].pos_end if not value_node else value_node.pos_end
'''

class VarAssignNode:
    def __init__(self, var_name_tok, value_node, _type, type_container):
        self.var_name_tok = var_name_tok
        self.value_node = value_node
        self.type = _type # 0 -> var, 1 -> let, 2 -> const
        self.type_container = type_container

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.value_node.pos_end

class VarRmNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class VarProtectNode:
    def __init__(self, var_name_tok):
        self.var_name_tok = var_name_tok

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.var_name_tok.pos_end

class StructAssignNode:
    def __init__(self, var_name_tok, field_toks, pos_start, pos_end):
        self.var_name_tok = var_name_tok
        self.field_toks = field_toks

        self.pos_start = pos_start
        self.pos_end = pos_end

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

        self.pos_start = self.left_node.pos_start
        self.pos_end = self.right_node.pos_end

    def __repr__(self):
        return f'({self.left_node}, {self.op_tok}, {self.right_node})'
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

        self.pos_start = self.op_tok.pos_start
        self.pos_end = self.node.pos_end

    def __repr__(self):
        return f'({self.op_tok}, {self.node})'
    
class IfNode:
    def __init__(self, cases, else_case):
        self.cases = cases
        self.else_case = else_case

        self.pos_start = self.cases[0][0].pos_start
        self.pos_end = (self.else_case or self.cases[-1])[0].pos_end
        
class ForNode:
    def __init__(self, var_name_tok, start_value_node, end_value_node, step_value_node, body_node, should_return_null):
        self.var_name_tok = var_name_tok
        self.start_value_node = start_value_node
        self.end_value_node = end_value_node
        self.step_value_node = step_value_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.var_name_tok.pos_start
        self.pos_end = self.body_node.pos_end

class WhileNode:
    def __init__(self, condition_node, body_node, should_return_null):
        self.condition_node = condition_node
        self.body_node = body_node
        self.should_return_null = should_return_null

        self.pos_start = self.condition_node.pos_start
        self.pos_end = self.body_node.pos_end

class FuncDefNode:
    def __init__(self, var_name_tok, arg_prototypes, res_type_container, body_node, should_auto_return):
        self.var_name_tok = var_name_tok
        self.arg_prototypes = arg_prototypes
        self.res_type_container = res_type_container
        self.body_node = body_node
        self.should_auto_return = should_auto_return

        if self.var_name_tok:
            self.pos_start = self.var_name_tok.pos_start
        elif len(self.arg_prototypes) > 0:
            self.pos_start = self.arg_prototypes[0][0].pos_start
        else:
            self.pos_start = self.body_node.pos_start

        self.pos_end = self.body_node.pos_end

class CallNode:
    def __init__(self, node_to_call, arg_nodes):
        self.node_to_call = node_to_call
        self.arg_nodes = arg_nodes

        self.pos_start = self.node_to_call.pos_start

        if len(self.arg_nodes) > 0:
            self.pos_end = self.arg_nodes[-1].pos_end
        else:
            self.pos_end = self.node_to_call.pos_end

class ArrayViewNode:
    def __init__(self, node_to_view, index_node, pos_end, value_node=None):
        self.node_to_view = node_to_view
        self.index_node = index_node
        self.value_node = value_node

        self.pos_start = self.node_to_view.pos_start
        self.pos_end = pos_end

class ArraySpliceNode:
    def __init__(self, node_to_splice, index_nodes, pos_end):
        self.node_to_splice = node_to_splice
        self.index_nodes = index_nodes

        self.pos_start = self.node_to_splice.pos_start
        self.pos_end = pos_end

class ReturnNode:
    def __init__(self, node_to_return, pos_start, pos_end):
        self.node_to_return = node_to_return

        self.pos_start = pos_start
        self.pos_end = pos_end

class ContinueNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end

class TypifyNode:
    def __init__(self, node_to_typify, pos_start, pos_end):
        self.node_to_typify = node_to_typify

        self.pos_start = pos_start
        self.pos_end = pos_end

class BreakNode:
    def __init__(self, pos_start, pos_end):
        self.pos_start = pos_start
        self.pos_end = pos_end