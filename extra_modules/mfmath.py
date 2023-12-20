import ctypes
import os
import extra_modules.Errors as errs
import extra_modules.position as pos
from extra_modules.constant_system_values import *

#! THIS IS A DEPRECATED PART OF AILANG DUE TO ITS INEFFICIENCY! PLEASE USE NORMAL FLOATS INSTEAD!

fpmath_c = ctypes.CDLL(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/c_lib/fpmath/c_src/fpmath.so')

half = ctypes.c_short

# Define multi-float and result containers
class Cfcontainer(ctypes.Union):
    _fields_ = [
        ("bool_", ctypes.c_bool),
        ("half_", half),
        ("float_", ctypes.c_float),
        ("double_", ctypes.c_double)
    ]

class Cmfloat(ctypes.Structure):
    _fields_ = [
        ("value", Cfcontainer),
        ("type", ctypes.c_int),
    ]

class Cresult(ctypes.Structure):
    _fields_ = [
        ("res", Cmfloat),
        ("error", ctypes.c_int),
    ]

class Cmfloat_consts(ctypes.Structure):
    _fields_ = [
        ("table", ctypes.POINTER(ctypes.POINTER(Cmfloat))),
        ("no_rows", ctypes.c_int),
    ]

class Cconsts_table_res(ctypes.Structure):
    _fields_ = [
        ("table", ctypes.POINTER(Cmfloat_consts)),
        ("error", ctypes.c_int),
    ]

# Define C enumerations

# *err
GOOD                    = 0
DIVBY0ERROR             = 1
TYPEINEQERROR           = 2
UNKNOWNTYPEERROR        = 3
INPUTERROR              = 4
MALLOCERROR             = 5 
RTERROR                 = 6
CONSTANTNOTFOUNDERROR   = 7
UNKNOWNERROR            = 8

# *types
BOOL                = ctypes.c_int(0) 
HALF                = ctypes.c_int(1)
FLOAT               = ctypes.c_int(2)
DOUBLE              = ctypes.c_int(3)

# *const_idxes
ZERO_IDX            = ctypes.c_int(0)
PI_IDX              = ctypes.c_int(1) 
E_IDX               = ctypes.c_int(2)
LN2_IDX             = ctypes.c_int(3)
LN10_IDX            = ctypes.c_int(4)

# Define C function signatures

fpmath_c.str2double.argtypes = [ctypes.c_char_p]
fpmath_c.str2double.restype = ctypes.c_double

fpmath_c.str2float.argtypes = [ctypes.c_char_p]
fpmath_c.str2float.restype = ctypes.c_float

fpmath_c.str2half.argtypes = [ctypes.c_char_p]
fpmath_c.str2half.restype = half

fpmath_c.conv_d_mfloat_to_d_str.argtypes = [Cmfloat, ctypes.c_char_p]
fpmath_c.conv_d_mfloat_to_d_str.restype = ctypes.c_void_p

fpmath_c.conv_f_mfloat_to_f_str.argtypes = [Cmfloat, ctypes.c_char_p]
fpmath_c.conv_f_mfloat_to_f_str.restype = ctypes.c_void_p

fpmath_c.conv_h_mfloat_to_f_str.argtypes = [Cmfloat, ctypes.c_char_p]
fpmath_c.conv_h_mfloat_to_f_str.restype = ctypes.c_void_p

fpmath_c.free_char_ptr.argtypes = [ctypes.POINTER(ctypes.c_char_p)]
fpmath_c.free_char_ptr.restype = ctypes.c_void_p

fpmath_c.promote_input.argtypes = [Cmfloat, ctypes.c_int]
fpmath_c.promote_input.restype = Cresult

fpmath_c.demote_input.argtypes = [Cmfloat, ctypes.c_int]
fpmath_c.demote_input.restype = Cresult

fpmath_c.set_input_type.argtypes = [Cmfloat, ctypes.c_int]
fpmath_c.set_input_type.restype = Cresult

fpmath_c.equalise_inputs.argtypes = [Cmfloat, Cmfloat]
fpmath_c.equalise_inputs.restype = ctypes.POINTER(Cresult)

fpmath_c.add_by.argtypes = [Cmfloat, Cmfloat]
fpmath_c.add_by.restype = Cresult

fpmath_c.sub_by.argtypes = [Cmfloat, Cmfloat]
fpmath_c.sub_by.restype = Cresult

fpmath_c.mult_by.argtypes = [Cmfloat, Cmfloat]
fpmath_c.mult_by.restype = Cresult

fpmath_c.div_by.argtypes = [Cmfloat, Cmfloat]
fpmath_c.div_by.restype = Cresult

fpmath_c.pow_by.argtypes = [Cmfloat, Cmfloat]
fpmath_c.pow_by.restype = Cresult

fpmath_c.get_comparison_eq.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_eq.restype = Cresult

fpmath_c.get_comparison_ne.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_ne.restype = Cresult

fpmath_c.get_comparison_lt.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_lt.restype = Cresult

fpmath_c.get_comparison_gt.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_gt.restype = Cresult

fpmath_c.get_comparison_lte.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_lte.restype = Cresult

fpmath_c.get_comparison_gte.argtypes = [Cmfloat, Cmfloat]
fpmath_c.get_comparison_gte.restype = Cresult

fpmath_c.define_mfloat.argtypes = [Cfcontainer, ctypes.c_int]
fpmath_c.define_mfloat.restype = Cmfloat

fpmath_c.mfloat_constant.argtypes = [ctypes.c_char_p, ctypes.c_int]
fpmath_c.mfloat_constant.restype = Cresult

fpmath_c.add_constant.argtypes = [ctypes.POINTER(Cmfloat_consts), ctypes.c_int, ctypes.c_char_p]
fpmath_c.add_constant.restype = Cconsts_table_res

fpmath_c.make_consts_table.argtypes = []
fpmath_c.make_consts_table.restype = Cconsts_table_res

fpmath_c.lookup_const.argtypes = [Cmfloat_consts, ctypes.c_int, ctypes.c_int]
fpmath_c.lookup_const.restype = Cresult

fpmath_c.ret_str_zero.argtypes = []
fpmath_c.ret_str_zero.restype = ctypes.c_char_p

fpmath_c.ret_str_pi.argtypes = []
fpmath_c.ret_str_pi.restype = ctypes.c_char_p

fpmath_c.ret_str_e.argtypes = []
fpmath_c.ret_str_e.restype = ctypes.c_char_p

fpmath_c.ret_str_ln2.argtypes = []
fpmath_c.ret_str_ln2.restype = ctypes.c_char_p

fpmath_c.ret_str_ln10.argtypes = []
fpmath_c.ret_str_ln10.restype = ctypes.c_char_p

# Define Python mfloat interface

class mfloat():
    def __init__(self, in_value, _type: int|None = None):
        '''
        self._value = None #TEST
        self._prev_value = None #TEST
        '''
        if isinstance(in_value, mfloat):
            self.value = in_value.value
        elif isinstance(in_value, Cmfloat):
            self.value = in_value
        elif type(in_value) is str:
            fcontainer = Cfcontainer()
            match _type:
                case 1: #HALF
                    c_stringified_value = ctypes.create_string_buffer(in_value.encode('utf-8'))
                    fcontainer.half_ = fpmath_c.str2half(c_stringified_value)
                    self.value = Cmfloat(fcontainer, HALF)
                case 2: #FLOAT
                    c_stringified_value = ctypes.create_string_buffer(in_value.encode('utf-8'))
                    fcontainer.float_ = fpmath_c.str2float(c_stringified_value)
                    self.value = Cmfloat(fcontainer, FLOAT)
                case 3: #DOUBLE
                    c_stringified_value = ctypes.create_string_buffer(in_value.encode('utf-8'))
                    fcontainer.double_ = fpmath_c.str2double(c_stringified_value)
                    self.value = Cmfloat(fcontainer, DOUBLE)
                case _:
                    raise ValueError("Unknown or no type!")
            
            del c_stringified_value
        else:
            raise ValueError("Type of in_value is not supported!")
        
        self.stringified_value = None

    '''
    @property
    def value(self) -> Cmfloat: #TEST
        print(f'VALUE VIEW {self._prev_value}, {self._value}')
        return self._value

    @value.setter
    def value(self, val): #TEST
        self._prev_value = self._value
        print(f'VALUE SET{self._prev_value}->{val}')
        self._value = val
    '''

    @property
    def type(self) -> ctypes.c_int:
        return getattr(self.value, "type")
    
    @property
    def res_repr(self) -> Cresult:
        return Cresult(self.value, GOOD)

    def __repr__(self):
        if not self.stringified_value:
            match self.type:
                case 1: #HALF
                    c_stringified_value = ctypes.create_string_buffer(HALF_STR_BUF_SIZE)
                    fpmath_c.conv_h_mfloat_to_f_str(self.value, c_stringified_value)
                    self.stringified_value = c_stringified_value.value.decode('utf-8') + 'mh'
                case 2: #FLOAT
                    c_stringified_value = ctypes.create_string_buffer(FLOAT_STR_BUF_SIZE)
                    fpmath_c.conv_f_mfloat_to_f_str(self.value, c_stringified_value)
                    self.stringified_value = c_stringified_value.value.decode('utf-8') + 'mf'
                case 3: #DOUBLE
                    c_stringified_value = ctypes.create_string_buffer(DOUBLE_STR_BUF_SIZE)
                    fpmath_c.conv_d_mfloat_to_d_str(self.value, c_stringified_value)
                    self.stringified_value = c_stringified_value.value.decode('utf-8') + 'md'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self):
        return self.__repr__()
    
    def equalise_inputs(self, other) -> tuple[list[Cmfloat], ctypes.c_int]:
        #print(type(other), type(other.value))
        eq_inputs_ptr = fpmath_c.equalise_inputs(self.value, other.value)
        res_lst = list(ctypes.cast(eq_inputs_ptr, ctypes.POINTER(Cresult * 2)).contents)
        lst = [getattr(result, "res") for result in res_lst]
        err = getattr(res_lst[0], "error")
        return lst, err
    
    def set_input_type(self, tgt_type: int) -> tuple[Cmfloat, ctypes.c_int]:
        res = fpmath_c.set_input_type(self.value, ctypes.c_int(tgt_type))

        if (err := getattr(res, "error")) != GOOD:
            return None, err
        return getattr(res, "res"), None

    def add_by(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        #print(list(map(lambda x: str(mfloat(x)), eq_in)), err1)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.add_by(eq_in[0], eq_in[1])

        #print(getattr(res, "res"), getattr(res, "error"))
        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def sub_by(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.sub_by(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def mult_by(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.mult_by(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def div_by(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.div_by(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def pow_by(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.pow_by(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_eq(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_eq(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_ne(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_ne(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_lt(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_lt(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_gt(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_gt(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_lte(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_lte(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
    def get_comparison_gte(self, other) -> tuple[Cmfloat|None, ctypes.c_int|None]:
        eq_in, err1 = self.equalise_inputs(other)
        if err1 != GOOD:
            return None, err1
        
        res = fpmath_c.get_comparison_gte(eq_in[0], eq_in[1])

        if (err2 := getattr(res, "error")) != GOOD:
            return None, err2
        return getattr(res, "res"), None
    
# Define constants and constant interface
def add_constant(in_const_table_ptr: ctypes.POINTER(Cmfloat_consts), row_idx: ctypes.c_int, str_form: ctypes.c_char_p) -> list[Cmfloat_consts|None, ctypes.c_int|None]:
    constant_table_res = fpmath_c.add_constant(in_const_table_ptr, row_idx, str_form)
    if (err := getattr(constant_table_res, "error")) != GOOD:
        return None, ctypes.c_int(err)
    constant_table_ptr = getattr(constant_table_res, "table")
    return constant_table_ptr, None

def lookup_const(in_const_table: Cmfloat_consts, row_idx: ctypes.c_int, type: ctypes.c_int) -> list[Cmfloat|None, ctypes.c_int|None]:
    constant_res = fpmath_c.lookup_const(in_const_table, row_idx, type)
    if (err := getattr(constant_res, "error")) != GOOD:
        return None, err
    return getattr(constant_res, "res"), None

def init_constants() -> list[Cmfloat_consts|None, ctypes.c_int|None]:
    constant_table_res = fpmath_c.make_consts_table()
    if (err := getattr(constant_table_res, "error")) != GOOD:
        return None, err
    constant_table_ptr = getattr(constant_table_res, "table")

    constant_table_ptr, err = add_constant(constant_table_ptr, PI_IDX, fpmath_c.ret_str_pi())
    if err != None:
        return None, err
    
    constant_table_ptr, err = add_constant(constant_table_ptr, E_IDX, fpmath_c.ret_str_e())
    if err != None:
        return None, err
    
    constant_table_ptr, err = add_constant(constant_table_ptr, LN2_IDX, fpmath_c.ret_str_ln2())
    if err != None:
        return None, err
    
    constant_table_ptr, err = add_constant(constant_table_ptr, LN10_IDX, fpmath_c.ret_str_ln10())
    if err != None:
        return None, err
    
    return constant_table_ptr.contents, None

# Define error interface
def AILang_err_repr(err: ctypes.c_int|None, ctx, pos_start: pos.Position, pos_end: pos.Position) -> errs.Error:
    match (None if err == None else int(err)):
        case None: #GOOD
            return None
        case 0: #GOOD
            return None
        case 1: #DIVBY0ERROR
            return errs.RTError(
                pos_start, pos_end,
                'Division by zero',
                ctx
            )
        case 2: #TYPEINEQERROR
            return errs.RTError(
                pos_start, pos_end,
                'Type of floating points numbers are not equal',
                ctx
            )
        case 3: #UNKNOWNTYPEERROR
            return errs.RTError(
                pos_start, pos_end,
                'Unknown floating point number type',
                ctx
            )
        case 4: #INPUTERROR
            return errs.RTError(
                pos_start, pos_end,
                'Invalid input/input type',
                ctx
            )
        case 5: #MALLOCERROR
            return errs.MallocError(
                pos_start, pos_end,
                'Unable to allocate memory',
            )
        case 6: #RTERROR
            return errs.RTError(
                pos_start, pos_end,
                'Runtime Error',
                ctx
            )
        case 7: #CONSTANTNOTFOUNDERROR
            return errs.RTError(
                pos_start, pos_end,
                'Constant not found in constant table',
                ctx
            )
        case 8: #UNKNOWNERROR
            return errs.RTError(
                pos_start, pos_end,
                'Unknown error',
                ctx
            )
#TODO: go back to AILang and implement!