import ctypes
import os
import extra_modules.execution_components.context_and_datatypes as dta
from itertools import chain
from extra_modules.execution_components.constant_system_values import SCIENTIFIC_STR_BUF_SIZE, INT_STR_BUF_SIZE, LONG_STR_BUF_SIZE
from extra_modules.c_apis.numbers import numbers_c, f16, f32, f64, i32, i64

linalg_c = ctypes.CDLL(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/c_lib/linalg/lib/linalg.so')

# Typedefs
error_t                 = ctypes.c_uint
matrix_type_t           = ctypes.c_uint

float16_t               = ctypes.c_ushort
float32_t               = ctypes.c_float
float64_t               = ctypes.c_double
int32_t                 = ctypes.c_int32
int64_t                 = ctypes.c_int64

f16_subvector_container = ctypes.POINTER(float16_t)
f32_subvector_container = ctypes.POINTER(float32_t)
f64_subvector_container = ctypes.POINTER(float64_t)
i32_subvector_container = ctypes.POINTER(int32_t)
i64_subvector_container = ctypes.POINTER(int64_t)

f16_matrix_container    = ctypes.POINTER(f16_subvector_container)
f32_matrix_container    = ctypes.POINTER(f32_subvector_container)
f64_matrix_container    = ctypes.POINTER(f64_subvector_container)
i32_matrix_container    = ctypes.POINTER(i32_subvector_container)
i64_matrix_container    = ctypes.POINTER(i64_subvector_container)

# Structs
class Cfloat16_matrix_t(ctypes.Structure):
    _fields_ = [
        ("m", f16_matrix_container),
        ("x", ctypes.c_size_t),
        ("y", ctypes.c_size_t),
    ]

class Cfloat32_matrix_t(ctypes.Structure):
    _fields_ = [
        ("m", f32_matrix_container),
        ("x", ctypes.c_size_t),
        ("y", ctypes.c_size_t),
    ]

class Cfloat64_matrix_t(ctypes.Structure):
    _fields_ = [
        ("m", f64_matrix_container),
        ("x", ctypes.c_size_t),
        ("y", ctypes.c_size_t),
    ]

class Cint32_matrix_t(ctypes.Structure):
    _fields_ = [
        ("m", i32_matrix_container),
        ("x", ctypes.c_size_t),
        ("y", ctypes.c_size_t),
    ]

class Cint64_matrix_t(ctypes.Structure):
    _fields_ = [
        ("m", i64_matrix_container),
        ("x", ctypes.c_size_t),
        ("y", ctypes.c_size_t),
    ]

class Cfloat16_matrix_res_t(ctypes.Structure):
    _fields_ = [
        ("res", Cfloat16_matrix_t),
        ("err", error_t),
    ]

class Cfloat32_matrix_res_t(ctypes.Structure):
    _fields_ = [
        ("res", Cfloat32_matrix_t),
        ("err", error_t),
    ]

class Cfloat64_matrix_res_t(ctypes.Structure):
    _fields_ = [
        ("res", Cfloat64_matrix_t),
        ("err", error_t),
    ]

class Cint32_matrix_res_t(ctypes.Structure):
    _fields_ = [
        ("res", Cint32_matrix_t),
        ("err", error_t),
    ]

class Cint64_matrix_res_t(ctypes.Structure):
    _fields_ = [
        ("res", Cint64_matrix_t),
        ("err", error_t),
    ]

# Matrix cast structures and types
class Cmatrix_container_t(ctypes.Union):
    _fields_ = [
        ("f16m", Cfloat16_matrix_t),
        ("f32m", Cfloat32_matrix_t),
        ("f64m", Cfloat64_matrix_t),
        ("i32m", Cint32_matrix_t),
        ("i64m", Cint64_matrix_t),
    ]

class Cmatrix_t(ctypes.Structure):
    _fields_ = [
        ("m", Cmatrix_container_t),
        ("matrix_type", matrix_type_t),
    ]

class Cmatrix_cast_res_t(ctypes.Structure):
    _fields_ = [
        ("res_matrix", Cmatrix_t),
        ("err", error_t),
    ]

type matrix_t = f16_matrix|f32_matrix|f64_matrix|i32_matrix|i64_matrix

# Function prototypes

numbers_c.conv_f16_to_sci_str.argtypes = [float16_t, ctypes.c_char_p]
numbers_c.conv_f16_to_sci_str.restype = ctypes.c_void_p

numbers_c.conv_f32_to_sci_str.argtypes = [float32_t, ctypes.c_char_p]
numbers_c.conv_f32_to_sci_str.restype = ctypes.c_void_p

numbers_c.conv_f64_to_sci_str.argtypes = [float64_t, ctypes.c_char_p]
numbers_c.conv_f64_to_sci_str.restype = ctypes.c_void_p

numbers_c.conv_i32_to_str.argtypes = [int32_t, ctypes.c_char_p]
numbers_c.conv_i32_to_str.restype = ctypes.c_void_p

numbers_c.conv_i64_to_str.argtypes = [int64_t, ctypes.c_char_p]
numbers_c.conv_i64_to_str.restype = ctypes.c_void_p

linalg_c.free_f16m.argtypes = [Cfloat16_matrix_t]
linalg_c.free_f16m.restype = ctypes.c_void_p

linalg_c.free_f32m.argtypes = [Cfloat32_matrix_t]
linalg_c.free_f32m.restype = ctypes.c_void_p

linalg_c.free_f64m.argtypes = [Cfloat64_matrix_t]
linalg_c.free_f64m.restype = ctypes.c_void_p

linalg_c.free_i32m.argtypes = [Cint32_matrix_t]
linalg_c.free_i32m.restype = ctypes.c_void_p

linalg_c.free_i64m.argtypes = [Cint64_matrix_t]
linalg_c.free_i64m.restype = ctypes.c_void_p

linalg_c.copy_f16m.argtypes = [Cfloat16_matrix_t]
linalg_c.copy_f16m.restype = Cfloat16_matrix_res_t

linalg_c.copy_f32m.argtypes = [Cfloat32_matrix_t]
linalg_c.copy_f32m.restype = Cfloat32_matrix_res_t

linalg_c.copy_f64m.argtypes = [Cfloat64_matrix_t]
linalg_c.copy_f64m.restype = Cfloat64_matrix_res_t

linalg_c.copy_i32m.argtypes = [Cint32_matrix_t]
linalg_c.copy_i32m.restype = Cint32_matrix_res_t

linalg_c.copy_i64m.argtypes = [Cint64_matrix_t]
linalg_c.copy_i64m.restype = Cint64_matrix_res_t

linalg_c.f16m_fill.argtypes = [ctypes.c_size_t, ctypes.c_size_t, float16_t]
linalg_c.f16m_fill.restype = Cfloat16_matrix_res_t

linalg_c.f32m_fill.argtypes = [ctypes.c_size_t, ctypes.c_size_t, float32_t]
linalg_c.f32m_fill.restype = Cfloat32_matrix_res_t

linalg_c.f64m_fill.argtypes = [ctypes.c_size_t, ctypes.c_size_t, float64_t]
linalg_c.f64m_fill.restype = Cfloat64_matrix_res_t

linalg_c.i32m_fill.argtypes = [ctypes.c_size_t, ctypes.c_size_t, int32_t]
linalg_c.i32m_fill.restype = Cint32_matrix_res_t

linalg_c.i64m_fill.argtypes = [ctypes.c_size_t, ctypes.c_size_t, int64_t]
linalg_c.i64m_fill.restype = Cint64_matrix_res_t

linalg_c.f16m_row_vector_to_matrix.argtypes = [Cfloat16_matrix_t, ctypes.c_size_t]
linalg_c.f16m_row_vector_to_matrix.restype = Cfloat16_matrix_res_t

linalg_c.f32m_row_vector_to_matrix.argtypes = [Cfloat32_matrix_t, ctypes.c_size_t]
linalg_c.f32m_row_vector_to_matrix.restype = Cfloat32_matrix_res_t

linalg_c.f64m_row_vector_to_matrix.argtypes = [Cfloat64_matrix_t, ctypes.c_size_t]
linalg_c.f64m_row_vector_to_matrix.restype = Cfloat64_matrix_res_t

linalg_c.i32m_row_vector_to_matrix.argtypes = [Cint32_matrix_t, ctypes.c_size_t]
linalg_c.i32m_row_vector_to_matrix.restype = Cint32_matrix_res_t

linalg_c.i64m_row_vector_to_matrix.argtypes = [Cint64_matrix_t, ctypes.c_size_t]
linalg_c.i64m_row_vector_to_matrix.restype = Cint64_matrix_res_t

linalg_c.f16m_column_vector_to_matrix.argtypes = [Cfloat16_matrix_t, ctypes.c_size_t]
linalg_c.f16m_column_vector_to_matrix.restype = Cfloat16_matrix_res_t

linalg_c.f32m_column_vector_to_matrix.argtypes = [Cfloat32_matrix_t, ctypes.c_size_t]
linalg_c.f32m_column_vector_to_matrix.restype = Cfloat32_matrix_res_t

linalg_c.f64m_column_vector_to_matrix.argtypes = [Cfloat64_matrix_t, ctypes.c_size_t]
linalg_c.f64m_column_vector_to_matrix.restype = Cfloat64_matrix_res_t

linalg_c.i32m_column_vector_to_matrix.argtypes = [Cint32_matrix_t, ctypes.c_size_t]
linalg_c.i32m_column_vector_to_matrix.restype = Cint32_matrix_res_t

linalg_c.i64m_column_vector_to_matrix.argtypes = [Cint64_matrix_t, ctypes.c_size_t]
linalg_c.i64m_column_vector_to_matrix.restype = Cint64_matrix_res_t

linalg_c.f16m_to_f32m.argtypes = [Cfloat16_matrix_t]
linalg_c.f16m_to_f32m.restype = Cfloat32_matrix_res_t

linalg_c.f16m_to_f64m.argtypes = [Cfloat16_matrix_t]
linalg_c.f16m_to_f64m.restype = Cfloat64_matrix_res_t

linalg_c.f32m_to_f16m.argtypes = [Cfloat32_matrix_t]
linalg_c.f32m_to_f16m.restype = Cfloat16_matrix_res_t

linalg_c.f32m_to_f64m.argtypes = [Cfloat32_matrix_t]
linalg_c.f32m_to_f64m.restype = Cfloat64_matrix_res_t

linalg_c.f64m_to_f16m.argtypes = [Cfloat64_matrix_t]
linalg_c.f64m_to_f16m.restype = Cfloat16_matrix_res_t

linalg_c.f64m_to_f32m.argtypes = [Cfloat64_matrix_t]
linalg_c.f64m_to_f32m.restype = Cfloat32_matrix_res_t

linalg_c.matrix_cast.argtypes = [Cmatrix_t, matrix_type_t]
linalg_c.matrix_cast.restype = Cmatrix_cast_res_t

linalg_c.f16m_add.argtypes = [Cfloat16_matrix_t, Cfloat16_matrix_t]
linalg_c.f16m_add.restype = Cfloat16_matrix_res_t

linalg_c.f32m_add.argtypes = [Cfloat32_matrix_t, Cfloat32_matrix_t]
linalg_c.f32m_add.restype = Cfloat32_matrix_res_t

linalg_c.f64m_add.argtypes = [Cfloat64_matrix_t, Cfloat64_matrix_t]
linalg_c.f64m_add.restype = Cfloat64_matrix_res_t

linalg_c.i32m_add.argtypes = [Cint32_matrix_t, Cint32_matrix_t]
linalg_c.i32m_add.restype = Cint32_matrix_res_t

linalg_c.i64m_add.argtypes = [Cint64_matrix_t, Cint64_matrix_t]
linalg_c.i64m_add.restype = Cint64_matrix_res_t

linalg_c.f16m_sub.argtypes = [Cfloat16_matrix_t, Cfloat16_matrix_t]
linalg_c.f16m_sub.restype = Cfloat16_matrix_res_t

linalg_c.f32m_sub.argtypes = [Cfloat32_matrix_t, Cfloat32_matrix_t]
linalg_c.f32m_sub.restype = Cfloat32_matrix_res_t

linalg_c.f64m_sub.argtypes = [Cfloat64_matrix_t, Cfloat64_matrix_t]
linalg_c.f64m_sub.restype = Cfloat64_matrix_res_t

linalg_c.i32m_sub.argtypes = [Cint32_matrix_t, Cint32_matrix_t]
linalg_c.i32m_sub.restype = Cint32_matrix_res_t

linalg_c.i64m_sub.argtypes = [Cint64_matrix_t, Cint64_matrix_t]
linalg_c.i64m_sub.restype = Cint64_matrix_res_t

linalg_c.f16m_mul.argtypes = [Cfloat16_matrix_t, Cfloat16_matrix_t]
linalg_c.f16m_mul.restype = Cfloat16_matrix_res_t

linalg_c.f32m_mul.argtypes = [Cfloat32_matrix_t, Cfloat32_matrix_t]
linalg_c.f32m_mul.restype = Cfloat32_matrix_res_t

linalg_c.f64m_mul.argtypes = [Cfloat64_matrix_t, Cfloat64_matrix_t]
linalg_c.f64m_mul.restype = Cfloat64_matrix_res_t

linalg_c.i32m_mul.argtypes = [Cint32_matrix_t, Cint32_matrix_t]
linalg_c.i32m_mul.restype = Cint32_matrix_res_t

linalg_c.i64m_mul.argtypes = [Cint64_matrix_t, Cint64_matrix_t]
linalg_c.i64m_mul.restype = Cint64_matrix_res_t

linalg_c.f16m_div.argtypes = [Cfloat16_matrix_t, Cfloat16_matrix_t]
linalg_c.f16m_div.restype = Cfloat16_matrix_res_t

linalg_c.f32m_div.argtypes = [Cfloat32_matrix_t, Cfloat32_matrix_t]
linalg_c.f32m_div.restype = Cfloat32_matrix_res_t

linalg_c.f64m_div.argtypes = [Cfloat64_matrix_t, Cfloat64_matrix_t]
linalg_c.f64m_div.restype = Cfloat64_matrix_res_t

linalg_c.i32m_div.argtypes = [Cint32_matrix_t, Cint32_matrix_t]
linalg_c.i32m_div.restype = Cint32_matrix_res_t

linalg_c.i64m_div.argtypes = [Cint64_matrix_t, Cint64_matrix_t]
linalg_c.i64m_div.restype = Cint64_matrix_res_t

linalg_c.f16m_matmul.argtypes = [Cfloat16_matrix_t, Cfloat16_matrix_t]
linalg_c.f16m_matmul.restype = Cfloat16_matrix_res_t

linalg_c.f32m_matmul.argtypes = [Cfloat32_matrix_t, Cfloat32_matrix_t]
linalg_c.f32m_matmul.restype = Cfloat32_matrix_res_t

linalg_c.f64m_matmul.argtypes = [Cfloat64_matrix_t, Cfloat64_matrix_t]
linalg_c.f64m_matmul.restype = Cfloat64_matrix_res_t

linalg_c.i32m_matmul.argtypes = [Cint32_matrix_t, Cint32_matrix_t]
linalg_c.i32m_matmul.restype = Cint32_matrix_res_t

linalg_c.i64m_matmul.argtypes = [Cint64_matrix_t, Cint64_matrix_t]
linalg_c.i64m_matmul.restype = Cint64_matrix_res_t

linalg_c.f16m_neg.argtypes = [Cfloat16_matrix_t]
linalg_c.f16m_neg.restype = Cfloat16_matrix_res_t

linalg_c.f32m_neg.argtypes = [Cfloat32_matrix_t]
linalg_c.f32m_neg.restype = Cfloat32_matrix_res_t

linalg_c.f64m_neg.argtypes = [Cfloat64_matrix_t]
linalg_c.f64m_neg.restype = Cfloat64_matrix_res_t

linalg_c.i32m_neg.argtypes = [Cint32_matrix_t]
linalg_c.i32m_neg.restype = Cint32_matrix_res_t

linalg_c.i64m_neg.argtypes = [Cint64_matrix_t]
linalg_c.i64m_neg.restype = Cint64_matrix_res_t

linalg_c.f16m_exp.argtypes = [Cfloat16_matrix_t]
linalg_c.f16m_exp.restype = Cfloat16_matrix_res_t

linalg_c.f32m_exp.argtypes = [Cfloat32_matrix_t]
linalg_c.f32m_exp.restype = Cfloat32_matrix_res_t

linalg_c.f64m_exp.argtypes = [Cfloat64_matrix_t]
linalg_c.f64m_exp.restype = Cfloat64_matrix_res_t

linalg_c.i32m_exp.argtypes = [Cint32_matrix_t]
linalg_c.i32m_exp.restype = Cint32_matrix_res_t

linalg_c.i64m_exp.argtypes = [Cint64_matrix_t]
linalg_c.i64m_exp.restype = Cint64_matrix_res_t

linalg_c.f16m_transpose.argtypes = [Cfloat16_matrix_t]
linalg_c.f16m_transpose.restype = Cfloat16_matrix_res_t

linalg_c.f32m_transpose.argtypes = [Cfloat32_matrix_t]
linalg_c.f32m_transpose.restype = Cfloat32_matrix_res_t

linalg_c.f64m_transpose.argtypes = [Cfloat64_matrix_t]
linalg_c.f64m_transpose.restype = Cfloat64_matrix_res_t

linalg_c.i32m_transpose.argtypes = [Cint32_matrix_t]
linalg_c.i32m_transpose.restype = Cint32_matrix_res_t

linalg_c.i64m_transpose.argtypes = [Cint64_matrix_t]
linalg_c.i64m_transpose.restype = Cint64_matrix_res_t

# Datatypes
class f16_matrix:
    def __init__(self, m):
        #Type of m: list[list[Float16]]|list[list[f16]]|Cfloat16_matrix_t|f16_matrix

        #*Check if m is a f16_matrix or Cfloat16_matrix_t instance
        if isinstance(m, f16_matrix):
            self.x = m.x
            self.y = m.y
            self.m = m.m
        elif isinstance(m, Cfloat16_matrix_t):
            self.x = int(getattr(m, 'x'))
            self.y = int(getattr(m, 'y'))
            self.m = m
        else:
            #*Check nesting depth of m
            if type(m) is not list or len(m) == 0 or not all(map(lambda v: type(v) is list, m)):
                raise ValueError("Matrix must have a nesting depth of exactly 2")
            
            #*Check if m is empty
            if len(m) == 1 and len(m[0]) == 0:
                raise ValueError("Matrix must not be empty")
            
            #*Check size of each subvector in m
            if not all(map(lambda v: len(v) == len(m[0]), m)):
                raise ValueError("Matrix must be rectangular")

            #*Check if all elements in m have equal type
            first_type = type(m[0][0])
            if not all(map(lambda x: type(x) is first_type, chain.from_iterable(m))):
                raise ValueError("All matrix elements must be of the same type")

            #*Check first type of the input data
            if first_type is f16:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f16_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float16_t * self.x)(*list(map(lambda x: x.val, v))), ctypes.POINTER(float16_t)), m))), ctypes.POINTER(f16_subvector_container))
                
                self.m = Cfloat16_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            elif first_type is dta.Float16:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f16_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float16_t * self.x)(*list(map(lambda x: x.value.val, v))), ctypes.POINTER(float16_t)), m))), ctypes.POINTER(f16_subvector_container))

                self.m = Cfloat16_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            else:
                raise ValueError("Matrix elements must be of type Float16 or f16")
    
    def free(self):
        linalg_c.free_f16m(self.m)
        del self.x
        del self.y

    @staticmethod
    def f16_sci_stringify(f16: float16_t):
        c_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
        numbers_c.conv_f16_to_sci_str(f16, c_stringified_value)
        return c_stringified_value.value.decode('utf-8')+'h'

    def __repr__(self): #All items are left-padded like this: [0.4213312, 0.3212   , 0.3112333]
        matrix = list(map(lambda ptr: ptr[:self.x], getattr(self.m, 'm')[:self.y]))
        max_str_len = max(map(lambda v: len(self.f16_sci_stringify(v)), chain.from_iterable(matrix)))

        stringified_vectors_with_padded_subvectors = list(map(lambda v: ' {'+', '.join(map(lambda x: self.f16_sci_stringify(x).ljust(max_str_len, ' '), v))+'},', matrix))
        
        stringified_vectors_with_padded_subvectors[0]  = '{' + stringified_vectors_with_padded_subvectors[0][1:]
        stringified_vectors_with_padded_subvectors[-1] = stringified_vectors_with_padded_subvectors[-1][:-2] + '}}'

        return '\n'.join(stringified_vectors_with_padded_subvectors)
    
    def __str__(self):
        return self.__repr__()
            
    def __add__(self, other):
        if isinstance(other, f16_matrix):
            c_res: Cfloat16_matrix_res_t = linalg_c.f16m_add(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f16_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __sub__(self, other):
        if isinstance(other, f16_matrix):
            c_res: Cfloat16_matrix_res_t = linalg_c.f16m_sub(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f16_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __mul__(self, other):
        if isinstance(other, f16_matrix):
            c_res: Cfloat16_matrix_res_t = linalg_c.f16m_mul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f16_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __truediv__(self, other):
        if isinstance(other, f16_matrix):
            c_res: Cfloat16_matrix_res_t = linalg_c.f16m_div(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 3: raise ZeroDivisionError("Zero found in second operand matrix")
                    case _: raise Exception("Unknown error")
            return f16_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __matmul__(self, other):
        if isinstance(other, f16_matrix):
            c_res: Cfloat16_matrix_res_t = linalg_c.f16m_matmul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"A {self.x}x{self.y} matrix is not compatible with a {other.x}x{other.y} matrix for matrix multiplication")
                    case _: raise Exception("Unknown error")
            return f16_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __neg__(self):
        c_res: Cfloat16_matrix_res_t = linalg_c.f16m_neg(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f16_matrix(getattr(c_res, 'res'))
    
    def exp(self):
        c_res: Cfloat16_matrix_res_t = linalg_c.f16m_exp(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f16_matrix(getattr(c_res, 'res'))
    
    def transpose(self):
        c_res: Cfloat16_matrix_res_t = linalg_c.f16m_transpose(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f16_matrix(getattr(c_res, 'res'))

    def copy(self):
        c_res: Cfloat16_matrix_res_t = linalg_c.copy_f16m(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate matrix copy")
                case _: raise Exception("Unknown error")
        return f16_matrix(getattr(c_res, 'res'))
    
class f32_matrix:
    def __init__(self, m):
        #Type of m: list[list[Float32]]|list[list[f32]]|Cfloat32_matrix_t|f32_matrix

        #*Check if m is a f32_matrix or Cfloat32_matrix_t instance
        if isinstance(m, f32_matrix):
            self.x = m.x
            self.y = m.y
            self.m = m.m
        elif isinstance(m, Cfloat32_matrix_t):
            self.x = int(getattr(m, 'x'))
            self.y = int(getattr(m, 'y'))
            self.m = m
        else:
            #*Check nesting depth of m
            if type(m) is not list or len(m) == 0 or not all(map(lambda v: type(v) is list, m)):
                raise ValueError("Matrix must have a nesting depth of exactly 2")
            
            #*Check if m is empty
            if len(m) == 1 and len(m[0]) == 0:
                raise ValueError("Matrix must not be empty")
            
            #*Check size of each subvector in m
            if not all(map(lambda v: len(v) == len(m[0]), m)):
                raise ValueError("Matrix must be rectangular")

            #*Check if all elements in m have equal type
            first_type = type(m[0][0])
            if not all(map(lambda x: type(x) is first_type, chain.from_iterable(m))):
                raise ValueError("All matrix elements must be of the same type")

            #*Check first type of the input data
            if first_type is f32:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f32_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float32_t * self.x)(*list(map(lambda x: x.val, v))), ctypes.POINTER(float32_t)), m))), ctypes.POINTER(f32_subvector_container))
                
                self.m = Cfloat32_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            elif first_type is dta.Float32:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f32_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float32_t * self.x)(*list(map(lambda x: x.value.val, v))), ctypes.POINTER(float32_t)), m))), ctypes.POINTER(f32_subvector_container))

                self.m = Cfloat32_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            else:
                raise ValueError("Matrix elements must be of type Float32 or f32")
    
    def free(self):
        linalg_c.free_f32m(self.m)
        del self.x
        del self.y

    @staticmethod
    def f32_sci_stringify(f32: float32_t):
        c_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
        numbers_c.conv_f32_to_sci_str(f32, c_stringified_value)
        return c_stringified_value.value.decode('utf-8')+'f'

    def __repr__(self): #All items are left-padded like this: [0.4213312, 0.3212   , 0.3112333]
        matrix = list(map(lambda ptr: ptr[:self.x], getattr(self.m, 'm')[:self.y]))
        max_str_len = max(map(lambda v: len(self.f32_sci_stringify(v)), chain.from_iterable(matrix)))

        stringified_vectors_with_padded_subvectors = list(map(lambda v: ' {'+', '.join(map(lambda x: self.f32_sci_stringify(x).ljust(max_str_len, ' '), v))+'},', matrix))
        
        stringified_vectors_with_padded_subvectors[0]  = '{' + stringified_vectors_with_padded_subvectors[0][1:]
        stringified_vectors_with_padded_subvectors[-1] = stringified_vectors_with_padded_subvectors[-1][:-2] + '}}'

        return '\n'.join(stringified_vectors_with_padded_subvectors)
    
    def __str__(self):
        return self.__repr__()
            
    def __add__(self, other):
        if isinstance(other, f32_matrix):
            c_res: Cfloat32_matrix_res_t = linalg_c.f32m_add(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __sub__(self, other):
        if isinstance(other, f32_matrix):
            c_res: Cfloat32_matrix_res_t = linalg_c.f32m_sub(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __mul__(self, other):
        if isinstance(other, f32_matrix):
            c_res: Cfloat32_matrix_res_t = linalg_c.f32m_mul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __truediv__(self, other):
        if isinstance(other, f32_matrix):
            c_res: Cfloat32_matrix_res_t = linalg_c.f32m_div(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 3: raise ZeroDivisionError("Zero found in second operand matrix")
                    case _: raise Exception("Unknown error")
            return f32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __matmul__(self, other):
        if isinstance(other, f32_matrix):
            c_res: Cfloat32_matrix_res_t = linalg_c.f32m_matmul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"A {self.x}x{self.y} matrix is not compatible with a {other.x}x{other.y} matrix for matrix multiplication")
                    case _: raise Exception("Unknown error")
            return f32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __neg__(self):
        c_res: Cfloat32_matrix_res_t = linalg_c.f32m_neg(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f32_matrix(getattr(c_res, 'res'))
    
    def exp(self):
        c_res: Cfloat32_matrix_res_t = linalg_c.f32m_exp(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f32_matrix(getattr(c_res, 'res'))
    
    def transpose(self):
        c_res: Cfloat32_matrix_res_t = linalg_c.f32m_transpose(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f32_matrix(getattr(c_res, 'res'))
    
    def copy(self):
        c_res: Cfloat32_matrix_res_t = linalg_c.copy_f32m(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate matrix copy")
                case _: raise Exception("Unknown error")
        return f32_matrix(getattr(c_res, 'res'))
    
class f64_matrix:
    def __init__(self, m):
        #Type of m: list[list[Float64]]|list[list[f64]]|Cfloat64_matrix_t|f64_matrix

        #*Check if m is a f64_matrix or Cfloat64_matrix_t instance
        if isinstance(m, f64_matrix):
            self.x = m.x
            self.y = m.y
            self.m = m.m
        elif isinstance(m, Cfloat64_matrix_t):
            self.x = int(getattr(m, 'x'))
            self.y = int(getattr(m, 'y'))
            self.m = m
        else:
            #*Check nesting depth of m
            if type(m) is not list or len(m) == 0 or not all(map(lambda v: type(v) is list, m)):
                raise ValueError("Matrix must have a nesting depth of exactly 2")
            
            #*Check if m is empty
            if len(m) == 1 and len(m[0]) == 0:
                raise ValueError("Matrix must not be empty")
            
            #*Check size of each subvector in m
            if not all(map(lambda v: len(v) == len(m[0]), m)):
                raise ValueError("Matrix must be rectangular")

            #*Check if all elements in m have equal type
            first_type = type(m[0][0])
            if not all(map(lambda x: type(x) is first_type, chain.from_iterable(m))):
                raise ValueError("All matrix elements must be of the same type")

            #*Check first type of the input data
            if first_type is f64:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f64_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float64_t * self.x)(*list(map(lambda x: x.val, v))), ctypes.POINTER(float64_t)), m))), ctypes.POINTER(f64_subvector_container))
                
                self.m = Cfloat64_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            elif first_type is dta.Float64:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((f64_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((float64_t * self.x)(*list(map(lambda x: x.value.val, v))), ctypes.POINTER(float64_t)), m))), ctypes.POINTER(f64_subvector_container))

                self.m = Cfloat64_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            else:
                raise ValueError("Matrix elements must be of type Float64 or f64")
    
    def free(self):
        linalg_c.free_f64m(self.m)
        del self.x
        del self.y

    @staticmethod
    def f64_sci_stringify(f64: float64_t):
        c_stringified_value = ctypes.create_string_buffer(SCIENTIFIC_STR_BUF_SIZE)
        numbers_c.conv_f64_to_sci_str(f64, c_stringified_value)
        return c_stringified_value.value.decode('utf-8')+'d'

    def __repr__(self): #All items are left-padded like this: [0.4213312, 0.6412   , 0.3112333]
        matrix = list(map(lambda ptr: ptr[:self.x], getattr(self.m, 'm')[:self.y]))
        max_str_len = max(map(lambda v: len(self.f64_sci_stringify(v)), chain.from_iterable(matrix)))

        stringified_vectors_with_padded_subvectors = list(map(lambda v: ' {'+', '.join(map(lambda x: self.f64_sci_stringify(x).ljust(max_str_len, ' '), v))+'},', matrix))
        
        stringified_vectors_with_padded_subvectors[0]  = '{' + stringified_vectors_with_padded_subvectors[0][1:]
        stringified_vectors_with_padded_subvectors[-1] = stringified_vectors_with_padded_subvectors[-1][:-2] + '}}'

        return '\n'.join(stringified_vectors_with_padded_subvectors)
    
    def __str__(self):
        return self.__repr__()
            
    def __add__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.f64m_add(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __sub__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.f64m_sub(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __mul__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.f64m_mul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __truediv__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.f64m_div(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 3: raise ZeroDivisionError("Zero found in second operand matrix")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __matmul__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.f64m_matmul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"A {self.x}x{self.y} matrix is not compatible with a {other.x}x{other.y} matrix for matrix multiplication")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __neg__(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.f64m_neg(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
    
    def exp(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.f64m_exp(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
    
    def transpose(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.f64m_transpose(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
    
    def copy(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.copy_f64m(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate matrix copy")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
        
class i32_matrix:
    def __init__(self, m):
        #Type of m: list[list[Int32]]|list[list[i32]]|Cfloat32_matrix_t|i32_matrix

        #*Check if m is a i32_matrix or Cint32_matrix_t instance
        if isinstance(m, i32_matrix):
            self.x = m.x
            self.y = m.y
            self.m = m.m
        elif isinstance(m, Cint32_matrix_t):
            self.x = int(getattr(m, 'x'))
            self.y = int(getattr(m, 'y'))
            self.m = m
        else:
            #*Check nesting depth of m
            if type(m) is not list or len(m) == 0 or not all(map(lambda v: type(v) is list, m)):
                raise ValueError("Matrix must have a nesting depth of exactly 2")
            
            #*Check if m is empty
            if len(m) == 1 and len(m[0]) == 0:
                raise ValueError("Matrix must not be empty")
            
            #*Check size of each subvector in m
            if not all(map(lambda v: len(v) == len(m[0]), m)):
                raise ValueError("Matrix must be rectangular")

            #*Check if all elements in m have equal type
            first_type = type(m[0][0])
            if not all(map(lambda x: type(x) is first_type, chain.from_iterable(m))):
                raise ValueError("All matrix elements must be of the same type")

            #*Check first type of the input data
            if first_type is i32:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((i32_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((int32_t * self.x)(*list(map(lambda x: x.val, v))), ctypes.POINTER(int32_t)), m))), ctypes.POINTER(i32_subvector_container))
                
                self.m = Cint32_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            elif first_type is dta.Int32:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((i32_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((int32_t * self.x)(*list(map(lambda x: x.value.val, v))), ctypes.POINTER(int32_t)), m))), ctypes.POINTER(i32_subvector_container))

                self.m = Cint32_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            else:
                raise ValueError("Matrix elements must be of type Int32 or dta.Int32")
    
    def free(self):
        linalg_c.free_i32m(self.m)
        del self.x
        del self.y

    @staticmethod
    def i32_stringify(i32: int32_t):
        c_stringified_value = ctypes.create_string_buffer(INT_STR_BUF_SIZE)
        numbers_c.conv_i32_to_str(i32, c_stringified_value)
        return c_stringified_value.value.decode('utf-8')+'i'

    def __repr__(self): #All items are left-padded like this: [0.4213312, 0.6412   , 0.3112333]
        matrix = list(map(lambda ptr: ptr[:self.x], getattr(self.m, 'm')[:self.y]))
        max_str_len = max(map(lambda v: len(self.i32_stringify(v)), chain.from_iterable(matrix)))

        stringified_vectors_with_padded_subvectors = list(map(lambda v: ' {'+', '.join(map(lambda x: self.i32_stringify(x).ljust(max_str_len, ' '), v))+'},', matrix))
        
        stringified_vectors_with_padded_subvectors[0]  = '{' + stringified_vectors_with_padded_subvectors[0][1:]
        stringified_vectors_with_padded_subvectors[-1] = stringified_vectors_with_padded_subvectors[-1][:-2] + '}}'

        return '\n'.join(stringified_vectors_with_padded_subvectors)
    
    def __str__(self):
        return self.__repr__()
            
    def __add__(self, other):
        if isinstance(other, i32_matrix):
            c_res: Cint32_matrix_res_t = linalg_c.i32m_add(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __sub__(self, other):
        if isinstance(other, i32_matrix):
            c_res: Cint32_matrix_res_t = linalg_c.i32m_sub(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __mul__(self, other):
        if isinstance(other, i32_matrix):
            c_res: Cint32_matrix_res_t = linalg_c.i32m_mul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __truediv__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.i32m_div(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 3: raise ZeroDivisionError("Zero found in second operand matrix")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __matmul__(self, other):
        if isinstance(other, i32_matrix):
            c_res: Cint32_matrix_res_t = linalg_c.i32m_matmul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"A {self.x}x{self.y} matrix is not compatible with a {other.x}x{other.y} matrix for matrix multiplication")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i32_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __neg__(self):
        c_res: Cint32_matrix_res_t = linalg_c.i32m_neg(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case 4: raise OverflowError('Integer overflow')
                case _: raise Exception("Unknown error")
        return i32_matrix(getattr(c_res, 'res'))
    
    def exp(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.i32m_exp(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
    
    def transpose(self):
        c_res: Cint32_matrix_res_t = linalg_c.i32m_transpose(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return i32_matrix(getattr(c_res, 'res'))
    
    def copy(self):
        c_res: Cint32_matrix_res_t = linalg_c.copy_i32m(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate matrix copy")
                case _: raise Exception("Unknown error")
        return i32_matrix(getattr(c_res, 'res'))

class i64_matrix:
    def __init__(self, m):
        #Type of m: list[list[Int64]]|list[list[i64]]|Cfloat64_matrix_t|i64_matrix

        #*Check if m is a i64_matrix or Cint64_matrix_t instance
        if isinstance(m, i64_matrix):
            self.x = m.x
            self.y = m.y
            self.m = m.m
        elif isinstance(m, Cint64_matrix_t):
            self.x = int(getattr(m, 'x'))
            self.y = int(getattr(m, 'y'))
            self.m = m
        else:
            #*Check nesting depth of m
            if type(m) is not list or len(m) == 0 or not all(map(lambda v: type(v) is list, m)):
                raise ValueError("Matrix must have a nesting depth of exactly 2")
            
            #*Check if m is empty
            if len(m) == 1 and len(m[0]) == 0:
                raise ValueError("Matrix must not be empty")
            
            #*Check size of each subvector in m
            if not all(map(lambda v: len(v) == len(m[0]), m)):
                raise ValueError("Matrix must be rectangular")

            #*Check if all elements in m have equal type
            first_type = type(m[0][0])
            if not all(map(lambda x: type(x) is first_type, chain.from_iterable(m))):
                raise ValueError("All matrix elements must be of the same type")

            #*Check first type of the input data
            if first_type is i64:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((i64_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((int64_t * self.x)(*list(map(lambda x: x.val, v))), ctypes.POINTER(int64_t)), m))), ctypes.POINTER(i64_subvector_container))
                
                self.m = Cint64_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            elif first_type is dta.Int64:
                self.y = len(m)
                self.x = len(m[0])

                m = ctypes.cast((i64_subvector_container * self.y)(*list(map(lambda v: ctypes.cast((int64_t * self.x)(*list(map(lambda x: x.value.val, v))), ctypes.POINTER(int64_t)), m))), ctypes.POINTER(i64_subvector_container))

                self.m = Cint64_matrix_t(m, ctypes.c_size_t(self.x), ctypes.c_size_t(self.y))
            else:
                raise ValueError("Matrix elements must be of type Int64 or i64")
    
    def free(self):
        linalg_c.free_i64m(self.m)
        del self.x
        del self.y

    @staticmethod
    def i64_stringify(i64: int64_t):
        c_stringified_value = ctypes.create_string_buffer(LONG_STR_BUF_SIZE)
        numbers_c.conv_i64_to_str(i64, c_stringified_value)
        return c_stringified_value.value.decode('utf-8')+'l'

    def __repr__(self): #All items are left-padded like this: [0.4213312, 0.6412   , 0.3112333]
        matrix = list(map(lambda ptr: ptr[:self.x], getattr(self.m, 'm')[:self.y]))
        max_str_len = max(map(lambda v: len(self.i64_stringify(v)), chain.from_iterable(matrix)))

        stringified_vectors_with_padded_subvectors = list(map(lambda v: ' {'+', '.join(map(lambda x: self.i64_stringify(x).ljust(max_str_len, ' '), v))+'},', matrix))
        
        stringified_vectors_with_padded_subvectors[0]  = '{' + stringified_vectors_with_padded_subvectors[0][1:]
        stringified_vectors_with_padded_subvectors[-1] = stringified_vectors_with_padded_subvectors[-1][:-2] + '}}'

        return '\n'.join(stringified_vectors_with_padded_subvectors)
    
    def __str__(self):
        return self.__repr__()
            
    def __add__(self, other):
        if isinstance(other, i64_matrix):
            c_res: Cint64_matrix_res_t = linalg_c.i64m_add(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __sub__(self, other):
        if isinstance(other, i64_matrix):
            c_res: Cint64_matrix_res_t = linalg_c.i64m_sub(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __mul__(self, other):
        if isinstance(other, i64_matrix):
            c_res: Cint64_matrix_res_t = linalg_c.i64m_mul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __truediv__(self, other):
        if isinstance(other, f64_matrix):
            c_res: Cfloat64_matrix_res_t = linalg_c.i64m_div(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"Matrix sizes must be equal ({self.x}x{self.y} != {other.x}x{other.y})")
                    case 3: raise ZeroDivisionError("Zero found in second operand matrix")
                    case _: raise Exception("Unknown error")
            return f64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __matmul__(self, other):
        if isinstance(other, i64_matrix):
            c_res: Cint64_matrix_res_t = linalg_c.i64m_matmul(self.m, other.m)
            err: int = getattr(c_res, 'err')
            if err != 0:
                match err:
                    case 1: raise MemoryError("Failed to allocate resulting matrix")
                    case 2: raise ValueError(f"A {self.x}x{self.y} matrix is not compatible with a {other.x}x{other.y} matrix for matrix multiplication")
                    case 4: raise OverflowError('Integer overflow')
                    case 5: raise OverflowError('Integer underflow')
                    case _: raise Exception("Unknown error")
            return i64_matrix(getattr(c_res, 'res'))
        else:
            raise ValueError("Matrix types must be same")
        
    def __neg__(self):
        c_res: Cint64_matrix_res_t = linalg_c.i64m_neg(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case 4: raise OverflowError('Integer overflow')
                case _: raise Exception("Unknown error")
        return i64_matrix(getattr(c_res, 'res'))
    
    def exp(self):
        c_res: Cfloat64_matrix_res_t = linalg_c.i64m_exp(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return f64_matrix(getattr(c_res, 'res'))
    
    def transpose(self):
        c_res: Cint64_matrix_res_t = linalg_c.i64m_transpose(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate resulting matrix")
                case _: raise Exception("Unknown error")
        return i64_matrix(getattr(c_res, 'res'))
    
    def copy(self):
        c_res: Cint64_matrix_res_t = linalg_c.copy_i64m(self.m)
        err: int = getattr(c_res, 'err')
        if err != 0:
            match err:
                case 1: raise MemoryError("Failed to allocate matrix copy")
                case _: raise Exception("Unknown error")
        return i64_matrix(getattr(c_res, 'res'))
    
# Fill and broadcast functions
#*Fill functions
def f16m_fill(x: ctypes.c_size_t, y: ctypes.c_size_t, fill_value: f16) -> f16_matrix:
    if x.value < 1 or y.value < 1:
        raise ValueError("Matrix dimensions must be above or equal to 1 row and 1 column")

    c_res: Cfloat16_matrix_res_t = linalg_c.f16m_fill(x, y, fill_value.val)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")
    return f16_matrix(getattr(c_res, 'res'))

def f32m_fill(x: ctypes.c_size_t, y: ctypes.c_size_t, fill_value: f32) -> f32_matrix:
    if x.value < 1 or y.value < 1:
        raise ValueError("Matrix dimensions must be above or equal to 1 row and 1 column")

    c_res: Cfloat32_matrix_res_t = linalg_c.f32m_fill(x, y, fill_value.val)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")
    return f32_matrix(getattr(c_res, 'res'))

def f64m_fill(x: ctypes.c_size_t, y: ctypes.c_size_t, fill_value: f64) -> f64_matrix:
    if x.value < 1 or y.value < 1:
        raise ValueError("Matrix dimensions must be above or equal to 1 row and 1 column")

    c_res: Cfloat64_matrix_res_t = linalg_c.f64m_fill(x, y, fill_value.val)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")
    return f64_matrix(getattr(c_res, 'res'))

def i32m_fill(x: ctypes.c_size_t, y: ctypes.c_size_t, fill_value: i32) -> i32_matrix:
    if x.value < 1 or y.value < 1:
        raise ValueError("Matrix dimensions must be above or equal to 1 row and 1 column")

    c_res: Cint32_matrix_res_t = linalg_c.i32m_fill(x, y, fill_value.val)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")
    return i32_matrix(getattr(c_res, 'res'))

def i64m_fill(x: ctypes.c_size_t, y: ctypes.c_size_t, fill_value: i64) -> i64_matrix:
    if x.value < 1 or y.value < 1:
        raise ValueError("Matrix dimensions must be above or equal to 1 row and 1 column")

    c_res: Cint64_matrix_res_t = linalg_c.i64m_fill(x, y, fill_value.val)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")
    return i64_matrix(getattr(c_res, 'res'))

#*(Row vector->matrix) broadcast functions
def f16m_row_vector_to_matrix(v: f16_matrix, no_rows: ctypes.c_size_t) -> f16_matrix:
    if no_rows.value < 1:
        raise ValueError("Number of rows must be above or equal to 1")

    c_res: Cfloat16_matrix_res_t = linalg_c.f16m_row_vector_to_matrix(v.m, no_rows)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.y} rows (expected 1 row)")
            case _: raise Exception("Unknown error")
    return f16_matrix(getattr(c_res, 'res'))

def f32m_row_vector_to_matrix(v: f32_matrix, no_rows: ctypes.c_size_t) -> f32_matrix:
    if no_rows.value < 1:
        raise ValueError("Number of rows must be above or equal to 1")

    c_res: Cfloat32_matrix_res_t = linalg_c.f32m_row_vector_to_matrix(v.m, no_rows)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.y} rows (expected 1 row)")
            case _: raise Exception("Unknown error")
    return f32_matrix(getattr(c_res, 'res'))

def f64m_row_vector_to_matrix(v: f64_matrix, no_rows: ctypes.c_size_t) -> f64_matrix:
    if no_rows.value < 1:
        raise ValueError("Number of rows must be above or equal to 1")

    c_res: Cfloat64_matrix_res_t = linalg_c.f64m_row_vector_to_matrix(v.m, no_rows)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.y} rows (expected 1 row)")
            case _: raise Exception("Unknown error")
    return f64_matrix(getattr(c_res, 'res'))

def i32m_row_vector_to_matrix(v: i32_matrix, no_rows: ctypes.c_size_t) -> i32_matrix:
    if no_rows.value < 1:
        raise ValueError("Number of rows must be above or equal to 1")

    c_res: Cint32_matrix_res_t = linalg_c.i32m_row_vector_to_matrix(v.m, no_rows)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.y} rows (expected 1 row)")
            case _: raise Exception("Unknown error")
    return i32_matrix(getattr(c_res, 'res'))

def i64m_row_vector_to_matrix(v: i64_matrix, no_rows: ctypes.c_size_t) -> i64_matrix:
    if no_rows.value < 1:
        raise ValueError("Number of rows must be above or equal to 1")

    c_res: Cint64_matrix_res_t = linalg_c.i64m_row_vector_to_matrix(v.m, no_rows)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.y} rows (expected 1 row)")
            case _: raise Exception("Unknown error")
    return i64_matrix(getattr(c_res, 'res'))

#*(Column vector->matrix) broadcast functions
def f16m_column_vector_to_matrix(v: f16_matrix, no_columns: ctypes.c_size_t) -> f16_matrix:
    if no_columns.value < 1:
        raise ValueError("Number of columns must be above or equal to 1")

    c_res: Cfloat16_matrix_res_t = linalg_c.f16m_column_vector_to_matrix(v.m, no_columns)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.x} columns (expected 1 column)")
            case _: raise Exception("Unknown error")
    return f16_matrix(getattr(c_res, 'res'))

def f32m_column_vector_to_matrix(v: f32_matrix, no_columns: ctypes.c_size_t) -> f32_matrix:
    if no_columns.value < 1:
        raise ValueError("Number of columns must be above or equal to 1")

    c_res: Cfloat32_matrix_res_t = linalg_c.f32m_column_vector_to_matrix(v.m, no_columns)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.x} columns (expected 1 column)")
            case _: raise Exception("Unknown error")
    return f32_matrix(getattr(c_res, 'res'))

def f64m_column_vector_to_matrix(v: f64_matrix, no_columns: ctypes.c_size_t) -> f64_matrix:
    if no_columns.value < 1:
        raise ValueError("Number of columns must be above or equal to 1")

    c_res: Cfloat64_matrix_res_t = linalg_c.f64m_column_vector_to_matrix(v.m, no_columns)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.x} columns (expected 1 column)")
            case _: raise Exception("Unknown error")
    return f64_matrix(getattr(c_res, 'res'))

def i32m_column_vector_to_matrix(v: i32_matrix, no_columns: ctypes.c_size_t) -> i32_matrix:
    if no_columns.value < 1:
        raise ValueError("Number of columns must be above or equal to 1")

    c_res: Cint32_matrix_res_t = linalg_c.i32m_column_vector_to_matrix(v.m, no_columns)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.x} columns (expected 1 column)")
            case _: raise Exception("Unknown error")
    return i32_matrix(getattr(c_res, 'res'))

def i64m_column_vector_to_matrix(v: i64_matrix, no_columns: ctypes.c_size_t) -> i64_matrix:
    if no_columns.value < 1:
        raise ValueError("Number of columns must be above or equal to 1")

    c_res: Cint64_matrix_res_t = linalg_c.i64m_column_vector_to_matrix(v.m, no_columns)
    err: int = getattr(c_res, 'err')
    if err != 0:
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case 2: raise ValueError(f"Input matrix has {v.x} columns (expected 1 column)")
            case _: raise Exception("Unknown error")
    return i64_matrix(getattr(c_res, 'res'))

# Matrix casting
py_matrix_type_to_matrix_type_t = {
    f16_matrix: (matrix_type_t(0), 'f16m'),
    f32_matrix: (matrix_type_t(1), 'f32m'),
    f64_matrix: (matrix_type_t(2), 'f64m'),
    i32_matrix: (matrix_type_t(3), 'i32m'),
    i64_matrix: (matrix_type_t(4), 'i64m'),
    u32_matrix: (matrix_type_t(5), 'u32m'),
    u64_matrix: (matrix_type_t(6), 'u64m'),
}

int_to_py_matrix = {
    0: (f16_matrix, 'f16m'),
    1: (f32_matrix, 'f32m'),
    2: (f64_matrix, 'f64m'),
    3: (i32_matrix, 'i32m'),
    4: (i64_matrix, 'i64m'),
    5: (u32_matrix, 'u32m'),
    6: (u64_matrix, 'u64m'),
}

def matrix_cast(m: matrix_t, tgt_type: type) -> matrix_t:
    c_current_type  = py_matrix_type_to_matrix_type_t[type(m)]
    c_tgt_type      = py_matrix_type_to_matrix_type_t[tgt_type]

    container = Cmatrix_container_t()

    setattr(container, c_current_type[1], m.m)

    out_res: Cmatrix_cast_res_t = linalg_c.matrix_cast(Cmatrix_t(container, c_current_type[0]), c_tgt_type[0])

    err: int = getattr(out_res, 'err')
    if err != 0:
        print(err) #*DEBUG
        match err:
            case 1: raise MemoryError("Failed to allocate matrix")
            case _: raise Exception("Unknown error")

    out_container = getattr(out_res, 'res_matrix')

    out_type = getattr(out_container, 'matrix_type')

    out = int_to_py_matrix[out_type][0](getattr(getattr(out_container, 'm'), int_to_py_matrix[out_type][1]))

    return out