s = "\eluxfqvF|Puzzce"  # 目标字符串

# 存储匹配的 j 值和对应的 ASCII 字符
j_values = []
ascii_chars = []

for i in range(len(s)):
    target_char = s[i]
    target_ascii = ord(target_char)
    
    for j in range(36, 160):
        # 位运算：(4*(j&3)) | ((j&0xC)>>2) | (j&0xF0)
        tmp = (4 * (j & 3)) | ((j & 0xC) >> 2) | (j & 0xF0)
        
        if tmp == target_ascii:
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