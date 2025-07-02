def ext_gcd(a, b):  # 扩展欧几里得算法求逆元
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = ext_gcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, gcd

def affine_decrypt(ciphertext, a, b):
    # 计算 a 的模 26 逆元
    a_inv, _, _ = ext_gcd(a, 26)
    if a_inv < 0:
        a_inv += 26  # 确保逆元是正数

    plaintext = ""
    for char in ciphertext:
        y = ord(char) - 97  # 转为 0-25
        x = (a_inv * (y - b)) % 26  # 解密公式: x = a⁻¹ * (y - b) mod 26
        plaintext += chr(x + 97)  # 转回 a-z
    return plaintext

# 题目参数
a = 5  # 乘数 (v12)
b = 5  # 位移 (v11)
ciphertext = "jmzfwgfibz"  # 密文

# 解密
plaintext = affine_decrypt(ciphertext, a, b)
print("解密结果:", plaintext)