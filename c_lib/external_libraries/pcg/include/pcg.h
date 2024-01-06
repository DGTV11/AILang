/*
 * PCG Random Number Generation for C.
 *
 * Copyright 2014 Melissa O'Neill <oneill@pcg-random.org>
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * For additional information about the PCG random number generation scheme,
 * including its license and other licensing options, visit
 *
 *     http://www.pcg-random.org
 */

/*
 * This code is derived from the full C implementation, which is in turn
 * derived from the canonical C++ PCG implementation. The C++ version
 * has many additional features and is preferable if you can use C++ in
 * your project.
 */

/*
 * This file was added to an 'include' folder by Daniel Wee to maintain consistency with the rest of c_src
 * This file was renamed to pcg.h
 * Removed unnecessary global pcg functions
 * Added pcg32x2 functions
 * Tweaked formatting
 */

#ifndef PCG_BASIC_H_INCLUDED
#define PCG_BASIC_H_INCLUDED 1

#include <inttypes.h>

#if __cplusplus
extern "C" {
#endif

typedef struct {    // Internals are *Private*.
    uint64_t state; // RNG state.  All values are possible.
    uint64_t inc;   // Controls which RNG sequence (stream) is
                    // selected. Must *always* be odd.
} pcg32_random_t;

typedef struct {
    pcg32_random_t gen[2];
} pcg32x2_random_t;

// If you *must* statically initialize it, here's one.

#define PCG32_INITIALIZER   { 0x853c49e6748fea9bULL, 0xda3e39cb94b95bdbULL }

//* pcg32
// pcg32_srandom_r(rng, initstate, initseq):
//     Seed the rng. Specified in two parts, state initializer and a
//     sequence selection constant (a.k.a. stream id)
void pcg32_srandom_r(pcg32_random_t* rng, uint64_t initstate,
                     uint64_t initseq);

// pcg32_random_r(rng)
//     Generate a uniformly distributed 32-bit random number
uint32_t pcg32_random_r(pcg32_random_t* rng);

// pcg32_boundedrand_r(rng, bound):
//     Generate a uniformly distributed 32-bit random number, r, where 0 <= r < bound
uint32_t pcg32_boundedrand_r(pcg32_random_t* rng, uint32_t bound);

//* pcg32x2
// pcg32x2_srandom_r(rng, seed1, seed2, seq1, seq2):
//     Seed both of the rngs to be tied together. Has two seeds and two sequences.
void pcg32x2_srandom_r(pcg32x2_random_t* rng, uint64_t seed1, uint64_t seed2,
                       uint64_t seq1, uint64_t seq2);

// pcg32x2_random_r(rng)
//     Generate a (hopefully) uniformly distributed 64-bit random number
uint64_t pcg32x2_random_r(pcg32x2_random_t* rng);

// pcg32_boundedrand_r(rng, bound):
//     Generate a (hopefully) uniformly distributed 64-bit random number, r, where 0 <= r < bound
uint64_t pcg32x2_boundedrand_r(pcg32x2_random_t* rng, uint64_t bound);

#if __cplusplus
}
#endif

#endif // PCG_BASIC_H_INCLUDED
