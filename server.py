import random
import socket
import lab1


sock = socket.socket()
sock.bind(('localhost', 8080))
sock.listen(5)
conn, addr = sock.accept()
print('connected: ', addr)


n_str = conn.recv(1024).decode()
n = int(n_str)
print('n = ', n)

v_str = conn.recv(1024)
v = int(v_str)
print('v = ', v)
round_ = 0

while True:
    round_ += 1
    print('______________________')
    print('Round №', round_)
    x_str = conn.recv(1024).decode()
    print('Принял X')
    x = int(x_str)
    print('x = ', x)
    e = random.randint(0, 1)
    conn.send(str(e).encode())
    print('e = ', int(e))
    y = int(conn.recv(1024))
    print('y от клиента = ', y)

    if y == 0:
        print(False)
        break
    y2 = lab1.my_fast_pow(y, 2, n)
    print('-y**2 = ', y2)

    x_mod_n = x % n
    v_e_mod_n = lab1.my_fast_pow(v, e, n)
    checking = (x_mod_n * v_e_mod_n) % n
    print('-Проверка = ', checking)
    print('Закончен раунд №', round_)
    if int(y2) == int(checking) and round_ == 30:
        message_done = 'Конец\nАвторизация прошла успешно'
        print(message_done)
        conn.send(message_done.encode())
        break

    if int(y2) == int(checking):
        message_round_ok = 'Раунд успешно пройден'
        print(message_round_ok)
        conn.send(message_round_ok.encode())

    if int(y2) != int(checking):
        message_fail = 'Конец\nАвторизация не прошла'
        print(message_fail)
        conn.send(message_fail.encode())
        break

conn.close()
