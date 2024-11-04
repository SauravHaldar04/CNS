import PIL.Image as Image
print("1.Text Encryption \n2.Image Decryption")
option = int(input("Enter your choice: "))

if option == 1:
    text = input("Enter the text to be encrypted: ")
    key = int(input("Enter the key: "))
    encrypted_text = ""
    for i in text:
        encrypted_text += chr((ord(i) + key) % 128)
    print("Encrypted text: ", encrypted_text)
    decrypted_text = ""
    for i in encrypted_text:
        decrypted_text += chr((ord(i) - key) % 128)
    print("Decrypted text: ", decrypted_text)
elif option == 2:
    image_path = input("Enter the image path: ")
    try:
        image = Image.open(image_path)
    except:
        print("Invalid image path")
    pixels = list(image.getdata())
    key = int(input("Enter the key: "))
    for i in range(len(pixels)):
        pixels[i] = ((pixels[i][0] + key)%256, (pixels[i][1] + key)%256, (pixels[i][2] + key)%256)
    new_image = Image.new(image.mode, image.size)
    new_image.putdata(pixels)
    new_image.save("encrypted_image.png")
    excrypted_image = Image.open("encrypted_image.png")
    encrypted_pixels = list(excrypted_image.getdata())
    for i in range(len(encrypted_pixels)):
        encrypted_pixels[i] = ((encrypted_pixels[i][0] - key)%256, (encrypted_pixels[i][1] - key)%256, (encrypted_pixels[i][2] - key)%256)
    decrypted_image = Image.new(excrypted_image.mode, excrypted_image.size)
    decrypted_image.putdata(encrypted_pixels)
    decrypted_image.save("decrypted_image.png")

