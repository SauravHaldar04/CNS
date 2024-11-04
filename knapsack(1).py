import random
from math import gcd
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

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

def encrypt_pixel(pixel, public_key):
    """Encrypts each channel (R, G, B) using the knapsack algorithm."""
    encrypted = []
    for channel in pixel:
        binary = format(channel, '08b')  # Convert channel value to 8-bit binary
        encrypted_channel = sum(int(bit) * key for bit, key in zip(binary, public_key))  # Encrypt binary bits
        encrypted.append(encrypted_channel)
    return tuple(encrypted)

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

def decrypt_pixel(encrypted_pixel, private_key, modulus, inverse):
    """Decrypts each channel (R, G, B) using the knapsack algorithm."""
    decrypted = []
    for channel in encrypted_pixel:
        decrypted_channel = (channel * inverse) % modulus
        binary = ""
        for key in reversed(private_key):
            if decrypted_channel >= key:
                binary = "1" + binary
                decrypted_channel -= key
            else:
                binary = "0" + binary
        decrypted.append(int(binary, 2))
    return tuple(decrypted)

def encrypt_image(image_path, public_key):
    """Encrypts the image by applying knapsack encryption to each pixel."""
    with Image.open(image_path) as img:
        img = img.convert('RGB')
        width, height = img.size
        encrypted_pixels = []
        for y in range(height):
            for x in range(width):
                pixel = img.getpixel((x, y))
                encrypted_pixel = encrypt_pixel(pixel, public_key)
                encrypted_pixels.append(encrypted_pixel)
    
    encrypted_array = np.array(encrypted_pixels, dtype=np.uint32)
    return encrypted_array.reshape(height, width, 3)

def decrypt_image(encrypted_image, private_key, modulus, coprime):
    """Decrypts the image by applying knapsack decryption to each pixel."""
    height, width, _ = encrypted_image.shape
    inverse = modular_inverse(coprime, modulus)
    decrypted_pixels = []
    
    for y in range(height):
        for x in range(width):
            encrypted_pixel = encrypted_image[y, x]
            decrypted_pixel = decrypt_pixel(encrypted_pixel, private_key, modulus, inverse)
            decrypted_pixels.append(decrypted_pixel)
    
    decrypted_array = np.array(decrypted_pixels, dtype=np.uint8)
    return Image.fromarray(decrypted_array.reshape(height, width, 3))

def display_images(original, encrypted, decrypted):
    """Display the original, encrypted, and decrypted images."""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    ax1.imshow(original)
    ax1.set_title('Original Image')
    ax1.axis('off')

    ax2.imshow(encrypted)
    ax2.set_title('Encrypted Image')
    ax2.axis('off')

    ax3.imshow(decrypted)
    ax3.set_title('Decrypted Image')
    ax3.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    image_path = input("Enter the path to the image file: ")

    # Generate Knapsack keys
    keys = generate_knapsack_keys()
    print("Keys generated successfully.")
    
    # Original Image
    original_image = Image.open(image_path).convert('RGB')
    
    # Encrypt Image
    encrypted_image = encrypt_image(image_path, keys['public_key'])
    print("Image encrypted successfully.")
    
    # Decrypt Image
    decrypted_image = decrypt_image(encrypted_image, keys['private_key'], keys['modulus'], keys['coprime'])
    print("Image decrypted successfully.")
    
    # Display Images
    display_images(original_image, encrypted_image, decrypted_image)
