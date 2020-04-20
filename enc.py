import random
from Crypto.Cipher import AES
import string
key = "".join([random.choice(string.ascii_letters) for i in range(16)])
iv = "".join([random.choice(string.ascii_letters) for i in range(16)])
obj = AES.new(key, AES.MODE_CBC, iv)
message = "The answer is no"
ciphertext = obj.encrypt(message)
print(ciphertext)
c = "".join([bin(i)[2:].zfill(8) for i in ciphertext])
print(c)
c1 = []
w = ''
for i in c:
    w += i
    if len(w) == 8:
        c1.append(w)
        w = ""
c1 = [int(i, 2) for i in c1]
t = bytearray(c1)
t = bytes(t)
obj2 = AES.new(key, AES.MODE_CBC, iv)
print(obj2.decrypt(t))
