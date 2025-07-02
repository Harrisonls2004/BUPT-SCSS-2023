#方法1
'''
v11 = 2
v10 = 7
# 2的模25逆元是13，因为(3*9)%26=1
inv_v11 = 13  
answer = "HIPHSFUPSU"

# 逆向计算原始flag
flag = []
for i in answer:
    encrypted_val = ord(i) -65  # 转换为数字
    # 逆向公式：original = (encrypted - v10) * inv_v11 % 25
    # 加密为(2x+7)%25,即(v11*x+v10)%25,x其实是v6
    original_val = (encrypted_val - v10) * inv_v11 % 25
    original_char = chr(original_val +65)  # 转换回字母
    flag.append(original_char)
flag = ''.join(flag)
print("flag:", flag)
'''
#方法2
def ext_gcd(a, b):  # 扩展欧几里得算法求逆元
    if b == 0:
        return 1, 0, a
    else:
        x, y, gcd = ext_gcd(b, a % b)
        x, y = y, (x - (a // b) * y)
        return x, y, gcd

def affine_decrypt(ciphertext, a, b):
    # 计算 a 的模 25 逆元
    a_inv, _, _ = ext_gcd(a, 25)
    if a_inv < 0:
        a_inv += 25  # 确保逆元是正数

    plaintext = ""
    for char in ciphertext:
        if not char.isupper():
            return "Invalid input! Only A-Z allowed."
        y = ord(char) - 65  # 转为 0-25
        x = (a_inv * (y - b)) % 25  # 解密公式: x = a⁻¹ * (y - b) mod 26
        plaintext += chr(x + 65)  # 转回 A-Z
    return plaintext

# 题目参数
a = 2  # 乘数 
b = 7  # 加数
ciphertext = "HIPHSFUPSU"  # 密文

# 解密
plaintext = affine_decrypt(ciphertext, a, b)
print("解密结果:", plaintext)