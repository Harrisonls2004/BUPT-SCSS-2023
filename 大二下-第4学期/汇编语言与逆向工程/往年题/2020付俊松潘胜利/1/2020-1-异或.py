from Crypto.Util.number import bytes_to_long, long_to_bytes

# 原始数据（去掉空格和 0x 前缀）
c_hex = "42 61 7F 69 5F 62 6C 66 41 74 6C 61 6D 66 72"
d_hex = "0F 0E 0D 0C 0B 0A 09 08 07 06 05 04 03 02 01"

# 转换为字节列表
c_bytes = bytes.fromhex(c_hex.replace(" ", ""))
d_bytes = bytes.fromhex(d_hex.replace(" ", ""))

# 逐字节异或
result = bytes([c ^ d for c, d in zip(c_bytes, d_bytes)])

print("解密结果:", result.decode('ascii'))