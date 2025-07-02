Str=[26,10,14,7,17,7,13,0]
key="realpwd"
flag=""
for i in range(7):
    flag+=chr(Str[i]^ord(key[i]))
print(flag)