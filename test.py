import os
import sys
import merkle

print("\nlen(sys.argv):", len(sys.argv))
if len(sys.argv) < 2:
    sys.exit()

print("\nName of file:", sys.argv[1])
f = open(sys.argv[1], "r")

size = os.path.getsize(sys.argv[1])
print("\nSize of file: ", size)

data = f.read().encode('utf-8')
print("\ndata: ", data)

root = merkle.create(data, 50)

merkle.printMerkleTree(root)
