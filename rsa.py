import random
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tabulate import tabulate

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    if m == 1:
        return 0
    while a > 1:
        q = a // m
        m, a = a % m, m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def generate_prime_candidate(length):
    p = random.getrandbits(length)
    return p | (1 << length - 1) | 1

def generate_prime(length):
    p = generate_prime_candidate(length)
    while not is_prime(p):
        p = generate_prime_candidate(length)
    return p

def generate_keys(bit_length):
    p = generate_prime(bit_length)
    q = generate_prime(bit_length)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    if gcd(e, phi) != 1:
        raise ValueError("e must be coprime to phi(n)")
    d = mod_inverse(e, phi)
    return (n, e), (n, d)

def modular_exponentiation(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if (exponent % 2) == 1:
            result = (result * base) % modulus
        exponent //= 2
        base = (base * base) % modulus
    return result

def rsa_encrypt(plaintext, public_key):
    n, e = public_key
    return modular_exponentiation(plaintext, e, n)

def rsa_decrypt(ciphertext, private_key):
    n, d = private_key
    return modular_exponentiation(ciphertext, d, n)

def pad_image_data(pixels, block_size):
    padding_length = (block_size - (len(pixels) % block_size)) % block_size
    padding = [0] * padding_length
    padded_pixels = np.append(pixels, padding)
    return padded_pixels, padding_length

def unpad_image_data(pixels, padding_length):
    if padding_length > 0:
        pixels = pixels[:-padding_length]
    return pixels

def encrypt_image(image_path, public_key, block_size=8):
    original_image = Image.open(image_path).convert('L')
    pixels = np.array(original_image).flatten()
    padded_pixels, padding_length = pad_image_data(pixels, block_size)
    encrypted_pixels = []
    for pixel in padded_pixels:
        encrypted_pixel = rsa_encrypt(pixel, public_key)
        encrypted_pixels.append(encrypted_pixel)
    return original_image, encrypted_pixels, padding_length

def decrypt_image(encrypted_pixels, private_key, original_shape, padding_length):
    decrypted_pixels = []
    for encrypted_pixel in encrypted_pixels:
        decrypted_pixel = rsa_decrypt(encrypted_pixel, private_key)
        decrypted_pixels.append(decrypted_pixel)
    decrypted_pixels = unpad_image_data(decrypted_pixels, padding_length)
    decrypted_image = np.array(decrypted_pixels, dtype=np.uint8).reshape(original_shape)
    return decrypted_image

def show_images(original_image, encrypted_image, decrypted_image):
    plt.figure(figsize=(12, 4))
    plt.subplot(1, 3, 1)
    plt.title('Original Image')
    plt.imshow(original_image, cmap='gray')
    plt.subplot(1, 3, 2)
    plt.title('Encrypted Image')
    plt.imshow(encrypted_image, cmap='gray')
    plt.subplot(1, 3, 3)
    plt.title('Decrypted Image')
    plt.imshow(decrypted_image, cmap='gray')
    plt.show()

if __name__ == "__main__":
    bit_length = 8
    public_key, private_key = generate_keys(bit_length)
    
    choice = input("Do you want to encrypt a [text] or [image]? ").lower()
    
    if choice == "image":
        image_path = input("Enter the path of the image to encrypt: ")
        original_image, encrypted_pixels, padding_length = encrypt_image(image_path, public_key)
        decrypted_image = decrypt_image(encrypted_pixels, private_key, original_image.size[::-1], padding_length)
        show_images(original_image, np.array(encrypted_pixels[:len(original_image.getdata())]).reshape(original_image.size[::-1]), decrypted_image)
    
    elif choice == "text":
        text = input("Enter the text to encrypt: ")
        encrypted_text = "".join(chr(rsa_encrypt(ord(char), public_key)) for char in text)
        print("Encrypted text:", encrypted_text)
        decrypted_text = "".join(chr(rsa_decrypt(ord(char), private_key)) for char in encrypted_text)
        print("Decrypted text:", decrypted_text)