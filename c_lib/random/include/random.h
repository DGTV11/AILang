#include "../../external_libraries/float16/include/float16.h"
#include "../../external_libraries/float16/c_src/conv.h"
#include "../../external_libraries/pcg-c-basic-0.9/include/pcg_basic.h"
#include <stdint.h>

// Typedefs
typedef float   float32_t;
typedef double  float64_t;

// Functions
//*u32
void seed_global_pcgu32(uint64_t seed, uint64_t seq);
void seed_local_pcgu32(pcg32_random_t* rng, uint64_t seed, uint64_t seq);

uint32_t gen_global_pcgu32();
uint32_t gen_local_pcgu32(pcg32_random_t* rng);

uint32_t bounded_gen_global_pcgu32(uint32_t bound);
uint32_t bounded_gen_local_pcgu32(pcg32_random_t* rng, uint32_t bound);