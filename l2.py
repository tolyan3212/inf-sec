from random import randint

def primary(n):
    a = [True] * (n+1)
    i = 2
    if a[i]:
        while i*i <= len(a):
            j = i*i
            while j < len(a):
                a[j] = False
                j += i
            i += 1
    i = len(a) - 1
    while not a[i]:
        i -= 1
    return i


msg_g = 'Генерация числа g:'
msg_p = 'Генерация числа p:'
msg_A = 'Алиса создала число A:'
msg_B = 'Боб создал число B:'

class Alice:
    def __init__(self):
        pass

    def info(self, info, msg):
        if msg == msg_g:
            self.g = info
        if msg == msg_p:
            self.p = info
            self.a = primary(randint(1000, 10000))
            self.A = (self.g**self.a) % self.p
            sendInfo(self.A, msg_A)
        if msg == msg_B:
            self.key = (info**self.a) % self.p

class Bob:
    def __init__(self):
        pass

    def info(self, info, msg):
        if msg == msg_g:
            self.g = info
        if msg == msg_p:
            self.p = info
        if msg == msg_A:
            self.b = primary(randint(1000, 10000))
            self.B = (self.g**self.b) % self.p

            self.key = (info**self.b) % self.p
            sendInfo(self.B, msg_B)

a = Alice()
b = Bob()

def sendInfo(info, msg):
    print(msg, info)
    b.info(info, msg)
    a.info(info, msg)

def main():
    sendInfo(randint(100, 1000), msg_g)
    sendInfo(randint(100, 1000), msg_p)
    print('Ключ Алисы:', a.key)
    print('Ключ Боба:', b.key)
