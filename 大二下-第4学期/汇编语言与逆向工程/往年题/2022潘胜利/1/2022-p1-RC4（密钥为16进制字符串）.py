def rc4_decrypt_hex_key(ciphertext, hex_key_str):
    # 1. 将十六进制字符串（如 "FCFB3B"）转换为字节（如 b'\xFC\xFB\x3B'）
    key = bytes.fromhex(hex_key_str)  # 关键修改点
    
    # 2. 可选：密钥预处理（如异或0x76，如果加密方做了同样操作）
    # key = bytes([b ^ 0x76 for b in key])  # 如果需要预处理则取消注释
    
    # 3. RC4 KSA + PRGA 解密流程
    S = list(range(256))
    j = 0
    for i in range(256):  # KSA
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    
    i = j = 0
    keystream = []
    for _ in range(len(ciphertext)):  # PRGA
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    
    # 4. 解密：密文异或密钥流
    plaintext = bytes([ciphertext[k] ^ keystream[k] for k in range(len(ciphertext))])
    return plaintext

# --- 使用示例 ---
if __name__ == "__main__":
    # 输入数据
    encrypted_data = [0x6E, 0x65, 0x11, 0xCF, 0x1D, 0x80, 0x3B, 0x4E, 0x20, 0x2A, 0xE0, 0xB6]  # 替换为你的密文
    hex_key_str = "FCFB3B0D736E"  # 直接输入十六进制字符串（如从IDA提取的密钥）
    
    # 解密
    decrypted = rc4_decrypt_hex_key(encrypted_data, hex_key_str)
    print(f"解密结果: {decrypted} (Hex: {decrypted.hex()})")