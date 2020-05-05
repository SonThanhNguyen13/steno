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
        self.matrix_dir = None
        self.len = None
        self.create_widgets()

    def create_widgets(self):
        self.master.title('Demo Decrypt')
        self.pack(fill='both', expand=1)
        self.labelfont = ('times', 20, 'bold')
        self.messagefont = ('times', 14)
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
        self.matrix_path_text = tk.StringVar()
        self.matrix_path_text.set('None')
        self.matrix_label = tk.Label(text='Matrix')
        self.matrix_label.config(font=self.labelfont)
        self.matrix_label.place(x=400, y=300)
        self.matrix_path_label = tk.Label(textvariable=self.matrix_path_text)
        self.matrix_path_label.place(x=550, y=300)
        self.select_matrix_button = tk.Button(
            text='Select', command=self.select_matrix)
        self.select_matrix_button.place(x=650, y=300)
        self.len_message_text = tk.StringVar()
        self.len_message_text.set('None')
        self.len_message_label = tk.Label(text='Length')
        self.len_message_label.config(font=self.labelfont)
        self.len_message_label.place(x=400, y=400)
        self.len_message = tk.Label(textvariable=self.len_message_text)
        self.len_message.place(x=550, y=400)
        self.select_len_button = tk.Button(
            text='Select',command=self.select_len
        )
        self.select_len_button.place(x=650,y=400)
        self.message_label = tk.Label(text='Message')
        self.message_label.config(font=self.labelfont)
        self.message_label.place(x=120, y=620)
        self.message_text = tk.StringVar()
        self.message_text.set('None')
        self.message = tk.Label(textvariable=self.message_text)
        self.message.config(font=self.messagefont)
        self.message.place(x=250, y=620)
        self.decrypt_button = tk.Button(
            text='Decrypt', fg='red', command=self.start_decrypt)
        self.decrypt_button.config(font=self.labelfont)
        self.decrypt_button.place(x=330, y=700)
            
    def open_file(self):
        file_name = askopenfilename(title='open')
        return file_name

    def open_dir(self):
        file_name = askdirectory(title='open')
        return file_name
    
    def select_len(self):
        try:
            len_dir = self.open_file()
            with open(len_dir, 'r') as f:
                self.len = f.readline()
            self.change_len_and_mess(self.len_message_text, self.len)
            self.len = int(self.len)
        except TypeError:
            return
        except UnicodeDecodeError:
            messagebox.showerror('Error', 'Please choose again')    

    def select_matrix(self):
        try:
            self.matrix_dir = askopenfilename(title='open')
            self.change_text(self.matrix_path_text, self.matrix_dir)
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

    def change_len_and_mess(self, var, text):
        var.set(text)

    def change_text(self, var, text):
        var.set(text[text.rfind('/'):])

    def read_key_and_iv(self, key_file, iv_file):
        with open(key_file, 'rb') as f:
            key = f.readline()
        with open(iv_file, 'rb') as f:
            iv = f.readline()
        return key, iv

    def decrypt_message(self, ciphertext, key, iv):
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
        decr = AES.new(key, AES.MODE_CBC, iv=iv)
        return(decr.decrypt(message))


    def to_list(self, matrix):
        for i in range(len(matrix)):
            matrix[i] = matrix[i].tolist()
        return matrix


    def to_bin(self, matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                for k in range(len(matrix[i][j])):
                    matrix[i][j][k] = round(matrix[i][j][k])
                    matrix[i][j][k] = bin(matrix[i][j][k]).replace('0b', "").zfill(8)
        return matrix


    def get_ciphertext(self, matrix, length):
        rows = len(matrix[1])
        num = len(matrix[1][1])
        ciphertext = ''
        for j in range(rows):
            for k in range(num):
                for i in range(1,4):
                    ciphertext += matrix[i][j][k][-1]
                    if len(ciphertext) == length * 8:
                        return ciphertext


    def decrypt(self, image, matrix, length):
        try:
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
            result = self.to_list(result)
            result = self.to_bin(result)
            ciphertext = self.get_ciphertext(result, length=length)
            return ciphertext
        except ValueError:
            messagebox.showerror('Error', 'Please select ".npy matrix file')

    def start_decrypt(self):
        if self.img_dir is None or self.key_dir is None or self.iv_dir is None or self.matrix_dir is None or self.len is None:
            messagebox.showerror('Error', 'Please input all file')
        else:
            start = time.time()
            key, iv = self.read_key_and_iv(self.key_dir, self.iv_dir)
            ciphertext = self.decrypt(self.img_dir, self.matrix_dir, self.len)
            message = self.decrypt_message(ciphertext, key, iv)
            message = '{}'.format(str(message).replace("b'", ""))
            self.change_len_and_mess(self.message_text, message)
            end = time.time()
            messagebox.showinfo('Success', 'Success decrypt message in {:.2f} s'.format(end - start))

def main():
    root = tk.Tk()
    app = Application(master=root)
    root.geometry('800x800')
    root.resizable(False, False)
    app.mainloop()


if __name__ == '__main__':
    main()
