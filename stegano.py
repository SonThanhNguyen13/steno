import argparse
import time
import math
from Crypto.Cipher import AES
import cv2
import numpy as np
import pywt

parser = argparse.ArgumentParser()
parser.add_argument('-i', '--image', required='True', help='Image')
parser.add_argument('-k', '--key', required='True', help='AES key')
parser.add_argument('-v', '--iv', required='True', help='AES initilization vector')
parser.add_argument('-s', '--save', default='result', help='Result dir')
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
    enc = AES.new(key, AES.MODE_CBC, iv=iv)
    ciphertext = enc.encrypt(message)
    ciphertext = "".join([bin(i)[2:].zfill(8) for i in ciphertext])
    return ciphertext


def to_int(matrix):
    for i in range(len(matrix)):
        matrix[i] = matrix[i].astype('int8')
    return matrix


def to_list(matrix):
    for i in range(len(matrix)):
        matrix[i] = matrix[i].tolist()
    return matrix


def to_bin(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                matrix[i][j][k] = bin(matrix[i][j][k]).replace('0b', "").zfill(8)
    return matrix


def bin_to_int(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            for k in range(len(matrix[i][j])):
                matrix[i][j][k] = int(matrix[i][j][k], 2)
    return matrix


def stegano(matrix, ciphertext):
    j = 0
    k = 0
    row_len = len(matrix[1][1])
    for index, item in enumerate(ciphertext):
        if index % 3 == 0:
            matrix[1][j][k] = matrix[1][j][k][:-1] + item
        elif index % 3 == 1:
            matrix[2][j][k] = matrix[2][j][k][:-1] + item
        else:
            matrix[3][j][k] = matrix[3][j][k][:-1] + item
            k += 1
            if k == row_len:
                j += 1
                k = 0
    return matrix


def to_np_array(matrix):
    for i in range(len(matrix)):
        matrix[i] = np.array(matrix[i])
    return matrix


def start_stegano(img, ciphertext):
    coeffs2 = pywt.dwt2(img, 'haar')
    LL, (LH, HL, HH) = coeffs2
    sub_imgs = []
    sub_imgs.append(LL)
    sub_imgs.append(LH)
    sub_imgs.append(HL)
    sub_imgs.append(HH)
    sub_imgs = to_int(sub_imgs)
    sub_imgs = to_list(sub_imgs)
    sub_imgs = to_bin(sub_imgs)
    sub_imgs = stegano(sub_imgs, ciphertext)
    sub_imgs = bin_to_int(sub_imgs)
    sub_imgs = to_np_array(sub_imgs)
    data = (sub_imgs[0], (sub_imgs[1], sub_imgs[2], sub_imgs[3]))
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
    with open('{}/len.txt'.format(args.save), 'w') as f:
        f.write(str(len(message)))
    start = time.time()
    key, iv = read_key_and_iv(args.key, args.iv)
    cipher = encrypt_message(message, key, iv)
    steno_img, H = start_stegano(img, cipher)
    np.save('{}/matrix'.format(args.save), H)
    cv2.imwrite('{}/result.png'.format(args.save), steno_img)
    print('Stenography image: {}/result.png'.format(args.save))
    print('Difference matrix: {}/matrix.npy'.format(args.save))
    print("Message's length: {}/len.txt".format(args.save))
    end = time.time()
    print("Encrpyt message in: {:.2f} s".format(end - start))


if __name__ == '__main__':
    main()
