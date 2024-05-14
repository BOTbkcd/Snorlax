import os

PLAYLIST_PATH = '/home/bot_bkcd/Volumes/Reservoir/MUsick/Playlists/'
ARTIST_PATH = '/home/bot_bkcd/Volumes/Reservoir/MUsick/Artists/'
PLAYLIST_DESTINATION_PATH = '/home/bot_bkcd/Volumes/Reservoir/MUsick/Archive/Playlists/'

# os.scandir is the most efficient approach
playlists = [f.path for f in os.scandir(PLAYLIST_PATH) if f.is_dir()]

for playlist in playlists:
		playlist_title = os.path.basename(playlist)
		playlist_content = []
		for f in os.scandir(playlist):
				if(f.is_file()):
						if(f.is_symlink()):
								playlist_content.append(os.readlink(f.path))
						else:
								playlist_content.append(f.path)
													
		playlist_content.sort()
		
		with open(PLAYLIST_DESTINATION_PATH + playlist_title + ".m3u", "w") as m3u_file:
			  m3u_file.write('\n'.join(playlist_content))
				

artists = [f.path for f in os.scandir(ARTIST_PATH) if f.is_dir()]

for artist in artists:
		playlist_title = os.path.basename(artist)
		playlist_content = []
		for f in os.scandir(artist):
				if(f.is_file()):
					playlist_content.append(f.path)

				else:
						album = os.path.basename(f)
						for m in os.scandir(f.path):
								playlist_content.append(m.path)
													
		playlist_content.sort()
		
		with open(PLAYLIST_DESTINATION_PATH + playlist_title + ".m3u", "w") as m3u_file:
			  m3u_file.write('\n'.join(playlist_content))
