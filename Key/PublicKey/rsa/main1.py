### Implement without a library

"""暗号化方式
暗号文 = 平文　**(E) mod N  公開鍵:{E, N}
平文　 = 暗号文**(D) mod N  秘密鍵:{D, N}

N = p * q (ランダムで十分に大きい素数 p, q)
L = (p-1)(q-1)
E : gcd(E, L) = 1 (1<E<L) (互いに素)
D : (E * D) mod L = 1 (1<D<L)
"""

from math import gcd


def generate_keys(p, q):
    """公開鍵・秘密鍵の作成
    p, q : 素数

    public_key  : (Encr, N)
    plivate_key : (Decr, N)
    """

    N = p * q
    L = (p-1)*(q-1)
    Encr = 2
    while True:
        if gcd(Encr, L) == 1:
            break
        Encr += 1

    Decr = 2
    while True:
        if Encr*Decr % L == 1:
            break
        Decr += 1

    return (Encr, N), (Decr, N)


def encrypt(text, key):
    """
    平文の暗号化
    plain_text
    public_ley: Encr, N

    => Text^{Encr} 𝑚𝑜𝑑 N

    return encrypted_text
    """
    encrypted_text = ''
    for s in list(text):
        encrypted_text += chr(pow(ord(s), key[0], key[1]))

    return encrypted_text


def decrypt(text, key):
    """
    暗号文の複号化
    encrypted_text
    plivate_key: Decr, N

    => Encr_Text^{Decr} 𝑚𝑜𝑑 N

    return decrypted_text
    """

    decrypted_text = ''

    for s in list(text):
        decrypted_text += chr(pow(int(ord(s)), key[0], key[1]))

    return decrypted_text


def main():
    plain_text = input("平文入力：")

    public_key, plivate_key= generate_keys(229, 2083)

    encrypted_text = encrypt(plain_text, public_key)
    decrypted_text = decrypt(encrypted_text, plivate_key)

    print("====================")
    print("公開鍵：", public_key)
    print("暗号化\n", encrypted_text)
    print("====================")
    print("秘密鍵：", plivate_key)
    print("復号化\n", decrypted_text)
    print("====================")
    print("成功しました" if plain_text == decrypted_text else "失敗しました")


if __name__ == "__main__":
    main()

    