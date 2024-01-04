// clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// DEBUG: clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c'
// TEST: clang -o 'c_lib/random/c_src/random' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg-c-basic-0.9/c_src/pcg_basic.c'

#include "../include/random.h"

//i32
void seed_global_pcgi32(uint64_t seed, uint64_t seq) {
    pcg2_srandom(seed, seq);
}

void seed_local_pcgi32(pcg32_random_t* rng, uint64_t seed, uint64_t seq) {
    pcg32_srandom_r(rng, seed, seq);
    return rng;
}

int32_t gen_global_pcgi32() {
    return pcg32_random();
}

int32_t gen_local_pcgi32(pcg32_random_t* rng) {
    return pcg32_random_r(rng);
}

int32_t bounded_gen_global_pcgu32(uint32_t bound) {
    return pcg32_boundedrand(bound);
}

i32resWboolErr_t bounded_gen_local_pcgi32(pcg32_random_t* rng, int32_t lower_bound, int32_t upper_bound) {
    i32resWboolErr_t res;
    res.has_err = false;

    if (lower_bound > upper_bound) {
        res.has_err = true;
        return res;
    } if (lower_bound == upper_bound) {
        res.n = lower_bound;
        return res;
    }
    return pcg32_boundedrand_r(rng, upper_bound-lower_bound) + lower_bound;
}