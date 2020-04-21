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

def encrypt_message(message, key, iv):
    obj = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = obj.encrypt(message)
    ciphertext = "".join([bin(i)[2:].zfill(8) for i in ciphertext])
    return ciphertext

def encrypt(image, ciphertext):
    img = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
    img = np.float32(img)
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
    rmk = rmk_origin.astype('uint64')
    H = rmk_origin - rmk
    return rmk, H
    
def padding(message):
    if len(message) < 16:
        message = message.ljust(16)
    return message

def main():
    message = input('Nhap thong diep (<= 16 ky tu): ')
    message = padding(message)
    key, iv = read_key_and_iv('key.txt', 'iv.txt')
    cipher = encrypt_message(message, key, iv)
    # with open('enc_mess.txt', 'w') as f:
        # f.write(cipher)
    steno_img, H = encrypt('lena.png', cipher)
    np.save('H', H)
    cv2.imwrite('result.png', steno_img)
    print('Stenography image: result.png')

if __name__ == '__main__':
    main()
