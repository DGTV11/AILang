// gcc -shared -o '/Volumes/Data stuffs/Python/AILang/builtins/AI.so' -O3 -Xpreprocessor -fopenmp -lomp -fomit-frame-pointer '/Volumes/Data stuffs/Python/AILang/builtins/AI.c'

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <immintrin.h>
#include <omp.h>

void ai_freeM(double **mat, int mrs) {
    for (int i=0; i<mrs; i++) {
        free(mat[i]);
    }
    free(mat);
}

/*
double **d_softmax(double *vecin, double *vecout, int size) {
    
    double **J = calloc(size, sizeof(double *));
    for (int i=0; i<size; i++){
        J[i] = calloc(size, sizeof(double));
    }
    
    #pragma omp parallel for
    for (int x=0; x<size; x++){
        for (int y=0; y<size; y++){
            if (x == y) {
                J[x][y] = vecout[x] * (1 - vecout[x]);
            } else {
                J[x][y] = -vecout[x] * vecout[y];
            }
        }
    }

    return J;
}
*/

double **d_softmax(double *vecin, double *vecout, int size) {

    double **J = calloc(size, sizeof(double *));
    for (int i=0; i<size; i++){
        J[i] = calloc(size, sizeof(double));
    }

    #pragma omp parallel for
    for (int x=0; x<size; x++){
        for (int y=x; y<size; y++){
            if (x == y) {
                J[x][y] = vecout[x] * (1 - vecout[x]);
            } else {
                double val = -vecout[x] * vecout[y];
                J[x][y] = val;
                J[y][x] = val;
            }
        }
    }

    return J;
}
