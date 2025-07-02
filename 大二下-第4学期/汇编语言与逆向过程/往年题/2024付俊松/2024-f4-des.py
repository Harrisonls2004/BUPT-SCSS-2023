from Crypto.Cipher import DES
#密文字节数组(根据C++中的ciphertext转换)
ciphertext = bytes([0xCD, 0x49, 0x33, 0x09, 0xF3, 0x23, 0x21, 0x8A])
#密钥(来自C++代码中的key)
key = (0xEF34D4A3C684E423).to_bytes(8, byteorder='big')

# 使用DES ECB模式解密
cipher = DES.new(key,DES.MODE_ECB)
plaintext = cipher.decrypt(ciphertext)

print("Decrypted plaintext:",plaintext.decode())