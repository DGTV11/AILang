// clang -shared -o 'c_lib/random/lib/random.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'
// DEBUG: clang -shared -o 'c_lib/random/lib/random.so' -O3 -Xpreprocessor -fopenmp -lomp -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'
// TEST: clang -o 'c_lib/random/lib/random' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer -mf16c 'c_lib/random/c_src/random.c' 'c_lib/external_libraries/float16/c_src/float16.c' 'c_lib/external_libraries/pcg/c_src/pcg.c'

#include "../include/random.h"

// Integer RNGs
//*i32
void seed_local_pcgi32(pcg32_random_t *rng, uint64_t seed, uint64_t seq)
{
    pcg32_srandom_r(rng, seed, seq);
}

int32_t gen_local_pcgi32(pcg32_random_t *rng)
{
    return pcg32_random_r(rng);
}

i32resWboolErr_t bounded_gen_local_pcgi32(pcg32_random_t *rng, int32_t lower_bound, int32_t upper_bound)
{
    i32resWboolErr_t res;
    res.has_err = false;

    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }
    res.n = (int32_t)pcg32_boundedrand_r(rng, upper_bound - lower_bound) + lower_bound; // TODO: TEST!
    return res;
}

//*i64
void seed_local_pcgi64(pcg32x2_random_t *rng, uint64_t seed1, uint64_t seed2, uint64_t seq1, uint64_t seq2)
{
    pcg32x2_srandom_r(rng, seed1, seed2, seq1, seq2);
}

int64_t gen_local_pcgi64(pcg32x2_random_t *rng)
{
    return pcg32x2_random_r(rng);
}

i64resWboolErr_t bounded_gen_local_pcgi64(pcg32x2_random_t *rng, int64_t lower_bound, int64_t upper_bound)
{
    i64resWboolErr_t res;
    res.has_err = false;

    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }
    res.n = (int64_t)pcg32x2_boundedrand_r(rng, upper_bound - lower_bound) + lower_bound; // TODO: TEST!
    return res;
}

// Float RNGs (see https://stackoverflow.com/questions/48228749/random-number-generator-pcg-library-how-to-generate-float-numbers-set-within-a, https://stackoverflow.com/questions/52147419/how-to-convert-random-uint64-t-to-random-double-in-range-0-1-using-bit-wise-o)
//*f16
float16_t gen_local_pcgf16_rng32x2(pcg32x2_random_t *rng)
{
    uint64_t u64_preprocessed = UINT64_TO_DOUBLE_01_MASK | ((pcg32x2_random_r(rng) >> 12) | 1);
    return FLOAT64_TO_FLOAT16((REINTERPRET_CAST(float64_t, u64_preprocessed) - 1.0));
}

f16resWboolErr_t bounded_gen_local_pcgf16_rng32x2(pcg32x2_random_t *rng, float16_t lower_bound, float16_t upper_bound)
{
    f16resWboolErr_t res;
    res.has_err = false;
    if (f16_gt(lower_bound, upper_bound))
    {
        res.has_err = true;
        return res;
    }
    else if (f16_eq(lower_bound, upper_bound))
    {
        res.n = lower_bound;
        return res;
    }

    float64_t f64_preprocessed = (float64_t)(pcg32x2_random_r(rng)) / (DOUBLE_UINT64_MAX)*FLOAT16_TO_FLOAT64(f16_sub(upper_bound, lower_bound)) + lower_bound;
    res.n = FLOAT64_TO_FLOAT16(f64_preprocessed);
    return res;
}

float16_t gen_local_pcgf16_rng32(pcg32_random_t *rng)
{
    uint32_t u32_preprocessed = UINT32_TO_SINGLE_01_MASK | ((pcg32_random_r(rng) >> 9) | 1);
    return FLOAT32_TO_FLOAT16((REINTERPRET_CAST(float32_t, u32_preprocessed) - 1.0f));
}

f16resWboolErr_t bounded_gen_local_pcgf16_rng32(pcg32_random_t *rng, float16_t lower_bound, float16_t upper_bound)
{
    f16resWboolErr_t res;
    res.has_err = false;
    if (f16_gt(lower_bound, upper_bound))
    {
        res.has_err = true;
        return res;
    }
    else if (f16_eq(lower_bound, upper_bound))
    {
        res.n = lower_bound;
        return res;
    }

    float32_t f32_preprocessed = (float32_t)(pcg32_random_r(rng)) / (SINGLE_UINT32_MAX)*FLOAT16_TO_FLOAT32(f16_sub(upper_bound, lower_bound)) + lower_bound;
    res.n = FLOAT32_TO_FLOAT16(f32_preprocessed);
    return res;
}

//*f32
float32_t gen_local_pcgf32_rng32x2(pcg32x2_random_t *rng)
{
    uint64_t u64_preprocessed = UINT64_TO_DOUBLE_01_MASK | ((pcg32x2_random_r(rng) >> 12) | 1);
    return (float32_t)(REINTERPRET_CAST(float64_t, u64_preprocessed) - 1.0);
}

f32resWboolErr_t bounded_gen_local_pcgf32_rng32x2(pcg32x2_random_t *rng, float32_t lower_bound, float32_t upper_bound)
{
    f32resWboolErr_t res;
    res.has_err = false;
    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }

    float64_t f64_preprocessed = (float64_t)(pcg32x2_random_r(rng)) / (DOUBLE_UINT64_MAX) * ((float64_t)(upper_bound - lower_bound)) + lower_bound;
    res.n = (float32_t)f64_preprocessed;
    return res;
}

float32_t gen_local_pcgf32_rng32(pcg32_random_t *rng)
{
    uint32_t u32_preprocessed = UINT32_TO_SINGLE_01_MASK | ((pcg32_random_r(rng) >> 9) | 1);
    return REINTERPRET_CAST(float32_t, u32_preprocessed) - 1.0f;
}

f32resWboolErr_t bounded_gen_local_pcgf32_rng32(pcg32_random_t *rng, float32_t lower_bound, float32_t upper_bound)
{
    f32resWboolErr_t res;
    res.has_err = false;
    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }

    float32_t f32_preprocessed = (float32_t)(pcg32_random_r(rng)) / (SINGLE_UINT32_MAX) * (upper_bound - lower_bound) + lower_bound;
    res.n = f32_preprocessed;
    return res;
}

//*f64
float64_t gen_local_pcgf64_rng32x2(pcg32x2_random_t *rng)
{
    uint64_t u64_preprocessed = UINT64_TO_DOUBLE_01_MASK | ((pcg32x2_random_r(rng) >> 12) | 1);
    return REINTERPRET_CAST(float64_t, u64_preprocessed) - 1.0;
}

f64resWboolErr_t bounded_gen_local_pcgf64_rng32x2(pcg32x2_random_t *rng, float64_t lower_bound, float64_t upper_bound)
{
    f64resWboolErr_t res;
    res.has_err = false;
    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }

    float64_t f64_preprocessed = (float64_t)(pcg32x2_random_r(rng)) / ((float64_t)UINT64_MAX) * (upper_bound - lower_bound) + lower_bound;
    res.n = f64_preprocessed;
    return res;
}

float64_t gen_local_pcgf64_rng32(pcg32_random_t *rng)
{
    uint32_t u32_preprocessed = UINT32_TO_SINGLE_01_MASK | ((pcg32_random_r(rng) >> 9) | 1);
    return (float64_t)(REINTERPRET_CAST(float32_t, u32_preprocessed) - 1.0f);
}

f64resWboolErr_t bounded_gen_local_pcgf64_rng32(pcg32_random_t *rng, float64_t lower_bound, float64_t upper_bound)
{
    f64resWboolErr_t res;
    res.has_err = false;
    if (lower_bound > upper_bound)
    {
        res.has_err = true;
        return res;
    }
    else if (lower_bound == upper_bound)
    {
        res.n = lower_bound;
        return res;
    }

    float32_t f32_preprocessed = (float32_t)(pcg32_random_r(rng)) / (SINGLE_UINT32_MAX) * (upper_bound - lower_bound) + lower_bound;
    res.n = (float64_t)f32_preprocessed;
    return res;
}