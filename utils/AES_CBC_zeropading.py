
import base64

from Crypto.Cipher import AES


def unzip_aes(encrypted_text):
    key = 'UJVQsx54ZY6wRqF1'
    aes = AES.new(str.encode(key), AES.MODE_ECB)
    decrypted_text = str(
        aes.decrypt(base64.decodebytes(bytes(encrypted_text, encoding='utf8'))).rstrip(b'\0').decode("utf8"))  # 解密
    print('解密值：', decrypted_text)
    return decrypted_text

