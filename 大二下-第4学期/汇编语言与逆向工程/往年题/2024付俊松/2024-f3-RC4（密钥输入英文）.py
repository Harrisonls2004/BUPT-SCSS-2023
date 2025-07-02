def rc4_decrypt(ciphertext, key):
    # 1. 密钥预处理：每个字节异或0x76
    key = bytes([b ^ 0x76 for b in key.encode()])
    key_len = len(key)
    
    # 2. RC4 KSA (Key-Scheduling Algorithm)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_len]) % 256
        S[i], S[j] = S[j], S[i]
    
    # 3. PRGA (Pseudo-Random Generation Algorithm) 生成密钥流
    i = j = 0
    keystream = []
    for _ in range(len(ciphertext)):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    
    # 4. 解密：密文异或密钥流
    plaintext = bytes([ciphertext[k] ^ keystream[k] for k in range(len(ciphertext))])
    return plaintext

# --- 使用示例 ---
if __name__ == "__main__":
    # 假设已知：
    encrypted_data = [0x61,0x6E,0x92,0x2C,0xEF,0x13,0x8B,0x13,0x28]  # 替换为实际的 byte_429B30 数据
    guessed_key = "EBPF1SGOOD"               # 替换为可能的密钥（如flag前缀）
    
    # 解密
    decrypted = rc4_decrypt(encrypted_data, guessed_key)
    print(f"解密结果: {decrypted} (Hex: {decrypted.hex()})")