import random
import sympy as sym
import random

'''
-- 鍵生成 --
1 ランダムな大きい素数𝑝と、法𝑝における原始根𝑔(1<𝑔<𝑝)を選ぶ。
2 0≤𝑥≤𝑝−2の範囲からランダムに整数𝑥を選ぶ。
3 𝑦≡𝑔^{𝑥} mod𝑝を計算。
公開鍵を(𝑝,𝑔,𝑦)、秘密鍵を𝑥とする。

-- 暗号化 --
1 0≤𝑟≤𝑝−2から整数𝑟をランダムに選ぶ。（暗号化するたびに異なる暗号文になる）
2 𝑐1≡𝑔^{𝑟} mod𝑝、𝑐2≡𝑚𝑦^{𝑟} mod𝑝を計算。
これにより計算された組(𝑐1,𝑐2)が暗号文になる。

-- 復号化 --
𝑐2𝑐1^{𝑝−1−𝑥} mod𝑝
原理：m*(y^{r}*g^{r(p-1-x)})=m(g^{rx}*g^{rp-r-rx}) = m(g^{r(p-1)})
'''


'''原始根
3以上の素数pと1以上p未満の整数rにおいて
「r, r^2, ..., r^(p-2)のいずれもがpで割って余り1ではない」
上記が成り立つときに rを法pに対する原始根と呼ぶ
(modに関してp-1でループする)
'''

'''位数
「r, r^2, ...」とした時，
初めて，pで割った余りが１になるときの指数を「rの位数」という
→　pに対して位数がp-1となるrを原始根という
'''


def key_generate(p):
    g = sym.primitive_root(p) ## 原始根 今度自分で実装
    x = random.randint(0, p-1)
    y = pow(g, x, p)

    return (p, g, y), x


def encrypt(public, m):
    p, g, y = public
    r = random.randint(0, p-2)

    c1 = pow(g, r, p)
    c2 = []

    for l in m:
        c2.append(l*pow(y, r) % p)

    return (c1, c2)

def decrypt(cipher, public, private):
    c1, c2 = cipher
    p, g, y = public
    x = private

    decode_text = ''
    for c in c2:
        m = (c * pow(c1, p-1-x)) % p
        decode_text += chr(m)

    return decode_text



if __name__ == "__main__":
    number = 1000 ## number番目の素数
    p = sym.prime(number)
    public, private = key_generate(p)

    prain_text = input('Input Prain-text: ')
    prain_code = list(map(ord, prain_text))

    cipher = encrypt(public, prain_code)
    decode_text = decrypt(cipher, public, private)

    print('=='*10)
    print('公開鍵 ( p, g, y ) : ', public)
    print('秘密鍵 x = : ', private)
    print('平文（文字コード）: ', prain_code)
    print(f'暗号文 : c1={cipher[0]}, c2={cipher[1]}')
    print('復号文 : ', decode_text)

    print('=='*10)
    print('成功' if prain_text==decode_text else '失敗')
