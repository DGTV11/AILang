// gcc -shared -o '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'
// DEBUG: gcc -shared -o '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'
// TEST: gcc -o '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/fpmath/c_src/fpmath.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include "../include/fpmath.h"
#include "../../float16/include/float16.h"
#include "../../float16/c_src/conv.h"

double str2double(char str[]) {
    return strtod(str, NULL);
}

float str2float(char str[]) {
    return strtof(str, NULL);
}

half str2half(char str[]) {
    float float_repr = str2float(str);
    half half_repr = float32_to_float16(float_repr);
    return half_repr;
}

void free_res_ptr(result* res) {
    free(res);
}

result check_inputs(mfloat self, mfloat other) {
    result res;
    if (self.type != other.type) {
        res.res.value.float_ = NAN;
        res.error = TYPEINEQERROR;
    } else if (self.type == BOOL || other.type == BOOL) {
        res.res.value.float_ = NAN;
        res.error = INPUTERROR;
    } else {
        res.res.value.float_ = NAN;
        res.error = GOOD;
    }
    res.res.type = FLOAT;
    return res;
}

result promote_input(mfloat self, int type) {
    result res;

    // Check inputs
    if (self.type < BOOL || self.type > DOUBLE) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (type < BOOL || type > DOUBLE) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (type < self.type) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (self.type == type || self.type == DOUBLE) {
        res.res.value = self.value;
        res.res.type = self.type;
        res.error = GOOD;
        return res;
    }

    // Promote by 1 type
    switch (self.type) {
        case BOOL:
            if (self.value.bool_) {
                res.res.value.half_ = 0x3C00;
                res.res.type = HALF;
                res.error = GOOD;
            } else {
                res.res.value.half_ = 0x0000;
                res.res.type = HALF;
                res.error = GOOD;
            }
            break;
        case HALF:
            res.res.value.float_ = float16_to_float32(self.value.half_);
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.double_ = (double)self.value.float_;
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNERROR;
    }

    // Handle errors
    if (res.error != GOOD) {
        return res;
    }

    // Recursively promote and return final result
    result final_res = promote_input(res.res, type);
    return final_res;
}

result demote_input(mfloat self, int type) {
    result res;

    // Check inputs
    if (self.type < BOOL || self.type > DOUBLE) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (type < BOOL || type > DOUBLE) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (type > self.type) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    } else if (self.type == type || self.type == BOOL) {
        res.res.value = self.value;
        res.res.type = self.type;
        res.error = GOOD;
        return res;
    }

    // Demote by 1 type
    switch (self.type) {
        case DOUBLE:
            res.res.value.float_ = (float)self.value.double_;
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.half_ = float32_to_float16(self.value.float_);
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case HALF:
            res.res.value.bool_ = ((self.value.half_) & 0x7FFF) != 0;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNERROR;
    }

    // Handle errors
    if (res.error != GOOD) {
        return res;
    }

    // Recursively demote and return final result
    result final_res = demote_input(res.res, type);
    return final_res;
}

result set_input_type(mfloat self, int type) {
    if (self.type == type) {
        result res;
        res.res = self;
        res.error = GOOD;
        return res;
    } else if (type > self.type) {
        return promote_input(self, type);
    } else if (type < self.type) {
        return demote_input(self, type);
    }
    result res;
    res.res.value.float_ = NAN;
    res.res.type = FLOAT;
    res.error = UNKNOWNERROR;
    return res;
}

result* equalise_inputs(mfloat self, mfloat other) {
    result* res = (result*)calloc(2, sizeof(result));

    if (self.type == other.type) {
        res[0].res = self;
        res[0].error = GOOD;
        res[1].res = other;
        res[1].error = GOOD;
    } else if (self.type < other.type) {
        res[0] = promote_input(self, other.type);
        res[1].res = other;
        res[1].error = res[0].error;
    } else if (self.type > other.type) {
        res[1] = promote_input(other, self.type);
        res[0].res = self;
        res[0].error = res[1].error;
    }

    return res;
}

result add_by(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch (self.type) {
        case HALF:
            res.res.value.half_ = f16_add(self.value.half_, other.value.half_);
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.float_ = self.value.float_ + other.value.float_;
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.double_ = self.value.double_ + other.value.double_;
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}
        
result sub_by(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.half_ = f16_sub(self.value.half_, other.value.half_);
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.float_ = self.value.float_ - other.value.float_;
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.double_ = self.value.double_ - other.value.double_;
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}
        
result mult_by(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.half_ = f16_mul(self.value.half_, other.value.half_);
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.float_ = self.value.float_ * other.value.float_;
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.double_ = self.value.double_ * other.value.double_;
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result div_by(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            if (((other.value.half_) & 0x7FFF) == 0) {
                res.res.value.float_ = NAN;
                res.res.type = FLOAT;
                res.error = DIVBY0ERROR;
                break;
            }
            res.res.value.half_ = f16_div(self.value.half_, other.value.half_);
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case FLOAT:
            if (other.value.float_ == 0.0f) {
                res.res.value.float_ = NAN;
                res.res.type = FLOAT;
                res.error = DIVBY0ERROR;
                break;
            }
            res.res.value.float_ = self.value.float_ / other.value.float_;
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case DOUBLE:
            if (other.value.double_ == 0.0) {
                res.res.value.float_ = NAN;
                res.res.type = FLOAT;
                res.error = DIVBY0ERROR;
                break;
            }
            res.res.value.double_ = self.value.double_ / other.value.double_;
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result pow_by(mfloat self, mfloat other) {
    #define CONV_HALF_TO_DOUBLE(mf) (double)float16_to_float32(mf.value.half_)
    #define CONV_DOUBLE_TO_HALF(lf) float32_to_float16((float)lf)
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.half_ = float32_to_float16(powf(float16_to_float32(self.value.half_), float16_to_float32(other.value.half_))); //TODO: TEST
            res.res.type = HALF;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.float_ = powf(self.value.float_, other.value.float_);
            res.res.type = FLOAT;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.double_ = pow(self.value.double_, other.value.double_);
            res.res.type = DOUBLE;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_eq(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_eq(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ == other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ == other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_ne(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_neq(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ != other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ != other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_lt(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_lt(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ < other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ < other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_gt(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_gt(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ > other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ > other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_lte(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_lte(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ <= other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ <= other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

result get_comparison_gte(mfloat self, mfloat other) {
    result res;
    result chk = check_inputs(self, other);
    if (chk.error != GOOD) {
        return chk;
    }
    switch(self.type) {
        case HALF:
            res.res.value.bool_ = f16_gte(self.value.half_, other.value.half_);
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case FLOAT:
            res.res.value.bool_ = self.value.float_ >= other.value.float_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        case DOUBLE:
            res.res.value.bool_ = self.value.double_ >= other.value.double_;
            res.res.type = BOOL;
            res.error = GOOD;
            break;
        default:
            res.res.value.float_ = NAN;
            res.res.type = FLOAT;
            res.error = UNKNOWNTYPEERROR;
    }
    return res;
}

mfloat define_mfloat(fcontainer container, int type) {
    mfloat mft;
    mft.type = type;
    mft.value = container;
    return mft;
}

result mfloat_constant(char str_constant[], int type) {
    result out_constant;
    switch (type) {
        case HALF:
            out_constant.res.value.half_ = str2half(str_constant);
            out_constant.res.type = HALF;
            out_constant.error = GOOD;
            break;
        case FLOAT:
            out_constant.res.value.float_ = str2float(str_constant);
            out_constant.res.type = FLOAT;
            out_constant.error = GOOD;
            break;
        case DOUBLE:
            out_constant.res.value.double_ = str2double(str_constant);
            out_constant.res.type = DOUBLE;
            out_constant.error = GOOD;
            break;
        default:
            out_constant.res.value.float_ = NAN;
            out_constant.res.type = FLOAT;
            out_constant.error = INPUTERROR;
            break;
    }
    return out_constant;
}

#define chk_for_malloc_err(ptr) if (ptr == NULL) {res.table = NULL; res.error = MALLOCERROR; return res;}
#define return_good_table(table_out) res.table = &table_out; res.error = GOOD; return res;
consts_table_res add_constant(mfloat_consts* consts_table, int row_idx, char str_form[]) {
    consts_table_res res;

    // Allocate rows if needed
    if (row_idx+1 > consts_table->no_rows) {
        consts_table->table = realloc(consts_table->table, (row_idx+1) * sizeof(mfloat*));
        chk_for_malloc_err(consts_table->table);
        for (int i = consts_table->no_rows; i < row_idx+1; i++) {
            consts_table->table[i] = (mfloat*)calloc(3, sizeof(mfloat));
            chk_for_malloc_err(consts_table->table[i]);
        }
    }

    consts_table->no_rows = row_idx+1;

    // Add constant
    for (int i=0;i<3;i++) {
        result r_const = mfloat_constant(str_form, i+1);
        if (r_const.error != GOOD) {
            res.table = NULL; 
            res.error = r_const.error;
            return res;
        }
        consts_table->table[row_idx][i] = r_const.res;
    }

    return_good_table(*consts_table);
}

consts_table_res make_consts_table() {
    consts_table_res res;
    res.table = (mfloat_consts*)calloc(1, sizeof(mfloat_consts*));
    chk_for_malloc_err(res.table);
    res.table->no_rows = 1;

    // Allocate memory for the table
    res.table->table = (mfloat**)calloc(1, sizeof(mfloat*));
    chk_for_malloc_err(res.table->table);
    for (int i = 0; i < 2; i++) {
        res.table->table[i] = (mfloat*)calloc(3, sizeof(mfloat));
        chk_for_malloc_err(res.table->table[i]);
    }

    // Initalise the table
    res = add_constant(res.table, 1, STR_ZERO);
    chk_for_malloc_err(res.table);

    // Return the table
    return res;
}

result lookup_const(mfloat_consts constants, int row_idx, int type) {
    result res;
    if (row_idx+1 > constants.no_rows) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = CONSTANTNOTFOUNDERROR;
        return res;
    } else if (type < HALF || type > DOUBLE) {
        res.res.value.float_ = NAN;
        res.res.type = FLOAT;
        res.error = INPUTERROR;
        return res;
    }
    res.res = constants.table[row_idx][type-1];
    res.error = GOOD;
    return res;
}

void conv_d_mfloat_to_d_str(mfloat d, char* buffer) {
    if (isinf(d.value.double_)) {
        if (d.value.double_ > 0.0) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(d.value.double_)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%lf", d.value.double_);
    }
}

void conv_f_mfloat_to_f_str(mfloat f, char* buffer) {
    if (isinf(f.value.float_)) {
        if (f.value.float_ > 0.0f) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (isnan(f.value.float_)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%f", f.value.float_);
    }
}

#define IS_INF(x) (((x) & 0x7FFF) == 0x7C00)
#define IS_NAN(x) (((x) & 0x7FFF) > 0x7C00)
void conv_h_mfloat_to_f_str(mfloat h, char* buffer) {
    if (IS_INF(h.value.half_)) {
        if (f16_gt(h.value.half_, 0x0000)) {
            sprintf(buffer, "+inf");
        } else {
            sprintf(buffer, "-inf");
        }
    } else if (IS_NAN(h.value.half_)) {
        sprintf(buffer, "NaN");
    } else {
        sprintf(buffer, "%.3f", float16_to_float32(h.value.half_));
    }
}

void free_char_ptr(char* buffer) {
    free(buffer);
}

/*
// TEST PROGRAM
int main() {
    // Str numbers
    char num1[] = "25";
    char num2[] = "25";

    fcontainer d1;
    fcontainer d2; 
    d1.double_ = str2double(num1);
    d2.double_ = str2double(num2);
    mfloat wd1 = define_mfloat(d1, DOUBLE);
    mfloat wd2 = define_mfloat(d2, DOUBLE);

    fcontainer f1;
    fcontainer f2; 
    f1.float_ = str2float(num1);
    f2.float_ = str2float(num2);
    mfloat wf1 = define_mfloat(f1, FLOAT);
    mfloat wf2 = define_mfloat(f2, FLOAT);
    
    fcontainer h1;
    fcontainer h2; 
    h1.half_ = str2half(num1);
    h2.half_ = str2half(num2);
    mfloat wh1 = define_mfloat(h1, HALF);
    mfloat wh2 = define_mfloat(h2, HALF);

    result resd = mult_by(wd1, wd2);
    result resf = mult_by(wf1, wf2);
    result resh = mult_by(wh1, wh2);

    char dbuffer[20];
    char fbuffer[20];
    char hbuffer[20];

    conv_d_mfloat_to_d_str(resd.res, dbuffer);
    printf("Double-precision representation: %s\n", dbuffer);

    conv_f_mfloat_to_f_str(resf.res, fbuffer);
    printf("Single-precision representation: %s\n", fbuffer);

    conv_h_mfloat_to_f_str(resh.res, hbuffer);
    printf("Half-precision representation: %s\n", hbuffer);

    // PRINT_RES_AS_F(resf);
    // PRINT_RES_AS_F(resh);
    return 0;
}
*/