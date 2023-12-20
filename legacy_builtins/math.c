// gcc -shared -o '/Volumes/Data stuffs/Python/AILang/builtins/math.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer '/Volumes/Data stuffs/Python/AILang/builtins/math.c'
// DEBUG: gcc -shared -o '/Volumes/Data stuffs/Python/AILang/builtins/math.so' -O3 -Xpreprocessor -fopenmp -lomp '/Volumes/Data stuffs/Python/AILang/builtins/math.c'

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <immintrin.h>
#include <omp.h>

double log_b(double v, double base)
{
    if (base == 10.0)
    {
        double log_v = log10(v);
        return log_v;
    } 
    double log_v = log(v) / log(base);
    return log_v;
}

double ln(double v)
{
    double log_v = log(v);
    return log_v;
}

// Vector math

void freeV(double *vec) {
    free(vec);
}

double *addV2V(double *vec1, double *vec2, int size) {
    // Allocate memory for the result array with cache alignment
    const int CACHE_LINE_SIZE = 64;
    double *res;
    int ret = posix_memalign((void **)&res, CACHE_LINE_SIZE, size * sizeof(double));
    if (ret != 0) {
        return NULL;
    }

    // Allocate memory for the result array in parallel
    #pragma omp parallel
    {
        int thread_num = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = (size + num_threads - 1) / num_threads;
        int chunk_start = thread_num * chunk_size;
        int chunk_end = (chunk_start + chunk_size < size) ? chunk_start + chunk_size : size;
        double *chunk_res = res + chunk_start;
        ret = posix_memalign((void **)&chunk_res, CACHE_LINE_SIZE, chunk_size * sizeof(double));
        if (ret != 0) {
            #pragma omp atomic write
            res = NULL;
        }
    }

    if (res == NULL) {
        free(res);
        return NULL;
    }

    // Add the elements of vec1 and vec2 and store the result in res
    #define TILE_SIZE 256
    int tile_size = TILE_SIZE;
    int num_tiles = (size + TILE_SIZE - 1) / TILE_SIZE;
    #pragma omp parallel for schedule(guided) default(none) shared(vec1, vec2, res, size, CACHE_LINE_SIZE) \
        firstprivate(tile_size, num_tiles)
    for (int i = 0; i < num_tiles; i++) {
        int tile_start = i * TILE_SIZE;
        int tile_end = (tile_start + TILE_SIZE < size) ? tile_start + TILE_SIZE : size;
        for (int j = tile_start; j < tile_end; j++) {
            res[j] = vec1[j] + vec2[j];
        }
        // Prefetch the next tile of vec1 and vec2
        int next_tile_start = tile_end;
        int next_tile_end = (next_tile_start + TILE_SIZE < size) ? next_tile_start + TILE_SIZE : size;
        for (int j = next_tile_start; j < next_tile_end; j += CACHE_LINE_SIZE / sizeof(double)) {
            __builtin_prefetch(&vec1[j], 0, 3);
            __builtin_prefetch(&vec2[j], 0, 3);
        }
        // Prefetch the next tile of res
        __builtin_prefetch(&res[next_tile_start], 1, 3); 
    }
    return res;
}

double *subVfV(double *vec1, double *vec2, int size) {
    // Allocate memory for the result array with cache alignment
    const int CACHE_LINE_SIZE = 64;
    double *res;
    int ret = posix_memalign((void **)&res, CACHE_LINE_SIZE, size * sizeof(double));
    if (ret != 0) {
        return NULL;
    }

    // Allocate memory for the result array in parallel
    #pragma omp parallel
    {
        int thread_num = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = (size + num_threads - 1) / num_threads;
        int chunk_start = thread_num * chunk_size;
        int chunk_end = (chunk_start + chunk_size < size) ? chunk_start + chunk_size : size;
        double *chunk_res = res + chunk_start;
        ret = posix_memalign((void **)&chunk_res, CACHE_LINE_SIZE, chunk_size * sizeof(double));
        if (ret != 0) {
            #pragma omp atomic write
            res = NULL;
        }
    }

    if (res == NULL) {
        free(res);
        return NULL;
    }

    // Find diff btwn the elements of vec1 and vec2 and store the result in res
    #define TILE_SIZE 256
    int tile_size = TILE_SIZE;
    int num_tiles = (size + TILE_SIZE - 1) / TILE_SIZE;
    #pragma omp parallel for schedule(guided) default(none) shared(vec1, vec2, res, size, CACHE_LINE_SIZE) \
        firstprivate(tile_size, num_tiles)
    for (int i = 0; i < num_tiles; i++) {
        int tile_start = i * TILE_SIZE;
        int tile_end = (tile_start + TILE_SIZE < size) ? tile_start + TILE_SIZE : size;
        for (int j = tile_start; j < tile_end; j++) {
            res[j] = vec1[j] - vec2[j];
        }
        // Prefetch the next tile of vec1 and vec2
        int next_tile_start = tile_end;
        int next_tile_end = (next_tile_start + TILE_SIZE < size) ? next_tile_start + TILE_SIZE : size;
        for (int j = next_tile_start; j < next_tile_end; j += CACHE_LINE_SIZE / sizeof(double)) {
            __builtin_prefetch(&vec1[j], 0, 3);
            __builtin_prefetch(&vec2[j], 0, 3);
        }
        // Prefetch the next tile of res
        __builtin_prefetch(&res[next_tile_start], 1, 3); 
    }
    return res;
}


double mulVbV(double *vec1, double *vec2, int size) {
    double res = 0.0;

    #pragma omp parallel
    {
        int thread_num = omp_get_thread_num();
        int num_threads = omp_get_num_threads();
        int chunk_size = (size + num_threads - 1) / num_threads;
        int chunk_start = thread_num * chunk_size;
        int chunk_end = (chunk_start + chunk_size < size) ? chunk_start + chunk_size : size;
        double local_res = 0.0;
        for (int i = chunk_start; i < chunk_end; i++) {
            local_res += vec1[i] * vec2[i];
        }
        #pragma omp atomic
        res += local_res;
    }

    return res;
}


double *mulNbV(double num, double *vec, int size) {
    // Allocate memory for the result array with cache alignment
    const int CACHE_LINE_SIZE = 64;
    double *res;
    int ret = posix_memalign((void **)&res, CACHE_LINE_SIZE, size * sizeof(double));
    if (ret != 0) {
        return NULL;
    }

    // Compute scalar multiplication of vec with num
    #define TILE_SIZE 256
    int tile_size = TILE_SIZE;
    int num_tiles = (size + TILE_SIZE - 1) / TILE_SIZE;
    #pragma omp parallel for schedule(guided) default(none) shared(num, vec, res, size, CACHE_LINE_SIZE) \
        firstprivate(tile_size, num_tiles)
    for (int i = 0; i < num_tiles; i++) {
        int tile_start = i * TILE_SIZE;
        int tile_end = (tile_start + TILE_SIZE < size) ? tile_start + TILE_SIZE : size;
        for (int j = tile_start; j < tile_end; j++) {
            res[j] = num * vec[j];
        }
        // Prefetch the next tile of vec
        int next_tile_start = tile_end;
        int next_tile_end = (next_tile_start + TILE_SIZE < size) ? next_tile_start + TILE_SIZE : size;
        for (int j = next_tile_start; j < next_tile_end; j += CACHE_LINE_SIZE / sizeof(double)) {
            __builtin_prefetch(&vec[j], 0, 3);
        }
        // Prefetch the next tile of res
        __builtin_prefetch(&res[next_tile_start], 1, 3); 
    }
    return res;
}

// Matrix math

void freeM(double **mat, int mrs) {
    for (int i=0; i<mrs; i++) {
        free(mat[i]);
    }
    free(mat);
}

/*
double **addM2M(double **mat1, double **mat2, int *md) {
    // Initalise
    int r = md[0];
    int c = md[1];

    // Add
    #pragma omp parallel for
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            mat1[i][j] += mat2[i][j];
        }
    }
    return mat1;
}
*/

double **gettranspose(double **mat, int *md) {
    // Initalise
    int r = md[0];
    int c = md[1];
    double **res;
    res = calloc(r, sizeof(double *));
    for (int i = 0; i < r; i++) {
        res[i] = calloc(c, sizeof(double));
    }

    // Transpose
    #pragma omp parallel for
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            res[j][i] = mat[i][j];
        }
    }

    return res;
}

double **addM2M(double **mat1, double **mat2, int *md) {
    // Initalise
    int r = md[0];
    int c = md[1];
    int cache_line_size = 64;
    int cache_align = cache_line_size / sizeof(double);
    double **res;

    // Allocate memory for result matrix with cache alignment
    /*
    res = malloc(r * sizeof(double *));
    double *data = malloc(r * c * sizeof(double) + cache_line_size);
    double *aligned_data = data + cache_line_size - ((uintptr_t)data % cache_line_size);
    for (int i = 0; i < r; i++) {
        res[i] = aligned_data + i * c;
    }
    */
    res = calloc(r, sizeof(double *));
    double *data = calloc(r * c + cache_align, sizeof(double));
    double *aligned_data = data + cache_align - ((uintptr_t)data % cache_align);
    for (int i = 0; i < r; i++) {
        res[i] = aligned_data + i * c;
    }

    // Add
    #pragma omp parallel for
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            res[i][j] = mat1[i][j] + mat2[i][j];
        }
    }
    free(data);
    return res;
}

double **subMfM(double **mat1, double **mat2, int *md) {
    // Initalise
    int r = md[0];
    int c = md[1];
    int cache_line_size = 64;
    int cache_align = cache_line_size / sizeof(double);
    double **res;

    // Allocate memory for result matrix with cache alignment
    /*
    res = malloc(r * sizeof(double *));
    double *data = malloc(r * c * sizeof(double) + cache_line_size);
    double *aligned_data = data + cache_line_size - ((uintptr_t)data % cache_line_size);
    for (int i = 0; i < r; i++) {
        res[i] = aligned_data + i * c;
    }
    */
    res = calloc(r, sizeof(double *));
    double *data = calloc(r * c + cache_align, sizeof(double));
    double *aligned_data = data + cache_align - ((uintptr_t)data % cache_align);
    for (int i = 0; i < r; i++) {
        res[i] = aligned_data + i * c;
    }

    // Add
    #pragma omp parallel for
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            res[i][j] = mat1[i][j] - mat2[i][j];
        }
    }
    free(data);
    return res;
}


double **mulMbM(double **mat1, double **mat2, int **mds) {
    // Initalise dim sizes
    int m1r = mds[0][0];
    int m1c = mds[0][1];
    int m2r = mds[1][0];
    int m2c = mds[1][1];

    // Initalise res
    double **res = calloc(m1r, sizeof(double *));
    for (int x = 0; x < m1r; x++) {
        res[x] = calloc(m2c, sizeof(double));
    }

    // Multiply
    #pragma omp parallel for
    for (int i=0; i<m1r; i++) {
        for (int j=0; j<m2c; j++) {
            for (int k=0; k<m1c; k++) {
                res[i][j] += mat1[i][k] * mat2[k][j];
            }
        }
    }

    return res;
}

/*
double **mulNbM(double num, double **mat, int *mds) {
    // Initalise dim sizes
    int r = mds[0];
    int c = mds[1];

    // Multiply
    #pragma omp parallel for
    for (int i = 0; i < r; i++) {
        for (int j = 0; j < c; j++) {
            mat[i][j] *= num;
        }
    }

    return mat;
}
*/

double **mulNbM(double num, double **mat, int *mds) {
    // Initalise dim sizes
    int r = mds[0];
    int c = mds[1];

    // Allocate memory for the resulting matrix
    double **result = malloc(r * sizeof(double*));
    int i, j;
    for (i = 0; i < r; i++) {
        posix_memalign((void **)&result[i], 64, c * sizeof(double));
        memcpy(result[i], mat[i], c * sizeof(double));
    }

    // Multiply using loop tiling
    int tile_size = 32;
    int ii, jj, k;
    #pragma omp parallel for private(ii, jj, k)
    for (i = 0; i < r; i += tile_size) {
        for (j = 0; j < c; j += tile_size) {
            for (ii = i; ii < i + tile_size && ii < r; ii++) {
                for (jj = j; jj < j + tile_size && jj < c; jj++) {
                    result[ii][jj] *= num;
                }
            }
        }
    }

    return result;
}