from PIL import Image

def int_to_bin(rgb):
    """Convert an integer tuple to a binary (string) tuple."""
    r, g, b = rgb
    return ('{0:08b}'.format(r),
            '{0:08b}'.format(g),
            '{0:08b}'.format(b))

def bin_to_int(rgb):
    """Convert a binary (string) tuple to an integer tuple."""
    r, g, b = rgb
    return (int(r, 2),
            int(g, 2),
            int(b, 2))

def encode(image_path, message):
    """Encode a message into an image."""
    img = Image.open(image_path)
    # Check if the message can be encoded in the image
    max_bytes = img.size[0] * img.size[1] * 3 // 8
    if len(message) > max_bytes:
        raise ValueError("Message too large for image.")
    # Convert message to binary
    message += '\0'  # Add null character to mark the end of the message
    bits = ''.join([format(ord(c), "08b") for c in message])
    # Encode bits into image pixels
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            if len(bits) > 0:
                # Get the RGB values of the current pixel
                rgb = int_to_bin(pixels[i, j])
                # Modify the least significant bit of each color component
                rgb = (rgb[0][:-1] + bits[:1],
                       rgb[1][:-1] + bits[:1],
                       rgb[2][:-1] + bits[:1])
                pixels[i, j] = bin_to_int(rgb)
                # Remove the least significant bit from the message
                bits = bits[1:]
            else:
                img.save(image_path.split('.')[0] + '_encoded.png')
                return
    img.save(image_path.split('.')[0] + '_encoded.png')

def decode(image_path):
    """Decode a message from an image."""
    img = Image.open(image_path)
    pixels = img.load()
    # Extract the least significant bit from each color component of each pixel
    binary = ''
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            rgb = int_to_bin(pixels[i, j])
            binary += rgb[0][-1] + rgb[1][-1] + rgb[2][-1]
    # Convert binary string to message
    message = ''
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        message += chr(int(byte, 2))
        if message[-1] == '\0':
            break
    return message[:-1]

encode('my_image.png', 'Here is some secret msg for u!!!')

message = decode('my_image_encoded.png')
print(message)
