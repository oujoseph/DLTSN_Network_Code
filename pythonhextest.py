import binascii

x = "READ"
y = x.encode("hex") + "0A"
aa = binascii.unhexlify(y)
print aa
print len(aa)
z = "0013a20040daebd0"
a = binascii.unhexlify(z)
# print a
