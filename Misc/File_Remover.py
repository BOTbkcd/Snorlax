import os
import re

ROOT_FOLDER = "/home/bot_bkcd/Volumes/Blitzkrieg/JavaScript/Angular/Udemy"

for root, dirs, files in os.walk(ROOT_FOLDER):
    for file in files:
        if re.search(".*srt", file):    
            os.remove(os.path.join(root,file))
