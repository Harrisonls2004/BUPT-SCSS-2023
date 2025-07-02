# 题目中给定的硬编码数据
v6 = "@URU@KE"  # 目标字符串
v5 = [2, 0, 2, 1, 6, 1, 22]  # XOR密钥（前7个字节）

# 计算正确的输入
correct_input = ''.join([chr(ord(v6_char) ^ v5[i]) for i, v6_char in enumerate(v6)])

print("正确的输入是:", correct_input)

# 验证解密是否正确
print("\n验证解密过程:")
for i in range(7):
    print(f"字符 {correct_input[i]} (ASCII: {ord(correct_input[i]):3d}) "
          f"^ {v5[i]:2d} = {ord(correct_input[i]) ^ v5[i]:3d} "
          f"→ {chr(ord(correct_input[i]) ^ v5[i])}")