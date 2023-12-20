import sys
sys.set_int_max_str_digits(0)

print("Loaded!")

def fib(n: int) -> float:
    tmp: float  = 0.0
    a: float    = 0.0
    b: float    = 1.0

    for i in range(n):
        tmp = a + b
        a = b
        b = tmp
    del tmp
    return a

print("10000000th fibonacci number:")
res: float = fib(10000000)
print(res)
del res