import math
from Crypto.Cipher import AES
import cv2
import numpy as np
import pywt

def read_key_and_iv(key_file, iv_file):
    with open(key_file, 'r') as f:
        key = f.readline()
    with open(iv_file, 'r') as f:
        iv = f.readline()
    return key, iv

def decrypt_message(ciphertext, key, iv):
    message = []
    character = ''
    for i in ciphertext:
        character += i
        if len(character) == 8:
            message.append(character)
            character = ""
    message = [int(i, 2) for i in message]
    message = bytearray(message)
    message = bytes(message)
    obj = AES.new(key, AES.MODE_CBC, iv)
    return(obj.decrypt(message))

def decrypt(image):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    H = np.load('H.npy')
    img = img + H
    coeffs2 = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs2
    result = []
    result.append(LL)
    result.append(LH)
    result.append(HL)
    result.append(HH)
    for i in range(len(result)):
        result[i] = result[i].tolist()
    for i in range(len(result)):
        for j in range(len(result[i])):
            for k in range(len(result[i][j])):
                result[i][j][k] = round(result[i][j][k])
                result[i][j][k] = bin(result[i][j][k]).replace('0b', "").zfill(8)
    rows = len(result[1])
    num = len(result[1][1])
    index = 0
    ciphertext = ''
    for j in range(rows):
        for k in range(num):
            for i in range(1,4):
                ciphertext += result[i][j][k][-1]
                if len(ciphertext) == 128:
                    return ciphertext
                

def main():
    key, iv = read_key_and_iv('key.txt', 'iv.txt')
    ciphertext = decrypt('result.png')
    message = decrypt_message(ciphertext, key, iv)
    print(message)

if __name__ == '__main__':
    main()
