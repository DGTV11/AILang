// clang -shared -o 'c_lib/linalg/c_src/linalg.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/float16/c_src/float16.c'
// DEBUG: clang -shared -o 'c_lib/linalg/c_src/linalg.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/float16/c_src/float16.c'
// TEST: clang -o 'c_lib/linalg/c_src/linalg' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/float16/c_src/float16.c'

#include "../include/linalg.h"
#include "../../float16/include/float16.h"
#include "../../float16/c_src/conv.h"

// Memory-related functions
//*Free matrices
void free_f16m(float16_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

void free_f32m(float32_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

void free_f64m(float64_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

//*Copy matrices
float16_matrix_res_t copy_f16m(float16_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t copy_f32m(float32_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t copy_f64m(float64_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Fill matrices with single floats
float16_matrix_res_t f16m_fill(size_t x, size_t y, float16_t fill_value) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<x; j++) {
            res.res.m[i][j] = fill_value;
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_fill(size_t x, size_t y, float32_t fill_value) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<x; j++) {
            res.res.m[i][j] = fill_value;
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_fill(size_t x, size_t y, float64_t fill_value) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<x; j++) {
            res.res.m[i][j] = fill_value;
        }
    }

    res.err = GOOD;
    return res;
}

//*Broadcast row vectors to matrices
float16_matrix_res_t f16m_row_vector_to_matrix(float16_matrix_t v, size_t no_rows) {
    float16_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<v.x; j++) {
            res.res.m[i][j] = v.m[0][j];
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_row_vector_to_matrix(float32_matrix_t v, size_t no_rows) {
    float32_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<v.x; j++) {
            res.res.m[i][j] = v.m[0][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_row_vector_to_matrix(float64_matrix_t v, size_t no_rows) {
    float64_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<v.x; j++) {
            res.res.m[i][j] = v.m[0][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Broadcast column vectors to matrices
float16_matrix_res_t f16m_column_vector_to_matrix(float16_matrix_t v, size_t no_columns) {
    float16_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<no_columns; j++) {
            res.res.m[i][j] = v.m[i][0];
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_column_vector_to_matrix(float32_matrix_t v, size_t no_columns) {
    float32_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<no_columns; j++) {
            res.res.m[i][j] = v.m[i][0];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_column_vector_to_matrix(float64_matrix_t v, size_t no_columns) {
    float64_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<no_columns; j++) {
            res.res.m[i][j] = v.m[i][0];
        }
    }

    res.err = GOOD;
    return res;
}

// Conversion functions
//*From f16m to other matrix types
float32_matrix_res_t f16m_to_f32m(float16_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = float16_to_float32(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f16m_to_f64m(float16_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (float64_t)float16_to_float32(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

//*From f32m to other matrix types
float16_matrix_res_t f32m_to_f16m(float32_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = float32_to_float16(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f32m_to_f64m(float32_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (float64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From f32m to other matrix types
float16_matrix_res_t f64m_to_f16m(float64_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = float32_to_float16((float32_t)m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f64m_to_f32m(float64_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (float32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

// Operation functions
//*Addition
float16_matrix_res_t f16m_add(float16_matrix_t m1, float16_matrix_t m2) {
    float16_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = f16_add(m1.m[i][j], m2.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_add(float32_matrix_t m1, float32_matrix_t m2) {
    float32_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] + m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_add(float64_matrix_t m1, float64_matrix_t m2) {
    float64_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] + m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Subtraction
float16_matrix_res_t f16m_sub(float16_matrix_t m1, float16_matrix_t m2) {
    float16_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = f16_sub(m1.m[i][j], m2.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_sub(float32_matrix_t m1, float32_matrix_t m2) {
    float32_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] - m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_sub(float64_matrix_t m1, float64_matrix_t m2) {
    float64_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] - m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Multiplication
float16_matrix_res_t f16m_mul(float16_matrix_t m1, float16_matrix_t m2) {
    float16_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = f16_mul(m1.m[i][j], m2.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_mul(float32_matrix_t m1, float32_matrix_t m2) {
    float32_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] * m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_mul(float64_matrix_t m1, float64_matrix_t m2) {
    float64_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            res.res.m[i][j] = m1.m[i][j] * m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Division
float16_matrix_res_t f16m_div(float16_matrix_t m1, float16_matrix_t m2) {
    float16_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            if (((m2.m[i][j]) & 0x7FFF) == 0) {
                ERROR_RES(res, ZERODIVERROR);
                return res;
            }
            res.res.m[i][j] = f16_div(m1.m[i][j], m2.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_div(float32_matrix_t m1, float32_matrix_t m2) {
    float32_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            if (m2.m[i][j] == 0.0f) {
                ERROR_RES(res, ZERODIVERROR);
                return res;
            }
            res.res.m[i][j] = m1.m[i][j] / m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_div(float64_matrix_t m1, float64_matrix_t m2) {
    float64_matrix_res_t res;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            if (m2.m[i][j] == 0.0) {
                ERROR_RES(res, ZERODIVERROR);
                return res;
            }
            res.res.m[i][j] = m1.m[i][j] / m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*Matrix multiplication
float16_matrix_res_t f16m_matmul(float16_matrix_t m1, float16_matrix_t m2) {
    float16_matrix_res_t res;

    if ((m1.x != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    res = f16m_fill(m1.y, m2.x, 0x0000);
    if (res.err != GOOD) {
        return res;
    }

    for (size_t i=0; i<m1.y; i++) {
        for (size_t j=0; j<m2.x; j++) {
            for (size_t k=0; k<m1.x; k++) {
                res.res.m[i][j] = f16_add(res.res.m[i][j], m1.m[i][k] * m2.m[k][j]);
            }
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_matmul(float32_matrix_t m1, float32_matrix_t m2) {
    float32_matrix_res_t res;

    if ((m1.x != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    res = f32m_fill(m1.y, m2.x, 0.0f);
    if (res.err != GOOD) {
        return res;
    }

    for (size_t i=0; i<m1.y; i++) {
        for (size_t j=0; j<m2.x; j++) {
            for (size_t k=0; k<m1.x; k++) {
                res.res.m[i][j] += m1.m[i][k] * m2.m[k][j];
            }
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_matmul(float64_matrix_t m1, float64_matrix_t m2) {
    float64_matrix_res_t res;

    if ((m1.x != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    res = f64m_fill(m1.y, m2.x, 0.0);
    if (res.err != GOOD) {
        return res;
    }

    for (size_t i=0; i<m1.y; i++) {
        for (size_t j=0; j<m2.x; j++) {
            for (size_t k=0; k<m1.x; k++) {
                res.res.m[i][j] += m1.m[i][k] * m2.m[k][j];
            }
        }
    }

    res.err = GOOD;
    return res;
}

//*Negate
float16_matrix_res_t f16m_neg(float16_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = f16_neg(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_neg(float32_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = -m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_neg(float64_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = -m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*e^x
float16_matrix_res_t f16m_exp(float16_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = float32_to_float16(expf(float16_to_float32(m.m[i][j])));
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_exp(float32_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = expf(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_exp(float64_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = exp(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

//*Transposes
float16_matrix_res_t f16m_transpose(float16_matrix_t m) {
    float16_matrix_res_t res;

    SET_DIMS(res.res, m.y, m.x);

    res.res.m = CALLOC(m.x, float16_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.y, float16_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[j][i];
        }
    }

    res.err = GOOD;
    return res;
}

float32_matrix_res_t f32m_transpose(float32_matrix_t m) {
    float32_matrix_res_t res;

    SET_DIMS(res.res, m.y, m.x);

    res.res.m = CALLOC(m.x, float32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.y, float32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[j][i];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t f64m_transpose(float64_matrix_t m) {
    float64_matrix_res_t res;

    SET_DIMS(res.res, m.y, m.x);

    res.res.m = CALLOC(m.x, float64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.y, float64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = m.m[j][i];
        }
    }

    res.err = GOOD;
    return res;
}

// Tests
