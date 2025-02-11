buf = []

def gets(buf):
    data = input("> ")
    for i in data:
        buf.append(i)

print "Welcome 2 HASHCTF"
try:
    gets(buf)
except:
    pass