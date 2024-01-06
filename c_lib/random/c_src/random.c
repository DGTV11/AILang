// clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'
// DEBUG: clang -shared -o 'c_lib/random/c_src/random.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'
// TEST: clang -o 'c_lib/random/c_src/random' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'

#include "../include/random.h"

//*i32
void seed_local_pcgi32(pcg32_random_t* rng, uint64_t seed, uint64_t seq) {
    pcg32_srandom_r(rng, seed, seq);
}

int32_t gen_local_pcgi32(pcg32_random_t* rng) {
    return pcg32_random_r(rng);
}

i32resWboolErr_t bounded_gen_local_pcgi32(pcg32_random_t* rng, int32_t lower_bound, int32_t upper_bound) {
    i32resWboolErr_t res;
    res.has_err = false;

    if (lower_bound > upper_bound) {
        res.has_err = true;
        return res;
    } else if (lower_bound == upper_bound) {
        res.n = lower_bound;
        return res;
    }
    res.n = (int32_t)pcg32_boundedrand_r(rng, upper_bound-lower_bound) + lower_bound; //TODO: TEST!
    return res;
}

//*i64
void seed_local_pcgi64(pcg32x2_random_t* rng, uint64_t seed1, uint64_t seed2, uint64_t seq1, uint64_t seq2) {
    pcg32x2_srandom_r(rng, seed, seq);
}

int64_t gen_local_pcgi64(pcg32x2_random_t* rng) {
    return pcg32z2_random_r(rng);
}

i64resWboolErr_t bounded_gen_local_pcgi64(pcg32x2_random_t* rng, int64_t lower_bound, int64_t upper_bound) {
    i64resWboolErr_t res;
    res.has_err = false;

    if (lower_bound > upper_bound) {
        res.has_err = true;
        return res;
    } else if (lower_bound == upper_bound) {
        res.n = lower_bound;
        return res;
    }
    res.n = (int64_t)pcg32x2_boundedrand_r(rng, upper_bound-lower_bound) + lower_bound; //TODO: TEST!
    return res;
}