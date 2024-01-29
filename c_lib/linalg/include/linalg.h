#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include <stdlib.h>
#include <stdio.h>
#include <immintrin.h>
#include <math.h>
#include <stdint.h>
#include <limits.h>

// Macros
//*Malloc and Calloc
#ifdef __cplusplus
#define MALLOC(count, item_type) (item_type*)malloc(count * sizeof(item_type))
#define CALLOC(count, item_type) (item_type*)calloc(count, sizeof(item_type))
#else
#define MALLOC(count, item_type) malloc(count * sizeof(item_type))
#define CALLOC(count, item_type) calloc(count, sizeof(item_type))
#endif

//*Normal result macros
#define SET_DIMS(matrix, x_coord, y_coord) {matrix.x = x_coord; matrix.y = y_coord;}
#define ERROR_RES(result, error) {result.err = error; SET_DIMS(result.res, 0, 0); result.res.m = NULL;}

//*Matrix cast result macros
#define MC_SET_RES_TYPE(result, type) {result.res_matrix.matrix_type = type;}
#define MC_SET_RES_ERROR(result, error) {result.err = error;}
#define MC_GOOD_RES(result) {MC_SET_RES_ERROR(result, GOOD);}

// Errors
typedef enum {
    GOOD = 0,
    MALLOCERROR,
    SHAPEERROR,
    ZERODIVERROR,
    INTOVERFLOW,
    INTUNDERFLOW,
    CASTTYPEERROR,
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
    int32_t** m;
    size_t x;
    size_t y;
} int32_matrix_t;

typedef struct {
    int64_t** m;
    size_t x;
    size_t y;
} int64_matrix_t;

typedef struct {
    uint32_t** m;
    size_t x;
    size_t y;
} uint32_matrix_t;

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

typedef struct {
    int32_matrix_t res;
    error_t err;
} int32_matrix_res_t;

typedef struct {
    int64_matrix_t res;
    error_t err;
} int64_matrix_res_t;

typedef struct {
    uint32_matrix_t res;
    error_t err;
} uint32_matrix_res_t;

typedef struct {
    uint64_matrix_t res;
    error_t err;
} uint64_matrix_res_t;

// Matrix cast structures
typedef enum {
    F16MT = 0,
    F32MT,
    F64MT,
    I32MT,
    I64MT,
    U32MT,
    U64MT,
} matrix_type_t;

typedef union {
    float16_matrix_t f16m;
    float32_matrix_t f32m;
    float64_matrix_t f64m;
    int32_matrix_t i32m;
    int64_matrix_t i64m;
    uint32_matrix_t u32m;
    uint64_matrix_t u64m;
} matrix_container_t;

typedef struct {
    matrix_container_t m;
    matrix_type_t matrix_type;
} matrix_t;

typedef struct {
    matrix_t res_matrix;
    error_t err;
} matrix_cast_res_t;

// Function prototypes
void free_f16m(float16_matrix_t m);
void free_f32m(float32_matrix_t m);
void free_f64m(float64_matrix_t m);
void free_i32m(int32_matrix_t m);
void free_i64m(int64_matrix_t m);
float16_matrix_res_t copy_f16m(float16_matrix_t m);
float32_matrix_res_t copy_f32m(float32_matrix_t m);
float64_matrix_res_t copy_f64m(float64_matrix_t m);
int32_matrix_res_t   copy_i32m(int32_matrix_t m);
int64_matrix_res_t   copy_i64m(int64_matrix_t m);

float16_matrix_res_t f16m_fill(size_t x, size_t y, float16_t fill_value);
float32_matrix_res_t f32m_fill(size_t x, size_t y, float32_t fill_value);
float64_matrix_res_t f64m_fill(size_t x, size_t y, float64_t fill_value);
int32_matrix_res_t   i32m_fill(size_t x, size_t y, int32_t fill_value);
int64_matrix_res_t   i64m_fill(size_t x, size_t y, int64_t fill_value);

float16_matrix_res_t f16m_row_vector_to_matrix(float16_matrix_t v, size_t no_rows);
float32_matrix_res_t f32m_row_vector_to_matrix(float32_matrix_t v, size_t no_rows);
float64_matrix_res_t f64m_row_vector_to_matrix(float64_matrix_t v, size_t no_rows);
int32_matrix_res_t   i32m_row_vector_to_matrix(int32_matrix_t v, size_t no_rows);
int64_matrix_res_t   i64m_row_vector_to_matrix(int64_matrix_t v, size_t no_rows);

float16_matrix_res_t f16m_column_vector_to_matrix(float16_matrix_t v, size_t no_columns);
float32_matrix_res_t f32m_column_vector_to_matrix(float32_matrix_t v, size_t no_columns);
float64_matrix_res_t f64m_column_vector_to_matrix(float64_matrix_t v, size_t no_columns);
int32_matrix_res_t   i32m_column_vector_to_matrix(int32_matrix_t v, size_t no_columns);
int64_matrix_res_t   i64m_column_vector_to_matrix(int64_matrix_t v, size_t no_columns);

float32_matrix_res_t f16m_to_f32m(float16_matrix_t m);
float64_matrix_res_t f16m_to_f64m(float16_matrix_t m);
int32_matrix_res_t   f16m_to_i32m(float16_matrix_t m);
int64_matrix_res_t   f16m_to_i64m(float16_matrix_t m);

float16_matrix_res_t f32m_to_f16m(float32_matrix_t m);
float64_matrix_res_t f32m_to_f64m(float32_matrix_t m); 
int32_matrix_res_t   f32m_to_i32m(float32_matrix_t m);
int64_matrix_res_t   f32m_to_i64m(float32_matrix_t m);

float16_matrix_res_t f64m_to_f16m(float64_matrix_t m);
float32_matrix_res_t f64m_to_f32m(float64_matrix_t m);
int32_matrix_res_t   f64m_to_i32m(float64_matrix_t m);
int64_matrix_res_t   f64m_to_i64m(float64_matrix_t m);

float16_matrix_res_t i32m_to_f16m(int32_matrix_t m);
float32_matrix_res_t i32m_to_f32m(int32_matrix_t m);
float64_matrix_res_t i32m_to_f64m(int32_matrix_t m);
int64_matrix_res_t   i32m_to_i64m(int32_matrix_t m);

float16_matrix_res_t i64m_to_f16m(int64_matrix_t m);
float32_matrix_res_t i64m_to_f32m(int64_matrix_t m);
float64_matrix_res_t i64m_to_f64m(int64_matrix_t m);
int32_matrix_res_t   i64m_to_i32m(int64_matrix_t m);

matrix_cast_res_t    matrix_cast(matrix_t in_m, matrix_type_t tgt_type);

float16_matrix_res_t f16m_add(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_add(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_add(float64_matrix_t m1, float64_matrix_t m2);
int32_matrix_res_t   i32m_add(int32_matrix_t m1, int32_matrix_t m2);
int64_matrix_res_t   i64m_add(int64_matrix_t m1, int64_matrix_t m2);

float16_matrix_res_t f16m_sub(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_sub(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_sub(float64_matrix_t m1, float64_matrix_t m2);
int32_matrix_res_t   i32m_sub(int32_matrix_t m1, int32_matrix_t m2);
int64_matrix_res_t   i64m_sub(int64_matrix_t m1, int64_matrix_t m2);

float16_matrix_res_t f16m_mul(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_mul(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_mul(float64_matrix_t m1, float64_matrix_t m2);
int32_matrix_res_t   i32m_mul(int32_matrix_t m1, int32_matrix_t m2);
int64_matrix_res_t   i64m_mul(int64_matrix_t m1, int64_matrix_t m2);

float16_matrix_res_t f16m_div(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_div(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_div(float64_matrix_t m1, float64_matrix_t m2);
float64_matrix_res_t i32m_div(int32_matrix_t m1, int32_matrix_t m2);
float64_matrix_res_t i64m_div(int64_matrix_t m1, int64_matrix_t m2);

float16_matrix_res_t f16m_matmul(float16_matrix_t m1, float16_matrix_t m2);
float32_matrix_res_t f32m_matmul(float32_matrix_t m1, float32_matrix_t m2);
float64_matrix_res_t f64m_matmul(float64_matrix_t m1, float64_matrix_t m2);
int32_matrix_res_t   i32m_matmul(int32_matrix_t m1, int32_matrix_t m2);
int64_matrix_res_t   i64m_matmul(int64_matrix_t m1, int64_matrix_t m2);

float16_matrix_res_t f16m_neg(float16_matrix_t m);
float32_matrix_res_t f32m_neg(float32_matrix_t m);
float64_matrix_res_t f64m_neg(float64_matrix_t m);
int32_matrix_res_t   i32m_neg(int32_matrix_t m);
int64_matrix_res_t   i64m_neg(int64_matrix_t m);

float16_matrix_res_t f16m_exp(float16_matrix_t m);
float32_matrix_res_t f32m_exp(float32_matrix_t m);
float64_matrix_res_t f64m_exp(float64_matrix_t m);
float64_matrix_res_t i32m_exp(int32_matrix_t m);
float64_matrix_res_t i64m_exp(int64_matrix_t m);

float16_matrix_res_t f16m_transpose(float16_matrix_t m);
float32_matrix_res_t f32m_transpose(float32_matrix_t m);
float64_matrix_res_t f64m_transpose(float64_matrix_t m);
int32_matrix_res_t   i32m_transpose(int32_matrix_t m);
int64_matrix_res_t   i64m_transpose(int64_matrix_t m);