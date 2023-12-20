// clang -o '/Volumes/Data stuffs/Python/AILang/c_lib/float16/test/inttest' -mf16c '/Volumes/Data stuffs/Python/AILang/c_lib/float16/test/inttest.c' '/Volumes/Data stuffs/Python/AILang/c_lib/float16/c_src/float16.c'

#include <stdio.h>
#include "../include/float16.h"

int main() {
    printf("3.0h = %d\n", f16_int(0x4200));
    printf("3.004h ~ %d\n", f16_int(0x4202));
    printf("3.5h ~ %d\n", f16_int(0x4300));
}
