from Crypto.Cipher import DES
#密文字节数组(根据C++中的ciphertext转换)
ciphertext = bytes([0x8F, 0x90, 0xE0, 0x4E, 0x67, 0x1E, 0x7F, 0x92])
#密钥(来自C++代码中的key)
key = b'SONGFENR'

# 使用DES ECB模式解密
cipher = DES.new(key,DES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted plaintext:",plaintext.decode())