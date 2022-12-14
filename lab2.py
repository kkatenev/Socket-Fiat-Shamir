import os
import random
import json
import lab1

file_path = "my_test_file.txt"


def read_file(filename):
    with open(filename, 'rb') as f:
        return bytearray(f.read())


def file_size(status, filename):
    if status != "Успешно":
        return "0 Kb"

    stats = os.stat(filename)
    return str(round(stats.st_size / 1024, 2)) + " Kb"


def result_validation(decode_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        origin_text = f.read()

    with open(decode_path, 'r', encoding='utf-8') as f:
        decode_text = f.read()

    if origin_text == decode_text:
        return True

    return False


def file_read(filename):
    with open(filename, 'rb') as f:
        return bytearray(f.read())


def endcode_file_write(filename, file):
    with open(f'result/{filename}', 'w') as f:
        f.write(str(file))


def decode_file_write(filename, file):
    with open(f'result/{filename}', 'wb') as f:
        f.write(bytearray(file))


def keys_read(path):
    with open(f'{path}/keys.json') as f:
        return json.load(f)


def keys_write(path, keys):
    with open(f'{path}/keys.json', 'w') as f:
        json.dump(keys, f, indent=4)


def get_coprime_numbers(p):
    Cn = lab1.create_prime_number()
    while lab1.my_gcd(p, Cn)[0] != 1:
        Cn = lab1.create_prime_number()
    return Cn


def shamir_encode(origin_file):
    status = "Успешно"
    keys = []
    endcode_file = list()

    try:
        p = lab1.create_prime_number()

        Ca = get_coprime_numbers(p - 1)
        Da = lab1.my_gcd(p - 1, Ca)[2]
        if Da < 0:
            Da += (p - 1)

        Cb = get_coprime_numbers(p - 1)
        Db = lab1.my_gcd(p - 1, Cb)[2]
        if Db < 0:
            Db += (p - 1)

        for part in origin_file:
            x1 = lab1.my_fast_pow(part, Ca, p)
            x2 = lab1.my_fast_pow(x1, Cb, p)
            x3 = lab1.my_fast_pow(x2, Da, p)
            endcode_file.append(x3)

        keys.append({'p': p, 'Ca': Ca, 'Da': Da, 'Cb': Cb, 'Db': Db})

        keys_write("result/Shamir Cipher", keys)

        endcode_file_write("Shamir Cipher/endcode.txt", endcode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return endcode_file, status


def shamir_decode(endcode_file):
    status = "Успешно"
    keys = keys_read("result/Shamir Cipher")
    decode_file = list()

    try:
        for key in keys:
            p = key['p']
            Db = key['Db']

        for part in endcode_file:
            x4 = lab1.my_fast_pow(part, Db, p)
            decode_file.append(x4)

        decode_file_write("Shamir Cipher/decode.txt", decode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return decode_file, status


def elgamal_encode(origin_file):
    status = "Успешно"
    keys = []
    endcode_file = list()

    try:
        g = p = 0

        p_stat = False
        while p_stat == False:
            q = lab1.create_prime_number()
            p = 2 * q + 1
            p_stat = lab1.is_prime(p)

        while lab1.my_fast_pow(g, q, p) != 1:
            g = random.randint(1, p - 1)

        Cb = random.randint(1, p - 1)
        Db = lab1.my_fast_pow(g, Cb, p)

        k = random.randint(1, p - 1)
        r = lab1.my_fast_pow(g, k, p)

        for m in origin_file:
            e = m * lab1.my_fast_pow(Db, k, p)
            endcode_file.append(e)

        keys.append({'g': g, 'p': p, 'Cb': Cb, 'Db': Db, 'k': k, 'r': r})

        keys_write("result/ElGamal Cipher", keys)

        endcode_file_write("ElGamal Cipher/endcode.txt", endcode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return endcode_file, status


def elgamal_decode(endcode_file):
    status = "Успешно"
    keys = keys_read("result/ElGamal Cipher")
    decode_file = list()

    try:
        for key in keys:
            p = key['p']
            Cb = key['Cb']
            r = key['r']

        for e in endcode_file:
            decode_file.append(e * lab1.my_fast_pow(r, p - 1 - Cb, p) % p)

        decode_file_write("ElGamal Cipher/decode.txt", decode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return decode_file, status


def vernam_encode(origin_file):
    status = "Успешно"
    keys = []
    endcode_file = list()

    try:
        for i in range(len(origin_file)):
            code = lab1.random_value()
            endcode_file.append(origin_file[i] ^ code)
            keys.append(code)

        keys_write("result/Vernam Cipher", keys)

        endcode_file_write("Vernam Cipher/endcode.txt", endcode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return endcode_file, status


def vernam_decode(endcode_file):
    status = "Успешно"
    keys = keys_read("result/Vernam Cipher")
    decode_file = list()

    try:
        code = keys

        for i in range(len(endcode_file)):
            decode_file.append(endcode_file[i] ^ code[i])

        decode_file_write("Vernam Cipher/decode.txt", decode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return decode_file, status


def rsa_encode(origin_file):
    status = "Успешно"
    keys = []
    endcode_file = list()

    try:
        p = lab1.create_prime_number()
        q = lab1.create_prime_number()

        n = p * q

        phi = (p - 1) * (q - 1)

        d = get_coprime_numbers(phi)

        c = lab1.my_gcd(d, phi)[1]
        if c < 0:
            c += phi

        for m in origin_file:
            e = lab1.my_fast_pow(m, d, n)
            endcode_file.append(e)

        keys.append({'p': p, 'q': q, 'n': n, 'phi': phi, 'd': d, 'c': c})

        keys_write("result/RSA cipher", keys)

        endcode_file_write("RSA cipher/endcode.txt", endcode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return endcode_file, status


def rsa_decode(endcode_file):
    status = "Успешно"
    keys = keys_read("result/RSA cipher")
    decode_file = list()

    try:
        for key in keys:
            n = key['n']
            c = key['c']

        for e in endcode_file:
            decode_file.append(lab1.my_fast_pow(e, c, n))

        decode_file_write("RSA cipher/decode.txt", decode_file)

    except Exception as ex:
        status = f"Ошибка ({ex})"

    return decode_file, status


def main():
    os.system("cls || clear")
    print(
        "Защита информации. Лабораторная работа №2. Черемисин Михаил Евгеньевич ИА-932. Бубенков Максим Максимович ИА-932")

    origin_file = read_file(file_path)

    print(f"\n\n-------------------------- Настройки ----------------------------")
    print(f"   * Файл для тестирования: {file_path} ({file_size('Успешно', file_path)})")

    print(f"\n\n-------------------------- Шифр Шамира --------------------------")
    f_shamir_endcode, endcode_status = shamir_encode(origin_file)
    f_shamir_decode, decode_status = shamir_decode(f_shamir_endcode)
    print(f"   * Кодирование:   {endcode_status} ({file_size(endcode_status, 'result/Shamir Cipher/endcode.txt')})")
    print(f"   * Декодирование: {decode_status}  ({file_size(decode_status, 'result/Shamir Cipher/decode.txt')})")
    print(f"   * Проверка:      {result_validation('result/Shamir Cipher/decode.txt')}")

    print(f"\n\n------------------------ Шифр Эль-Гамаля ------------------------")
    f_elgamal_endcode, endcode_status = elgamal_encode(origin_file)
    f_elgamal_decode, decode_status = elgamal_decode(f_elgamal_endcode)
    print(f"   * Кодирование:   {endcode_status} ({file_size(endcode_status, 'result/ElGamal Cipher/endcode.txt')})")
    print(f"   * Декодирование: {decode_status}  ({file_size(decode_status, 'result/ElGamal Cipher/decode.txt')})")
    print(f"   * Проверка:      {result_validation('result/ElGamal Cipher/decode.txt')}")

    print(f"\n\n-------------------------- Шифр Вернама -------------------------")
    f_vernam_endcode, endcode_status = vernam_encode(origin_file)
    f_vernam_decode, decode_status = vernam_decode(f_vernam_endcode)
    print(f"   * Кодирование:   {endcode_status} ({file_size(endcode_status, 'result/Vernam Cipher/endcode.txt')})")
    print(f"   * Декодирование: {decode_status}  ({file_size(decode_status, 'result/Vernam Cipher/decode.txt')})")
    print(f"   * Проверка:      {result_validation('result/Vernam Cipher/decode.txt')}")

    print(f"\n\n---------------------------- Шифр RSA ---------------------------")
    f_rsa_endcode, endcode_status = rsa_encode(origin_file)
    f_rsa_decode, decode_status = rsa_decode(f_rsa_endcode)
    print(f"   * Кодирование:   {endcode_status} ({file_size(endcode_status, 'result/RSA cipher/endcode.txt')})")
    print(f"   * Декодирование: {decode_status}  ({file_size(decode_status, 'result/RSA cipher/decode.txt')})")
    print(f"   * Проверка:      {result_validation('result/RSA cipher/decode.txt')}")


if __name__ == '__main__':
    main()