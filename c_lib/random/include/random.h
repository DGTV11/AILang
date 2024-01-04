#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include "../../external_libraries/pcg-c-basic-0.9/include/pcg_basic.h"
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

// Functions
//*i32
void seed_global_pcgi32(uint64_t seed, uint64_t seq);
void seed_local_pcgi32(pcg32_random_t* rng, uint64_t seed, uint64_t seq);

int32_t gen_global_pcgi32();
int32_t gen_local_pcgi32(pcg32_random_t* rng);

int32_t bounded_gen_global_pcgi32(uint32_t bound);
int32_t bounded_gen_local_pcgi32(pcg32_random_t* rng, uint32_t bound);