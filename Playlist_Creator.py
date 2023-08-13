import os

PLAYLIST_PATH = '/home/bot_bkcd/Volumes/Reservoir/MUsick/Playlists/'
PLAYLIST_DESTINATION_PATH = '/home/bot_bkcd/Volumes/Reservoir/MUsick/'

# os.scandir is the most efficient approach
playlists = [f.path for f in os.scandir(PLAYLIST_PATH) if f.is_dir()]

for playlist in playlists:
      playlist_title = os.path.basename(playlist)
      playlist_content = [("Playlists/" + playlist_title + "/" + f.name ) for f in os.scandir(playlist) if f.is_file()] 

      with open(PLAYLIST_DESTINATION_PATH + playlist_title + ".m3u", "w") as m3u_file:
        m3u_file.write('\n'.join(playlist_content))