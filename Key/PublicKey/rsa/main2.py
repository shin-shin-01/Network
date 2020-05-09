## 暗号化ライブラリ　使用して作ってみる

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

"""
pem の書式（鍵＋証明書）

-----BEGIN RSA PRIVATE KEY-----
鍵ファイルのｂase64エンコード
-----END RSA PRIVATE KEY-----
-----BEGIN CERTIFICATE-----
証明書ファイルのｂase64エンコード
-----END CERTIFICATE-----
"""

"""
PKCS1_OAEP：RSAおよびOAEPパディングに基づく非対称暗号。
"""


def generate_key():
    ## 秘密鍵の作成
    private_key = RSA.generate(2048)

    with open('private.pem', 'w') as f:
        f.write(private_key.exportKey('PEM').decode('utf-8'))

    ## 秘密鍵に基づいて公開鍵を作成
    ## private_key.publickey
    public_key = private_key.publickey()
    with open('public.pem', 'w') as f:
        f.write(public_key.exportKey('PEM').decode('utf-8'))

def load_key():
    ## pem-Load
    with open('private.pem', 'br') as f:
        private_pem = f.read()
        print("[ Print Private-PemFile ]\n", private_pem)
        private_key = RSA.import_key(private_pem)

    with open('public.pem', 'br') as f:
        public_pem = f.read()
        public_key = RSA.import_key(public_pem)

    return public_key, private_key


def encrypt(message, key):
    ## メッセージの暗号化
    """
    PKCS1_OAEP.new
        return: Cipher object

    PKCS1_OAEP.new.encrypt()
        Parameters: Message (bytes/bytearray/memoryview)
        return: The Ciphertext, as large as the RSA modulus. (bytes)
    """
    public_cipher = PKCS1_OAEP.new(key)
    encrypted_text = public_cipher.encrypt(message.encode())

    return encrypted_text

def decrypt(encrypted_text, key):
    ## メッセージの復号
    """
    PKCS1_OAEP.new
        return: Cipher object

    PKCS1_OAEP.new.encrypt()
        Parameters: Ciphertext (bytes/bytearray/memoryview)
        return: The original message (bytes)
    """
    private_cipher = PKCS1_OAEP.new(key)
    decrypted_text = private_cipher.decrypt(encrypted_text).decode('utf-8')

    return decrypted_text


def main():
    message = input("平文入力：")

    generate_key()
    public_key, private_key = load_key()    

    encrypted_text = encrypt(message, public_key)
    decrypted_text = decrypt(encrypted_text, private_key)

    print('========================')
    print('公開鍵：', public_key)
    print('暗号文\n', (encrypted_text))
    print('========================')
    print('秘密鍵：', private_key)
    print('復号文\n', (decrypted_text))
    print('========================')
    print("成功しました" if message == decrypted_text else "失敗しました")


if __name__ == "__main__":
    main()