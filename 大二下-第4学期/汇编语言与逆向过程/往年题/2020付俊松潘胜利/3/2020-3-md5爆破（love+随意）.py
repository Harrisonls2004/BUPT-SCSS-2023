import hashlib

dic = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'

for a in dic:
    for b in dic:
        for c in dic:
            for d in dic:
                t = str(a) + str(b) + str(c) +str(d)
                amd5 = hashlib.md5(t.encode(encoding='UTF-8')).hexdigest()      #md5(),sha1(),sha256(),sha512()
                if amd5[:32] == 'b5c0b187fe309af0f4d35982fd961d7e':             #32/40/64/128 自己找哈希值并改变长度
                    print(t)