#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include "../../external_libraries/pcg/include/pcg.h"
#include <stdint.h>
#include <stdbool.h>
#include <limits.h>

// Macros
#define UINT64_TO_DOUBLE_01_MASK 0x3FEFFFFFFFFFFFFFULL
#define DOUBLE_UINT64_MAX 0x43F0000000000000

#define REINTERPRET_CAST(tgt_type, value) *(tgt_type*)&value
#define FLOAT16_TO_FLOAT32(x) float16_to_float32(x)
#define FLOAT32_TO_FLOAT16(x) float32_to_float16(x)
#define FLOAT16_TO_FLOAT64(x) (float64_t)float16_to_float32((x))
#define FLOAT64_TO_FLOAT16(x) float32_to_float16((float32_t)(x))

// Typedefs
typedef float   float32_t;
typedef double  float64_t;

// Structs
typedef struct {
    int32_t n;
    bool has_err;
} i32resWboolErr_t;

typedef struct {
    int64_t n;
    bool has_err;
} i64resWboolErr_t;

typedef struct {
    float16_t n;
    bool has_err;
} f16resWboolErr_t;

typedef struct {
    float32_t n;
    bool has_err;
} f32resWboolErr_t;

typedef struct {
    float64_t n;
    bool has_err;
} f64resWboolErr_t;

// Functions
//*i32
void seed_local_pcgi32(pcg32_random_t* rng, uint64_t seed, uint64_t seq);
int32_t gen_local_pcgi32(pcg32_random_t* rng);
i32resWboolErr_t bounded_gen_local_pcgi32(pcg32_random_t* rng, int32_t lower_bound, int32_t upper_bound);

//*i64
void seed_local_pcgi64(pcg32x2_random_t* rng, uint64_t seed1, uint64_t seed2, uint64_t seq1, uint64_t seq2);
int64_t gen_local_pcgi64(pcg32x2_random_t* rng);
i64resWboolErr_t bounded_gen_local_pcgi64(pcg32x2_random_t* rng, int64_t lower_bound, int64_t upper_bound);

//*f16
float16_t gen_local_pcgf16(pcg32x2_random_t* rng);
f16resWboolErr_t bounded_gen_local_pcgf16(pcg32x2_random_t* rng, float16_t lower_bound, float16_t upper_bound);

//*f32
float32_t gen_local_pcgf32(pcg32x2_random_t* rng);
f32resWboolErr_t bounded_gen_local_pcgf32(pcg32x2_random_t* rng, float32_t lower_bound, float32_t upper_bound);

//*f64
float64_t gen_local_pcgf64(pcg32x2_random_t* rng);
f64resWboolErr_t bounded_gen_local_pcgf64(pcg32x2_random_t* rng, float64_t lower_bound, float64_t upper_bound);