r = [0x35, 0x2F, 0x2F, 0x32, 0x28, 0x14, 0x27, 0x3B, 0x3D, 0x70,
     0x3C, 0x0A, 0x3D, 0x73, 0x3A, 0x0A, 0x1F, 0x73, 0x3D, 0x66,
     0x21, 0x1C, 0x6D, 0x28]
key = 'SCNU'

flag = ''
for i in range(len(r)):
    flag += chr(ord(key[i % 4]) ^ r[i])

print(flag) # flag{Winn3r_n0t_L0s3r_#}