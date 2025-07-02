import hashlib

target = "382e766581df7c496ef87244f943dedcd74d6b6aab8af8789df88a6a22d170eb" 
         #493f877692ea8d507fa98355a054efede85e7c7bbc9ba9890ea99b7b33e281fc
         #先0变成:、a变g、最后全部减去1
def modify_hash(h):
    result = []
    for c in h:
        new_c = chr(ord(c) + 1)
        if new_c == 'g':
            new_c = 'a'
        elif new_c == ':':
            new_c = '0'
        result.append(new_c)
    return ''.join(result)

for a in range(32, 127):
    for b in range(32, 127):
        for c in range(32, 127):
            for d in range(32, 127):
                s = chr(a) + chr(b) + chr(c) + chr(d)
                h = hashlib.sha256(s.encode()).hexdigest()
                if modify_hash(h) == target:
                    print("Found:", s)
                    exit()
print("Not found.")