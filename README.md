# An Image Steganography Algorithm using Haar Discrete Wavelet Transform with Advanced Encryption System
## Requirements:
    - Python3
## Install:
    pip3 install -r requirements.txt
## Usasage
 ### Gen key: 
    python3 gen_key.py
    output: key (key.txt), Initilization Vector (iv.txt)
 ### Encrypt: 
    python3 enc.py -i 'image_path' -k key.txt -v iv.txt (optional: -s 'save_dir', default: result/)
    output: A steganography image (.png), a difference matrix (.npy), len message (len.txt)
 ### Decrypt: 
    python3 decr.py -i 'image_path' -k key.txt -v iv.txt -m 'difference_matrix_path' -l 'len_message_file_path'
