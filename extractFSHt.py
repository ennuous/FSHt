import hashlib
import os

dirPath = os.path.dirname(os.path.realpath(__file__))

with open('data.fsht', 'rb+') as fsht:
  type = fsht.read(4).decode('UTF8')
  if type == 'FSHt':
    print('Yes, it\'s a FSHt file')
    fsht.seek(4)
    version = hex(int.from_bytes(fsht.read(1), byteorder='big'))[2:]
    print("FSHt Version 1.0%s" % version)
  else:
    print('No, it\'s not a FSHt file')
    exit()
  files = int.from_bytes(fsht.read(4), byteorder='big')
  print("There are %.0f file(s)" % files)
  if not os.path.exists(dirPath + "\\Extracts\\"):
    os.makedirs(dirPath + "\\Extracts\\")
  for f in range(0, files):
    print("Extracting file %.0f..." % (f))
    if f == 0:
      fsht.seek(0,2)
    else:
      fsht.seek(dataOffset -1)
    fsht.seek(-3, 1)
    pathSize = int.from_bytes(fsht.read(4), byteorder='big')
    fsht.seek(-24, 1)
    oldHash = hex(int.from_bytes(fsht.read(20), byteorder='big'))[2:]
    if len(oldHash) == 39:
      oldHash = "0" + oldHash
    elif len(oldHash) == 38:
      oldHash = "00" + oldHash
    fsht.seek(-24, 1)
    size = int.from_bytes(fsht.read(4), byteorder='big')
    fsht.seek(-8, 1)
    offset = int.from_bytes(fsht.read(4), byteorder='big')
    fsht.seek(-4 - pathSize, 1)
    path = fsht.read(pathSize).decode('UTF8')
    print("   Name: %s" % path)
    print("   Offset: %s" % offset)
    print("   Size: %s" % size)
    print("   SHA1: %s" % oldHash)
    fsht.seek(-pathSize, 1)
    dataOffset = fsht.tell()
    fsht.seek(offset); file = fsht.read(size)
    newHash = hashlib.sha1(file).hexdigest()
    path = dirPath + "\\Extracts\\" + path
    if newHash == oldHash:
      os.makedirs(os.path.dirname(path), exist_ok=True)
      with open("%s" % path, "wb+") as n:
        n.write(file)
    else:
      print("SHA1 doesn't match, skipping file.")
  print("Process complete.")
