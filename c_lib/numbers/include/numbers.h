#include "../../float16/include/float16.h"
#include "../../float16/c_src/conv.h"
#include <stdlib.h>
#include <stdbool.h>
#include <stdio.h>
#include <math.h>

// Typedefs
typedef float   float32_t;
typedef double  float64_t;

// Structs
typedef struct {
    float16_t res;
    bool has_error;
} f16_res;

typedef struct {
    float32_t res;
    bool has_error;
} f32_res;

typedef struct {
    float64_t res;
    bool has_error;
} f64_res;

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

// Conversions
float32_t f16_to_f32(float16_t x);
float64_t f16_to_f64(float16_t x);

float16_t f32_to_f16(float32_t x);
float64_t f32_to_f64(float32_t x);

float16_t f64_to_f16(float64_t x);
float32_t f64_to_f32(float64_t x);