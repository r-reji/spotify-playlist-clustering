# Spotify Playlist Clustering

#### This project was an effort to organise my ever-growing Spotify library without having to manually assign thousands of songs to each of my many playlists. It makes use of clustering algorithms on track audio feature data that is extracted using [Spotipy](https://spotipy.readthedocs.io/en/2.21.0/). 

#### If you would like to take a look at the playlists generated check out these links.

The project is written in Python and makes use of Spotipy which is a Python wrapper for the Spotify Web API.

#### Links: [Playlists](#playlist-links) | [Prerequisites](#prerequisites) | [Usage](#usage) | [Visualisations](#visualisations)

#### Things to note
- The data set does not take advantage of every metric available for analysis - this is something that I will revisit in the future. Two of the most important metrics I'd like to take advantage of are `Release Date` and `Popularity` as the current playlists generated have a mix of old and new songs which can be quite jarring even if the songs are similar.
- During implementation, I noticed that a significant proportion (~25%) of the popularity values requested are zero. This is a known issue and is being worked on at the time of writing. This bug has impacted the type of visualisations I can produce and the level of analysis I can conduct - it is something I am looking forward to revisiting in the future.
- Data extraction can take a long time to run (~1.2 seconds per song) depending on the subset of your library you are trying to extract. I have taken steps to introduce artificial delays to avoid hitting an API request limit - feel free to play with these values for slightly better performance at the risk of running a timeout error.
- As explained in [data.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/data.py), you can take advantage of parallel processing or multiple API keys for better data extraction performance - this is something you will need to implement yourself!

#### Prerequisites

- The Spotify Web API needs your API key to authenticate any requests. You can set this up after signing up on the [Spotify developer dashboard.](https://developer.spotify.com)
- Setting up an app on the dashboard will give you access to the `spotifyClientID` and `spotifyClientSecret` variables which will be used later.
- You will also need to specify a redirect URL and make sure to use the same in your code
- All the details of my API key have been kept in a separate Python file called `credentials.py`
   - You can either do the same or add your API Key details directly into each file
   - I have also kept file paths in `credentials.py` so please add the necessary paths
  
#### Dependencies
Please make sure you have installed the necessary libraries before running the files. 
The data used for these files is generated from `data.py` and contains a small subset of my Spotify library (data on 1929 songs). This data may not be representative of your own library.

#### Usage
I have included detailed explanations of each file within them, here I provide a top-line overview.

- [data.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/data.py)
   - Extracts song data from any Spotify playlist using your API key
   - Request audio feature data for each song and collates it into a .csv file
- [cluster.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/cluster.py)
   - Selects the data for analysis and standardises it for further analysis
   - Performs principle component analysis to reduce the complexity of the data set
   - Use the WCSS (within-cluster sum of squares) metric and the elbow method to implement a k-means clustering algorithm
- [playlist.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/playlist.py)
   - Uses the clustered data produced from the k-means algorithm to define playlists
   - Makes use of user-specific authentication to automatically generate a playlist for each cluster in your Spotify library

#### Visualisations
Here I include some of the visualisations generated. There are some other cumulative variance plots that you can check out in [figures.](https://github.com/r-reji/spotifyPlaylistClustering/tree/main/figures) 

**Note:** the hyperlinked figures will take you to a version that displays song information on hover!


- [Figure 1: 'Acousticness' vs 'Speechiness'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/acousticnessSpeechiness.html) 
 
>![acousticnessSpeechiness](https://user-images.githubusercontent.com/112977394/196700847-249a9ad7-c260-4439-9805-a51015a95abb.png)

- [Figure 2: 'Energy' vs 'Danceability'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/energyDanceability.html)
 
>![energyDanceability](https://user-images.githubusercontent.com/112977394/196703934-d9a6b759-670a-4289-8d9f-6ffc9829447e.png)

- [Figure 3: 'PCA Metric 1' vs 'PCA Metric 2'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/metric1Metric2.html)
 
>![metric1Metric2](https://user-images.githubusercontent.com/112977394/196703971-9c4195ac-0e06-488c-8dc2-ce3d2ba45955.png)

- Figure 4: 'PCA Metrics by Cluster'

>![pcaMetricsByCluster](https://user-images.githubusercontent.com/112977394/196703998-cd22d9f5-6cf2-4b12-bdbf-16d4b5274a7c.png)

#### Playlist Links
These playlists will most likely remain untouched by me except for potential privacy changes. In any case, you will still be able to access them through the links below.

- [Playlist 1](https://open.spotify.com/playlist/7EqhbZpWL2bTsl9bYprD5K?si=1a457b9c0aac41b9)
- [Playlist 2](https://open.spotify.com/playlist/2UjwUlCtMSG5fJqCIUduGb?si=3abe588148574e70)
- [Playlist 3](https://open.spotify.com/playlist/0LOQHsLS4Ah8qoGEocD2BV?si=4184afd542fa49d2)
- [Playlist 4](https://open.spotify.com/playlist/58zj05l9BBQ7qRF5aZAdJs?si=557c8f26d93f4f20)
- [Playlist 5](https://open.spotify.com/playlist/2k1O2u8wcWzcfaHjBPBdKo?si=e3e0c6a016134024)
- [Playlist 6](https://open.spotify.com/playlist/06YL9wvAiCBQPYSCN1NPkW?si=410add145ff4458e)
- [Playlist 7](https://open.spotify.com/playlist/1xKk6ZFGqlJ8mBoL9fAKhm?si=02840b7989b34129)

At some point I will be starting another project with the aim of consolidating my **whole** library with an entirely new clustering solution and implement a few more features but until then hopefully these playlists will be enjoyable!


