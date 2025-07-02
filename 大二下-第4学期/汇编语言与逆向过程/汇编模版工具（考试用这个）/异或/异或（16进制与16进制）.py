from Crypto.Util.number import bytes_to_long, long_to_bytes

# 原始数据（去掉空格和 0x 前缀）
c_hex = "52 67 75 61 6B 72 7F 5C 61 62 70 72"
d_hex = "01 02 03 04 05 06 06 05 04 03 02 01"

# 转换为字节列表
c_bytes = bytes.fromhex(c_hex.replace(" ", ""))
d_bytes = bytes.fromhex(d_hex.replace(" ", ""))

# 逐字节异或
result = bytes([c ^ d for c, d in zip(c_bytes, d_bytes)])

print("解密结果:", result.decode('ascii'))