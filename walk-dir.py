import os
from pathlib import Path

root_path = ""

for root, dirs, file in os.walk("C:/Users/Martin RATH/Documents"):
    print(dirs)
