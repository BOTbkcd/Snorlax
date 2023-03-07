import subprocess
from pathlib import Path

# Location where nnn store the selected files
# The file paths are seperated by null byte
NNN_SELECTION = '/home/bot_bkcd/.config/nnn/.selection'

with open(NNN_SELECTION, 'rb') as file:
    raw_data = file.read()
    list = raw_data.split(b'\0')

for item in list:
    subprocess.run(["chmod", "666", Path(item.decode())])

