from PIL import Image

import numpy as np

def encode(image_path, message):
    """Encode a message into an image."""
    img = Image.open(image_path)
    # Checking if the message can be encoded in the image
    max_bytes = img.size[0] * img.size[1] * 3 // 8
    if len(message) > max_bytes:
        raise ValueError("Message too large for image.")
    # Converting message to binary
    message += '\0'  # Add null character to mark the end of the message
    bits = np.array([int(bit) for c in message for bit in format(ord(c), "08b")])
    # Reshaping bits into 3 columns of pixels
    bits = bits.reshape(-1, 3)
    # Encoding bits into image pixels
    pixels = np.array(img)
    pixels = pixels.reshape(-1, 3)
    pixels[:, :] &= 0b11111110  # Clearing the least significant bit of each color component
    pixels[:, :] |= bits[:, :]  # Setting the least significant bit of each color component
    img_encoded = Image.fromarray(pixels.reshape(img.size))
    img_encoded.save(image_path.split('.')[0] + '_encoded.png')

def decode(image_path):
    """Decode a message from an image."""
    img = Image.open(image_path)
    pixels = img.load()
    # Extracting the least significant bit from each color component of each pixel
    binary = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            rgb = int_to_bin(pixels[i, j])
            binary += rgb[0][-1] + rgb[1][-1] + rgb[2][-1]
    # Converting binary string to message
    message = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        message += chr(int(byte, 2))
        if message[-1] == '\0':
            break
    return message[:-1]

def decode(image_path):
    """Decode a message from an image."""
    img = Image.open(image_path)
    pixels = np.array(img)
    # Extracting the least significant bit from each color component of each pixel
    binary = np.unpackbits(pixels[:, :, :3] & 0b00000001)
    binary = binary.reshape(-1, 8)
    # Converting binary string to message
    message = ''.join([chr(int(byte, 2)) for byte in binary.tolist()])
    message = message.split('\0')[0]
    return message


encode('my_image.png', 'Here is some secret msg for u!!!')

message = decode('my_image_encoded.png')
print(message)
