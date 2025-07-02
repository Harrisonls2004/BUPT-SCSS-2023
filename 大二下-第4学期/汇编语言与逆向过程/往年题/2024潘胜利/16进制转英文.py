hex_str = " 6c6f7665"  # "Hello World" 的 Hex

# 转换为 bytes 再解码为 ASCII
text = bytes.fromhex(hex_str).decode('ascii')

print(text)  # 输出: Hello World