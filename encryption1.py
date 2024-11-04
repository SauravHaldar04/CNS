# To perform the frequency analysis of the encrypted text and generate histograms of the pixel values for the images, I'll start by writing the necessary code to perform these tasks.

import PIL.Image as Image
import matplotlib.pyplot as plt
import collections

def encrypt_text(text, key):
    encrypted_text = ""
    for i in text:
        encrypted_text += chr((ord(i) + key) % 128)
    return encrypted_text

def decrypt_text(encrypted_text, key):
    decrypted_text = ""
    for i in encrypted_text:
        decrypted_text += chr((ord(i) - key) % 128)
    return decrypted_text

def frequency_analysis(text):
    frequency = collections.Counter(text)
    return frequency

def plot_frequency_analysis(original_text, encrypted_text):
    original_freq = frequency_analysis(original_text)
    encrypted_freq = frequency_analysis(encrypted_text)
    
    # Plotting
    fig, axs = plt.subplots(1, 2, figsize=(15, 5))
    
    axs[0].bar(original_freq.keys(), original_freq.values())
    axs[0].set_title("Frequency Analysis of Original Text")
    
    axs[1].bar(encrypted_freq.keys(), encrypted_freq.values())
    axs[1].set_title("Frequency Analysis of Encrypted Text")
    
    plt.show()

def encrypt_image(image_path, key):
    try:
        image = Image.open(image_path)
    except:
        print("Invalid image path")
        return None, None, None

    original_image = image.copy()
    pixels = list(image.getdata())
    for i in range(len(pixels)):
        if isinstance(pixels[i], int):  # For grayscale images
            pixels[i] = (pixels[i] + key) % 256
        else:  # For RGB images
            pixels[i] = (
                (pixels[i][0] + key) % 256,
                (pixels[i][1] + key) % 256,
                (pixels[i][2] + key) % 256
            )

    encrypted_image = Image.new(image.mode, image.size)
    encrypted_image.putdata(pixels)
    
    return original_image, encrypted_image, key

def decrypt_image(encrypted_image, key):
    encrypted_pixels = list(encrypted_image.getdata())
    for i in range(len(encrypted_pixels)):
        if isinstance(encrypted_pixels[i], int):  # For grayscale images
            encrypted_pixels[i] = (encrypted_pixels[i] - key) % 256
        else:  # For RGB images
            encrypted_pixels[i] = (
                (encrypted_pixels[i][0] - key) % 256,
                (encrypted_pixels[i][1] - key) % 256,
                (encrypted_pixels[i][2] - key) % 256
            )

    decrypted_image = Image.new(encrypted_image.mode, encrypted_image.size)
    decrypted_image.putdata(encrypted_pixels)
    return decrypted_image

def plot_histograms(original_image, encrypted_image, decrypted_image):
    original_pixels = list(original_image.getdata())
    encrypted_pixels = list(encrypted_image.getdata())
    decrypted_pixels = list(decrypted_image.getdata())
    
    # Flatten pixel data for histogram
    if isinstance(original_pixels[0], int):  # Grayscale
        original_pixels = original_pixels
        encrypted_pixels = encrypted_pixels
        decrypted_pixels = decrypted_pixels
    else:  # RGB
        original_pixels = [item for sublist in original_pixels for item in sublist]
        encrypted_pixels = [item for sublist in encrypted_pixels for item in sublist]
        decrypted_pixels = [item for sublist in decrypted_pixels for item in sublist]
    
    # Plotting histograms
    fig, axs = plt.subplots(1, 3, figsize=(15, 5))
    
    axs[0].hist(original_pixels, bins=256, color='blue', alpha=0.7)
    axs[0].set_title("Histogram of Original Image")
    
    axs[1].hist(encrypted_pixels, bins=256, color='green', alpha=0.7)
    axs[1].set_title("Histogram of Encrypted Image")
    
    axs[2].hist(decrypted_pixels, bins=256, color='red', alpha=0.7)
    axs[2].set_title("Histogram of Decrypted Image")
    
    plt.show()

# Example usage
text = "Hello, World! This is a test."
key_text = 5
encrypted_text = encrypt_text(text, key_text)
decrypted_text = decrypt_text(encrypted_text, key_text)
plot_frequency_analysis(text, encrypted_text)

# Example usage for images (assuming a valid image path is provided)
image_path = "CNS\cover_image.png"  # Replace with a valid image path
key_image = 10
original_image, encrypted_image, key_image = encrypt_image(image_path, key_image)
decrypted_image = decrypt_image(encrypted_image, key_image)
plot_histograms(original_image, encrypted_image, decrypted_image)
