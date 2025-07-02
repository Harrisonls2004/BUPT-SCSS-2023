from Crypto.Cipher import DES
#密文字节数组(根据C++中的ciphertext转换)
ciphertext = bytes([0x28, 0x70, 0x77, 0x48, 0x7B, 0x4F, 0xFF, 0x3D])
#密钥(来自C++代码中的key)
key = b'TakeEasy'

# 使用DES ECB模式解密
cipher = DES.new(key,DES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted plaintext:",plaintext.decode())