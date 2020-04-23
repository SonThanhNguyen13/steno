import argparse
import time
from Crypto.Cipher import AES
import cv2
import numpy as np
import pywt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required='True', help='Stenography image')
parser.add_argument('-k', '--key', required='True', help='AES key')
parser.add_argument('-v', '--iv', required='True', help='Initialization vector for AES')
parser.add_argument('-m', '--matrix', required = 'True', help='Difference Matrix ')
parser.add_argument('-l', '--length', required = 'True', help='Message Length')
args = parser.parse_args()

def read_key_and_iv(key_file, iv_file):
    with open(key_file, 'rb') as f:
        key = f.readline()
    with open(iv_file, 'rb') as f:
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
    obj = AES.new(key, AES.MODE_CBC, iv=iv)
    return(obj.decrypt(message))

def decrypt(image, matrix, length):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    H = np.load(matrix)
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
                if len(ciphertext) == length * 8:
                    return ciphertext

def read_msg_length(file):
    with open(file, 'r') as f:
        msg_len = f.readline()
        return int(msg_len)

def main():
    start = time.time()
    key, iv = read_key_and_iv(args.key, args.iv)
    length = read_msg_length(args.length)
    ciphertext = decrypt(args.image, args.matrix, length)
    message = decrypt_message(ciphertext, key, iv)
    print(message)
    end = time.time()
    print("Decrypt message in: {:.2f} s".format(end - start))

if __name__ == '__main__':
    main()
