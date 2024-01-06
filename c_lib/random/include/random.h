#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include "../../external_libraries/pcg/include/pcg.h"
#include <stdint.h>
#include <stdbool.h>

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

// Functions
//*i32
void seed_local_pcgi32(pcg32_random_t* rng, uint64_t seed, uint64_t seq);

int32_t gen_local_pcgi32(pcg32_random_t* rng);

i32resWboolErr_t bounded_gen_local_pcgi32(pcg32_random_t* rng, int32_t lower_bound, int32_t upper_bound);