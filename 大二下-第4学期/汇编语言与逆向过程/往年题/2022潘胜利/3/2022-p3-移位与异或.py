mid = [0x06, 0x07, 0x08, 0x09, 0x0A, 0x0B, 0x0C, 0x0D]
fin = [0x52, 0xC7, 0xC2, 0xCD, 0xEE, 0xEB, 0xFE, 0xF5]

# 存储匹配的 j 值
j_values = []
# 存储对应的 ASCII 字符
ascii_chars = []

for i in range(8):
    for j in range(36, 160):
        Str = j
        # Perform the bit manipulation
        tmp = ((Str & 1) << 7) | ((Str & 0x80) >> 7) | (Str & 0x7E)
        tmp ^= mid[i]
        if tmp == fin[i]:
            j_values.append(j)
            # Check if j is a printable ASCII character (32-126)
            if 32 <= j <= 126:
                ascii_chars.append(chr(j))
            else:
                ascii_chars.append(".")  # Non-printable character
            break

# 输出 j 值（十进制）
print("Matching j values (decimal):", " ".join(map(str, j_values)))

# 输出对应的 ASCII 字符
print("Corresponding ASCII characters:", " ".join(ascii_chars))