import socket
import random
import lab1

sock = socket.socket()
sock.connect(('localhost', 1080))

q = 0
p = 0


status = False
while status == False:
    q = lab1.create_prime_number()
    p = 2 * q + 1
    status = lab1.is_prime(p)

n = p * q
print('n =', n)
sock.send(str(n).encode())
print('отправил n')

s = random.randint(1, n-1)
while lab1.my_gcd(s, n)[0] != 1:
    s = random.randint(1, n-1)

v = lab1.my_fast_pow(s, 2, n)
sock.send(str(v).encode())
print('отправил V')
print(f's = {s}\nV = {v}')

rounds = 30
for i in range(rounds):
    print('________________________________')
    print(f'START OF ROUND {i + 1}')
    r = random.randint(1, n - 1)
    x = lab1.my_fast_pow(r, 2, n)
    print('x = ', x)
    sock.send(str(x).encode())
    print('отправил x = ', x)
    str_e = sock.recv(1024)
    print('принял e')
    e = random.randint(0, 1)
    print(f'r = {r}\nx = {x}')
    print('n = ', n)
    print('e =', e)
    if e == 0:
        y = r
    else:
        r_mod_n = r % n
        s_e_mod_n = lab1.my_fast_pow(s, e, n)
        y = r_mod_n * s_e_mod_n

    sock.send(str(y).encode())
    print('отправил y')

    message_from_server = sock.recv(1024)
    print(message_from_server.decode('utf-8'))
sock.close()