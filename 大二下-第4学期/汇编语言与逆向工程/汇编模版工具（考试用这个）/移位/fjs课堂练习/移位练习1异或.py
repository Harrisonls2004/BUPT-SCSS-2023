s = [0x52, 0xC7, 0xC2, 0xCD, 0xEE, 0xEB, 0xFE, 0xF5]  # 目标字符串
yi = [0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D]

# 存储匹配的 j 值和对应的 ASCII 字符
j_values = []
ascii_chars = []

for i in range(len(s)):
    tmp = s[i]
    target_ascii = tmp
    
    for j in range(36, 160):
        # 位运算：Str[i] = ((Str[i] & 1) << 7) | ((Str[i] & 0x80) >> 7) | Str[i] & 0x7E
        # 最低位左移7位，移动到最高位。最高位右移7位，移动到最低位。中间6位保持不变。
        tmp = ((j & 1) << 7) | ((j & 0x80) >> 7) | (j & 0x7E)
        tmp ^= yi[i]

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