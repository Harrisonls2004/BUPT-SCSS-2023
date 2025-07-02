key1=[119, 111, 104, 122, 123, 77, 49, 104, 117, 45, 55, 49,45, 52, 104, 48, 45, 57, 116, 45, 104, 45,33,125]
flag=''
for i in range(24):
    if key1[i]<65 or key1[i]>122:
        flag+=chr(key1[i])
    elif key1[i]<=90:
        for j in range(65,91):
            if ((j-65)*3+7)%26+65==key1[i]:
                flag+=chr(j)
                break
    else:
        for j in range(97,123):
            if ((j-97)*3+7)%26+97==key1[i]:
                flag+=chr(j)
                break

print(flag)
        