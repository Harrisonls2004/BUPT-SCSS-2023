def affine_decrypt(ciphertext: str) -> str:
    """解密仿射加密的密文（暴力破解法）"""
    decrypted = []
    for char in ciphertext:
        if 'a' <= char <= 'z':
            # 解方程: (14 * x + 2) % 26 == (ord(char) - 97)
            target = (ord(char) - 97 - 2) % 26
            # 枚举 x ∈ [0,25]，找到满足 14*x ≡ target mod 26
            for x in range(26):
                if (14 * x) % 26 == target:
                    decrypted_char = chr(x + 97)
                    break
        elif 'A' <= char <= 'Z':
            # 解方程: (14 * x + 2) % 26 == (ord(char) - 65)
            target = (ord(char) - 65 - 2) % 26
            for x in range(26):
                if (14 * x) % 26 == target:
                    decrypted_char = chr(x + 65)
                    break
        else:
            decrypted_char = char  # 非字母字符保留原样
        decrypted.append(decrypted_char)
    return ''.join(decrypted)

# 解密示例
ciphertext = "IqqsAwem"  # 替换为你的密文
plaintext = affine_decrypt(ciphertext)
print(f"解密结果: {plaintext}")