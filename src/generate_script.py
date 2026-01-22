import os 
import time
from pathlib import Path
import random
import string

BASE = Path(r"C:\Xyno\DesMume\_test")
BASE.mkdir(exist_ok=True)

def rand_name():
    return ''.join(random.choices(string.ascii_lowercase, k=8)) + ".txt"

files = []

for _ in range(30):
    p = BASE / rand_name()
    with open(p, "w") as f:
        f.write("test\n")
    files.append(p)
    time.sleep(0.1)

time.sleep(1)
for p in files:
    p.unlink()
    time.sleep(0.05)