// clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// DEBUG: clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// TEST: clang -o 'c_lib/random/c_src/random' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg-c-basic-0.9/c_src/pcg_basic.c'

#include "../include/random.h"

void seed_global_pcgu32(uint64_t seed, uint64_t seq) {
    pcg2_srandom(seed, seq);
}

void seed_local_pcgu32(pcg32_random_t* rng, uint64_t seed, uint64_t seq) {
    pcg32_srandom_r(rng, seed, seq);
    return rng;
}

uint32_t gen_global_pcgu32() {
    return pcg32_random();
}

uint32_t gen_local_pcgu32(pcg32_random_t* rng) {
    return pcg32_random_r(rng);
}

uint32_t bounded_gen_global_pcgu32(uint32_t bound) {
    return pcg32_boundedrand(bound);
}

uint32_t bounded_gen_local_pcgu32(pcg32_random_t* rng, uint32_t bound) {
    return pcg32_boundedrand_r(rng, bound);
}