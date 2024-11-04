# -*- coding: utf-8 -*-

import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

# Key Generation
def generate_keys(key):
    # Initial permutation
    p10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    p8 = [6, 3, 7, 4, 8, 5, 10, 9]
    
    # Perform P10 permutation
    key = ''.join([key[i-1] for i in p10])
    
    # Split into two halves
    left = key[:5]
    right = key[5:]
    
    # Generate two keys
    keys = []
    for i in range(2):
        # Left shift both halves
        left = left[1:] + left[0]
        right = right[1:] + right[0]
        if i == 1:
            left = left[1:] + left[0]
            right = right[1:] + right[0]
        
        # Combine and perform P8 permutation
        combined = left + right
        keys.append(''.join([combined[i-1] for i in p8]))
    
    return keys

# Initial and Final Permutations
IP = [2, 6, 3, 1, 4, 8, 5, 7]
IP_inv = [4, 1, 3, 5, 7, 2, 8, 6]

# Expansion and P4 Permutation
EP = [4, 1, 2, 3, 2, 3, 4, 1]
P4 = [2, 4, 3, 1]

# S-Boxes
S0 = [
    [1, 0, 3, 2],
    [3, 2, 1, 0],
    [0, 2, 1, 3],
    [3, 1, 3, 2]
]

S1 = [
    [0, 1, 2, 3],
    [2, 0, 1, 3],
    [3, 0, 1, 0],
    [2, 1, 0, 3]
]

def apply_sbox(s, input):
    row = int(input[0] + input[3], 2)
    col = int(input[1] + input[2], 2)
    return format(s[row][col], '02b')

def f_function(right, subkey):
    # Expansion
    expanded = ''.join([right[i-1] for i in EP])
    
    # XOR with subkey
    xored = ''.join([str(int(a) ^ int(b)) for a, b in zip(expanded, subkey)])
    
    # Apply S-Boxes
    left = xored[:4]
    right = xored[4:]
    output = apply_sbox(S0, left) + apply_sbox(S1, right)
    
    # P4 permutation
    return ''.join([output[i-1] for i in P4])

def sdes_encrypt(plaintext, key):
    subkeys = generate_keys(key)
    
    # Initial Permutation
    plaintext = ''.join([plaintext[i-1] for i in IP])
    
    left = plaintext[:4]
    right = plaintext[4:]
    
    # Two rounds of Feistel network
    for i in range(2):
        new_right = ''.join([str(int(a) ^ int(b)) for a, b in zip(left, f_function(right, subkeys[i]))])
        left = right
        right = new_right
    
    # Combine and apply final permutation
    combined = right + left
    ciphertext = ''.join([combined[i-1] for i in IP_inv])
    
    return ciphertext

def sdes_decrypt(ciphertext, key):
    subkeys = generate_keys(key)
    
    # Initial Permutation
    ciphertext = ''.join([ciphertext[i-1] for i in IP])
    
    left = ciphertext[:4]
    right = ciphertext[4:]
    
    # Two rounds of Feistel network (reverse order of subkeys)
    for i in range(1, -1, -1):
        new_right = ''.join([str(int(a) ^ int(b)) for a, b in zip(left, f_function(right, subkeys[i]))])
        left = right
        right = new_right
    
    # Combine and apply final permutation
    combined = right + left
    plaintext = ''.join([combined[i-1] for i in IP_inv])
    
    return plaintext

def text_to_binary(text):
    return ''.join(format(ord(char), '08b') for char in text)

def binary_to_text(binary):
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))

def encrypt_text(plaintext, key):
    binary = text_to_binary(plaintext)
    encrypted_binary = ''.join(sdes_encrypt(binary[i:i+8], key) for i in range(0, len(binary), 8))
    return encrypted_binary

def decrypt_text(ciphertext, key):
    decrypted_binary = ''.join(sdes_decrypt(ciphertext[i:i+8], key) for i in range(0, len(ciphertext), 8))
    return binary_to_text(decrypted_binary)

def encrypt_image(image, key):
    width, height = image.size
    pixels = np.array(image)
    encrypted_pixels = np.zeros_like(pixels)
    
    for i in range(height):
        for j in range(width):
            for k in range(3):  # RGB channels
                pixel_value = format(pixels[i, j, k], '08b')
                encrypted_value = sdes_encrypt(pixel_value, key)
                encrypted_pixels[i, j, k] = int(encrypted_value, 2)
    
    return Image.fromarray(encrypted_pixels.astype('uint8'))

def decrypt_image(encrypted_image, key):
    width, height = encrypted_image.size
    pixels = np.array(encrypted_image)
    decrypted_pixels = np.zeros_like(pixels)
    
    for i in range(height):
        for j in range(width):
            for k in range(3):  # RGB channels
                pixel_value = format(pixels[i, j, k], '08b')
                decrypted_value = sdes_decrypt(pixel_value, key)
                decrypted_pixels[i, j, k] = int(decrypted_value, 2)
    
    return Image.fromarray(decrypted_pixels.astype('uint8'))

def binary_to_alphanumeric(binary):
    return ''.join([chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)])

def main():
    key = "1010000010"  # Hardcoded 10-bit key
    
    choice = input("Do you want to encrypt text or image? (text/image): ").lower()
    
    if choice == "text":
        plaintext = input("Enter the text to encrypt: ")
        
        plaintext_binary = text_to_binary(plaintext)
        cipher_binary = encrypt_text(plaintext, key)
        decrypted_binary = ''.join(sdes_decrypt(cipher_binary[i:i+8], key) for i in range(0, len(cipher_binary), 8))
        decrypted_text = binary_to_text(decrypted_binary)
        
        print(f"Plain text (alphanumeric): {plaintext}")
        print(f"Plain text (binary): {plaintext_binary}")
        print(f"Cipher text (alphanumeric): {binary_to_alphanumeric(cipher_binary)}")
        print(f"Cipher text (binary): {cipher_binary}")
        print(f"Decrypted text (alphanumeric): {decrypted_text}")
        print(f"Decrypted text (binary): {decrypted_binary}")
    
    elif choice == "image":
        image_path = input("Enter the path to the image file: ")
        original_image = Image.open(image_path)
        
        encrypted_image = encrypt_image(original_image, key)
        decrypted_image = decrypt_image(encrypted_image, key)
        
        plt.figure(figsize=(15, 5))
        plt.subplot(131)
        plt.title("Original Image")
        plt.imshow(original_image)
        plt.axis('off')
        
        plt.subplot(132)
        plt.title("Encrypted Image")
        plt.imshow(encrypted_image)
        plt.axis('off')
        
        plt.subplot(133)
        plt.title("Decrypted Image")
        plt.imshow(decrypted_image)
        plt.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    else:
        print("Invalid choice. Please run the program again and choose 'text' or 'image'.")

if __name__ == "__main__":
    main()