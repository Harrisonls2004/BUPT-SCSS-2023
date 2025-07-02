byte_429A30 = [0xBD, 0x9A, 0x9E, 0x8B, 0xD5, 0xCF, 0x92, 0x96, 0x9C, 0x8D, 0x90, 0x91, 0xD5, 0xDE]

# 计算 FLAG 的每个字节
FLAG = [b ^ 0xFF for b in byte_429A30]

# 转换为 16 进制字符串
flag_hex = " ".join(f"{b:02X}" for b in FLAG)
print("FLAG (hex):", flag_hex)

# 转换为 ASCII 字符串（如果可能是可打印字符）
flag_ascii = "".join(chr(b) if 32 <= b <= 126 else "." for b in FLAG)
print("FLAG (ASCII):", flag_ascii)