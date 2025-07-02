# 解题思路：1.先利用IDA调试，初步判断秘密为18位，有除零异常
# 2.OD动态调试，设置异常时忽略其他异常，只看除零异常，F9调试，然后输入一个18位密码，然后通过视图中的SEH链找到异常函数的起始位置（那个表就是第一个函数的起始位置）
# 3.返回IDA找到对应的起始位置，反编译进行判断
# 4.根据变化条件判断，原文进行变化后，其中的每一个数值会从ABCDEFGH变为ABCDGHEF
# 5.求出的flag为16位，后面随便加两位作为密码就能得到“Congratulations! You are right!”
res=[0x5C,0x65,0x6C, 0x75, 0x78, 0x66, 0x71, 0x76,  0x46, 0x7C ,0x50, 0x75 ,0x7A, 0x7A, 0x63, 0x65]
flag=""
for i in range(16):
    res[i]=(4 * (res[i] & 3)) | ((res[i] & 0xC) >> 2) | res[i] & 0xF0
    flag+=chr(res[i])
print(flag)