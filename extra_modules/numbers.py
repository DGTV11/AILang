import ctypes
import os
import extra_modules.Errors as errs
import extra_modules.position as pos
from extra_modules.constant_system_values import *

numbers_c = ctypes.CDLL(os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/c_lib/numbers/c_src/numbers.so')

# Typedefs
overflow_type_t     = ctypes.c_uint
num_type_t          = ctypes.c_uint

float16_t           = ctypes.c_ushort
float32_t           = ctypes.c_float
float64_t           = ctypes.c_double
int32_t             = ctypes.c_int32
int64_t             = ctypes.c_int64

# Structs
class Cf16_res(ctypes.Structure):
    _fields_ = [
        ("res", float16_t),
        ("error", ctypes.c_bool),
    ]

class Cf32_res(ctypes.Structure):
    _fields_ = [
        ("res", float32_t),
        ("error", ctypes.c_bool),
    ]

class Cf64_res(ctypes.Structure):
    _fields_ = [
        ("res", float64_t),
        ("error", ctypes.c_bool),
    ]

class Ci32_res(ctypes.Structure):
    _fields_ = [
        ("res", int32_t),
        ("overflow_type", overflow_type_t),
    ]

class Ci64_res(ctypes.Structure):
    _fields_ = [
        ("res", int64_t),
        ("overflow_type", overflow_type_t),
    ]

# Numerical cast structures
class Cnum_container_t(ctypes.Union):
    _fields_ = [
        ("f16", float16_t),
        ("f32", float32_t),
        ("f64", float64_t),
        ("i32", int32_t),
        ("i64", int64_t),
    ]

class Cnum_t(ctypes.Structure):
    _fields_ = [
        ("num", Cnum_container_t),
        ("type", num_type_t),
    ]

type num_t = int|f16|f32|f64|i32|i64

# Functions

## f16
numbers_c.str2f16.argtypes = [ctypes.c_char_p]
numbers_c.str2f16.restype = float16_t

numbers_c.conv_f16_to_str.argtypes = [float16_t, ctypes.c_char_p]
numbers_c.conv_f16_to_str.restype = ctypes.c_void_p

numbers_c.conv_f16_to_sci_str.argtypes = [float16_t, ctypes.c_char_p]
numbers_c.conv_f16_to_sci_str.restype = ctypes.c_void_p

numbers_c.f16_add.argtypes = [float16_t, float16_t]
numbers_c.f16_add.restype = float16_t

numbers_c.f16_sub.argtypes = [float16_t, float16_t]
numbers_c.f16_sub.restype = float16_t

numbers_c.f16_mul.argtypes = [float16_t, float16_t]
numbers_c.f16_mul.restype = float16_t

numbers_c.f16_divide.argtypes = [float16_t, float16_t]
numbers_c.f16_divide.restype = Cf16_res

numbers_c.f16_pow.argtypes = [float16_t, float16_t]
numbers_c.f16_pow.restype = float16_t

numbers_c.f16_neg.argtypes = [float16_t]
numbers_c.f16_neg.restype = float16_t

numbers_c.f16_gte.argtypes = [float16_t, float16_t]
numbers_c.f16_gte.restype = ctypes.c_bool

numbers_c.f16_gt.argtypes = [float16_t, float16_t]
numbers_c.f16_gt.restype = ctypes.c_bool

numbers_c.f16_eq.argtypes = [float16_t, float16_t]
numbers_c.f16_eq.restype = ctypes.c_bool

numbers_c.f16_lte.argtypes = [float16_t, float16_t]
numbers_c.f16_lte.restype = ctypes.c_bool

numbers_c.f16_lt.argtypes = [float16_t, float16_t]
numbers_c.f16_lt.restype = ctypes.c_bool

numbers_c.f16_neq.argtypes = [float16_t, float16_t]
numbers_c.f16_neq.restype = ctypes.c_bool

## f32
numbers_c.str2f32.argtypes = [ctypes.c_char_p]
numbers_c.str2f32.restype = float32_t

numbers_c.conv_f32_to_str.argtypes = [float32_t, ctypes.c_char_p]
numbers_c.conv_f32_to_str.restype = ctypes.c_void_p

numbers_c.conv_f32_to_sci_str.argtypes = [float32_t, ctypes.c_char_p]
numbers_c.conv_f32_to_sci_str.restype = ctypes.c_void_p

numbers_c.f32_add.argtypes = [float32_t, float32_t]
numbers_c.f32_add.restype = float32_t

numbers_c.f32_sub.argtypes = [float32_t, float32_t]
numbers_c.f32_sub.restype = float32_t

numbers_c.f32_mul.argtypes = [float32_t, float32_t]
numbers_c.f32_mul.restype = float32_t

numbers_c.f32_divide.argtypes = [float32_t, float32_t]
numbers_c.f32_divide.restype = Cf32_res

numbers_c.f32_pow.argtypes = [float32_t, float32_t]
numbers_c.f32_pow.restype = float32_t

numbers_c.f32_neg.argtypes = [float32_t]
numbers_c.f32_neg.restype = float32_t

numbers_c.f32_gte.argtypes = [float32_t, float32_t]
numbers_c.f32_gte.restype = ctypes.c_bool

numbers_c.f32_gt.argtypes = [float32_t, float32_t]
numbers_c.f32_gt.restype = ctypes.c_bool

numbers_c.f32_eq.argtypes = [float32_t, float32_t]
numbers_c.f32_eq.restype = ctypes.c_bool

numbers_c.f32_lte.argtypes = [float32_t, float32_t]
numbers_c.f32_lte.restype = ctypes.c_bool

numbers_c.f32_lt.argtypes = [float32_t, float32_t]
numbers_c.f32_lt.restype = ctypes.c_bool

numbers_c.f32_neq.argtypes = [float32_t, float32_t]
numbers_c.f32_neq.restype = ctypes.c_bool

## f64
numbers_c.str2f64.argtypes = [ctypes.c_char_p]
numbers_c.str2f64.restype = float64_t

numbers_c.conv_f64_to_str.argtypes = [float64_t, ctypes.c_char_p]
numbers_c.conv_f64_to_str.restype = ctypes.c_void_p

numbers_c.conv_f64_to_sci_str.argtypes = [float64_t, ctypes.c_char_p]
numbers_c.conv_f64_to_sci_str.restype = ctypes.c_void_p

numbers_c.f64_add.argtypes = [float64_t, float64_t]
numbers_c.f64_add.restype = float64_t

numbers_c.f64_sub.argtypes = [float64_t, float64_t]
numbers_c.f64_sub.restype = float64_t

numbers_c.f64_mul.argtypes = [float64_t, float64_t]
numbers_c.f64_mul.restype = float64_t

numbers_c.f64_divide.argtypes = [float64_t, float64_t]
numbers_c.f64_divide.restype = Cf64_res

numbers_c.f64_pow.argtypes = [float64_t, float64_t]
numbers_c.f64_pow.restype = float64_t

numbers_c.f64_neg.argtypes = [float64_t]
numbers_c.f64_neg.restype = float64_t

numbers_c.f64_gte.argtypes = [float64_t, float64_t]
numbers_c.f64_gte.restype = ctypes.c_bool

numbers_c.f64_gt.argtypes = [float64_t, float64_t]
numbers_c.f64_gt.restype = ctypes.c_bool

numbers_c.f64_eq.argtypes = [float64_t, float64_t]
numbers_c.f64_eq.restype = ctypes.c_bool

numbers_c.f64_lte.argtypes = [float64_t, float64_t]
numbers_c.f64_lte.restype = ctypes.c_bool

numbers_c.f64_lt.argtypes = [float64_t, float64_t]
numbers_c.f64_lt.restype = ctypes.c_bool

numbers_c.f64_neq.argtypes = [float64_t, float64_t]
numbers_c.f64_neq.restype = ctypes.c_bool

## i32
numbers_c.str2i32.argtypes = [ctypes.c_char_p]
numbers_c.str2i32.restype = int32_t

numbers_c.conv_i32_to_str.argtypes = [int32_t, ctypes.c_char_p]
numbers_c.conv_i32_to_str.restype = ctypes.c_void_p

numbers_c.i32_add.argtypes = [int32_t, int32_t]
numbers_c.i32_add.restype = Ci32_res

numbers_c.i32_sub.argtypes = [int32_t, int32_t]
numbers_c.i32_sub.restype = Ci32_res

numbers_c.i32_mul.argtypes = [int32_t, int32_t]
numbers_c.i32_mul.restype = Ci32_res

numbers_c.i32_divide.argtypes = [int32_t, int32_t]
numbers_c.i32_divide.restype = Cf64_res

numbers_c.i32_pow.argtypes = [int32_t, int32_t]
numbers_c.i32_pow.restype = float64_t

numbers_c.i32_neg.argtypes = [int32_t]
numbers_c.i32_neg.restype = Ci32_res

numbers_c.i32_gte.argtypes = [int32_t, int32_t]
numbers_c.i32_gte.restype = ctypes.c_bool

numbers_c.i32_gt.argtypes = [int32_t, int32_t]
numbers_c.i32_gt.restype = ctypes.c_bool

numbers_c.i32_eq.argtypes = [int32_t, int32_t]
numbers_c.i32_eq.restype = ctypes.c_bool

numbers_c.i32_lte.argtypes = [int32_t, int32_t]
numbers_c.i32_lte.restype = ctypes.c_bool

numbers_c.i32_lt.argtypes = [int32_t, int32_t]
numbers_c.i32_lt.restype = ctypes.c_bool

numbers_c.i32_neq.argtypes = [int32_t, int32_t]
numbers_c.i32_neq.restype = ctypes.c_bool

## i64
numbers_c.str2i64.argtypes = [ctypes.c_char_p]
numbers_c.str2i64.restype = int64_t

numbers_c.conv_i64_to_str.argtypes = [int64_t, ctypes.c_char_p]
numbers_c.conv_i64_to_str.restype = ctypes.c_void_p

numbers_c.i64_add.argtypes = [int64_t, int64_t]
numbers_c.i64_add.restype = Ci64_res

numbers_c.i64_sub.argtypes = [int64_t, int64_t]
numbers_c.i64_sub.restype = Ci64_res

numbers_c.i64_mul.argtypes = [int64_t, int64_t]
numbers_c.i64_mul.restype = Ci64_res

numbers_c.i64_divide.argtypes = [int64_t, int64_t]
numbers_c.i64_divide.restype = Cf64_res

numbers_c.i64_pow.argtypes = [int64_t, int64_t]
numbers_c.i64_pow.restype = float64_t

numbers_c.i64_neg.argtypes = [int64_t]
numbers_c.i64_neg.restype = Ci64_res

numbers_c.i64_gte.argtypes = [int64_t, int64_t]
numbers_c.i64_gte.restype = ctypes.c_bool

numbers_c.i64_gt.argtypes = [int64_t, int64_t]
numbers_c.i64_gt.restype = ctypes.c_bool

numbers_c.i64_eq.argtypes = [int64_t, int64_t]
numbers_c.i64_eq.restype = ctypes.c_bool

numbers_c.i64_lte.argtypes = [int64_t, int64_t]
numbers_c.i64_lte.restype = ctypes.c_bool

numbers_c.i64_lt.argtypes = [int64_t, int64_t]
numbers_c.i64_lt.restype = ctypes.c_bool

numbers_c.i64_neq.argtypes = [int64_t, int64_t]
numbers_c.i64_neq.restype = ctypes.c_bool

# Conversions
numbers_c.numerical_cast.argtypes = [Cnum_t, num_type_t]
numbers_c.numerical_cast.restype = Cnum_t

# Datatypes
class f16:
    def __init__(self, val: str|int|float16_t):
        if isinstance(val, str):
            c_stringified_value = ctypes.create_string_buffer(val.encode('utf-8'))
            self.val: float16_t = numbers_c.str2f16(c_stringified_value)
        elif isinstance(val, int):
            self.val: float16_t = float16_t(val)
        elif isinstance(val, float16_t):
            self.val: float16_t = val
        else:
            raise TypeError("Value must be a string or float16_t")

        self.stringified_value = None
        self.sci_stringified_value = None
        
    def __repr__(self) -> str:
        if not self.stringified_value:
            c_stringified_value = ctypes.create_string_buffer(HALF_STR_BUF_SIZE)
            numbers_c.conv_f16_to_str(self.val, c_stringified_value)
            self.stringified_value = c_stringified_value.value.decode('utf-8')+'h'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def sci_str(self) -> str:
        if not self.sci_stringified_value:
            c_sci_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
            numbers_c.conv_f16_to_sci_str(self.val, c_sci_stringified_value)
            self.sci_stringified_value = c_sci_stringified_value.value.decode('utf-8')+'h'
            del c_sci_stringified_value
        return self.sci_stringified_value
    
    def __add__(self, other):
        if isinstance(other, f16):
            return f16(numbers_c.f16_add(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'f16' and '{type(other)}'")
        
    def __sub__(self, other):
        if isinstance(other, f16):
            return f16(numbers_c.f16_sub(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'f16' and '{type(other)}'")
        
    def __mul__(self, other):
        if isinstance(other, f16):
            return f16(numbers_c.f16_mul(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'f16' and '{type(other)}'")
        
    def __truediv__(self, other):
        if isinstance(other, f16):
            res: Cf16_res = numbers_c.f16_divide(self.val, other.val)
            if bool(getattr(res, 'error')):
                raise ZeroDivisionError('Division by zero')
            return f16(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'f16' and '{type(other)}'")
        
    def __pow__(self, other):
        if isinstance(other, f16):
            return f16(numbers_c.f16_pow(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for **: 'f16' and '{type(other)}'")
        
    def __neg__(self):
        return f16(numbers_c.f16_neg(self.val))
    
    def __ge__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_gte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >=: 'f16' and '{type(other)}'")
        
    def __gt__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_gt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >: 'f16' and '{type(other)}'")
        
    def __eq__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_eq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for ==: 'f16' and '{type(other)}'")
        
    def __le__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_lte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <=: 'f16' and '{type(other)}'")
        
    def __lt__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_lt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <: 'f16' and '{type(other)}'")
        
    def __ne__(self, other):
        if isinstance(other, f16):
            return numbers_c.f16_neq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for !=: 'f16' and '{type(other)}'")
        
class f32:
    def __init__(self, val: str|float|float32_t):
        if isinstance(val, str):
            c_stringified_value = ctypes.create_string_buffer(val.encode('utf-8'))
            self.val: float32_t = numbers_c.str2f32(c_stringified_value)
        elif isinstance(val, float32_t):
            self.val: float32_t = val
        elif isinstance(val, float):
            self.val: float32_t = float32_t(val)
        else:
            raise TypeError("Value must be a string or float32_t")

        self.stringified_value = None
        self.sci_stringified_value = None
        
    def __repr__(self) -> str:
        if not self.stringified_value:
            c_stringified_value = ctypes.create_string_buffer(FLOAT_STR_BUF_SIZE)
            numbers_c.conv_f32_to_str(self.val, c_stringified_value)
            self.stringified_value = c_stringified_value.value.decode('utf-8')+'f'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def sci_str(self) -> str:
        if not self.sci_stringified_value:
            c_sci_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
            numbers_c.conv_f32_to_sci_str(self.val, c_sci_stringified_value)
            self.sci_stringified_value = c_sci_stringified_value.value.decode('utf-8')+'f'
            del c_sci_stringified_value
        return self.sci_stringified_value
    
    def __add__(self, other):
        if isinstance(other, f32):
            return f32(numbers_c.f32_add(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'f32' and '{type(other)}'")
        
    def __sub__(self, other):
        if isinstance(other, f32):
            return f32(numbers_c.f32_sub(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'f32' and '{type(other)}'")
        
    def __mul__(self, other):
        if isinstance(other, f32):
            return f32(numbers_c.f32_mul(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'f32' and '{type(other)}'")
        
    def __truediv__(self, other):
        if isinstance(other, f32):
            res: Cf32_res = numbers_c.f32_divide(self.val, other.val)
            if bool(getattr(res, 'error')):
                raise ZeroDivisionError('Division by zero')
            return f32(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'f32' and '{type(other)}'")
        
    def __pow__(self, other):
        if isinstance(other, f32):
            return f32(numbers_c.f32_pow(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for **: 'f32' and '{type(other)}'")
        
    def __neg__(self):
        return f32(numbers_c.f32_neg(self.val))
    
    def __ge__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_gte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >=: 'f32' and '{type(other)}'")
        
    def __gt__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_gt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >: 'f32' and '{type(other)}'")
        
    def __eq__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_eq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for ==: 'f32' and '{type(other)}'")
        
    def __le__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_lte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <=: 'f32' and '{type(other)}'")
        
    def __lt__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_lt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <: 'f32' and '{type(other)}'")
        
    def __ne__(self, other):
        if isinstance(other, f32):
            return numbers_c.f32_neq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for !=: 'f32' and '{type(other)}'")
        
class f64:
    def __init__(self, val: str|float|float64_t):
        if isinstance(val, str):
            c_stringified_value = ctypes.create_string_buffer(val.encode('utf-8'))
            self.val: float64_t = numbers_c.str2f64(c_stringified_value)
        elif isinstance(val, float64_t):
            self.val: float64_t = val
        elif isinstance(val, float):
            self.val: float64_t = float64_t(val)
        else:
            raise TypeError("Value must be a string or float64_t")

        self.stringified_value = None
        self.sci_stringified_value = None
        
    def __repr__(self) -> str:
        if not self.stringified_value:
            c_stringified_value = ctypes.create_string_buffer(DOUBLE_STR_BUF_SIZE)
            numbers_c.conv_f64_to_str(self.val, c_stringified_value)
            self.stringified_value = c_stringified_value.value.decode('utf-8')+'d'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def sci_str(self) -> str:
        if not self.sci_stringified_value:
            c_sci_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
            numbers_c.conv_f64_to_sci_str(self.val, c_sci_stringified_value)
            self.sci_stringified_value = c_sci_stringified_value.value.decode('utf-8')+'d'
            del c_sci_stringified_value
        return self.sci_stringified_value
    
    def __add__(self, other):
        if isinstance(other, f64):
            return f64(numbers_c.f64_add(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'f64' and '{type(other)}'")
        
    def __sub__(self, other):
        if isinstance(other, f64):
            return f64(numbers_c.f64_sub(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'f64' and '{type(other)}'")
        
    def __mul__(self, other):
        if isinstance(other, f64):
            return f64(numbers_c.f64_mul(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'f64' and '{type(other)}'")
        
    def __truediv__(self, other):
        if isinstance(other, f64):
            res: Cf64_res = numbers_c.f64_divide(self.val, other.val)
            if bool(getattr(res, 'error')):
                raise ZeroDivisionError('Division by zero')
            return f64(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'f64' and '{type(other)}'")
        
    def __pow__(self, other):
        if isinstance(other, f64):
            return f64(numbers_c.f64_pow(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for **: 'f64' and '{type(other)}'")
        
    def __neg__(self):
        return f64(numbers_c.f64_neg(self.val))
    
    def __ge__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_gte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >=: 'f64' and '{type(other)}'")
        
    def __gt__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_gt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >: 'f64' and '{type(other)}'")
        
    def __eq__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_eq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for ==: 'f64' and '{type(other)}'")
        
    def __le__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_lte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <=: 'f64' and '{type(other)}'")
        
    def __lt__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_lt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <: 'f64' and '{type(other)}'")
        
    def __ne__(self, other):
        if isinstance(other, f64):
            return numbers_c.f64_neq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for !=: 'f64' and '{type(other)}'")
        
class i32:
    def __init__(self, val: str|int|int32_t):
        if isinstance(val, str):
            c_stringified_value = ctypes.create_string_buffer(val.encode('utf-8'))
            self.val: int32_t = numbers_c.str2i32(c_stringified_value)
        elif isinstance(val, int):
            self.val: int32_t = int32_t(val)
        elif isinstance(val, int32_t):
            self.val: int32_t = val

        self.stringified_value = None

    def __repr__(self) -> str:
        if not self.stringified_value:
            c_stringified_value = ctypes.create_string_buffer(INT_STR_BUF_SIZE)
            numbers_c.conv_i32_to_str(self.val, c_stringified_value)
            self.stringified_value = c_stringified_value.value.decode('utf-8')+'i'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __add__(self, other):
        if isinstance(other, i32):
            res: Ci32_res = numbers_c.i32_add(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i32(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'i32' and '{type(other)}'")
    
    def __sub__(self, other):
        if isinstance(other, i32):
            res: Ci32_res = numbers_c.i32_sub(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i32(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'i32' and '{type(other)}'")
        
    def __mul__(self, other):
        if isinstance(other, i32):
            res: Ci32_res = numbers_c.i32_mul(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i32(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'i32' and '{type(other)}'")
        
    def __truediv__(self, other):
        if isinstance(other, i32):
            res: Cf64_res = numbers_c.i32_divide(self.val, other.val)
            if bool(getattr(res, 'error')):
                raise ZeroDivisionError('Division by zero')
            return f64(getattr(res, 'res')) 
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'i32' and '{type(other)}'")
        
    def __pow__(self, other):
        if isinstance(other, i32):
            return f64(numbers_c.i32_pow(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for **: 'i32' and '{type(other)}'")
        
    def __neg__(self):
        res: Ci32_res = numbers_c.i32_neg(self.val)
        overflow_type: int = getattr(res, 'overflow_type')
        if overflow_type != 0:
            match overflow_type:
                case 1: #INTOVERFLOW
                    raise OverflowError('Integer overflow')
                case _:
                    raise Exception('Unknown error')
        return i32(getattr(res, 'res'))
    
    def __ge__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_gte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >=: 'i32' and '{type(other)}'")

    def __gt__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_gt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >: 'i32' and '{type(other)}'")
        
    def __eq__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_eq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for ==: 'i32' and '{type(other)}'")
        
    def __le__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_lte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <=: 'i32' and '{type(other)}'")
        
    def __lt__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_lt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <: 'i32' and '{type(other)}'")
        
    def __ne__(self, other):
        if isinstance(other, i32):
            return numbers_c.i32_neq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for !=: 'i32' and '{type(other)}'")

class i64:
    def __init__(self, val: str|int|int64_t):
        if isinstance(val, str):
            c_stringified_value = ctypes.create_string_buffer(val.encode('utf-8'))
            self.val: int64_t = numbers_c.str2i64(c_stringified_value)
        elif isinstance(val, int):
            self.val: int64_t = int64_t(val)
        elif isinstance(val, int64_t):
            self.val: int64_t = val

        self.stringified_value = None

    def __repr__(self) -> str:
        if not self.stringified_value:
            c_stringified_value = ctypes.create_string_buffer(INT_STR_BUF_SIZE)
            numbers_c.conv_i64_to_str(self.val, c_stringified_value)
            self.stringified_value = c_stringified_value.value.decode('utf-8')+'i'
            del c_stringified_value
        return self.stringified_value
    
    def __str__(self) -> str:
        return self.__repr__()
    
    def __add__(self, other):
        if isinstance(other, i64):
            res: Ci64_res = numbers_c.i64_add(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i64(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for +: 'i64' and '{type(other)}'")
    
    def __sub__(self, other):
        if isinstance(other, i64):
            res: Ci64_res = numbers_c.i64_sub(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i64(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'i64' and '{type(other)}'")
        
    def __mul__(self, other):
        if isinstance(other, i64):
            res: Ci64_res = numbers_c.i64_mul(self.val, other.val)
            overflow_type: int = getattr(res, 'overflow_type')
            if overflow_type != 0:
                match overflow_type:
                    case 1: #INTOVERFLOW
                        raise OverflowError('Integer overflow')
                    case 2: #INTUNDERFLOW
                        raise OverflowError('Integer underflow')
                    case _:
                        raise Exception('Unknown error')
            return i64(getattr(res, 'res'))
        else:
            raise TypeError(f"Unsupported operand type(s) for *: 'i64' and '{type(other)}'")
        
    def __truediv__(self, other):
        if isinstance(other, i64):
            res: Cf64_res = numbers_c.i64_divide(self.val, other.val)
            if bool(getattr(res, 'error')):
                raise ZeroDivisionError('Division by zero')
            return f64(getattr(res, 'res')) 
        else:
            raise TypeError(f"Unsupported operand type(s) for /: 'i64' and '{type(other)}'")
        
    def __pow__(self, other):
        if isinstance(other, i64):
            return f64(numbers_c.i64_pow(self.val, other.val))
        else:
            raise TypeError(f"Unsupported operand type(s) for **: 'i64' and '{type(other)}'")
        
    def __neg__(self):
        res: Ci64_res = numbers_c.i64_neg(self.val)
        overflow_type: int = getattr(res, 'overflow_type')
        if overflow_type != 0:
            match overflow_type:
                case 1: #INTOVERFLOW
                    raise OverflowError('Integer overflow')
                case _:
                    raise Exception('Unknown error')
        return i64(getattr(res, 'res'))
    
    def __ge__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_gte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >=: 'i64' and '{type(other)}'")

    def __gt__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_gt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for >: 'i64' and '{type(other)}'")
        
    def __eq__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_eq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for ==: 'i64' and '{type(other)}'")
        
    def __le__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_lte(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <=: 'i64' and '{type(other)}'")
        
    def __lt__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_lt(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for <: 'i64' and '{type(other)}'")
        
    def __ne__(self, other):
        if isinstance(other, i64):
            return numbers_c.i64_neq(self.val, other.val)
        else:
            raise TypeError(f"Unsupported operand type(s) for !=: 'i64' and '{type(other)}'")

# Numerical casting
py_num_type_to_num_type_t = {
    f16: (num_type_t(0), 'f16'),
    f32: (num_type_t(1), 'f32'),
    f64: (num_type_t(2), 'f64'),
    i32: (num_type_t(3), 'i32'),
    i64: (num_type_t(4), 'i64'),
}

int_to_py_num = {
    0: (f16, 'f16'),
    1: (f32, 'f32'),
    2: (f64, 'f64'),
    3: (i32, 'i32'),
    4: (i64, 'i64'),
}

def numerical_cast(x: num_t, tgt_type: type) -> num_t: #TODO!!!
    if isinstance(x, int):
        if tgt_type is f16:
            x = f64(float64_t(float(x)))
        elif tgt_type is f32:
            x = f64(float64_t(float(x)))
        elif tgt_type is f64:
            x = f64(float64_t(float(x)))
        elif tgt_type is i32:
            x = i64(int64_t(x))
        elif tgt_type is i64:
            x = i64(int64_t(x))
        elif tgt_type is int:
            return x
    
    if tgt_type is int:
        y = True
        tgt_type = i64
    else:
        y = False

    c_current_type  = py_num_type_to_num_type_t[type(x)]
    c_tgt_type      = py_num_type_to_num_type_t[tgt_type]

    container = Cnum_container_t()

    '''
    match (c_current_type[1]):
        case 'f16':
            container.f16 = x.val
        case 'f32':
            container.f32 = x.val
        case 'f64':
            container.f64 = x.val
        case 'i32':
            container.i32 = x.val
        case 'i64':
            container.i64 = x.val
    '''

    #print(c_current_type[1], type(x))

    setattr(container, c_current_type[1], x.val)

    out_container = numbers_c.numerical_cast(Cnum_t(container, c_current_type[0]), c_tgt_type[0])

    if getattr(out_container, 'type') == 5:
        raise Exception('Unknown error')

    out_type = getattr(out_container, 'type') 

    out = int_to_py_num[out_type][0](getattr(getattr(out_container, 'num'), int_to_py_num[out_type][1]))

    if y:
        return out.val.value
    return out