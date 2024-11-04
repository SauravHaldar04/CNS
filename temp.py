import random
from math import gcd

def generate_super_increasing_array(length, start=1, factor=2):
    array = [start]
    for _ in range(1, length):
        next_num = sum(array) * factor
        array.append(next_num)
    return array

def select_modulus(private_key):
    return sum(private_key) + random.randint(1, 100)

def select_coprime(modulus):
    while True:
        n = random.randint(2, modulus - 1)
        if gcd(n, modulus) == 1:
            return n

def generate_public_key(private_key, n, m):
    return [(w * n) % m for w in private_key]

def generate_knapsack_keys(length=8):
    private_key = generate_super_increasing_array(length)
    modulus = select_modulus(private_key)
    coprime = select_coprime(modulus)
    public_key = generate_public_key(private_key, coprime, modulus)
    
    return {
        'private_key': private_key,
        'public_key': public_key,
        'modulus': modulus,
        'coprime': coprime
    }

def encrypt(plaintext, public_key, modulus):
    ciphertext = []
    for char in plaintext:
        binary = format(ord(char), '08b')
        encrypted_char = sum(int(bit) * key for bit, key in zip(binary, public_key))
        ciphertext.append(encrypted_char % modulus)
    return ciphertext

def modular_inverse(a, m):
    def extended_euclidean(a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = extended_euclidean(b % a, a)
            return gcd, y - (b // a) * x, x
    
    gcd, x, _ = extended_euclidean(a, m)
    if gcd != 1:
        raise ValueError(f"Modular inverse does not exist as {a} and {m} are not coprime.")
    else:
        return x % m

def decrypt(ciphertext, private_key, modulus, coprime):
    decrypted_text = ""
    inverse = modular_inverse(coprime, modulus)
    
    for char in ciphertext:
        decrypted_char = (char * inverse) % modulus
        binary = ""
        for key in reversed(private_key):
            if decrypted_char >= key:
                binary = "1" + binary
                decrypted_char -= key
            else:
                binary = "0" + binary
        decrypted_text += chr(int(binary, 2))
    
    return decrypted_text

if __name__ == "__main__":
    keys = generate_knapsack_keys()
    print("Private Key:", keys['private_key'])
    print("Public Key:", keys['public_key'])
    print("Modulus:", keys['modulus'])
    print("Coprime:", keys['coprime'])
    plaintext = input("Enter plaintext: ")
    ciphertext = encrypt(plaintext, keys['public_key'], keys['modulus'])
    print("Ciphertext:", ciphertext)
    decrypted_text = decrypt(ciphertext, keys['private_key'], keys['modulus'], keys['coprime'])
    print("Decrypted text:", decrypted_text)