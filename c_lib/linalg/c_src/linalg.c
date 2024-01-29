// clang -shared -o 'c_lib/linalg/lib/linalg.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// DEBUG: clang -shared -o 'c_lib/linalg/lib/linalg.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// TEST: clang -o 'c_lib/linalg/lib/linalg' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/linalg/c_src/linalg.c' 'c_lib/external_libraries/float16/c_src/float16.c'

#include "../include/linalg.h"

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

void free_i32m(int32_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

void free_i64m(int64_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

void free_u32m(uint32_matrix_t m) {
    for (size_t i=0; i<m.y; i++) {
        free(m.m[i]);
    }
    free(m.m);
}

void free_u64m(uint64_matrix_t m) {
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

int32_matrix_res_t copy_i32m(int32_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
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

int64_matrix_res_t copy_i64m(int64_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
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

uint32_matrix_res_t copy_u32m(uint32_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
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

uint64_matrix_res_t copy_u64m(uint64_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
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

//*Fill matrices with single numbers
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

int32_matrix_res_t i32m_fill(size_t x, size_t y, int32_t fill_value) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, int32_t);
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

int64_matrix_res_t i64m_fill(size_t x, size_t y, int64_t fill_value) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, int64_t);
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

uint32_matrix_res_t u32m_fill(size_t x, size_t y, uint32_t fill_value) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, uint32_t);
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

uint64_matrix_res_t u64m_fill(size_t x, size_t y, uint64_t fill_value) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, x, y);

    res.res.m = CALLOC(y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<y; i++) {
        res.res.m[i] = CALLOC(x, uint64_t);
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

int32_matrix_res_t i32m_row_vector_to_matrix(int32_matrix_t v, size_t no_rows) {
    int32_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, int32_t);
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

int64_matrix_res_t i64m_row_vector_to_matrix(int64_matrix_t v, size_t no_rows) {
    int64_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, int64_t);
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

uint32_matrix_res_t u32m_row_vector_to_matrix(uint32_matrix_t v, size_t no_rows) {
    uint32_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, uint32_t);
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

uint64_matrix_res_t u64m_row_vector_to_matrix(uint64_matrix_t v, size_t no_rows) {
    uint64_matrix_res_t res;

    if (v.y != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, v.x, no_rows);

    res.res.m = CALLOC(no_rows, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<no_rows; i++) {
        res.res.m[i] = CALLOC(v.x, uint64_t);
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

int32_matrix_res_t i32m_column_vector_to_matrix(int32_matrix_t v, size_t no_columns) {
    int32_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, int32_t);
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

int64_matrix_res_t i64m_column_vector_to_matrix(int64_matrix_t v, size_t no_columns) {
    int64_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, int64_t);
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

uint32_matrix_res_t u32m_column_vector_to_matrix(uint32_matrix_t v, size_t no_columns) {
    uint32_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, uint32_t);
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

uint64_matrix_res_t u64m_column_vector_to_matrix(uint64_matrix_t v, size_t no_columns) {
    uint64_matrix_res_t res;

    if (v.x != 1) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, no_columns, v.y);

    res.res.m = CALLOC(v.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<v.y; i++) {
        res.res.m[i] = CALLOC(no_columns, uint64_t);
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

int32_matrix_res_t f16m_to_i32m(float16_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)float16_to_float32(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t f16m_to_i64m(float16_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)float16_to_float32(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t f16m_to_u32m(float16_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)float16_to_float32(m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

uint64_matrix_res_t f16m_to_u64m(float16_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res;
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)float16_to_float32(m.m[i][j]);
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

int32_matrix_res_t f32m_to_i32m(float32_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t f32m_to_i64m(float32_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t f32m_to_u32m(float32_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)m.m[i][j];
        }
    }
    
    res.err = GOOD;
    return res;
}

uint64_matrix_res_t f32m_to_u64m(float32_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From f64m to other matrix types
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

int32_matrix_res_t f64m_to_i32m(float64_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t f64m_to_i64m(float64_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);
    
    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t f64m_to_u32m(float64_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint64_matrix_res_t f64m_to_u64m(float64_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From i32m to other matrix types
float16_matrix_res_t i32m_to_f16m(int32_matrix_t m) {
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

float32_matrix_res_t i32m_to_f32m(int32_matrix_t m) {
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

float64_matrix_res_t i32m_to_f64m(int32_matrix_t m) {
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

int64_matrix_res_t i32m_to_i64m(int32_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t i32m_to_u32m(int32_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint64_matrix_res_t i32m_to_u64m(int32_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From i64m to other matrix types
float16_matrix_res_t i64m_to_f16m(int64_matrix_t m) {
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

float32_matrix_res_t i64m_to_f32m(int64_matrix_t m) {
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

float64_matrix_res_t i64m_to_f64m(int64_matrix_t m) {
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

int32_matrix_res_t i64m_to_i32m(int64_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t i64m_to_u32m(int64_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint64_matrix_res_t i64m_to_u64m(int64_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From u32m to other matrix types
float16_matrix_res_t u32m_to_f16m(uint32_matrix_t m) {
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

float32_matrix_res_t u32m_to_f32m(uint32_matrix_t m) {
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

float64_matrix_res_t u32m_to_f64m(uint32_matrix_t m) {
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

int32_matrix_res_t u32m_to_i32m(uint32_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t u32m_to_i64m(uint32_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)m.m[i][j];
        }
    }
    
    res.err = GOOD;
    return res;
}

uint64_matrix_res_t u32m_to_u64m(uint32_matrix_t m) {
    uint64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//*From u64m to other matrix types
float16_matrix_res_t u64m_to_f16m(uint64_matrix_t m) {
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

float32_matrix_res_t u64m_to_f32m(uint64_matrix_t m) {
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

float64_matrix_res_t u64m_to_f64m(uint64_matrix_t m) {
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

int32_matrix_res_t u64m_to_i32m(uint64_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t u64m_to_i64m(uint64_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (int64_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

uint32_matrix_res_t u64m_to_u32m(uint64_matrix_t m) {
    uint32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, uint32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, uint32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            res.res.m[i][j] = (uint32_t)m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

//* Matrix casting
matrix_cast_res_t matrix_cast(matrix_t in_m, matrix_type_t tgt_type) { 
    matrix_cast_res_t res;

    if (in_m.matrix_type == tgt_type) {
        MC_SET_RES_TYPE(res, in_m.matrix_type);
        MC_GOOD_RES(res);
        return res;
    }
    
    float16_matrix_res_t    f16mr;
    float32_matrix_res_t    f32mr;
    float64_matrix_res_t    f64mr;
    int32_matrix_res_t      i32mr;
    int64_matrix_res_t      i64mr;
    uint32_matrix_res_t     u32mr;
    uint64_matrix_res_t     u64mr;

    MC_SET_RES_TYPE(res, tgt_type);
    switch (in_m.matrix_type) {
        case F16MT:
            switch (tgt_type) {
                case F32MT:
                    f32mr = f16m_to_f32m(in_m.m.f16m);
                    if (f32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f32mr.err);
                        return res;
                    }
                    res.res_matrix.m.f32m = f32mr.res;
                    break;
                case F64MT:
                    f64mr = f16m_to_f64m(in_m.m.f16m);
                    if (f64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f64mr.err);
                        return res;
                    }
                    res.res_matrix.m.f64m = f64mr.res;
                    break;
                case I32MT:
                    i32mr = f16m_to_i32m(in_m.m.f16m);
                    if (i32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i32mr.err);
                        return res;
                    }
                    res.res_matrix.m.i32m = i32mr.res;
                    break;
                case I64MT:
                    i64mr = f16m_to_i64m(in_m.m.f16m);
                    if (i64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i64mr.err);
                        return res;
                    }
                    res.res_matrix.m.i64m = i64mr.res;
                    break;
                default:
                    MC_SET_RES_ERROR(res, CASTTYPEERROR);
                    return res;
            }
            break;
        case F32MT:
            switch (tgt_type) {
                case F16MT:
                    f16mr = f32m_to_f16m(in_m.m.f32m);
                    if (f16mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f16mr.err);
                        return res;
                    }
                    res.res_matrix.m.f32m = f32mr.res;
                    break;
                case F64MT:
                    f64mr = f32m_to_f64m(in_m.m.f32m);
                    if (f64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f64mr.err);
                        return res;
                    }
                    res.res_matrix.m.f64m = f64mr.res;
                    break;
                case I32MT:
                    i32mr = f32m_to_i32m(in_m.m.f32m);
                    if (i32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i32mr.err);
                        return res;
                    }
                    res.res_matrix.m.i32m = i32mr.res;
                    break;
                case I64MT:
                    i64mr = f32m_to_i64m(in_m.m.f32m);
                    if (i64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i64mr.err);
                        return res;
                    }
                    res.res_matrix.m.i64m = i64mr.res;
                    break;
                default:
                    MC_SET_RES_ERROR(res, CASTTYPEERROR);
                    break;
            }
            break;
        case F64MT:
            switch (tgt_type) {
                case F16MT:
                    f16mr = f64m_to_f16m(in_m.m.f64m);
                    if (f16mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f16mr.err);
                        return res;
                    }
                    res.res_matrix.m.f16m = f16mr.res;
                    break;
                case F32MT:
                    f32mr = f64m_to_f32m(in_m.m.f64m);
                    if (f32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f32mr.err);
                        return res;
                    }
                    res.res_matrix.m.f32m = f32mr.res;
                    break;
                case I32MT:
                    i32mr = f64m_to_i32m(in_m.m.f64m);
                    if (i32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i32mr.err);
                        return res;
                    }
                    res.res_matrix.m.i32m = i32mr.res;
                    break;
                case I64MT:
                    i64mr = f64m_to_i64m(in_m.m.f64m);
                    if (i64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i64mr.err);
                        return res;
                    }
                    res.res_matrix.m.i64m = i64mr.res;
                    break;
                default:
                    MC_SET_RES_ERROR(res, CASTTYPEERROR);
                    break;
            }
            break;
        case I32MT:
            switch (tgt_type) {
                case F16MT:
                    f16mr = i32m_to_f16m(in_m.m.i32m);
                    if (f16mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f16mr.err);
                        return res;
                    }
                    res.res_matrix.m.f16m = f16mr.res;
                    break;
                case F32MT:
                    f32mr = i32m_to_f32m(in_m.m.i32m);
                    if (f32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f32mr.err);
                        return res;
                    }
                    res.res_matrix.m.f32m = f32mr.res;
                    break;
                case F64MT:
                    f64mr = i32m_to_f64m(in_m.m.i32m);
                    if (f64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f64mr.err);
                        return res;
                    }
                    res.res_matrix.m.f64m = f64mr.res;
                    break;
                case I64MT:
                    i64mr = i32m_to_i64m(in_m.m.i32m);
                    if (i64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i64mr.err);
                        return res;
                    }
                    res.res_matrix.m.i64m = i64mr.res;
                    break;
                default:
                    MC_SET_RES_ERROR(res, CASTTYPEERROR);
                    break;
            }
            break;
        case I64MT:
            switch (tgt_type) {
                case F16MT:
                    f16mr = i64m_to_f16m(in_m.m.i64m);
                    if (f16mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f16mr.err);
                        return res;
                    }
                    res.res_matrix.m.f16m = f16mr.res;
                    break;
                case F32MT:
                    f32mr = i64m_to_f32m(in_m.m.i64m);
                    if (f32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f32mr.err);
                        return res;
                    }
                    res.res_matrix.m.f32m = f32mr.res;
                    break;
                case F64MT:
                    f64mr = i64m_to_f64m(in_m.m.i64m);
                    if (f64mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, f64mr.err);
                        return res;
                    }
                    res.res_matrix.m.f64m = f64mr.res;
                    break;
                case I32MT:
                    i32mr = i64m_to_i32m(in_m.m.i64m);
                    if (i32mr.err != GOOD) {
                        MC_SET_RES_ERROR(res, i32mr.err);
                        return res;
                    }
                    res.res_matrix.m.i32m = i32mr.res;
                    break;
                default:
                    MC_SET_RES_ERROR(res, CASTTYPEERROR);
                    break;
            }
            break;
        default:
            MC_SET_RES_ERROR(res, CASTTYPEERROR);
            break;
    }
    MC_GOOD_RES(res);
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

int32_matrix_res_t i32m_add(int32_matrix_t m1, int32_matrix_t m2) {
    int32_matrix_res_t res;
    int32_t a;
    int32_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a > 0 && b > INT_MAX - a) {
                ERROR_RES(res, INTOVERFLOW);
                return res;
            } else if (a < 0 && b < INT_MIN - a) {
                ERROR_RES(res, INTUNDERFLOW);
                return res;
            }
            res.res.m[i][j] = a + b;
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t i64m_add(int64_matrix_t m1, int64_matrix_t m2) {
    int64_matrix_res_t res;
    int64_t a;
    int64_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a > 0 && b > LLONG_MAX - a) {
                ERROR_RES(res, INTOVERFLOW);
                return res;
            } else if (a < 0 && b < LLONG_MIN - a) {
                ERROR_RES(res, INTUNDERFLOW);
                return res;
            }
            res.res.m[i][j] = a + b;
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

int32_matrix_res_t i32m_sub(int32_matrix_t m1, int32_matrix_t m2) {
    int32_matrix_res_t res;
    int32_t a;
    int32_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a > 0 && b < INT_MIN - a) {
                ERROR_RES(res, INTOVERFLOW);
            } else if (a < 0 && b > INT_MAX - a) {
                ERROR_RES(res, INTUNDERFLOW);
            }
            res.res.m[i][j] = a - b;
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t i64m_sub(int64_matrix_t m1, int64_matrix_t m2) {
    int64_matrix_res_t res;
    int64_t a;
    int64_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a > 0 && b < LLONG_MIN - a) {
                ERROR_RES(res, INTOVERFLOW);
            } else if (a < 0 && b > LLONG_MAX - a) {
                ERROR_RES(res, INTUNDERFLOW);
            }
            res.res.m[i][j] = a - b;
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

int32_matrix_res_t i32m_mul(int32_matrix_t m1, int32_matrix_t m2) {
    int32_matrix_res_t res;
    int32_t a;
    int32_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a == 0 || b == 0) {
                res.res.m[i][j] = 0;
            } else if (b > 0) {
                if (a > INT_MAX / b) {
                    ERROR_RES(res, INTOVERFLOW);
                } else if (a < INT_MIN / b) {
                    ERROR_RES(res, INTUNDERFLOW);
                }
            } else if (b < 0) {
                if (a < INT_MIN / b) {
                    ERROR_RES(res, INTOVERFLOW);
                } else if (a > INT_MAX / b) {
                    ERROR_RES(res, INTUNDERFLOW);
                }
            }
            res.res.m[i][j] = a * b;
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t i64m_mul(int64_matrix_t m1, int64_matrix_t m2) {
    int64_matrix_res_t res;
    int64_t a;
    int64_t b;

    if ((m1.x != m2.x) || (m1.y != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    SET_DIMS(res.res, m1.x, m1.y);

    res.res.m = CALLOC(m1.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m1.y; i++) {
        res.res.m[i] = CALLOC(m1.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m1.x; j++) {
            a = m1.m[i][j];
            b = m2.m[i][j];

            if (a == 0 || b == 0) {
                res.res.m[i][j] = 0;
            } else if (b > 0) {
                if (a > LLONG_MAX / b) {
                    ERROR_RES(res, INTOVERFLOW);
                } else if (a < LLONG_MIN / b) {
                    ERROR_RES(res, INTUNDERFLOW);
                }
            } else if (b < 0) {
                if (a < LLONG_MIN / b) {
                    ERROR_RES(res, INTOVERFLOW);
                } else if (a > LLONG_MAX / b) {
                    ERROR_RES(res, INTUNDERFLOW);
                }
            }
            res.res.m[i][j] = a * b;
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

float64_matrix_res_t i32m_div(int32_matrix_t m1, int32_matrix_t m2) {
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
            if (m2.m[i][j] == 0) {
                ERROR_RES(res, ZERODIVERROR);
                return res;
            }
            res.res.m[i][j] = (float64_t)m1.m[i][j] / (float64_t)m2.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t i64m_div(int64_matrix_t m1, int64_matrix_t m2) {
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
            if (m2.m[i][j] == 0) {
                ERROR_RES(res, ZERODIVERROR);
                return res;
            }
            res.res.m[i][j] = (float64_t)m1.m[i][j] / (float64_t)m2.m[i][j];
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

int32_matrix_res_t i32m_matmul(int32_matrix_t m1, int32_matrix_t m2) {
    int32_matrix_res_t res;

    if ((m1.x != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    res = i32m_fill(m1.y, m2.x, 0);
    if (res.err != GOOD) {
        return res;
    }

    int32_t a;
    int32_t b;
    int32_t c;

    for (size_t i=0; i<m1.y; i++) {
        for (size_t j=0; j<m2.x; j++) {
            for (size_t k=0; k<m1.x; k++) {
                a = m1.m[i][k];
                b = m2.m[k][j];   
                if (a == 0 || b == 0) {
                    res.res.m[i][j] = 0;
                } else if (b > 0) {
                    if (a > INT_MAX / b) {
                        ERROR_RES(res, INTOVERFLOW);
                    } else if (a < INT_MIN / b) {
                        ERROR_RES(res, INTUNDERFLOW);
                    }
                } else if (b < 0) {
                    if (a < INT_MIN / b) {
                        ERROR_RES(res, INTOVERFLOW);
                    } else if (a > INT_MAX / b) {
                        ERROR_RES(res, INTUNDERFLOW);
                    }
                }
                c = a * b;

                if (res.res.m[i][j] > 0 && c > INT_MAX - res.res.m[i][j]) {
                    ERROR_RES(res, INTOVERFLOW);
                    return res;
                } else if (res.res.m[i][j] < 0 && c < INT_MIN - res.res.m[i][j]) {
                    ERROR_RES(res, INTUNDERFLOW);
                    return res;
                }

                res.res.m[i][j] += c;
            }
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t i64m_matmul(int64_matrix_t m1, int64_matrix_t m2) {
    int64_matrix_res_t res;

    if ((m1.x != m2.y)) {
        ERROR_RES(res, SHAPEERROR);
        return res;
    }

    res = i64m_fill(m1.y, m2.x, 0);
    if (res.err != GOOD) {
        return res;
    }

    int64_t a;
    int64_t b;
    int64_t c;

    for (size_t i=0; i<m1.y; i++) {
        for (size_t j=0; j<m2.x; j++) {
            for (size_t k=0; k<m1.x; k++) {
                a = m1.m[i][k];
                b = m2.m[k][j];   
                if (a == 0 || b == 0) {
                    res.res.m[i][j] = 0;
                } else if (b > 0) {
                    if (a > LLONG_MAX / b) {
                        ERROR_RES(res, INTOVERFLOW);
                    } else if (a < LLONG_MIN / b) {
                        ERROR_RES(res, INTUNDERFLOW);
                    }
                } else if (b < 0) {
                    if (a < LLONG_MIN / b) {
                        ERROR_RES(res, INTOVERFLOW);
                    } else if (a > LLONG_MAX / b) {
                        ERROR_RES(res, INTUNDERFLOW);
                    }
                }
                c = a * b;

                if (res.res.m[i][j] > 0 && c > LLONG_MAX - res.res.m[i][j]) {
                    ERROR_RES(res, INTOVERFLOW);
                    return res;
                } else if (res.res.m[i][j] < 0 && c < LLONG_MIN - res.res.m[i][j]) {
                    ERROR_RES(res, INTUNDERFLOW);
                    return res;
                }

                res.res.m[i][j] += c;
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

int32_matrix_res_t i32m_neg(int32_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int32_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            if (m.m[i][j] == INT_MIN) {
                ERROR_RES(res, INTOVERFLOW);
            }
            res.res.m[i][j] = -m.m[i][j];
        }
    }

    res.err = GOOD;
    return res;
}

int64_matrix_res_t i64m_neg(int64_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.x, m.y);

    res.res.m = CALLOC(m.y, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.x, int64_t);
        if (res.res.m[i] == NULL) {
            ERROR_RES(res, MALLOCERROR);
            return res;
        }
        for (size_t j=0; j<m.x; j++) {
            if (m.m[i][j] == LLONG_MIN) {
                ERROR_RES(res, INTOVERFLOW);
            }
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

float64_matrix_res_t i32m_exp(int32_matrix_t m) {
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
            res.res.m[i][j] = exp((float64_t)m.m[i][j]);
        }
    }

    res.err = GOOD;
    return res;
}

float64_matrix_res_t i64m_exp(int64_matrix_t m) {
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
            res.res.m[i][j] = exp((float64_t)m.m[i][j]);
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

int32_matrix_res_t i32m_transpose(int32_matrix_t m) {
    int32_matrix_res_t res;

    SET_DIMS(res.res, m.y, m.x);

    res.res.m = CALLOC(m.x, int32_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.y, int32_t);
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

int64_matrix_res_t i64m_transpose(int64_matrix_t m) {
    int64_matrix_res_t res;

    SET_DIMS(res.res, m.y, m.x);

    res.res.m = CALLOC(m.x, int64_t*);
    if (res.res.m == NULL) {
        ERROR_RES(res, MALLOCERROR);
        return res; 
    }
    for (size_t i=0; i<m.y; i++) {
        res.res.m[i] = CALLOC(m.y, int64_t);
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
