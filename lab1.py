from math import sqrt
import random
import os

RANDOM_MIN_NUM = 0
RANDOM_MAX_NUM = 10
RANDOM_DEGREE = 9


def random_value():
    return random.randint(RANDOM_MIN_NUM, RANDOM_MAX_NUM ** RANDOM_DEGREE)


def my_fast_pow(num, degree, module):
    bin_num = degree
    bin_str = ""

    while bin_num > 0:
        bin_str = bin_str + str(bin_num % 2)
        bin_num = bin_num // 2

    y = 1
    s = num

    for val in bin_str:
        if val == "1":
            y = y * s % module
        s = s * s % module
    return y


def my_gcd(a, b):
    u = [a, 1, 0]
    v = [b, 0, 1]
    while v[0] != 0:
        q = u[0] // v[0]
        t = [u[0] % v[0], u[1] - q * v[1], u[2] - q * v[2]]
        u, v = v, t
    return u


def create_prime_number():
    while True:
        p = random.randint(RANDOM_MIN_NUM, RANDOM_MAX_NUM ** RANDOM_DEGREE)
        if is_prime(p):
            return p


def is_prime(num):
    for n in range(2,int(num**0.5)+1):
        if num%n==0:
            return False
    return True


def my_DH():
    status = False
    while status == False:
        q = create_prime_number()
        p = 2 * q + 1
        status = is_prime(p)

    g = random.randint(1, p - 1)
    while my_fast_pow(g, q, p) == 1:
        g = random.randint(1, p - 1)

    X = [0, 0]
    Y = [0, 0]
    Z = [0, 0]

    X[0] = 0
    X[1] = 0

    while X[0] == X[1]:
        X[0] = random.randint(1, p - 1)
        X[1] = random.randint(1, p - 1)

    for i in range(len(X)):
        Y[i] = my_fast_pow(g, X[i], p)

    Z[0] = my_fast_pow(Y[1], X[0], p)
    Z[1] = my_fast_pow(Y[0], X[1], p)

    return Z


def my_big_step_small_step(a, p, y):
    if p <= y or p <= a:
        return f"Числа a и b должны быть меньше p!"

    k = m = int(sqrt(p)) + 1
    if m * k <= p:
        return f"Не выполняется условие m({m}) * k({k}) > p({p})"

    small = []
    X = []

    for i in range(m):
        small.append((my_fast_pow(y, 1, p) * my_fast_pow(a, i, p)) % p)

    for i in range(1, k + 1):
        try:
            big = my_fast_pow(a, i * m, p)
            j = small.index(big)
            X.append((i) * m - j)
        except:
            continue

    if X == []:
        X = "Решения для указанных данных не существует"

    return X


def main():
    os.system("cls || clear")
    print(
        "Защита информации. Лабораторная работа №1. Черемисин Михаил Евгеньевич ИА-932. Бубенков Максим Максимович ИА-932\n\n")
    a = random_value()
    b = random_value()
    c = random_value()
    p = create_prime_number()

    while a >= p or b >= p:
        a = random_value()
        b = random_value()

    FAST_POW = my_fast_pow(a, b, c)
    print(f"[1] Быстрое возведение в степень по модулю ({a} ^ {b} % {c}):")
    print(f"    Решение: {FAST_POW}\n\n")

    if b > a:
        a, b = b, a

    GCD = my_gcd(a, b)
    print(f"[2] Обобщенный алгоритм Евклида (qcd({a},{b})):")
    print(f"    Решение: {GCD[0]}")
    if b > a:
        print(f"    Проверка: {b * GCD[1] + a * GCD[2] == GCD[0]}\n\n")
    else:
        print(f"    Проверка: {a * GCD[1] + b * GCD[2] == GCD[0]}\n\n")

    DH = my_DH()
    print(f"[3] Алгоритм Диффи-Хеллмана:")
    print(f"    Решение: {DH}")
    print(f"    Проверка: {DH[0] == DH[1]}\n\n")

    BIG_SMALL = my_big_step_small_step(a, p, b)
    print(f"[4] Алгоритм шаг младенца - шаг великана ({a} ^ x % {p} = {b}):")
    print(f"    Решение: {BIG_SMALL}")
    if BIG_SMALL != "Решения для указанных данных не существует":
        for degree in BIG_SMALL:
            print(f"    Проверка: {my_fast_pow(a, degree, p) == b}")


if __name__ == "__main__":
    main()