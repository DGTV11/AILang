#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

//Types: double, float (single), half
typedef short half;

enum err {GOOD, DIVBY0ERROR, TYPEINEQERROR, UNKNOWNTYPEERROR, INPUTERROR, MALLOCERROR, RTERROR, CONSTANTNOTFOUNDERROR, UNKNOWNERROR};
enum types {BOOL, HALF, FLOAT, DOUBLE};

typedef union multi_float_container {
    bool bool_;
    half half_;
    float float_;
    double double_;
} fcontainer;

typedef struct multi_float {
    fcontainer value;
    int type;
} mfloat;

typedef struct result_container {
    mfloat res;
    int error;
} result;

enum const_idxes {ZERO_IDX, PI_IDX, E_IDX, LN2_IDX, LN10_IDX};
char STR_ZERO[]     = "0.000000000000000000000000";
char* ret_str_zero()     {return STR_ZERO;}
char STR_PI[]       = "3.141592653589793238462643";
char* ret_str_pi()       {return STR_PI;}
char STR_E[]        = "2.718281828459045235360287";
char* ret_str_e()        {return STR_E;}
char STR_LN2[]      = "0.693147180559945309417232";
char* ret_str_ln2()      {return STR_LN2;}
char STR_LN10[]     = "2.302585092994045684017991";
char* ret_str_ln10()     {return STR_LN10;}

typedef struct consts_lookup_table {
    mfloat** table;
    int no_rows;
} mfloat_consts;

typedef struct consts_lookup_table_and_error_wrapper {
    mfloat_consts* table;
    int error;
} consts_table_res;

result      check_inputs(mfloat self, mfloat other);
result      promote_input(mfloat self, int type);
result      demote_input(mfloat self, int type);
result      set_input_type(mfloat self, int type);
result*     equalise_inputs(mfloat self, mfloat other);
result      add_by(mfloat self, mfloat other);
result      sub_by(mfloat self, mfloat other);
result      mult_by(mfloat self, mfloat other);
result      div_by(mfloat self, mfloat other);
result      pow_by(mfloat self, mfloat other);
result      get_comparison_eq(mfloat self, mfloat other);
result      get_comparison_ne(mfloat self, mfloat other);
result      get_comparison_lt(mfloat self, mfloat other);
result      get_comparison_gt(mfloat self, mfloat other);
result      get_comparison_lte(mfloat self, mfloat other);
result      get_comparison_gte(mfloat self, mfloat other);