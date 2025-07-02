from Crypto.Cipher import DES
#密文字节数组(根据C++中的ciphertext转换)
ciphertext = bytes([0xDB, 0x23, 0xD9, 0xEA, 0xD0, 0x7A, 0x27, 0xCE])
#密钥(来自C++代码中的key)
key = b'DES_EN1C'

# 使用DES ECB模式解密
cipher = DES.new(key,DES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted plaintext:",plaintext.decode())