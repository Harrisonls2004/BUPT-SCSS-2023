a = '1f2e28649c4g:25:8bb:24c3D3EGF6GFg22dff:1dbd916df13239513g21e4663'
b = []

for char in a:
    # Decrement the ASCII value by 1 and convert back to character
    new_char = chr(ord(char) - 1)
    b.append(new_char)

# Convert the list to a string
b = ''.join(b)
print(b)