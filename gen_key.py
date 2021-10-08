import random
import string


def gen_key():
    """
    Generate key and iv for AES encryption
    """
    characters = string.ascii_letters
    for i in range(10):
        characters += str(i)
    key = "".join([random.choice(characters) for i in range(16)])
    iv = "".join([random.choice(characters) for i in range(16)])
    return key, iv


def save(key, iv):
    with open('keys/key.txt', 'w') as f:
        f.write(key)
    with open('keys/iv.txt', 'w') as f:
        f.write(iv)


def main():
    key, iv = gen_key()
    save(key, iv)
    print('Done')


if __name__ == '__main__':
    main()
