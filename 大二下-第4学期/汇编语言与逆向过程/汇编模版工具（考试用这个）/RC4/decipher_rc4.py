# -*- coding: utf-8 -*-
from Crypto.Cipher import ARC4

def encrypt(message, key):    # 加密
    des = ARC4.new(key)
    cipher_text = des.encrypt(message)
    
    return cipher_text

def decrypt(cipher_text, key): # 解密
    des3 = ARC4.new(key)
    message = des3.decrypt(cipher_text)
    
    return message

if __name__ == "__main__":
    key = 'RC4key'.encode("utf8")
    
    # message = 'Is_Th13_Simple_Rc4?'.encode("utf8")    
    # cipher_text = encrypt(message, key)
    # print('密文:', cipher_text.hex().upper())
    
    cipher_text = b'\x1B\xCA\xAE\xEF\x1E\x95\x4B\xC2\xD5\xE3\x33\x76\x4F\xF9\x4F\xD2\xFC\x60\x96'  
    message = decrypt(cipher_text, key)
    print('得到的\'FLAG\':', message.decode("utf-8"))
    