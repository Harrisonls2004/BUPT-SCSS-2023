from Crypto.Util.number import *
c = 0x331911320D27211122101127283D36
d = 0x787878787878787878787878787878
print(long_to_bytes(c^d))
