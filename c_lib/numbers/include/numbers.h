#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>

// Macros
#define OVERFLOW_RES(result, type_of_overflow) {res.res = 0; res.overflow_type = type_of_overflow;}
#define GOOD_INT_RES(result, value) {res.res = value; res.overflow_type = NOOVERFLOW;}

#define NAN_STR_BUF_SIZE 4
#define INF_STR_BUF_SIZE 5
#define HALF_STR_BUF_SIZE 21
#define FLOAT_STR_BUF_SIZE 41
#define DOUBLE_STR_BUF_SIZE 311
#define SCIENTIFIC_STR_BUF_SIZE 14
#define INT_STR_BUF_SIZE 12
#define LONG_STR_BUF_SIZE 21
#define UINT_STR_BUF_SIZE 11
#define ULONG_STR_BUF_SIZE 21

// Typedefs
typedef float   float32_t;
typedef double  float64_t;

// Enums
typedef enum {
    NOOVERFLOW = 0,
    INTOVERFLOW,
    INTUNDERFLOW,
} overflow_type_t;

// Structs
typedef struct {
    float16_t res;
    bool has_error; //Div by zero
} f16_res;

typedef struct {
    float32_t res;
    bool has_error; //Div by zero
} f32_res;

typedef struct {
    float64_t res;
    bool has_error; //Div by zero
} f64_res;

typedef struct {
    int32_t res;
    overflow_type_t overflow_type; 
} i32_res;

typedef struct {
    int64_t res;
    overflow_type_t overflow_type; 
} i64_res;

typedef struct {
    uint32_t res;
    overflow_type_t overflow_type; 
} u32_res;

typedef struct {
    uint64_t res;
    overflow_type_t overflow_type; 
} u64_res;

// Numerical cast structures
typedef enum {
    F16 = 0,
    F32,
    F64,
    I32,
    I64,
    U32,
    U64,
    INVALID,
} num_type_t;

typedef union {
    float16_t f16;
    float32_t f32;
    float64_t f64;
    int32_t i32;
    int64_t i64;
    uint32_t u32;
    uint64_t u64;
} num_container_t;

typedef struct {
    num_container_t num;
    num_type_t type;
} num_t;

// f16
float16_t   str2f16(char str[]);
void        conv_f16_to_str(float16_t h, char* buffer);
void        conv_f16_to_sci_str(float16_t h, char* buffer);
f16_res     f16_divide(float16_t a, float16_t b);
float16_t   f16_pow(float16_t a, float16_t b);

// f32
float32_t   str2f32(char str[]);
void        conv_f32_to_str(float32_t f, char* buffer);
void        conv_f32_to_sci_str(float32_t f, char* buffer);
float32_t   f32_add(float32_t a, float32_t b);
float32_t   f32_sub(float32_t a, float32_t b);
float32_t   f32_mul(float32_t a, float32_t b);
f32_res     f32_divide(float32_t a, float32_t b);
float32_t   f32_pow(float32_t a, float32_t b);
float32_t   f32_neg(float32_t a);
bool        f32_gte(float32_t a, float32_t b);
bool        f32_gt(float32_t a, float32_t b);
bool        f32_eq(float32_t a, float32_t b);
bool        f32_lte(float32_t a, float32_t b);
bool        f32_lt(float32_t a, float32_t b);
bool        f32_neq(float32_t a, float32_t b);

// f64
float64_t   str2f64(char str[]);
void        conv_f64_to_str(float64_t d, char* buffer);
void        conv_f64_to_sci_str(float64_t d, char* buffer);
float64_t   f64_add(float64_t a, float64_t b);
float64_t   f64_sub(float64_t a, float64_t b);
float64_t   f64_mul(float64_t a, float64_t b);
f64_res     f64_divide(float64_t a, float64_t b);
float64_t   f64_pow(float64_t a, float64_t b);
float64_t   f64_neg(float64_t a);
bool        f64_gte(float64_t a, float64_t b);
bool        f64_gt(float64_t a, float64_t b);
bool        f64_eq(float64_t a, float64_t b);
bool        f64_lte(float64_t a, float64_t b);
bool        f64_lt(float64_t a, float64_t b);
bool        f64_neq(float64_t a, float64_t b);

// i32
int32_t     str2i32(char str[]);
void        conv_i32_to_str(int32_t n, char* buffer);
i32_res     i32_add(int32_t a, int32_t b);
i32_res     i32_sub(int32_t a, int32_t b);
i32_res     i32_mul(int32_t a, int32_t b);
f64_res     i32_divide(int32_t a, int32_t b);
float64_t   i32_pow(int32_t a, int32_t b);
i32_res     i32_neg(int32_t a);
bool        i32_gte(int32_t a, int32_t b);
bool        i32_gt(int32_t a, int32_t b);
bool        i32_eq(int32_t a, int32_t b);
bool        i32_lte(int32_t a, int32_t b);
bool        i32_lt(int32_t a, int32_t b);
bool        i32_neq(int32_t a, int32_t b);
int32_t     i32_bitwise_lshift(int32_t a, int32_t b);
int32_t     i32_bitwise_rshift(int32_t a, int32_t b);
int32_t     i32_bitwise_xor(int32_t a, int32_t b);
int32_t     i32_bitwise_or(int32_t a, int32_t b);
int32_t     i32_bitwise_and(int32_t a, int32_t b);
int32_t     i32_bitwise_not(int32_t a);

// i64
int64_t     str2i64(char str[]);
void        conv_i64_to_str(int64_t n, char* buffer);
i64_res     i64_add(int64_t a, int64_t b);
i64_res     i64_sub(int64_t a, int64_t b);
i64_res     i64_mul(int64_t a, int64_t b);
f64_res     i64_divide(int64_t a, int64_t b);
float64_t   i64_pow(int64_t a, int64_t b);
i64_res     i64_neg(int64_t a);
bool        i64_gte(int64_t a, int64_t b);
bool        i64_gt(int64_t a, int64_t b);
bool        i64_eq(int64_t a, int64_t b);
bool        i64_lte(int64_t a, int64_t b);
bool        i64_lt(int64_t a, int64_t b);
bool        i64_neq(int64_t a, int64_t b);
int64_t     i64_bitwise_lshift(int64_t a, int64_t b);
int64_t     i64_bitwise_rshift(int64_t a, int64_t b);
int64_t     i64_bitwise_xor(int64_t a, int64_t b);
int64_t     i64_bitwise_or(int64_t a, int64_t b);
int64_t     i64_bitwise_and(int64_t a, int64_t b);
int64_t     i64_bitwise_not(int64_t a);

// u32
uint32_t    str2u32(char str[]);
void        conv_u32_to_str(uint32_t n, char* buffer);
u32_res     u32_add(uint32_t a, uint32_t b);
u32_res     u32_sub(uint32_t a, uint32_t b);
u32_res     u32_mul(uint32_t a, uint32_t b);
f64_res     u32_divide(uint32_t a, uint32_t b);
float64_t   u32_pow(uint32_t a, uint32_t b);
bool        u32_gte(uint32_t a, uint32_t b);
bool        u32_gt(uint32_t a, uint32_t b);
bool        u32_eq(uint32_t a, uint32_t b);
bool        u32_lte(uint32_t a, uint32_t b);
bool        u32_lt(uint32_t a, uint32_t b);
bool        u32_neq(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_lshift(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_rshift(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_xor(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_or(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_and(uint32_t a, uint32_t b);
uint32_t    u32_bitwise_not(uint32_t a);

// u64
uint64_t    str2u64(char str[]);
void        conv_u64_to_str(uint64_t n, char* buffer);
u64_res     u64_add(uint64_t a, uint64_t b);
u64_res     u64_sub(uint64_t a, uint64_t b);
u64_res     u64_mul(uint64_t a, uint64_t b);
f64_res     u64_divide(uint64_t a, uint64_t b);
float64_t   u64_pow(uint64_t a, uint64_t b);
bool        u64_gte(uint64_t a, uint64_t b);
bool        u64_gt(uint64_t a, uint64_t b);
bool        u64_eq(uint64_t a, uint64_t b);
bool        u64_lte(uint64_t a, uint64_t b);
bool        u64_lt(uint64_t a, uint64_t b);
bool        u64_neq(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_lshift(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_rshift(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_xor(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_or(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_and(uint64_t a, uint64_t b);
uint64_t    u64_bitwise_not(uint64_t a);

// Numerical casting
num_t       numerical_cast(num_t x, num_type_t tgt_type);