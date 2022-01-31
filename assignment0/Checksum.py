import zlib
import sys

user_src_file = sys.argv[1]

with open(f"{user_src_file}", "rb") as f:
    bytes = f.read()

checksum = zlib.crc32(bytes)
print(checksum)