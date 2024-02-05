import ctypes
import os

numbers_c = ctypes.CDLL(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/c_lib/random/lib/random.so')

# Typedefs
float16_t           = ctypes.c_ushort
float32_t           = ctypes.c_float
float64_t           = ctypes.c_double
int32_t             = ctypes.c_int32
int64_t             = ctypes.c_int64
uint32_t            = ctypes.c_uint32
uint64_t            = ctypes.c_uint64

# Structs
class i32resWboolErr_t(ctypes.Structure):
    _fields_ = [
        ("n", int32_t),
        ("has_err", ctypes.c_bool),
    ]

class i64resWboolErr_t(ctypes.Structure):
    _fields_ = [
        ("n", int64_t),
        ("has_err", ctypes.c_bool),
    ]

class f16resWboolErr_t(ctypes.Structure):
    _fields_ = [
        ("n", float16_t),
        ("has_err", ctypes.c_bool),
    ]

class f32resWboolErr_t(ctypes.Structure):
    _fields_ = [
        ("n", float32_t),
        ("has_err", ctypes.c_bool),
    ]

class f64resWboolErr_t(ctypes.Structure):
    _fields_ = [
        ("n", float64_t),
        ("has_err", ctypes.c_bool),
    ]