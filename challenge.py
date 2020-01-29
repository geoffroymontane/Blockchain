from hashlib import sha256
import random



n = random.randint(0, 999999999)
hash = sha256(str(n).encode("utf-8")).hexdigest()
while hash[0:5] != "00000":
    n += 1
    hash = sha256(str(n).encode("utf-8")).hexdigest()


print(n)
print(hash)

