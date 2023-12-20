#include <stdlib.h>
#include <stdio.h>
#include <immintrin.h>
#include <math.h>

// Macros
#ifdef __cplusplus
#define MALLOC(count, item_type) (item_type*)malloc(count * sizeof(item_type))
#define CALLOC(count, item_type) (item_type*)calloc(count, sizeof(item_type))
#else
#define MALLOC(count, item_type) malloc(count * sizeof(item_type))
#define CALLOC(count, item_type) calloc(count, sizeof(item_type))
#endif

#define SET_DIMS(matrix, x_coord, y_coord) {matrix.x = x_coord; matrix.y = y_coord;}
#define ERROR_RES(result, error) {result.err = error; SET_DIMS(result.res, 0, 0); result.res.m = NULL;}

// Errors
typedef enum {
    GOOD = 0,
    MALLOCERROR,
    SHAPEERROR,
    ZERODIVERROR,
} error_t;

// Typedefs
typedef unsigned short  float16_t;
typedef float           float32_t;
typedef double          float64_t;

// Structs and unions
typedef struct {
    float16_t** m;
    size_t x;
    size_t y;
} float16_matrix_t;

typedef struct {
    float32_t** m;
    size_t x;
    size_t y;
} float32_matrix_t;

typedef struct {
    float64_t** m;
    size_t x;
    size_t y;
} float64_matrix_t;

typedef struct {
    float16_matrix_t res;
    error_t err;
} float16_matrix_res_t;

typedef struct {
    float32_matrix_t res;
    error_t err;
} float32_matrix_res_t;

typedef struct {
    float64_matrix_t res;
    error_t err;
} float64_matrix_res_t;

// Function prototypes
void free_f16m(float16_matrix_t m);
void free_f32m(float32_matrix_t m);
void free_f64m(float64_matrix_t m);
float16_matrix_res_t copy_f16m(float16_matrix_t m);
float32_matrix_res_t copy_f32m(float32_matrix_t m);
float64_matrix_res_t copy_f64m(float64_matrix_t m);
float16_matrix_res_t f16m_fill(size_t x, size_t y, float16_t fill_value);
float32_matrix_res_t f32m_fill(size_t x, size_t y, float32_t fill_value);
float64_matrix_res_t f64m_fill(size_t x, size_t y, float64_t fill_value);

float32_matrix_res_t f16m_to_f32m(float16_matrix_t m);
float64_matrix_res_t f16m_to_f64m(float16_matrix_t m);
float16_matrix_res_t f32m_to_f16m(float32_matrix_t m);
float64_matrix_res_t f32m_to_f64m(float32_matrix_t m);
float16_matrix_res_t f64m_to_f16m(float64_matrix_t m);
float32_matrix_res_t f64m_to_f32m(float64_matrix_t m);

float16_matrix_res_t f16m_add(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_add(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_add(float64_matrix_t m1, float64_matrix_t m2);

float16_matrix_res_t f16m_sub(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_sub(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_sub(float64_matrix_t m1, float64_matrix_t m2);

float16_matrix_res_t f16m_mul(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_mul(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_mul(float64_matrix_t m1, float64_matrix_t m2);

float16_matrix_res_t f16m_div(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_div(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_div(float64_matrix_t m1, float64_matrix_t m2);

float16_matrix_res_t f16m_matmul(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_matmul(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_matmul(float64_matrix_t m1, float64_matrix_t m2);

float16_matrix_res_t f16m_neg(float16_matrix_t m);
float32_matrix_res_t f32m_neg(float32_matrix_t m);
float64_matrix_res_t f64m_neg(float64_matrix_t m);

float16_matrix_res_t f16m_exp(float16_matrix_t m);
float32_matrix_res_t f32m_exp(float32_matrix_t m);
float64_matrix_res_t f64m_exp(float64_matrix_t m);

float16_matrix_res_t f16m_transpose(float16_matrix_t m);
float32_matrix_res_t f32m_transpose(float32_matrix_t m);
float64_matrix_res_t f64m_transpose(float64_matrix_t m);