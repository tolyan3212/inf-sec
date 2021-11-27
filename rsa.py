import random
import math
from time import time


def checkIfPrime(n):
    if n <= 5:
        if n in [1, 2, 3, 5]:
            return True
        return False
    if (n % 2 == 0):
        return False
    temp = n-1
    s = 0
    while (temp % 2 == 0):
        temp /= 2
        s += 1
    d = int((n-1) / (2**s))
    for i in range(5):
        a = random.randint(1, 50 if n > 50 else (n-1))
        x = pow(a, d, n)
        c = False
        if x == 1:
            c = True
        if not c:
            for r in range(s - 1):
                if x == n - 1:
                    c = True
                    break
                x = pow(x, 2, n)
            if x == n - 1:
                c = True
        if not c:
            # print('a', a,', d', d)
            return False
    return True
    

def primary(startFrom):
    while not checkIfPrime(startFrom):
        startFrom += 1
    return startFrom


f = []
primes = []
res = []
def test():
    global f, primes, res
    p = None
    with open('primes.txt') as f:
        p = eval(f.read())
    f = []
    for i in range(5, p[-1]):
        if checkIfPrime(i) and not i in p:
            f.append(i)

    primes = p
    res = []
    for i in range(5, p[-1] + 1):
        if checkIfPrime(i):
            res.append(i)
            


bob_msg = 'hello'
msg_public_key = 'Алиса публикует открытый ключ: (e, n) ='
msg_bob_encoded = 'Боб отправляет зашифрованное сообщение:'

def sendInfo(msg, data):
    print(msg, data)
    a.accept_info(msg, data)
    b.accept_info(msg, data)

class Alice:
    def __inif__(self):
        pass

    def accept_info(self, msg, data):
        if msg == msg_bob_encoded:
            message = self.decode_message(data)
            print('Алиса расшифровала сообщение:', message)

    def generateKeys(self):
        p = primary(random.randint(20, 100))
        q = primary(random.randint(20, 100))
        n = p*q
        phi = (p-1)*(q-1)
        e = primary(random.randint(5, phi))
        while e >= phi:
            e = primary(random.randint(5, phi))

        d = 5
        while (d * e) % phi != 1:
            d += 1

        self.private_key = (d, n)
        print('Закрытый ключ Алисы:', (d, n))
        sendInfo(msg_public_key, (e, n))

    def decode_message(self, data):
        msg = [
            chr(pow(c, self.private_key[0], self.private_key[1]))
            for c in data
        ]
        return ''.join(msg)

class Bob:
    def __init__(self):
        pass

    def accept_info(self, msg, data):
        if msg == msg_public_key:
            self.public_key = data
            print('Боб хочет отправить сообщение:', bob_msg)
            message = self.encode_message(bob_msg)
            sendInfo(msg_bob_encoded, message)
            

    def encode_message(self, message):
        m = [ord(c) for c in message]
        encoded_message = [
            pow(a, self.public_key[0], self.public_key[1])
            for a in m
        ]
        return encoded_message

a = Alice()
b = Bob()

a.generateKeys()
