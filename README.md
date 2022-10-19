# spotifyPlaylistClustering

#### This project was an effort to organise my ever-growing Spotify library without having to manually assign thousands of songs to each of my many playlists. It makes use of clustering algorithms uses track audio feature data that is extracted using Spotipy. 

#### If you would like to take a look at the playlists generated check out these links.

The project is written in Python and makes use of the Spotipy which is a Python wrapper for the Spotify Web API.

#### Links: Playlists | Prerequisites | Usage | Interactive Figures

#### Things to note
- The data set does not take advanteage of every metric available for analysis - this is something that I will revisit in the future. Two of the most important metrics I'd like to take advantage of are `Release Date` and `Popularity` as the current playlists generated have a mix of old a new songs which can be a bit jarring even if the songs are similar.
- During implementation I noticed that a significant proportion (~25%) of the popularity values requested are zero. This is a known issue and is being worked on at the time of writing. This bug has impacted the type of visualisations I can produce and the level of analysis I can conduct - it is something I am looking forward to revisiting in the future.
- Data extraction can take a long time to run depending on the subset of your library you are trying to extract.

#### Prerequisites

- The Spotify Web API needs your API key to authenticate any requests. You can set this up after signing up on the [Spotify developer dashboard.](https://developer.spotify.com)
- Setting up an app on the dashboard will give you access to the `spotifyClientID` and `spotifyClientSecret` variables which will be used later.
- You will also need to specify a redirect URL and make sure to use the same in your code
- All the details of my API key have been kept in a seperate Python file called `credentials.py`
   - You can either do the same or add your API Key details directly into each file
   - I have also kept file paths in `credentials.py` so please add the necessary paths
  
#### Dependancies
Please make sure you have installed the necessary libraries before running the files. 
The data used for this file is generated from `data.py` and contains a small subset of my Spotify library (information for ~2000 songs). This data may not be representative of your own library.

#### Usage
I have included detailed exmplanations of each file within them, here I will provide a top line overview.

- [data.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/data.py)
   - Extracts song data from any spotify playlist using your API key
   - Request audio feature data for each song and collates it into a .csv file
- [cluster.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/cluster.py)
   - Selects the data for analysis and standardises it for forther analysis
   - Perform principle component analysis to reduce the complexity of the data set
   - Use the WCSS (within-cluster sum of squares) metric and the elbow method to implement a k-means clustering algorithm
- [playlist.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/playlist.py)
   - Uses the clustered data produced form the k-means algorithm to define playlists
   - Makes use of user specific authentication to automatically generate a playlist for each cluster in your Spotify library




