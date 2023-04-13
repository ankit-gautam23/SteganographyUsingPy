from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

def encrypt(key, message):
    f = Fernet(key)
    return f.encrypt(message.encode()).decode()

def decrypt(key, message):
    f = Fernet(key)
    return f.decrypt(message.encode()).decode()

def encode(image_path, key, message):
    """Encode an encrypted message into an image."""
    encrypted_message = encrypt(key, message)
    img = Image.open(image_path)
    # Check if the message can be encoded in the image
    max_bytes = img.size[0] * img.size[1] * 3 // 8
    if len(encrypted_message) > max_bytes:
        raise ValueError("Message too large for image.")
    # Convert message to binary
    encrypted_message += '\0'  # Add null character to mark the end of the message
    bits = np.array([int(bit) for c in encrypted_message for bit in format(ord(c), "08b")])
    # Reshape bits into 3 columns of pixels
    bits = bits.reshape(-1, 3)
    # Encode bits into image pixels
    pixels = np.array(img)
    pixels = pixels.reshape(-1, 3)
    pixels[:, :] &= 0b11111110  # Clear the least significant bit of each color component
    pixels[:, :] |= bits[:, :]  # Set the least significant bit of each color component
    img_encoded = Image.fromarray(pixels.reshape(img.size))
    img_encoded.save(image_path.split('.')[0] + '_encoded.png')

def decode(image_path, key):
    """Decode an encrypted message from an image."""
    img = Image.open(image_path)
    pixels = np.array(img)
    # Extract the least significant bit from each color component of each pixel
    binary = np.unpackbits(pixels[:, :, :3] & 0b00000001)
    binary = binary.reshape(-1, 8)
    # Convert binary string to message
    encrypted_message = ''.join([chr(int(byte, 2)) for byte in binary.tolist()])
    encrypted_message = encrypted_message.split('\0')[0]
    message = decrypt(key, encrypted_message)
    return message

message = 'Secret message here'
image_path = 'image_file_name.jpg'
decoded_message = decode('image_file_name_encoded.png')
print(decoded_message)

