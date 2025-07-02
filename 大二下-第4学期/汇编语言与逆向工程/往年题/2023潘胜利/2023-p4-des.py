from Crypto.Cipher import DES
#密文字节数组(根据C++中的ciphertext转换)
ciphertext = bytes([0x42, 0xAC, 0x43, 0xD3, 0xF1, 0x44, 0xB1, 0x36])
#密钥(来自C++代码中的key)
key = b'#$12*&^)'

# 使用DES ECB模式解密
cipher = DES.new(key,DES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted plaintext:",plaintext.decode())