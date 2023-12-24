// gcc -shared -o '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'
// DEBUG: gcc -shared -o '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'
// TEST: gcc -o '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/numbers/c_src/numbers.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'

#include "../include/numbers.h"

// f16

/*
float16_t f16_abs(float16_t x) {
    return x & 0x8000 ? f16_neg(x) : x;
}
*/

float16_t str2f16(char str[]) {
    float32_t float_repr = strtof(str, NULL);
    float16_t half_repr = float32_to_float16(float_repr);
    return half_repr;
}

#define IS_INF(x) (((x) & 0x7FFF) == 0x7C00)
#define IS_NAN(x) (((x) & 0x7FFF) > 0x7C00)
void conv_f16_to_str(float16_t h, char* buffer) {
    if (IS_INF(h)) {
        if (f16_gt(h, 0x0000)) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (IS_NAN(h)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%.3f", float16_to_float32(h));
    }
}

void conv_f16_to_sci_str(float16_t h, char* buffer) {
    if (IS_INF(h)) {
        if (f16_gt(h, 0x0000)) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (IS_NAN(h)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%e", float16_to_float32(h));
    }
}

f16_res f16_divide(float16_t a, float16_t b) {
    f16_res result;
    if (f16_eq(b, 0x0000)) {
        result.has_error = true;
        result.res = 0x7FFF;
    } else {
        result.has_error = false;
        result.res = f16_div(a, b);
    }
    return result;
}

float16_t f16_pow(float16_t a, float16_t b) {
    /*!DO NOT USE - MONSTERS INSIDE!
    if (f16_lt(b, 0x0000)) {
        return f16_div(0x3C00, f16_pow(a, f16_negate(b)));
    } else if (f16_from_int(f16_int(b)) == b) {
        float16_t ans = 0x3C00;
        for (size_t i=0; i<f16_int(b); i++) {
            ans = f16_mul(ans, a);
        }
        return ans;
    } else if (f16_eq(a, 0x0000)) {
        return 0x0000;
    }
    assert(f16_gt(a, 0x0000));
    */
    return float32_to_float16(powf(float16_to_float32(a), float16_to_float32(b)));
}

// f32

float32_t str2f32(char str[]) {
    return strtof(str, NULL);
}

void conv_f32_to_str(float32_t f, char* buffer) {
    if (isinf(f)) {
        if (f > 0.0f) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(f)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%f", f);
    }
}

void conv_f32_to_sci_str(float32_t f, char* buffer) {
    if (isinf(f)) {
        if (f > 0.0f) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(f)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%e", f);
    }
}

float32_t f32_add(float32_t a, float32_t b) {
    return a + b;
}

float32_t f32_sub(float32_t a, float32_t b) {
    return a - b;
}

float32_t f32_mul(float32_t a, float32_t b) {
    return a * b;
}

f32_res f32_divide(float32_t a, float32_t b) {
    f32_res result;
    if (b == 0.0f) {
        result.has_error = true;
        result.res = NAN;
    } else {
        result.has_error = false;
        result.res = a / b;
    }
    return result;
}

float32_t f32_pow(float32_t a, float32_t b) {
    return powf(a, b);
}

float32_t f32_neg(float32_t a) {
    return -a;
}

bool f32_gte(float32_t a, float32_t b) {
    return a >= b;
}

bool f32_gt(float32_t a, float32_t b) {
    return a > b;
}

bool f32_eq(float32_t a, float32_t b) {
    return a == b;
}

bool f32_lte(float32_t a, float32_t b) {
    return a <= b;
}

bool f32_lt(float32_t a, float32_t b) {
    return a < b;
}

bool f32_neq(float32_t a, float32_t b) {
    return a != b;
}

// f64

float64_t str2f64(char str[]) {
    return strtod(str, NULL);
}

void conv_f64_to_str(float64_t d, char* buffer) {
    if (isinf(d)) {
        if (d > 0.0) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(d)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%lf", d);
    }
}

void conv_f64_to_sci_str(float64_t d, char* buffer) {
    if (isinf(d)) {
        if (d > 0.0) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(d)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%e", d);
    }
}

float64_t f64_add(float64_t a, float64_t b) {
    return a + b;
}

float64_t f64_sub(float64_t a, float64_t b) {
    return a - b;
}

float64_t f64_mul(float64_t a, float64_t b) {
    return a * b;
}

f64_res f64_divide(float64_t a, float64_t b) {
    f64_res result;
    if (b == 0.0) {
        result.has_error = true;
        result.res = NAN;
    } else {
        result.has_error = false;
        result.res = a / b;
    }
    return result;
}

float64_t f64_pow(float64_t a, float64_t b) {
    return pow(a, b);
}

float64_t f64_neg(float64_t a) {
    return -a;
}

bool f64_gte(float64_t a, float64_t b) {
    return a >= b;
}

bool f64_gt(float64_t a, float64_t b) {
    return a > b;
}

bool f64_eq(float64_t a, float64_t b) {
    return a == b;
}

bool f64_lte(float64_t a, float64_t b) {
    return a <= b;
}

bool f64_lt(float64_t a, float64_t b) {
    return a < b;
}

bool f64_neq(float64_t a, float64_t b) {
    return a != b;
}

//i32
int32_t str2i32(char str[]) {
    return atoi(str);
}

void conv_i32_to_str(int32_t n, char* buffer) {
    sprintf(buffer, "%d", n);
}

i32_res i32_add(int32_t a, int32_t b) {
    i32_res res;
    if (a > 0 && b > INT_MAX - a) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else if (a < 0 && b < INT_MIN - a) {
        OVERFLOW_RES(res, INTUNDERFLOW)
    } else {
        GOOD_INT_RES(res, a+b);
    }
    return res;
}

i32_res i32_sub(int32_t a, int32_t b) {
    i32_res res;
    if (a > 0 && b < INT_MIN - a) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else if (a < 0 && b > INT_MAX - a) {
        OVERFLOW_RES(res, INTUNDERFLOW);
    } else {
        GOOD_INT_RES(res, a-b);
    }
    return res;
}

i32_res i32_mul(int32_t a, int32_t b) {
    i32_res res;
    if (a == 0 || b == 0) {
        GOOD_INT_RES(res, 0);
    } else if (b > 0) {
        if (a > INT_MAX / b) {
            OVERFLOW_RES(res, INTOVERFLOW);
        } else if (a < INT_MIN / b) {
            OVERFLOW_RES(res, INTUNDERFLOW);
        }
    } else if (b < 0 && a < INT_MIN / b) {
        if (a < INT_MIN / b) {
            OVERFLOW_RES(res, INTOVERFLOW);
        } else if (a > INT_MAX / b) {
            OVERFLOW_RES(res, INTUNDERFLOW);
        }
    }
    return res;
}

f64_res i32_divide(int32_t a, int32_t b) {
    return f64_divide((float64_t)a, (float64_t)b);
}

float64_t i32_pow(int32_t a, int32_t b) {
    return f64_pow((float64_t)a, (float64_t)b);
}

i32_res i32_neg(int32_t a) {
    i32_res res;
    if (a == INT_MIN) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else {
        GOOD_INT_RES(res, -a);
    }
    return res;
}

bool i32_gte(int32_t a, int32_t b) {
    return a >= b;
}

bool i32_gt(int32_t a, int32_t b) {
    return a > b;
}

bool i32_eq(int32_t a, int32_t b) {
    return a == b;
}

bool i32_lte(int32_t a, int32_t b) {
    return a <= b;
}

bool i32_lt(int32_t a, int32_t b) {
    return a < b;
}

bool i32_neq(int32_t a, int32_t b) {
    return a != b;
}

//i64
int64_t str2i64(char str[]) {
    return atoll(str);
}

void conv_i64_to_str(int64_t n, char* buffer) {
    sprintf(buffer, "%lld", n);
}

i64_res i64_add(int64_t a, int64_t b) {
    i64_res res;
    if (a > 0 && b > LLONG_MAX - a) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else if (a < 0 && b < LLONG_MIN - a) {
        OVERFLOW_RES(res, INTUNDERFLOW)
    } else {
        GOOD_INT_RES(res, a+b);
    }
    return res; 
}

i64_res i64_sub(int64_t a, int64_t b) {
    i64_res res;
    if (a > 0 && b < LLONG_MIN - a) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else if (a < 0 && b > LLONG_MAX - a) {
        OVERFLOW_RES(res, INTUNDERFLOW);
    } else {
        GOOD_INT_RES(res, a-b);
    }
    return res;
}

i64_res i64_mul(int64_t a, int64_t b) {
    i64_res res;
    if (a == 0 || b == 0) {
        GOOD_INT_RES(res, 0);
    } else if (b > 0) {
        if (a > LLONG_MAX / b) {
            OVERFLOW_RES(res, INTOVERFLOW);
        } else if (a < LLONG_MIN / b) {
            OVERFLOW_RES(res, INTUNDERFLOW);
        }
    } else if (b < 0 && a < INT_MIN / b) {
        if (a < LLONG_MIN / b) {
            OVERFLOW_RES(res, INTOVERFLOW);
        } else if (a > LLONG_MAX / b) {
            OVERFLOW_RES(res, INTUNDERFLOW);
        }
    }
    return res;
}

f64_res i64_divide(int64_t a, int64_t b) {
    return f64_divide((float64_t)a, (float64_t)b);
}

float64_t i64_pow(int64_t a, int64_t b) {
    return f64_pow((float64_t)a, (float64_t)b);
}

i64_res i64_neg(int64_t a) {
    i64_res res;
    if (a == LLONG_MIN) {
        OVERFLOW_RES(res, INTOVERFLOW);
    } else {
        GOOD_INT_RES(res, -a);
    }
    return res;
}

bool i64_gte(int64_t a, int64_t b) {
    return a >= b;
}

bool i64_gt(int64_t a, int64_t b) {
    return a > b;
}

bool i64_eq(int64_t a, int64_t b) {
    return a == b;
}

bool i64_lte(int64_t a, int64_t b) {
    return a <= b;
}

bool i64_lt(int64_t a, int64_t b) {
    return a < b;
}

bool i64_neq(int64_t a, int64_t b) {
    return a != b;
}

// Conversions
//*From f16 to other float types
float32_t f16_to_f32(float16_t x) {
    return float16_to_float32(x);
}

float64_t f16_to_f64(float16_t x) {
    return (float64_t)float16_to_float32(x);
}

//*From f32 to other float types
float16_t f32_to_f16(float32_t x) {
    return float32_to_float16(x);
}

float64_t f32_to_f64(float32_t x) {
    return (float64_t)x;
}

//*From f64 to other float types
float16_t f64_to_f16(float64_t x) {
    return float32_to_float16((float32_t)x);
}

float32_t f64_to_f32(float64_t x) {
    return (float32_t)x;
}

//*From i32/i64 types to i64/i32
int64_t i32_to_i64(int32_t x) {
    return (int64_t)x;
}

int32_t i64_to_i32(int64_t x) {
    return (int32_t)x;
}

//*From f32 to int types
int32_t f32_to_i32(float32_t x) {
    return (int32_t)x;
}

int64_t f32_to_i64(float32_t x) {
    return (int64_t)x;
}

//*From int types to f32
float32_t i32_to_f32(int32_t x) {
    return (float32_t)x;
}

float32_t i64_to_f32(int64_t x) {
    return (float32_t)x;
}