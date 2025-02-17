from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os, sys

os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

def encrypt_language_file(input_file, output_file, key):
    iv = os.urandom(16)  # Tạo IV ngẫu nhiên
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    with open(input_file, 'rb') as f:
        data = f.read()

    # Thêm padding để dữ liệu khớp block size
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()

    # Mã hóa dữ liệu
    encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

    # Ghi IV và dữ liệu mã hóa vào file
    with open(output_file, 'wb') as f:
        f.write(iv + encrypted_data)

def decrypt_language_file(input_file, output_file, key):
    with open(input_file, 'rb') as f:
        iv = f.read(16)  # Đọc IV (16 bytes đầu tiên)
        encrypted_data = f.read()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    # Giải mã dữ liệu
    decrypted_padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

    # Gỡ padding
    unpadder = padding.PKCS7(128).unpadder()
    decrypted_data = unpadder.update(decrypted_padded_data) + unpadder.finalize()

    # Ghi dữ liệu giải mã ra file
    with open(output_file, 'wb') as f:
        f.write(decrypted_data)

# Khóa AES (32 bytes cho AES-256)
key = os.urandom(32)
encrypt_language_file("C:\\Users\\duyph\\Desktop\\EHD\\File.py\\ToolDriverPrinter\\Languages\\vi.lng", 'vi.bin', key)
decrypt_language_file("vi.bin", "vi_de.lng", key)
