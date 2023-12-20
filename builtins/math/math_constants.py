# Imports
from extra_modules.context_and_datatypes import MultiFloatConst, Float16, Float32, Float64

# Initalise
local_pusher = []

# Define funcs & variables
local_pusher.append(('mf_pi',       MultiFloatConst(1)))
local_pusher.append(('mf_e',        MultiFloatConst(2)))
local_pusher.append(('mf_ln2',      MultiFloatConst(3)))
local_pusher.append(('mf_ln10',     MultiFloatConst(4)))

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