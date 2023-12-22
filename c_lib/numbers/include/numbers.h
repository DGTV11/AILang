#include "../../float16/include/float16.h"
#include "../../float16/c_src/conv.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <math.h>
#include <limits.h>

// Typedefs
typedef float   float32_t;
typedef double  float64_t;

//Enums
typedef enum {
    GOOD = 0,
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
i32_res     i32_add(int32_t a, int32_t b);
i32_res     i32_sub(int32_t a, int32_t b);
i32_res     i32_mul(int32_t a, int32_t b);
f64_res     i32_divide(int32_t a, int32_t b);
i32_res     i32_pow(int32_t a, int32_t b);
i32_res     i32_neg(int32_t a);
bool        i32_gte(int32_t a, int32_t b);
bool        i32_gt(int32_t a, int32_t b);
bool        i32_eq(int32_t a, int32_t b);
bool        i32_lte(int32_t a, int32_t b);
bool        i32_lt(int32_t a, int32_t b);
bool        i32_neq(int32_t a, int32_t b);

// i64
int64_t     str2i64(char str[]);
i64_res     i64_add(int64_t a, int64_t b);
i64_res     i64_sub(int64_t a, int64_t b);
i64_res     i64_mul(int64_t a, int64_t b);
f64_res     i64_divide(int64_t a, int64_t b);
i64_res     i64_pow(int64_t a, int64_t b);
i32_res     i64_neg(int64_t a);
bool        i64_gte(int64_t a, int64_t b);
bool        i64_gt(int64_t a, int64_t b);
bool        i64_eq(int64_t a, int64_t b);
bool        i64_lte(int64_t a, int64_t b);
bool        i64_lt(int64_t a, int64_t b);
bool        i64_neq(int64_t a, int64_t b);

// Conversions
float32_t f16_to_f32(float16_t x);
float64_t f16_to_f64(float16_t x);

float16_t f32_to_f16(float32_t x);
float64_t f32_to_f64(float32_t x);

float16_t f64_to_f16(float64_t x);
float32_t f64_to_f32(float64_t x);

int32_t     f32_to_i32(float32_t x);
int64_t     f32_to_i64(float32_t x);

float32_t   i32_to_f32(int32_t x);
float32_t   i64_to_f32(int64_t x);