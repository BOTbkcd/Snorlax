import subprocess
import random

profiles = subprocess.run(["gsettings", "get", "org.gnome.Terminal.ProfilesList", "list"], capture_output=True).stdout.decode()
profiles = profiles[1:-2].split(',')

for index, profile in enumerate(profiles):
    profiles[index] = profile.strip(" '")

new_profile = profiles[random.randint(0, len(profiles)-1)]

subprocess.run(["gsettings", "set", "org.gnome.Terminal.ProfilesList", "default", new_profile])


