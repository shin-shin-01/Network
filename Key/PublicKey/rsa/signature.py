## 秘密鍵で署名を作成し、公開鍵で署名の妥当性を検証してみる

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.Signature import pkcs1_15

"""
SHA-256
- Belongs to the SHA-2 family of cryptographic hashes.
  It produces the 256 bit digest of a message.
"""

"""
PKCS1_15
- An old but still solid digital signature scheme based on RSA.
"""

def generate_key():
    ## 秘密鍵の作成
    private_key = RSA.generate(2048)

    with open('private.pem', 'w') as f:
        f.write(private_key.exportKey('PEM').decode('utf-8'))
    
    ## 秘密鍵に基づいて公開鍵を作成
    public_key = private_key.publickey()
    with open('public.pem', 'w') as f:
        f.write(public_key.exportKey('PEM').decode('utf-8'))

def load_key():
    ## Pem-Load
    with open('private.pem', 'br') as f:
        private_pem = f.read()
        private_key = RSA.import_key(private_pem)

    with open('public.pem', 'br') as f:
        public_pem = f.read()
        public_key = RSA.import_key(public_pem)

    return public_key, private_key


def signature(message, private_key):
    ## メッセージと秘密鍵から署名を作成
    """
    SHA256.new(data)
        Parameters: Data (byte string/byte array/memoryview)
        return: SHA-256 hash object.

    Crypto.Signature.pkcs1_15.new(rsa_key)
        Parameters: RSA_Key (RSA object)
        return: a PKCS115_SigScheme signature object
    
    sign(msg_hash)
        Parameters: msg_hash (hash object)
        return: the signature encoded as a byte string.
    """
    h1 = SHA256.new(message.encode())
    sign = pkcs1_15.new(private_key).sign(h1)

    return sign

def verification(message, sign, public_key):
    ## 署名の検証
    """
    verify(msg_hash, signature)
        Parameters
            msg_hash (hash object)
            signature  (byte string) 
        return: Nothing

        Raises: ValueError –if the signature is not valid.
    """

    h2 = SHA256.new(message.encode())
    try:
        pkcs1_15.new(public_key).verify(h2, sign)
        verified = "The signature is valid."
    except ValueError:
        verified = "The signature is not valid."

    return verified

def main():
    message = input('平文：')

    generate_key()
    public_key, private_key = load_key()

    sign = signature(message, private_key)
    verified = verification(message, sign, public_key)

    print('=======================')
    print("署名\n",sign)
    print('=======================')
    print(verified)


if __name__ == "__main__":
    main()






