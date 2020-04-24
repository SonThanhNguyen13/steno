import argparse
import time
import math
from Crypto.Cipher import AES
import cv2
import numpy as np
import pywt
from PIL import Image

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required='True', help='Image')
parser.add_argument('-k', '--key', required='True', help='AES key')
parser.add_argument('-v', '--iv', required='True', help='AES initilization vector')
parser.add_argument('-s', '--save', default='result', help = 'Result dir')
args = parser.parse_args()

def read_key_and_iv(key_file, iv_file):
    with open(key_file, 'r') as f:
        key = f.readline()
    with open(iv_file, 'r') as f:
        iv = f.readline()
    return key, iv

def encrypt_message(message, key, iv):
    key = bytes(key, 'utf-8')
    iv = bytes(iv, 'utf-8')
    message = bytes(message, 'utf-8')
    obj = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = obj.encrypt(message)
    ciphertext = "".join([bin(i)[2:].zfill(8) for i in ciphertext])
    return ciphertext

def encrypt(img, ciphertext):
    coeffs2 = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs2
    result = []
    result.append(LL)
    result.append(LH)
    result.append(HL)
    result.append(HH)

    for i in range(len(result)):
        result[i] = result[i].astype('int64')
        result[i] = result[i].tolist()
    for i in range(len(result)):
        for j in range(len(result[i])):
            for k in range(len(result[i][j])):
                result[i][j][k] = bin(result[i][j][k]).replace('0b', "").zfill(8)
    rows = len(result[1])
    num = len(result[1][1])
    index = 0
    try: 
        for j in range(rows):
            for k in range(num):
                for i in range(1,4):
                    result[i][j][k] = result[i][j][k][:-1] + ciphertext[index]
                    index += 1
    except IndexError:
        pass
    for i in range(len(result)):
        for j in range(len(result[i])):
            for k in range(len(result[i][j])):
                result[i][j][k] = int(result[i][j][k], 2)

    for i in range(len(result)):
        result[i] = np.array(result[i])
    data = (result[0], (result[1], result[2], result[3]))
    rmk_origin = pywt.idwt2(data, 'haar')
    rmk = rmk_origin.astype('uint8')
    H = rmk_origin - rmk
    return rmk, H
    
def padding(message):
    if len(message) % 16 == 0:
        return message
    else:
        n = math.ceil(len(message) / 16)
        return message.ljust(n * 16)

def main():
    message = input('Insert message: ')
    img = cv2.imread(args.image, cv2.IMREAD_GRAYSCALE)
    message = padding(message)
    with open('len.txt', 'w') as f:
        f.write(str(len(message)))
    start = time.time()
    key, iv = read_key_and_iv(args.key, args.iv)
    cipher = encrypt_message(message, key, iv)
    steno_img, H = encrypt(img, cipher)
    np.save('{}/matrix'.format(args.save), H)
    cv2.imwrite('{}/result.png'.format(args.save), steno_img)
    print('Stenography image: {}/result.png'.format(args.save))
    print('Difference matrix: {}/matrix.npy'.format(args.save))
    end = time.time()
    print("Encrpyt message in: {:.2f} s".format(end - start))
    img = Image.fromarray(steno_img)
    img.show()


if __name__ == '__main__':
    main()
