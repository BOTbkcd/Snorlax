
import subprocess
from pathlib import Path

# Location where nnn store the selected files
# The file paths are seperated by null byte
NNN_SELECTION = '/home/bot_bkcd/.config/nnn/.selection'

def sanitizePath(fileName):
    return fileName.replace("'", "\\'")

with open(NNN_SELECTION, 'rb') as file:
    raw_data = file.read()
    list = raw_data.split(b'\0')

for item in list:
    subprocess.run(["kid3-cli", "-c", f"set title '{sanitizePath(Path(item.decode()).stem)}'", Path(item.decode())])


