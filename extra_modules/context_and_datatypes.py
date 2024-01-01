# Imports
from extra_modules.results import *
from extra_modules.position import *
import extra_modules.Errors as err
import extra_modules.Warnings as wrn
import extra_modules.numbers as numbers
import extra_modules.linalg as linalg

from dataclasses import dataclass
from copy import deepcopy
import weakref
import os
import importlib
import importlib.util
import ctypes
import string

# Constants
## Index types
INDEX_TYPE_INT      = 'int'
INDEX_TYPE_FLOAT    = 'float'
INDEX_TYPE_KEY      = 'key'
    
# Main datatypes
## BaseValue and Type types
class BaseValue:
    def __init__(self):
        self.set_pos()
        self.set_context()
        self.type = 'BaseValue'

    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    def set_context(self, context=None):
        self.context = context
        return self
    
    '''
    def is_truthy(self):
        if (x := getattr(self, 'value', None)):
            if type(x) is str:
                return len(x) != 0
            elif type(x) is int or type(x) is float:
                return x != 0
        elif (x := getattr(self, 'elements', None)):
            if type(x) is dict:
                return len(x) != 0
            elif type(x) is list or type(x) is collections.deque:
                def is_tech_filled(_list):
                    if len(_list) == 0:
                        return False
                    elif len(_list) == 1 and type(_list) is list or type(_list) is collections.deque:
                        return is_tech_filled(_list[0])
                    else:
                        return True
                return is_tech_filled(x)
        elif (x := getattr(self, 'context', None)):
            x: Context
            return len(x.symbol_table.symbols) != 0
    '''

    def add_by(self, other):
        return None, self.illegal_operation(other)
        
    def sub_by(self, other):
        return None, self.illegal_operation(other)
        
    def mult_by(self, other):
        return None, self.illegal_operation(other)
    
    def matmult_by(self, other):
        return None, self.illegal_operation(other)
        
    def div_by(self, other):
        return None, self.illegal_operation(other)
        
    def pow_by(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_eq(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_ne(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_lt(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_gt(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_lte(self, other):
        return None, self.illegal_operation(other)
        
    def get_comparison_gte(self, other):
        return None, self.illegal_operation(other)
        
    def and_by(self, other):
        return None, self.illegal_operation(other)
        
    def or_by(self, other):
        return None, self.illegal_operation(other)
    
    def bitwise_and_by(self, other):
        return None, self.illegal_operation(other)
    
    def bitwise_or_by(self, other):
        return None, self.illegal_operation(other)
    
    def bitwise_xor_by(self, other):
        return None, self.illegal_operation(other)
    
    def left_shift_by(self, other):
        return None, self.illegal_operation(other)
    
    def right_shift_by(self, other):
        return None, self.illegal_operation(other)
    
    def complement(self, other):
        return None, self.illegal_operation(other)
    
    def not_(self):
        return None, self.illegal_operation()
    
    def neg(self):
        return None, self.illegal_operation()
    
    def execute(self):
        return None, self.illegal_operation()
    
    def copy(self):
        raise Exception('No copy method defined')

    def is_true(self):
        return False

    def illegal_operation(self, other=None):
        if other is None: other = self
        return err.RTError(
            self.pos_start, other.pos_end,
            'Illegal operation',
            self.context
        )
    
    def __len__(self):
        return RTResult().failure(err.RTError(
            self.pos_start, self.pos_end,
            'len() not defined on this type (not an iterable)',
            self.context
        ))

class Type(BaseValue):
    def __init__(self, typename: str|None = None):
        super().__init__()
        self.type = 'Type'
        self.typename = typename

    def is_true(self):
        return len(self.typename) > 0
    
    def copy(self):
        copy = Type(self.typename)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
        
    def __str__(self):
        return f'{"Any" if not self.typename else self.typename}'

    def __repr__(self):
        return f'Type("{self.__str__()}")'
Type.Any  = Type()
Type.Type = Type('Type')

## Null type
Type.Null       = Type('Null')
class Null(BaseValue):
    def __init__(self):
        super().__init__()
        self.type = 'Null'

    def is_true(self):
        return len(self.typename) > 0
    
    def copy(self):
        '''
        copy = self
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
        '''
        return self
        
    def __str__(self):
        return 'Null'

    def __repr__(self):
        return self.__str__()
Null.null = Null()

## Integer types
Type.Integer    = Type('Integer')
class Integer(BaseValue): #BigInteger
    def __init__(self, value: int):
        super().__init__()
        self.type = 'Integer'
        self.value = value

    def add_by(self, other):
        if isinstance(other, Integer):
            return Integer(self.value + other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Integer):
            return Integer(self.value - other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Integer):
            return Integer(self.value * other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Integer):
            if other.value == 0:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
            return Float64(numbers.f64(numbers.float64_t(self.value / other.value))).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def pow_by(self, other):
        if isinstance(other, Integer):
            return Integer(self.value ** other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value == other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value != other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value < other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value > other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value <= other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value >= other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def and_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value and other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def or_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value or other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def bitwise_and_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value & other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def bitwise_or_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value | other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def bitwise_xor_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value ^ other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def left_shift_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value << other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def right_shift_by(self, other):
        if isinstance(other, Integer):
            return Integer(int(self.value >> other.value)).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def complement(self):
        return Integer(int(~self.value)).set_context(self.context), None
    
    def not_(self):
        return Integer(int(not self.value)).set_context(self.context), None
    
    def neg(self):
        return Integer(int(-self.value)).set_context(self.context), None
    
    def copy(self):
        copy = Integer(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.value != 0

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Integer.false   = Integer(0)
Integer.true    = Integer(1)

Type.Int32 = Type('Int32')
class Int32(BaseValue):
    def __init__(self, value: str|int|numbers.i32):
        super().__init__()
        self.type = 'Int32'

        if isinstance(value, str) or isinstance(value, int):
            self.value: numbers.i32 = numbers.i32(value)
        else:
            self.value: numbers.i32 = value
    
    def add_by(self, other):
        if isinstance(other, Int32):
            try:
                return Int32(self.value + other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Int32):
            try:
                return Int32(self.value - other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)

    def mult_by(self, other):
        if isinstance(other, Int32):
            try:
                return Int32(self.value * other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def div_by(self, other):
        if isinstance(other, Int32):
            try:
                return Float64(self.value / other.value), None
            except ZeroDivisionError:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def pow_by(self, other):
        if isinstance(other, Int32):
            return Float64(self.value ** other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value == other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value < other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value > other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value <= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Int32):
            return Integer(int(self.value >= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def bitwise_and_by(self, other):
        if isinstance(other, Int32):
            return Int32(self.value & other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def bitwise_or_by(self, other):
        if isinstance(other, Int32):
            return Int32(self.value | other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def bitwise_xor_by(self, other):
        if isinstance(other, Int32):
            return Int32(self.value ^ other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def left_shift_by(self, other):
        if isinstance(other, Int32):
            return Int32(self.value << other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def right_shift_by(self, other):
        if isinstance(other, Int32):
            return Int32(self.value >> other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def complement(self):
        return Int32(~self.value).set_context(self.context), None

    def not_(self):
        n = Int32(0) if self.is_true() else Int32(1)
        return n, None

    def neg(self):
        try:
            return Int32(-self.value), None
        except OverflowError as e:
            return None, err.IntegerOverflowError(self.pos_start, self.pos_end, e, self.context)

    def copy(self):
        copy = Int32(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.get_comparison_ne(Int32.zero)[0].value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Int32.zero = Int32(0)

Type.Int64 = Type('Int64')
class Int64(BaseValue):
    def __init__(self, value: str|int|numbers.i64):
        super().__init__()
        self.type = 'Int64'

        if isinstance(value, str) or isinstance(value, int):
            self.value: numbers.i64 = numbers.i64(value)
        else:
            self.value: numbers.i64 = value
    
    def add_by(self, other):
        if isinstance(other, Int64):
            try:
                return Int64(self.value + other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Int64):
            try:
                return Int64(self.value - other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)

    def mult_by(self, other):
        if isinstance(other, Int64):
            try:
                return Int64(self.value * other.value), None
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def div_by(self, other):
        if isinstance(other, Int64):
            try:
                return Float64(self.value / other.value), None
            except ZeroDivisionError:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def pow_by(self, other):
        if isinstance(other, Int64):
            return Float64(self.value ** other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value == other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def get_comparison_ne(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)

    def get_comparison_ne(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value < other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value > other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value <= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Int64):
            return Integer(int(self.value >= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def bitwise_and_by(self, other):
        if isinstance(other, Int64):
            return Int64(self.value & other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def bitwise_or_by(self, other):
        if isinstance(other, Int64):
            return Int64(self.value | other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def bitwise_xor_by(self, other):
        if isinstance(other, Int64):
            return Int64(self.value ^ other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def left_shift_by(self, other):
        if isinstance(other, Int64):
            return Int64(self.value << other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def right_shift_by(self, other):
        if isinstance(other, Int64):
            return Int64(self.value >> other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def complement(self):
        return Int64(~self.value).set_context(self.context), None

    def not_(self):
        n = Int64(0) if self.is_true() else Int64(1)
        return n, None

    def neg(self):
        try:
            return Int64(-self.value), None
        except OverflowError as e:
            return None, err.IntegerOverflowError(self.pos_start, self.pos_end, e, self.context)

    def copy(self):
        copy = Int64(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.get_comparison_ne(Int64.zero)[0].value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Int64.zero = Int64(0)

## Float types

Type.Float16 = Type('Float16')
class Float16(BaseValue):
    def __init__(self, value: str|numbers.f16):
        super().__init__()
        self.type = 'Float16'

        if isinstance(value, str):
            self.value: numbers.f16 = numbers.f16(value)
        else:
            self.value: numbers.f16 = value

    def add_by(self, other):
        if isinstance(other, Float16):
            return Float16(self.value + other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float16):
            return Float16(self.value - other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float16):
            return Float16(self.value * other.value), None
        elif isinstance(other, Integer) and other.value == -1:
            return Float16(-self.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float16):
            try:
                return Float16(self.value / other.value), None
            except ZeroDivisionError:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def pow_by(self, other):
        if isinstance(other, Float16):
            return Float16(self.value ^ other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value == other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value < other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value > other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value <= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Float16):
            return Integer(int(self.value >= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def neg(self):
        return Float16(-self.value), None

    def copy(self):
        copy = Float16(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.get_comparison_ne(Float16.zero)[0].value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Float16.zero = Float16('0')

Type.Float32 = Type('Float32')
class Float32(BaseValue):
    def __init__(self, value: str|numbers.f32):
        super().__init__()
        self.type = 'Float32'

        if isinstance(value, str):
            self.value: numbers.f32 = numbers.f32(value)
        else:
            self.value: numbers.f32 = value

    def add_by(self, other):
        if isinstance(other, Float32):
            return Float32(self.value + other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float32):
            return Float32(self.value - other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float32):
            return Float32(self.value * other.value), None
        elif isinstance(other, Integer) and other.value == -1:
            return Float32(-self.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float32):
            try:
                return Float32(self.value / other.value), None
            except ZeroDivisionError:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def pow_by(self, other):
        if isinstance(other, Float32):
            return Float32(self.value ^ other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value == other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value < other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value > other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value <= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Float32):
            return Integer(int(self.value >= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def neg(self):
        return Float32(-self.value), None

    def copy(self):
        copy = Float32(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.get_comparison_ne(Float32.zero)[0].value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Float32.zero = Float32('0')

Type.Float64 = Type('Float64')
class Float64(BaseValue):
    def __init__(self, value: str|numbers.f64):
        super().__init__()
        self.type = 'Float64'

        if isinstance(value, str):
            self.value: numbers.f64 = numbers.f64(value)
        else:
            self.value: numbers.f64 = value

    def add_by(self, other):
        if isinstance(other, Float64):
            return Float64(self.value + other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float64):
            return Float64(self.value - other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float64):
            return Float64(self.value * other.value), None
        elif isinstance(other, Integer) and other.value == -1:
            return Float64(-self.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float64):
            try:
                return Float64(self.value / other.value), None
            except ZeroDivisionError:
                return None, err.RTError(
                    other.pos_start, other.pos_end,
                    'Division by zero',
                    self.context
                )
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def pow_by(self, other):
        if isinstance(other, Float64):
            return Float64(self.value ^ other.value), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_eq(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value == other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_ne(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value != other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lt(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value < other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gt(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value > other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_lte(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value <= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def get_comparison_gte(self, other):
        if isinstance(other, Float64):
            return Integer(int(self.value >= other.value)), None
        else:
            return None, BaseValue.illegal_operation(self, other)
    
    def neg(self):
        return Float64(-self.value), None

    def copy(self):
        copy = Float64(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy

    def is_true(self):
        return self.get_comparison_ne(Float64.zero)[0].value

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return self.__str__()
Float64.zero = Float64('0')

## Matrix types
Type.Float16Matrix = Type('Float16Matrix')
class Float16Matrix(BaseValue):
    def __init__(self, matrix: linalg.f16_matrix):
        super().__init__()
        self.type = 'Float16Matrix'
        self.matrix = matrix
    
    def __repr__(self):
        return repr(self.matrix)
    
    def __str__(self):
        return str(self.matrix)

    def add_by(self, other):
        if isinstance(other, Float16Matrix):
            try:
                return Float16Matrix(self.matrix + other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float16Matrix):
            try:
                return Float16Matrix(self.matrix - other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float16Matrix):
            try:
                return Float16Matrix(self.matrix * other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float16Matrix):
            try:
                return Float16Matrix(self.matrix / other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.rterror(self.pos_start, other.pos_end, e, self.context)
            except ZeroDivisionError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def matmult_by(self, other):
        if isinstance(other, Float16Matrix):
            try:
                return Float16Matrix(self.matrix @ other.matrix), None
            except MemoryError as e:
                return None, err.mallocerror(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def neg(self):
        try:
            return Float16Matrix(-self.matrix), None
        except MemoryError as e:
            return None, err.MallocError(self.pos_start, self.pos_end, e, self.context)
        except Exception as e:
            return None, err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
    
    def copy(self):
        try:
            return Float16Matrix(self.matrix.copy())
        except Exception as e:
            wrn.CopyWarning(self.pos_start, self.pos_end, e)
            return Null()

    def is_true(self):
        return True
    
    def free_mem(self):
        self.matrix.free()

Type.Float32Matrix = Type('Float32Matrix')
class Float32Matrix(BaseValue):
    def __init__(self, matrix: linalg.f32_matrix):
        super().__init__()
        self.type = 'Float32Matrix'
        self.matrix = matrix
    
    def __repr__(self):
        return repr(self.matrix)
    
    def __str__(self):
        return str(self.matrix)

    def add_by(self, other):
        if isinstance(other, Float32Matrix):
            try:
                return Float32Matrix(self.matrix + other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float32Matrix):
            try:
                return Float32Matrix(self.matrix - other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float32Matrix):
            try:
                return Float32Matrix(self.matrix * other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float32Matrix):
            try:
                return Float32Matrix(self.matrix / other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except ZeroDivisionError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def matmult_by(self, other):
        if isinstance(other, Float32Matrix):
            try:
                return Float32Matrix(self.matrix @ other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def neg(self):
        try:
            return Float32Matrix(-self.matrix), None
        except MemoryError as e:
            return None, err.MallocError(self.pos_start, self.pos_end, e, self.context)
        except Exception as e:
            return None, err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
    
    def copy(self):
        try:
            return Float32Matrix(self.matrix.copy())
        except Exception as e:
            wrn.CopyWarning(self.pos_start, self.pos_end, e)
            return Null()

    def is_true(self):
        return True
    
    def free_mem(self):
        self.matrix.free()

Type.Float64Matrix = Type('Float64Matrix')
class Float64Matrix(BaseValue):
    def __init__(self, matrix: linalg.f64_matrix):
        super().__init__()
        self.type = 'Float64Matrix'
        self.matrix = matrix
    
    def __repr__(self):
        return repr(self.matrix)
    
    def __str__(self):
        return str(self.matrix)

    def add_by(self, other):
        if isinstance(other, Float64Matrix):
            try:
                return Float64Matrix(self.matrix + other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Float64Matrix):
            try:
                return Float64Matrix(self.matrix - other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Float64Matrix):
            try:
                return Float64Matrix(self.matrix * other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Float64Matrix):
            try:
                return Float64Matrix(self.matrix / other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except ZeroDivisionError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def matmult_by(self, other):
        if isinstance(other, Float64Matrix):
            try:
                return Float64Matrix(self.matrix @ other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def neg(self):
        try:
            return Float64Matrix(-self.matrix), None
        except MemoryError as e:
            return None, err.MallocError(self.pos_start, self.pos_end, e, self.context)
        except Exception as e:
            return None, err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
    
    def copy(self):
        try:
            return Float64Matrix(self.matrix.copy())
        except Exception as e:
            wrn.copywarning(self.pos_start, self.pos_end, e)
            return Null()

    def is_true(self):
        return True
    
    def free_mem(self):
        self.matrix.free()

Type.Int32Matrix = Type('Int32Matrix')
class Int32Matrix(BaseValue):
    def __init__(self, matrix: linalg.i32_matrix):
        super().__init__()
        self.type = 'Int32Matrix'
        self.matrix = matrix
    
    def __repr__(self):
        return repr(self.matrix)
    
    def __str__(self):
        return str(self.matrix)

    def add_by(self, other):
        if isinstance(other, Int32Matrix):
            try:
                return Int32Matrix(self.matrix + other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Int32Matrix):
            try:
                return Int32Matrix(self.matrix - other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Int32Matrix):
            try:
                return Int32Matrix(self.matrix * other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Int32Matrix):
            try:
                return Int32Matrix(self.matrix / other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except ZeroDivisionError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def matmult_by(self, other):
        if isinstance(other, Int32Matrix):
            try:
                return Int32Matrix(self.matrix @ other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def neg(self):
        try:
            return Int32Matrix(-self.matrix), None
        except MemoryError as e:
            return None, err.MallocError(self.pos_start, self.pos_end, e, self.context)
        except OverflowError as e:
            return None, err.IntegerOverflowError(self.pos_start, self.pos_end, e, self.context)
        except Exception as e:
            return None, err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
    
    def copy(self):
        try:
            return Int32Matrix(self.matrix.copy())
        except Exception as e:
            wrn.copywarning(self.pos_start, self.pos_end, e)
            return Null()

    def is_true(self):
        return True
    
    def free_mem(self):
        self.matrix.free()

Type.Int64Matrix = Type('Int64Matrix')
class Int64Matrix(BaseValue):
    def __init__(self, matrix: linalg.i64_matrix):
        super().__init__()
        self.type = 'Int64Matrix'
        self.matrix = matrix
    
    def __repr__(self):
        return repr(self.matrix)
    
    def __str__(self):
        return str(self.matrix)

    def add_by(self, other):
        if isinstance(other, Int64Matrix):
            try:
                return Int64Matrix(self.matrix + other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def sub_by(self, other):
        if isinstance(other, Int64Matrix):
            try:
                return Int64Matrix(self.matrix - other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Int64Matrix):
            try:
                return Int64Matrix(self.matrix * other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def div_by(self, other):
        if isinstance(other, Int64Matrix):
            try:
                return Int64Matrix(self.matrix / other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except ZeroDivisionError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def matmult_by(self, other):
        if isinstance(other, Int64Matrix):
            try:
                return Int64Matrix(self.matrix @ other.matrix), None
            except MemoryError as e:
                return None, err.MallocError(self.pos_start, other.pos_end, e, self.context)
            except ValueError as e:
                return None, err.RTError(self.pos_start, other.pos_end, e, self.context)
            except OverflowError as e:
                return None, err.IntegerOverflowError(self.pos_start, other.pos_end, e, self.context)
            except Exception as e:
                return None, err.UnknownRTError(self.pos_start, other.pos_end, e, self.context)
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def neg(self):
        try:
            return Int64Matrix(-self.matrix), None
        except MemoryError as e:
            return None, err.MallocError(self.pos_start, self.pos_end, e, self.context)
        except OverflowError as e:
            return None, err.IntegerOverflowError(self.pos_start, self.pos_end, e, self.context)
        except Exception as e:
            return None, err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
    
    def copy(self):
        try:
            return Int64Matrix(self.matrix.copy())
        except Exception as e:
            wrn.copywarning(self.pos_start, self.pos_end, e)
            return Null()

    def is_true(self):
        return True
    
    def free_mem(self):
        self.matrix.free()

## Array types
Type.String = Type('String')
class String(BaseValue):
    def __init__(self, value):
        super().__init__()
        self.type = 'String'
        self.value = value

    def add_by(self, other):
        if isinstance(other, String):
            return String(self.value + other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Integer):
            return String(self.value * other.value).set_context(self.context), None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def is_true(self):
        return len(self.value) > 0
    
    def copy(self):
        copy = String(self.value)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
        
    def __str__(self):
        return self.value

    def __repr__(self):
        return f'"{self.value}"'
    
    def __len__(self):
        return len(self.value)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            try:
                start, stop, step = index.start, index.stop, index.step
                return String(self.value[start:stop:step])
            except IndexError:
                return None
        try:
            return self.value[index]
        except IndexError:
            return None

Type.IterArray = Type('IterArray')
class IterArray(BaseValue):
    def __init__(self, elements):
        super().__init__()
        self.type = 'IterArray'
        self.elements: list = elements
        self.index_type = INDEX_TYPE_INT
    
    def add_by(self, other):
        if isinstance(other, IterArray):
            new_list = self.copy()
            new_list.elements.extend(other.elements)
            return new_list, None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def mult_by(self, other):
        if isinstance(other, Integer):
            new_list = self.copy()
            new_list.elements *= other.value
            return new_list, None
        else:
            return None, BaseValue.illegal_operation(self, other)
        
    def is_true(self):
        return len(self.elements) > 0
    
    def copy(self):
        copy = IterArray(self.elements)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f'[{", ".join([str(x) for x in self.elements])}]'

    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        return len(self.elements)
    
    def __getitem__(self, index):
        if isinstance(index, slice):
            try:
                start, stop, step = index.start, index.stop, index.step
                return IterArray(self.elements[start:stop:step])
            except IndexError:
                return None
        try:
            return self.elements[index]
        except IndexError:
            return None

    def __setitem__(self, index, value):
        try:
            self.elements[index] = value
            return True
        except IndexError:
            return False

## Structure types
class Structure(BaseValue):
    def __init__(self, name, elements: dict, _isinstance: bool = False):
        super().__init__()
        self.name: str      = name
        self.type           = f"{name}_Struct"
        self.elements: dict = elements
        self.isinstance     = _isinstance
        
    def is_true(self):
        return len(self.elements) > 0
    
    def copy(self):
        # copy = Structure(self.name, self.elements.copy(), self.isinstance)
        copy = Structure(self.name, deepcopy(self.elements), self.isinstance)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def make_instance(self, pos_start: Position, pos_end: Position):
        ins = Structure(self.name, deepcopy(self.elements), True)
        ins.set_pos(pos_start, pos_end)
        ins.set_context(self.context)
        return ins
    
    def free_mem(self):
        if not self.isinstance:
            self.context.symbol_table.rm_type(self.type)
    
    def __str__(self):
        name = f'{self.name} [{", ".join(["%s (%s): %s"%(field, "|".join([str(type_) for type_ in value[0]]), value[1]) for field, value in self.elements.items()])}]'
        if self.isinstance: return f'<Structure instance of ' + name + '>'
        return '<Structure definition ' + name + '>'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.elements)

Type.Namespace = Type('Namespace')
class Namespace(BaseValue):
    def __init__(self, name, elements: dict): #TODO: use typing to make this betterrrrrrrrrrrr
        super().__init__()
        self.type           = 'Namespace'
        self.name: str      = name
        self.elements: dict = elements
        
    def is_true(self):
        return len(self.elements) > 0
    
    def copy(self):
        copy = Namespace(self.name, self.elements.copy())
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def __str__(self):
        return f'<Namespace {self.name}>'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.elements)

'''
class Class(BaseValue): #TODO
    def __init__(self, name, parent, parent_context, _isinstance: bool = False):
        super().__init__()
        self.type = 'Class'
        self.name: str = name
        self.parent: Class|None = parent

        #TODO: check if _isinstance in interpreter out of __init__
        self.parent_symbols: dict = {} if type(self.parent) is None else self.parent.context.symbol_table.symbols

        self.context: Context = Context(self.name, parent_context, self.pos_start, parent_context.strict_mode)
        self._isinstance = _isinstance
        self.context.symbol_table.is_cls_ins = self._isinstance
        
    def is_true(self):
        return len(self.context.symbol_table.symbols) > 0
    
    def copy(self):
        copy = Class(self.name, self.parent, self.context.copy(), self._isinstance)
        copy.set_pos(self.pos_start, self.pos_end)
        copy.set_context(self.context)
        return copy
    
    def make_instance(self, pos_start: Position, pos_end: Position, arg_nodes):
        ins = Class(self.name, self.parent, self.context.copy(), True)
        ins.set_pos(pos_start, pos_end)
        ins.set_context(self.context)
        res = RTResult()

        args = []
        for arg_node in arg_nodes:
            args.append(res.register(self.visit(arg_node, self.context)))
            if res.should_return(): return res

        return_value = res.register(value_to_call.execute(node, args))
        if res.should_return(): return res
        return_value = return_value.copy().set_pos(node.pos_start, node.pos_end).set_context(context)
        return res.success(return_value)

        return ins
    
    def __str__(self):
        if self._isinstance: return '<class instance of ' + self.name + '>'
        return '<class definition ' + self.name + '>'

    def __repr__(self):
        return self.__str__()

    def __len__(self):
        return len(self.context.symbol_table.symbols)
Type.Class = Type('Class')

class BaseMethod(BaseValue):
    def __init__(self, name):
        super().__init__()
        self.type = 'BaseMethod'
        self.name = name
        self.exec_ctx: Context|None = None

    def generate_new_context(self):
        self.exec_ctx = Context(self.name, self.context, self.pos_start, self.context.strict_mode)
        self.exec_ctx.symbol_table: SymbolTable = SymbolTable(self.exec_ctx.parent.symbol_table)
    
    def check_args(self, arg_names, args): #TODO (self.methodX())
        res = RTResult()
        if len(args) > len(arg_names) or len(args) < len(arg_names):
            return res.failure(err.RTError(
            self.pos_start, self.pos_end,
				f"'{self.name}' takes {len(arg_names)} arguments but {len(args)} {'was' if len(args) == 1 else 'were'} given",
				self.context
			))
        
        return res.success(Null.null)
    
    def populate_args(self, node, arg_names, args):
        for an, a in zip(arg_names, args):
            arg_name = an
            arg_value = a.set_context(self.exec_ctx)
            self.exec_ctx.symbol_table.set_var(node, self.exec_ctx, arg_name, arg_value, True, True)

    def check_and_populate_args(self, node, arg_names, args):
        res = RTResult()
        res.register(self.check_args(arg_names, args))
        if res.should_return(): return res
        self.populate_args(node, arg_names, args)
        return res.success(Null.null)

class Method(BaseMethod):
    def __init__(self, name, body_node, arg_names, should_auto_return):
        super().__init__(name)
        self.type = 'Method'
        self.body_node = body_node
        self.arg_names = arg_names
        self.should_auto_return = should_auto_return
    
    def execute(self, node, args):
        res = RTResult()
        interpreter = Interpreter()
        self.generate_new_context()

        res.register(self.check_and_populate_args(node, self.arg_names, args))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, self.exec_ctx))
        if res.should_return() and res.func_return_value == None: return res 

        if self.should_auto_return:
            ret_value = value
        elif res.func_return_value != None and res.func_return_value.is_true():
            ret_value = res.func_return_value
        else:
            ret_value = Null.null

        #ret_value = (value if self.should_auto_return else None) or res.func_return_value or Null.null
        return res.success(ret_value)
    
    def copy(self):
        copy = Method(self.name, self.body_node, self.arg_names, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<method {self.name}>"
Type.Method = Type('Method')
'''

## Function types
Type.Function = Type('Function')
class BaseFunction(BaseValue):
    def __init__(self, name):
        super().__init__()
        self.type = 'BaseFunction'
        self.name = name or '<anonymous>'
        self.exec_ctx: Context|None = None

    def generate_new_context(self):
        self.exec_ctx = Context(self.name, self.context, self.pos_start, self.context.strict_mode)
        self.exec_ctx.symbol_table: SymbolTable = SymbolTable(self.exec_ctx.parent.symbol_table)
    
    def check_args(self, arg_prototypes, args):
        res = RTResult()
        if len(args) > len(arg_prototypes) or len(args) < len(arg_prototypes):
            return res.failure(err.RTError(
            self.pos_start, self.pos_end,
				f"'{self.name}' takes {len(arg_prototypes)} arguments but {len(args)} {'was' if len(args) == 1 else 'were'} given",
				self.context
			))
        
        for arg, arg_prototype in zip(args, arg_prototypes):
            arg_name    = arg_prototype[0]
            arg_types   = arg_prototype[1]
            
            typenamified_types = [t.typename for t in arg_types]
            if Type.Any.typename not in typenamified_types and arg.type not in typenamified_types:
                return res.failure(err.RTError(
                    self.pos_start, self.pos_end,
                    f"Argument type ({Type(arg.type)}) is not accepted by the type of argument '{arg_name}' of function '{self.name}' ({"|".join(typenamified_types)})",
                    self.exec_ctx
                ))
        
        return res.success(Null.null)
    
    def populate_args(self, node, arg_prototypes, args):
        for ap, a in zip(arg_prototypes, args):
            arg_name    = ap[0]
            arg_types   = ap[1]
            arg_value = a.set_context(self.exec_ctx)
            self.exec_ctx.symbol_table.set_var(node, self.exec_ctx, arg_name, arg_types, arg_value, True, True)

    def check_and_populate_args(self, node, arg_prototypes, args):
        res = RTResult()
        res.register(self.check_args(arg_prototypes, args))
        if res.should_return(): return res
        self.populate_args(node, arg_prototypes, args)
        return res.success(Null.null)

class Function(BaseFunction):
    def __init__(self, name, body_node, arg_prototypes, res_types, should_auto_return):
        super().__init__(name)
        self.type = 'Function'
        self.body_node = body_node
        self.arg_prototypes = arg_prototypes
        self.res_types = res_types
        self.should_auto_return = should_auto_return
    
    def execute(self, node, args):
        res = RTResult()
        interpreter = Interpreter()
        self.generate_new_context()

        res.register(self.check_and_populate_args(node, self.arg_prototypes, args))
        if res.should_return(): return res

        value = res.register(interpreter.visit(self.body_node, self.exec_ctx))
        if res.should_return() and res.func_return_value == None: return res 

        if self.should_auto_return:
            ret_value = value
        elif res.func_return_value is not None and res.func_return_value.is_true():
            ret_value = res.func_return_value
        else:
            ret_value = Null.null

        typenamified_types = [t.typename for t in self.res_types]
        if Type.Any.typename not in typenamified_types and ret_value.type not in typenamified_types:
            return res.failure(err.RTError(
                node.pos_start, node.pos_end,
                #f"Type of '{value}' ({Type(value.type)}) is not accepted by the return type of the function '{self.name}' ({"|".join(typenamified_types)})",
                f"Type of return value is not accepted by the return type of the function '{self.name}' ({"|".join(typenamified_types)})",
                self.exec_ctx
            ))

        #ret_value = (value if self.should_auto_return else None) or res.func_return_value or Null.null
        return res.success(ret_value)
    
    def copy(self):
        copy = Function(self.name, self.body_node, self.arg_prototypes, self.res_types, self.should_auto_return)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<function {self.name}>"

Type.BuiltInFunction = Type('BuiltInFunction')
class BuiltInFunction(BaseFunction):
    def __init__(self, name):
        super().__init__(name)
        self.type = 'BuiltInFunction'

    def execute(self, node, args):
        res = RTResult()
        self.generate_new_context()

        method_name = f'execute_{self.name}'
        method = getattr(self, method_name, self.no_visit_method) 

        #res.register(self.check_and_populate_args(node, [[arg_name, [Type.Any]] for arg_name in method.arg_names], args))
        res.register(self.check_and_populate_args(node, method.arg_prototypes, args))
        if res.should_return(): return res

        self.node = node
        return_value = res.register(method(self.exec_ctx))
        if res.should_return(): return res

        return res.success(return_value)

    def no_visit_method(self):
        raise Exception(f'No execute_{self.name} method defined')
    
    def copy(self):
        copy = BuiltInFunction(self.name)
        copy.set_context(self.context)
        copy.set_pos(self.pos_start, self.pos_end)
        return copy

    def __repr__(self):
        return f"<built-in function {self.name}>"
    
    def __str__(self):
        return self.__repr__()
    
    #EXECS
    
    def execute_print(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get_var('value')))
        return RTResult().success(Null.null)
    execute_print.arg_prototypes = [['value', [Type.Any]]]

    def execute_stringify(self, exec_ctx):
        return RTResult().success(String(str(exec_ctx.symbol_table.get_var('value'))))
    execute_stringify.arg_prototypes = [['value', [Type.Any]]]

    def execute_print_without_end(self, exec_ctx):
        print(str(exec_ctx.symbol_table.get_var('value')), end='')
        return RTResult().success(Null.null)
    execute_print_without_end.arg_prototypes = [['value', [Type.Any]]]

    def execute_get_float_sci_str(self, exec_ctx):
        return RTResult().success(String(exec_ctx.symbol_table.get_var('value').value.sci_str()))
    execute_get_float_sci_str.arg_prototypes = [['value', [Type.Float16, Type.Float32, Type.Float64]]]

    def execute_input(self, exec_ctx):
        text = input(str(exec_ctx.symbol_table.get_var('message').value))
        return RTResult().success(String(text))
    execute_input.arg_prototypes = [['message', [Type.Any]]]

    def execute_input_int(self, exec_ctx):
        while True:
            try:
                text = input(str(exec_ctx.symbol_table.get_var('message').value))
                number = int(text)
                break
            except ValueError:
                print(f"'{text}' must be an integer. Please try again!")
        return RTResult().success(Integer(number))
    execute_input_int.arg_prototypes = [['message', [Type.Any]]]

    def execute_clear(self, exec_ctx):
        os.system('cls' if os.name == 'nt' else 'clear')
        return RTResult().success(Null.null)
    execute_clear.arg_prototypes = []

    def execute_terminal_prompt(self, exec_ctx):
        os.system(exec_ctx.symbol_table.get_var('prompt'))
        return RTResult().success(Null.null)
    execute_terminal_prompt.arg_prototypes = [['prompt', [Type.String]]]
    
    def execute_exit(self, exec_ctx):
        exit()
    execute_exit.arg_prototypes = []

    def execute_quit(self, exec_ctx):
        quit()
    execute_quit.arg_prototypes = []

    def execute_push(self, exec_ctx):
        iterarray = exec_ctx.symbol_table.get_var('iterarray')
        value = exec_ctx.symbol_table.get_var('value')
        
        iterarray.elements.append(value)
        return RTResult().success(Null.null)
    execute_push.arg_prototypes = [['iterarray', [Type.IterArray]], ['value', [Type.Any]]]

    def execute_pop(self, exec_ctx):
        iterarray = exec_ctx.symbol_table.get_var('iterarray')
        index = exec_ctx.symbol_table.get_var('index')
        
        try:
            elements = iterarray.elements.pop(index.value)
        except:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Index out of range',
                    exec_ctx
                ))

        return RTResult().success(elements)
    execute_pop.arg_prototypes = [['iterarray', [Type.IterArray]], ['index', [Type.Integer]]]

    def execute_len(self, exec_ctx):
        iterable = exec_ctx.symbol_table.get_var('iterable')
        res = RTResult()
        
        _len = iterable.__len__()
        
        if isinstance(_len, RTResult): #WARNING: ELDRICH MONSTER INSIDE THIS COMMENT CAGE@
            res.register(_len)
            return res

        len_type = type(_len)
        if len_type is int or len_type is float:
            return res.success(Integer(_len))
        elif len_type is list:
            return res.success(IterArray(_len))
        elif len_type is tuple:
            return res.success(IterArray([item for item in _len]))
        else: return Null.null

    execute_len.arg_prototypes = [['iterable', [Type.Any]]]

    '''
    def execute_write_to_python(self, exec_ctx):
        import serialisation as ser
        obj = exec_ctx.symbol_table.get_var('value')
        fn = exec_ctx.symbol_table.get_var('fn')
        if not isinstance(fn, String):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'First argument must be a filename',
                    exec_ctx
                ))
        sb = ser.SharedBuffer(fn.value)
        x = sb.write_frm_ail(obj, exec_ctx)

        return x

    execute_write_to_python.arg_names = ['value', 'fn']

    
    def execute_read_frm_python(self, exec_ctx):
        import serialisation as ser
        fn = exec_ctx.symbol_table.get_var('fn')
        if not isinstance(fn, String):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a filename',
                    exec_ctx
                ))
        sb = ser.SharedBuffer(fn.value)
        x = sb.read_frm_ail(self, exec_ctx)

        return x

    execute_read_frm_python.arg_names = ['fn']

    def execute_wait_for_write_frm_python(self, exec_ctx):
        import serialisation as ser
        fn = exec_ctx.symbol_table.get_var('fn')
        if not isinstance(fn, String):
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    'Argument must be a filename',
                    exec_ctx
                ))
        sb = ser.SharedBuffer(fn.value)
        sb.wait_for_write()

        return RTResult().success(Null.null)
    execute_wait_for_write_frm_python.arg_names = []
    '''
    
    def execute_exec_prog(self, exec_ctx):
        fn = exec_ctx.symbol_table.get_var('fn')
        
        fn = fn.value

        try:
            with open(fn, 'r') as f:
                script = f.read()
        except Exception as e:
            return RTResult().failure(err.PLoadError(
                    self.pos_start, self.pos_end,
                    f'Failed to load script "{fn}"\n' + str(e),
                    exec_ctx
                ))
        
        _, error = run(fn, script, progpath=fn, st=exec_ctx.symbol_table)

        if error:
            return RTResult().failure(err.RTError(
                    self.pos_start, self.pos_end,
                    f'Failed to finish executing script "{fn}"\n' +
                    error.as_str(),
                    exec_ctx
                ))
        
        return RTResult().success(Null.null)
    execute_exec_prog.arg_prototypes = [['fn', [Type.String]]]

    def execute_load_module(self, exec_ctx): #TODO: set pos n context of the namespace
        fn = exec_ctx.symbol_table.get_var('mod_name')
        
        fn = fn.value

        out_path_dict = {}

        for path in exec_ctx.symbol_table.get_var('__path__').elements:
            name, ext = os.path.splitext(os.path.basename(path))
            out_path_dict[name] = path
        if fn not in out_path_dict:
            return RTResult().failure(err.MLoadError(
                    self.pos_start, self.pos_end,
                    f'Script "{fn}" not found in __path__',
                    exec_ctx
                ))
        fp = out_path_dict[fn]

        _, ext = os.path.splitext(fp)

        if ext == '.py':
            try:
                spec = importlib.util.spec_from_file_location(fn, fp)
                my_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(my_module)

                module_namespace = Namespace(getattr(my_module, 'module_name'), dict()).set_pos(self.pos_start, self.pos_end).set_context(self.context)
                for name, value in getattr(my_module, 'to_be_pushed'):
                    module_namespace.elements[name] = value.set_pos(self.pos_start, self.pos_end).set_context(self.context)

                for symbol_table in SymbolTable.get_global_instances():
                    symbol_table.set_sys_var(module_namespace.name, module_namespace)
            except Exception as e:
                return RTResult().failure(err.MLoadError(
                        self.pos_start, self.pos_end,
                        f'Failed to finish executing script "{fp}"\n' + 
                        str(e),
                        exec_ctx
                    ))
        elif ext == '.ail': # MAKE IT PUT VARS AND FUNCS IN ALL SYMBOL TABLES
            try:
                with open(fp, 'r') as f:
                    script = f.read()
            except Exception as e:
                return RTResult().failure(err.MLoadError(
                        self.pos_start, self.pos_end,
                        f'Failed to load script "{fp}"\n' + str(e),
                        exec_ctx
                    ))
            _, error = run(fp, script, progpath=fp, st=exec_ctx.symbol_table)

            if error:
                return RTResult().failure(err.MLoadError(
                        self.pos_start, self.pos_end,
                        f'Failed to finish loading module "{fp}"\n' +
                        error.as_str(),
                        exec_ctx
                    ))
        else:
            try:
                init_fp = fp + '/init.py'
                spec = importlib.util.spec_from_file_location(fn, init_fp)
                my_module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(my_module)

                module_namespace = Namespace(getattr(my_module, 'module_name'), dict()).set_pos(self.pos_start, self.pos_end).set_context(self.context)
                for name, value in getattr(my_module, 'to_be_pushed'):
                    module_namespace.elements[name] = value.set_pos(self.pos_start, self.pos_end).set_context(self.context)

                for symbol_table in SymbolTable.get_global_instances():
                    symbol_table.set_sys_var(module_namespace.name, module_namespace)
            except Exception as e:
                return RTResult().failure(err.MLoadError(
                        self.pos_start, self.pos_end,
                        f'Failed to finish loading package "{fp}"\n' + 
                        str(e),
                        exec_ctx
                    ))
        
        return RTResult().success(Null.null)
    execute_load_module.arg_prototypes = [['mod_name', [Type.String]]]

    def execute_range(self, exec_ctx):
        start = exec_ctx.symbol_table.get_var('start')
        end = exec_ctx.symbol_table.get_var('end')
        
        if end.value <= start.value:
            return RTResult().failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument must be greater than first argument',
                        exec_ctx
                    ))

        range_result = IterArray([Integer(n) for n in range(start.value, end.value)])

        return RTResult().success(range_result)
    execute_range.arg_prototypes = [['start', [Type.Integer]], ['end', [Type.Integer]]]

    def execute_map(self, exec_ctx):
        global r
        global ctx
        ctx = exec_ctx
        r = RTResult()
        func = ctx.symbol_table.get_var('func')
        iterarray = ctx.symbol_table.get_var('iterarray')

        if not isinstance(func, BaseFunction):
            return r.failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'First argument must be a function',
                        ctx
                    ))
        
        if not isinstance(iterarray, IterArray):
            return r.failure(err.RTError(
                        self.pos_start, self.pos_end,
                        'Second argument must be an iterarray',
                        ctx
                    ))
        def x(i):
            global r
            global ctx
            return_value = r.register(func.execute(self.node, [i])).set_pos(self.pos_start, self.pos_end).set_context(ctx)
            if r.should_return(): return r
            return return_value
        mapped = list(map(x, iterarray.elements))

        if r.should_return(): return r
        return r.success(IterArray(mapped))
    
    execute_map.arg_prototypes = [['func', [Type.Function, Type.BuiltInFunction]], ['iterarray', [Type.IterArray]]]

    def execute_numerical_cast(self, exec_ctx):
        res = RTResult()
        x = exec_ctx.symbol_table.get_var('x')
        tgt_type = exec_ctx.symbol_table.get_var('tgt_type')

        tgt_valuetype = BuiltInFunction.numcast_conv_tgt_types_to_tgt_valuetypes.get(tgt_type.typename, None)
        if not tgt_valuetype:
            return res.failure(
                err.RTError(
                    self.pos_start, self.pos_end,
                    "Invalid target datatype for numerical cast",
                    self.context
                )
            )

        num_res = numbers.numerical_cast(x.value, tgt_valuetype)
        return res.success(
            BuiltInFunction.numcast_conv_num_type_to_num_wrapper[type(num_res)](num_res)
        )
    numcast_conv_tgt_types_to_tgt_valuetypes = {
        'Integer':      int,
        'Float16':      numbers.f16,
        'Float32':      numbers.f32,
        'Float64':      numbers.f64,
        'Int32':        numbers.i32,
        'Int64':        numbers.i64,
    }
    numcast_conv_num_type_to_num_wrapper = {
        int:            Integer,
        numbers.f16:    Float16,
        numbers.f32:    Float32,
        numbers.f64:    Float64,
        numbers.i32:    Int32,
        numbers.i64:    Int64,
    }
    execute_numerical_cast.arg_prototypes = [['x', [Type.Integer, Type.Int32, Type.Int64, Type.Float16, Type.Float32, Type.Float64]], ['tgt_type', [Type.Type]]]

    def execute_matrix_cast(self, exec_ctx):
        res = RTResult()
        m = exec_ctx.symbol_table.get_var('m')
        tgt_type = exec_ctx.symbol_table.get_var('tgt_type')

        tgt_valuetype = BuiltInFunction.matrixcast_conv_tgt_types_to_tgt_valuetypes.get(tgt_type.typename, None)
        if not tgt_valuetype:
            return res.failure(
                err.RTError(
                    self.pos_start, self.pos_end,
                    "Invalid target datatype for numerical cast",
                    self.context
                )
            )
        
        try:
            matrix_res = linalg.matrix_cast(m.matrix, tgt_valuetype)
        except MemoryError as e:
            return res.failure(err.MallocError(self.pos_start, self.pos_end, e, self.context))
        except Exception as e:
            return res.failure(err.UnknownRTError(self.pos_start, self.pos_end, e, self.context))

        return res.success(
            BuiltInFunction.matrixcast_conv_matrix_type_to_matrix_wrapper[type(matrix_res)](matrix_res)
        )
    matrixcast_conv_tgt_types_to_tgt_valuetypes = {
        'Float16Matrix':    linalg.f16_matrix,
        'Float32Matrix':    linalg.f32_matrix,
        'Float64Matrix':    linalg.f64_matrix,
        'Int32Matrix':      linalg.i32_matrix,
        'Int64Matrix':      linalg.i64_matrix,
    }
    matrixcast_conv_matrix_type_to_matrix_wrapper = {
        linalg.f16_matrix:  Float16Matrix,
        linalg.f32_matrix:  Float32Matrix,
        linalg.f64_matrix:  Float64Matrix,
        linalg.i32_matrix:  Int32Matrix,
        linalg.i64_matrix:  Int64Matrix,
    }
    execute_matrix_cast.arg_prototypes = [['m', [Type.Float16Matrix, Type.Float32Matrix, Type.Float64Matrix, Type.Int32Matrix, Type.Int64Matrix]], ['tgt_type', [Type.Type]]]

    def execute_matrix_fill(self, exec_ctx):
        res = RTResult()
        x = exec_ctx.symbol_table.get_var('x')
        y = exec_ctx.symbol_table.get_var('y')
        fill_value = exec_ctx.symbol_table.get_var('fill_value')

        try:
            match fill_value.type:
                case 'Float16':
                    return res.success(Float16Matrix(
                        linalg.f16m_fill(ctypes.c_size_t(x.value), ctypes.c_size_t(y.value), fill_value.value)
                    ))
                case 'Float32':
                    return res.success(Float32Matrix(
                        linalg.f32m_fill(ctypes.c_size_t(x.value), ctypes.c_size_t(y.value), fill_value.value)
                    ))
                case 'Float64':
                    return res.success(Float64Matrix(
                        linalg.f64m_fill(ctypes.c_size_t(x.value), ctypes.c_size_t(y.value), fill_value.value)
                    ))
                case 'Int32':
                    return res.success(Int32Matrix(
                        linalg.i32m_fill(ctypes.c_size_t(x.value), ctypes.c_size_t(y.value), fill_value.value)
                    ))
                case 'Int64':
                    return res.success(Int64Matrix(
                        linalg.i64m_fill(ctypes.c_size_t(x.value), ctypes.c_size_t(y.value), fill_value.value)
                    ))
                case _:
                    return res.failure(
                        err.UnknownRTError(self.pos_start, self.pos_end, "Unknown error", self.context)
                    )
        except MemoryError as e:
            return res.failure(
                err.MallocError(self.pos_start, self.pos_end, e, self.context)
            )
        except ValueError as e:
            return res.failure(
                err.RTError(self.pos_start, self.pos_end, e, self.context)
            )
        except Exception as e:
            return res.failure(
                err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
            )
    execute_matrix_fill.arg_prototypes = [['x', [Type.Integer]], ['y', [Type.Integer]], ['fill_value', [Type.Float16, Type.Float32, Type.Float64, Type.Int32, Type.Int64]]]

    def execute_row_vector_to_matrix(self, exec_ctx):
        res = RTResult()
        v = exec_ctx.symbol_table.get_var('v')
        no_rows = exec_ctx.symbol_table.get_var('no_rows')

        try:
            match v.type:
                case 'Float16Matrix':
                    return res.success(Float16Matrix(
                        linalg.f16m_row_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Float32Matrix':
                    return res.success(Float32Matrix(
                        linalg.f32m_row_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Float64Matrix':
                    return res.success(Float64Matrix(
                        linalg.f64m_row_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Int32Matrix':
                    return res.success(Int32Matrix(
                        linalg.i32m_row_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Int64Matrix':
                    return res.success(Int64Matrix(
                        linalg.i64m_row_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case _:
                    return res.failure(
                        err.UnknownRTError(self.pos_start, self.pos_end, "Unknown error", self.context)
                    )
        except MemoryError as e:
            return res.failure(
                err.MallocError(self.pos_start, self.pos_end, e, self.context)
            )
        except ValueError as e:
            return res.failure(
                err.RTError(self.pos_start, self.pos_end, e, self.context)
            )
        except Exception as e:
            return res.failure(
                err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
            )
    execute_row_vector_to_matrix.arg_prototypes = [['v', [Type.Float16Matrix, Type.Float32Matrix, Type.Float64Matrix, Type.Int32Matrix, Type.Int64Matrix]], ['no_rows', [Type.Integer]]]

    def execute_column_vector_to_matrix(self, exec_ctx):
        res = RTResult()
        v = exec_ctx.symbol_table.get_var('v')
        no_rows = exec_ctx.symbol_table.get_var('no_rows')

        try:
            match v.type:
                case 'Float16Matrix':
                    return res.success(Float16Matrix(
                        linalg.f16m_column_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Float32Matrix':
                    return res.success(Float32Matrix(
                        linalg.f32m_column_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Float64Matrix':
                    return res.success(Float64Matrix(
                        linalg.f64m_column_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Int32Matrix':
                    return res.success(Int32Matrix(
                        linalg.i32m_column_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case 'Int64Matrix':
                    return res.success(Int64Matrix(
                        linalg.i64m_column_vector_to_matrix(v.matrix, ctypes.c_size_t(no_rows.value))
                    ))
                case _:
                    return res.failure(
                        err.UnknownRTError(self.pos_start, self.pos_end, "Unknown error", self.context)
                    )
        except MemoryError as e:
            return res.failure(
                err.MallocError(self.pos_start, self.pos_end, e, self.context)
            )
        except ValueError as e:
            return res.failure(
                err.RTError(self.pos_start, self.pos_end, e, self.context)
            )
        except Exception as e:
            return res.failure(
                err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
            )
    execute_column_vector_to_matrix.arg_prototypes = [['v', [Type.Float16Matrix, Type.Float32Matrix, Type.Float64Matrix, Type.Int32Matrix, Type.Int64Matrix]], ['no_rows', [Type.Integer]]]

    def execute_transpose_matrix(self, exec_ctx):
        res = RTResult()
        m = exec_ctx.symbol_table.get_var('m')
        
        try:
            matrix_res: linalg.f16_matrix|linalg.f32_matrix|linalg.f64_matrix = m.transpose()
        except MemoryError as e:
            return res.failure(
                err.MallocError(self.pos_start, self.pos_end, e, self.context)
            )
        except Exception as e:
            return res.failure(
                err.UnknownRTError(self.pos_start, self.pos_end, e, self.context)
            )

        match m.type:
            case 'Float16Matrix':
                return res.success(Float16Matrix(matrix_res))
            case 'Float32Matrix':
                return res.success(Float32Matrix(matrix_res))
            case 'Float64Matrix':
                return res.success(Float64Matrix(matrix_res))
            case _:
                return res.failure(
                    err.UnknownRTError(self.pos_start, self.pos_end, "Unknown error", self.context)
                )
    execute_transpose_matrix.arg_prototypes = [['m', [Type.Float16Matrix, Type.Float32Matrix, Type.Float64Matrix]]]
BuiltInFunction.print                           = BuiltInFunction('print')
BuiltInFunction.stringify                       = BuiltInFunction('stringify')
BuiltInFunction.print_without_end               = BuiltInFunction('print_without_end')
BuiltInFunction.get_float_sci_str               = BuiltInFunction('get_float_sci_str')
BuiltInFunction.input                           = BuiltInFunction('input')
BuiltInFunction.input_int                       = BuiltInFunction('input_int')
BuiltInFunction.input_multi_float               = BuiltInFunction('input_multi_float')
BuiltInFunction.clear                           = BuiltInFunction('clear')
BuiltInFunction.terminal_prompt                 = BuiltInFunction('terminal_prompt')
BuiltInFunction.exit                            = BuiltInFunction('exit')
BuiltInFunction.quit                            = BuiltInFunction('quit')
BuiltInFunction.push                            = BuiltInFunction('push')
BuiltInFunction.pop                             = BuiltInFunction('pop')
BuiltInFunction.len                             = BuiltInFunction('len')
BuiltInFunction.exec_prog                       = BuiltInFunction('exec_prog')
BuiltInFunction.load_module                     = BuiltInFunction('load_module')
BuiltInFunction.range                           = BuiltInFunction('range')
BuiltInFunction.map                             = BuiltInFunction('map')
BuiltInFunction.numerical_cast                  = BuiltInFunction('numerical_cast')
BuiltInFunction.matrix_cast                     = BuiltInFunction('matrix_cast')
BuiltInFunction.matrix_fill                     = BuiltInFunction('matrix_fill')
BuiltInFunction.row_vector_to_matrix            = BuiltInFunction('row_vector_to_matrix')
BuiltInFunction.column_vector_to_matrix         = BuiltInFunction('column_vector_to_matrix')
BuiltInFunction.transpose_matrix                = BuiltInFunction('transpose_matrix')

# Context

@dataclass
class Symbol:
    types: list[Type]|tuple[Type]
    is_raable: bool
    is_delable: bool
    value: BaseValue

class SymbolTable: #TODO: Get local var copy thingmabob implemented (global)
    _global_instances = set()

    def __init__(self, parent=None, is_cls_ins=False) -> None:
        self.parent: None|SymbolTable = parent
        self.symbols: dict[str, Symbol] = {} #if parent==None else parent.symbols.copy() #TODO: add scoping (global)
        # self.cls_name: None|str = cls_name
        self.is_cls_ins: bool = is_cls_ins

    def get_var(self, var_name):
        symbol = self.symbols.get(var_name, None)
    
        if symbol:
            return symbol.value
        if self.parent:
            return self.parent.get_var(var_name)
        return None
    
    def get_types(self, var_name):
        symbol = self.symbols.get(var_name, None)
        
        if symbol:
            return symbol.types
        if self.parent:
            return self.parent.get_types(var_name)
        return None

    '''
    def get_var(self, name):
        value = self.symbols.get(name, None)
        if not value and self.parent:
            return self.parent.get_var(name)
        return value[0] if value else None
    '''
    
    def chk_var_in_symbols(self, name):
        # return SymbolName(name) in self.symbols
        return name in self.symbols
    
    def set_var(self, node, ctx, name: str, types: Type, value, is_raable:bool=False, is_delable:bool=False): # no raa = let/const, no del = const
        if self.chk_var_in_symbols(name):
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                'Variable already exists in current scope',
                ctx
            ))
        elif Type.Any.typename not in (m:=[t.typename for t in types]) and value.type not in m:
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                f"Type of '{value}' ({Type(value.type)}) is not accepted by the type of the variable '{name}' ({"|".join(m)})",
                ctx
            ))
        '''
        if not self.cls_name:
            if privated:
                return RTResult().failure(err.RTError(
                    node.pos_start, node.pos_end,
                    'Private variable cannot be assigned out of class',
                ))
            if isinstance(value, BaseMethod):
                return RTResult().failure(err.RTError(
                    node.pos_start, node.pos_end,
                    'Method cannot be assigned out of class',
                    ctx
                ))
        '''

        # self.symbols[SymbolName(name)] = [value, is_raable, is_delable]
        # self.symbols[name] = [types, value, is_raable, is_delable, privated]
        self.symbols[name] = Symbol(types, is_raable, is_delable, value.set_pos(node.pos_start, node.pos_end).set_context(ctx))
        return RTResult().success(value)
    
    def set_sys_var(self, name, value, is_raable:bool=False, is_delable:bool=False): # no raa = let/const, no del = const
        # self.symbols[SymbolName(name)] = [value, is_raable, is_delable]
        # self.symbols[name] = [Type.Structure, value, is_raable, is_delable, False]
        self.symbols[name] = Symbol([Type.Any], is_raable, is_delable, value.set_pos(Position.system_pos, Position.system_pos).set_context(None)) #TODO: find way to carry ctx to system variables

    def set_struct(self, node, ctx, name, struct):
        if self.chk_var_in_symbols(name):
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                'Variable already exists',
                ctx
            ))
        # self.symbols[SymbolName(name)] = [struct, False, True]
        # self.symbols[name] = [Type.Struct, struct, False, True, False]
        self.symbols[name] = Symbol([Type(struct.type)], False, True, struct.set_pos(node.pos_start, node.pos_end).set_context(ctx))
        return RTResult().success(Null.null)

    def ra_var(self, node, ctx, name, value):
        if not self.chk_var_in_symbols(name):
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                'Variable does not exist in current scope',
                ctx
            ))
        elif not self.symbols[name].is_raable:
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                'Variable is either a constant or a \'let\' variable',
                ctx
            ))
        elif Type.Any.typename not in (m:=[t.typename for t in self.get_types(name)]) and value.type not in m:
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                f"Type of '{value}' ({Type(value.type)}) is not accepted by the type of the variable '{name}' ({"|".join(m)})",
                ctx
            ))
        
        
        # self.symbols[SymbolName(name)][0] = value
        # self.symbols[name][0] = value
        self.symbols[name].value = value
        return RTResult().success(value)

    def protect_var(self, name, node, ctx):
        # if not self.symbols[SymbolName(name)][2]:
        if not self.symbols[name].is_delable:
            return RTResult().failure(err.RTError(
                node.pos_start, node.pos_end,
                'Variable is either a constant or an already protected variable',
                ctx
            ))
        # self.symbols[SymbolName(name)][2] = False
        self.symbols[name].is_delable = False
        return RTResult().success(Null.null)

    def rm_var(self, name, node, ctx):
        # if self.symbols[SymbolName(name)][2]:
        if self.symbols[name].is_delable:
            if getattr(self.symbols[name].value, 'free_mem', None):
                self.symbols[name].value.free_mem()
            del self.symbols[name]
            return RTResult().success(Null.null)
        return RTResult().failure(err.RTError(
            node.pos_start, node.pos_end,
            'Variable is either a constant or a protected variable',
            ctx
        ))
    
    def rm_type(self, name):
        del self.symbols[name]
        return RTResult().success(Null.null)
    
    def promote(self):
        SymbolTable._global_instances.add(weakref.ref(self))

    @classmethod
    def get_global_instances(cls):
        return [instance() for instance in cls._global_instances if instance()]
    
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None, strict_mode=True):
        self.display_name = display_name
        self.parent = parent
        self.parent_entry_pos = parent_entry_pos
        self.symbol_table: SymbolTable|None = None
        self.strict_mode: bool = strict_mode

    def copy(self):
        return Context(self.display_name, self.parent, self.parent_entry_pos, self.strict_mode)
    
# Context-dependent imports
from main import run

from extra_modules.Interpreter import Interpreter