import time
import math
from Crypto.Cipher import AES
import cv2
import numpy as np
import pywt
from tkinter.filedialog import askopenfilename, askdirectory
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import PIL


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.master = master
        self.key_dir = None
        self.iv_dir = None
        self.img_dir = None
        self.save_dir = None
        self.create_widgets()

    def create_widgets(self):
        self.master.title('Demo Encrypt')
        self.pack(fill='both', expand=1)
        self.labelfont = ('times', 20, 'bold')
        self.img_path = tk.StringVar()
        self.img_path.set('None')
        self.image_label = tk.Label(text="Image", fg='blue')
        self.image_label.place(x=100, y=50)
        self.image_label.config(font=self.labelfont)
        self.panel = tk.Label(image=None, text='x')
        self.panel.place(x=50, y=100)
        self.image_path = tk.Label(textvariable=self.img_path)
        self.image_path.place(x=100, y=530)
        self.select_image_button = tk.Button(text='Select image', command=self.show)
        self.select_image_button.place(x=200, y=530)
        self.key_path_text = tk.StringVar()
        self.key_path_text.set('None')
        self.key_label = tk.Label(text='Key')
        self.key_label.place(x=400, y=100)
        self.key_label.config(font=self.labelfont)
        self.key_path_label = tk.Label(textvariable=self.key_path_text)
        self.key_path_label.place(x=550, y=100)
        self.select_key_button = tk.Button(
            text='Select', command=self.select_key)
        self.select_key_button.place(x=650, y=100)
        self.iv_label = tk.Label(text="Init vector")
        self.iv_label.place(x=400, y=200)
        self.iv_label.config(font=self.labelfont)
        self.iv_path_text = tk.StringVar()
        self.iv_path_text.set('None')
        self.iv_path_label = tk.Label(textvariable=self.iv_path_text)
        self.iv_path_label.place(x=550, y=200)
        self.select_iv_button = tk.Button(text='Select', command=self.select_iv)
        self.select_iv_button.place(x=650, y=200)
        self.save_path_text = tk.StringVar()
        self.save_path_text.set('None')
        self.save_label = tk.Label(text='Save')
        self.save_label.config(font=self.labelfont)
        self.save_label.place(x=400, y=300)
        self.save_path_label = tk.Label(textvariable=self.save_path_text)
        self.save_path_label.place(x=550, y=300)
        self.select_save_button = tk.Button(
            text='Select', command=self.select_save)
        self.select_save_button.place(x=650, y=300)
        self.encrypt_button = tk.Button(
            text='Encrypt', fg='red', command=self.start_encrypt)
        self.encrypt_button.config(font=self.labelfont)
        self.encrypt_button.place(x=330, y=600)
        self.message_input_label = tk.Label(text='Message')
        self.message_input_label.config(font=self.labelfont)
        self.message_input_label.place(x=400, y=400)
        self.message_imput = tk.Entry()
        self.message_imput.place(x=550, y=400, width=200, height=30)
        self.message_imput.bind('<Key-Return>', self.start_encrypt)

    def open_file(self):
        file_name = askopenfilename(title='open')
        return file_name

    def open_dir(self):
        file_name = askdirectory(title='open')
        return file_name

    def select_save(self):
        try:
            self.save_dir = self.open_dir()
            self.change_text(self.save_path_text, self.save_dir)
        except AttributeError:
            return

    def select_iv(self):
        try:
            self.iv_dir = self.open_file()
            self.change_text(self.iv_path_text, self.iv_dir)
        except AttributeError:
            return

    def select_key(self):
        try:
            self.key_dir = self.open_file()
            self.change_text(self.key_path_text, self.key_dir)
        except AttributeError:
            return

    def show(self):
        try:
            file_name = self.open_file()
            self.img_dir = file_name
            img = Image.open(file_name)
            img = img.resize((300, 400))
            self.change_text(self.img_path, file_name)
            img = ImageTk.PhotoImage(img)
            self.panel.configure(image=img)
            self.panel.image = img
        except PIL.UnidentifiedImageError:
            messagebox.showerror('Error', 'Please select correct image type')
            return
        except AttributeError:
            return

    def change_text(self, var, text):
        var.set(text[text.rfind('/'):])

    def read_key_and_iv(self, key_file, iv_file):
        with open(key_file, 'r') as f:
            key = f.readline()
        with open(iv_file, 'r') as f:
            iv = f.readline()
        return key, iv

    def encrypt_message(self, message, key, iv):
        key = bytes(key, 'utf-8')
        iv = bytes(iv, 'utf-8')
        message = bytes(message, 'utf-8')
        enc = AES.new(key, AES.MODE_CBC, iv=iv)
        ciphertext = enc.encrypt(message)
        ciphertext = "".join([bin(i)[2:].zfill(8) for i in ciphertext])
        return ciphertext

    def to_int(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = matrix[i].astype('int64')
        return matrix

    def to_list(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = matrix[i].tolist()
        return matrix

    def to_bin(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(matrix[i][j])):
                    matrix[i][j][k] = bin(
                        matrix[i][j][k]).replace(
                        '0b', "").zfill(8)
        return matrix

    def bin_to_int(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(matrix[i][j])):
                    matrix[i][j][k] = int(matrix[i][j][k], 2)
        return matrix

    def stegano(self, matrix, ciphertext):
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

    def to_np_array(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = np.array(matrix[i])
        return matrix

    def encrypt(self, img, ciphertext):
        coeffs2 = pywt.dwt2(img, 'haar')
        LL, (LH, HL, HH) = coeffs2
        sub_imgs = []
        sub_imgs.append(LL)
        sub_imgs.append(LH)
        sub_imgs.append(HL)
        sub_imgs.append(HH)
        sub_imgs = self.to_int(sub_imgs)
        sub_imgs = self.to_list(sub_imgs)
        sub_imgs = self.to_bin(sub_imgs)
        sub_imgs = self.stegano(sub_imgs, ciphertext)
        sub_imgs = self.bin_to_int(sub_imgs)
        sub_imgs = self.to_np_array(sub_imgs)
        data = (sub_imgs[0], (sub_imgs[1], sub_imgs[2], sub_imgs[3]))
        rmk_origin = pywt.idwt2(data, 'haar')
        rmk = rmk_origin.astype('uint8')
        H = rmk_origin - rmk
        return rmk, H

    def padding(self, message):
        if len(message) % 16 == 0:
            return message
        else:
            n = math.ceil(len(message) / 16)
            return message.ljust(n * 16)

    def start_encrypt(self, event=None):
        if self.img_dir is None or self.key_dir is None or self.iv_dir is None or self.save_dir is None:
            messagebox.showerror('Error', 'Please input all file')
        else:
            message = self.message_imput.get()
            img = cv2.imread(self.img_dir, cv2.IMREAD_GRAYSCALE)
            message = self.padding(message)
            with open('{}/len.txt'.format(self.save_dir), 'w') as f:
                f.write(str(len(message)))
            start = time.time()
            key, iv = self.read_key_and_iv(self.key_dir, self.iv_dir)
            cipher = self.encrypt_message(message, key, iv)
            steno_img, H = self.encrypt(img, cipher)
            np.save('{}/matrix'.format(self.save_dir), H)
            cv2.imwrite('{}/result.png'.format(self.save_dir), steno_img)
            end = time.time()
            messagebox.showinfo(
                'Success',
                'Success\n Encrpyt message in: {:.2f} s'.format(
                    end - start))


def main():
    root = tk.Tk()
    app = Application(master=root)
    root.geometry('800x700')
    root.resizable(False, False)
    app.mainloop()


if __name__ == '__main__':
    main()
