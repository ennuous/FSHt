import hashlib
import os
def file_hash(filename):
  h = hashlib.sha1()
  with open(filename, 'rb', buffering=0) as f:
    for b in iter(lambda : f.read(128*1024), b''):
      h.update(b)
  return h.hexdigest()
dirPath = os.path.dirname(os.path.realpath(__file__))
filePath = dirPath + "\\Files\\"
filesPath = ".\\Files\\"
f = []
for root, dirs, files in os.walk(filesPath, topdown=False):
   for name in files:
      f.extend([os.path.join(root, name)[7:]])
table = []
with open(dirPath + "\FSHt\data.FSHt","wb+") as fsht:
    fsht.write(bytearray.fromhex('465348740400000000000000'))
    for file in f:
        print('Adding file...')
        print('   Name: %s' % file)
        bytes = os.path.getsize(filePath + file)
        print('   Size: %s' % bytes)
        offset = fsht.tell()
        print('   Offset: %s' % offset)
        fileHash = file_hash(filePath + file)
        print('   SHA1: %s' % fileHash)
        with open(filePath + file, "rb+") as uf:
            fsht.write(uf.read())
            hashOffset = fsht.tell()
        table.extend([str.encode(file)])
        table.extend([offset.to_bytes(4, byteorder="big")])
        table.extend([bytes.to_bytes(4, byteorder='big')])
        table.extend([bytearray.fromhex(fileHash)])
        table.extend([len(file).to_bytes(4, byteorder='big')])
        fsht.seek(hashOffset)
    fsht.seek(5, 0)
    fsht.write(len(f).to_bytes(4, byteorder='big'))
    fsht.seek(0,2)
    for t in table:
      fsht.write(t)
        
