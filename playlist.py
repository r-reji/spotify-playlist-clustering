"""  
This file uses the clustered dataset created in cluster.py to create a playlist of songs
for each cluster. The playlist is created in my Spotify account and has been made public. 
This may change in the future but you will still be able to access them via the links on
the GitHub repository.

"""

from credentials import *
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import numpy as np
import pandas as pd
import time
from requests.exceptions import ReadTimeout

redirectURL = 'http://localhost/'

"""
Setup is the same as in data.py - do note that the scope is different to allow us to create 
playlists.
"""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = spotifyClientID, client_secret = spotifyClientSecret, redirect_uri = redirectURL, scope = 'user-library-read playlist-modify-private playlist-modify-public playlist-read-private', requests_timeout = 10))

dataReader = pd.read_csv(folderLoc +'/clusteredData.csv', chunksize = 500, iterator = True)
dfClusteredTracks = pd.concat(dataReader, ignore_index = True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

"""
The following code is used to create a playlist for each cluster. Note that the API limits 
you to 100 sequential requests which is why the upload has been split up and artificial 
delays been introduced. 

"""

for i in range(1, dfClusteredTracks['Cluster'].nunique() + 1):
    playlist = sp.user_playlist_create(username, 'Clustered Playlist ' + str(i), public = True, collaborative = False, description = 'Playlist created from some clustering algorithms I ran on a small section of my stupidly large Spotify library (Info: https://github.com/r-reji/playlistClustering). These playlists are still long ... just imagine the mess they were made from. Hope they are enjoyable!')
    playlistID = playlist['id']
    songs = list(dfClusteredTracks.loc[dfClusteredTracks['Cluster'] == i]['trackID'])
    length = len(songs)
    div = length // 100
    for j in range(div):
        sp.playlist_add_items(playlistID, songs[j*100:(j+1)*100])
        time.sleep(np.random.uniform(0, 10))
        print(str((j+1)*100) + ' tracks uploaded to playlist ' + str(i))
    sp.playlist_add_items(playlistID, songs[div*100:])
    print('Playlist ' + str(i) + ' created')

print('All playlists created')

""" 
The playlists have been created as public, you can view them via the links on the GitHub 
repository even if they are changed to be private in future.

"""