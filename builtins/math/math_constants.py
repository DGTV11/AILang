# Imports
from extra_modules.execution_components.context_and_datatypes import Float16, Float32, Float64, Int32, Int64, UInt32, UInt64

# Initalise
local_pusher = []

# Define funcs & variables
local_pusher.append(('f16_pi',      Float16('3.14159')))
local_pusher.append(('f16_e',       Float16('2.71828')))
local_pusher.append(('f16_ln2',     Float16('0.69315')))
local_pusher.append(('f16_ln10',    Float16('2.30259')))

local_pusher.append(('f32_pi',      Float32('3.141592654')))
local_pusher.append(('f32_e',       Float32('2.718281828')))
local_pusher.append(('f32_ln2',     Float32('0.693147181')))
local_pusher.append(('f32_ln10',    Float32('2.302585093')))

local_pusher.append(('f64_pi',      Float64('3.14159265358979324')))
local_pusher.append(('f64_e',       Float64('2.71828182845904524')))
local_pusher.append(('f64_ln2',     Float64('0.69314718055994531')))
local_pusher.append(('f64_ln10',    Float64('2.30258509299404568')))

local_pusher.append(('i32_min',     Int32('-2147483648')))
local_pusher.append(('i32_max',     Int32('2147483647')))

local_pusher.append(('i64_min',     Int64('-9223372036854775808')))
local_pusher.append(('i64_max',     Int64('9223372036854775807')))

local_pusher.append(('u32_max',     UInt32('4294967295')))

local_pusher.append(('u64_max',     UInt64('18446744073709551615')))