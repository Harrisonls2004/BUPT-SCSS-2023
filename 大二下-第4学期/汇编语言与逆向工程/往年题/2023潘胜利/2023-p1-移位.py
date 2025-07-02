'''
# Destination[i] = Destination[i] & 3 | (16 * (Destination[i] & 0xC)) | ((Destination[i] & 0xF0) >> 2)
# Destination[i] & 3 → 保留最低2位
# 16 * (Destination[i] & 0xC) → 保留中间2位并左移4位
# (Destination[i] & 0xF0) >> 2 → 保留最高4位并右移2位

def decrypt(enc_byte, i):
    low_2bits = (enc_byte >> 6) & 0x03 
    mid_2bits = (enc_byte >> 2) & 0x0C  
    high_4bits = (enc_byte << 4) & 0xF0 
    original_byte = low_2bits | mid_2bits | high_4bits
    original_byte -= i
    return original_byte & 0xFF

byte_429A30 = [0xD5, 0x96, 0xC4, 0xF6, 0x07, 0x45, 0x57, 0x77, 0x76, 0xE5, 0xF6, 0x48, 0x47, 0xF7, 0x48, 0x17]
flag = bytes([decrypt(byte_429A30[i], i) for i in range(16)])
print(flag.decode())
'''


s = [0xD5, 0x96, 0xC4, 0xF6, 0x07, 0x45, 0x57, 0x77, 0x76, 0xE5, 0xF6, 0x48, 0x47, 0xF7, 0x48, 0x17]

# 存储匹配的 j 值和对应的 ASCII 字符
j_values = []
ascii_chars = []

for i in range(len(s)):
    target_byte = s[i]
    
    for j in range(36, 160):
        # 正向加密逻辑（与 decrypt 对应）
        tmp = (j + i) & 0xFF  # 先加 i
        tmp = ((tmp & 3) << 6) | ((tmp & 0x0C) << 2) | ((tmp & 0xF0) >> 4)
        #
        
        if tmp == target_byte:
            # 检查是否是可打印 ASCII 字符
            if 32 <= j <= 126:
                ascii_char = chr(j)
            else:
                ascii_char = "."
            
            j_values.append(j)
            ascii_chars.append(ascii_char)
            break

# 输出连在一起的 j 值（十进制）
print("Matching j values (decimal):", "".join(map(str, j_values)))

# 输出连在一起的 ASCII 字符
print("Corresponding ASCII characters:", "".join(ascii_chars))