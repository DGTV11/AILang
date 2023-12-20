import sys
sys.set_int_max_str_digits(0)

print("Loaded!")

def fib(n: int, i: int, a: float, b: float) -> list:
    tmp: float = 0

    for i in range(n):
        tmp = a + b
        a = b
        b = tmp
    del tmp
    return [n, i, a, b]

print("Result 1 - 10th fibonacci number:")
res1: list = fib(10, 0, 0.0, 1.0)
print(res1[2])

print("Result 2 - 100th fibonacci number:")
res2: list = fib(100, res1[1], res1[2], res1[3])
print(res2[2])
del res1

print("Result 3 - 1000th fibonacci number:")
res3: list = fib(1000, res2[1], res2[2], res2[3])
print(res3[2])
del res2

print("Result 4 - 10000th fibonacci number:")
res4: list = fib(10000, res3[1], res3[2], res3[3])
print(res4[2])
del res3

print("Result 5 - 100000th fibonacci number:")
res5: list = fib(100000, res4[1], res4[2], res4[3])
print(res5[2])
del res4

print("Result 6 - 1000000th fibonacci number:")
res6: list = fib(1000000, res5[1], res5[2], res5[3])
print(res6[2])
del res5

print("Result 7 - 10000000th fibonacci number:")
res7: list = fib(10000000, res6[1], res6[2], res6[3])
print(res7[2])
del res6
del res7