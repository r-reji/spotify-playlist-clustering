# spotifyPlaylistClustering

#### This project was an effort to organise my ever-growing Spotify library without having to manually assign thousands of songs to each of my many playlists. It makes use of clustering algorithms uses track audio feature data that is extracted using Spotipy. 

#### If you would like to take a look at the playlists generated check out these links.

The project is written in Python and makes use of Spotipy which is a Python wrapper for the Spotify Web API.

#### Links: [Playlists](#playlist-links) | [Prerequisites](#prerequisites) | [Usage](#usage) | [Interactive Figures](#visualisations)

#### Things to note
- The data set does not take advanteage of every metric available for analysis - this is something that I will revisit in the future. Two of the most important metrics I'd like to take advantage of are `Release Date` and `Popularity` as the current playlists generated have a mix of old a new songs which can be a bit jarring even if the songs are similar.
- During implementation I noticed that a significant proportion (~25%) of the popularity values requested are zero. This is a known issue and is being worked on at the time of writing. This bug has impacted the type of visualisations I can produce and the level of analysis I can conduct - it is something I am looking forward to revisiting in the future.
- Data extraction can take a long time to run (~1.2 seconds per song) depending on the subset of your library you are trying to extract. I have taken steps to introduce artifical delays to avoid hitting an API request limit - feel free to play wiht these values for slightly better performance at the risk of running a timeout error
- As explained in [data.py](https://github.com/r-reji/spotifyPlaylistClustering/blob/main/data.py), you can take advantage of parallel pricessing or multiple API keys for better data extraction performance - this is somthing you will need to implement yourself

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

#### Visualisations
Here I include some of the visualisations generated. There are some other cumulative vairance plots that you can check out in [figures.](https://github.com/r-reji/spotifyPlaylistClustering/tree/main/figures) Please note that the figures that have hyperlinks below will also take you to a lovely interactive version where hovers will give you song information.

- [Figure 1: 'Acousticness' vs 'Speechiness'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/acousticnessSpeechiness.html) 
 
![acousticnessSpeechiness](https://user-images.githubusercontent.com/112977394/196700847-249a9ad7-c260-4439-9805-a51015a95abb.png)

- [Figure 2: 'Energy' vs 'Danceability'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/energyDanceability.html)
 
![energyDanceability](https://user-images.githubusercontent.com/112977394/196703934-d9a6b759-670a-4289-8d9f-6ffc9829447e.png)

- [Figure 3: 'PCA Metric 1' vs 'PCA Metric 2'](https://htmlpreview.github.io/?https://github.com/r-reji/spotifyPlaylistClustering/blob/main/figures/metric1Metric2.html)
 
![metric1Metric2](https://user-images.githubusercontent.com/112977394/196703971-9c4195ac-0e06-488c-8dc2-ce3d2ba45955.png)

- Figure 4: 'PCA Metrics by Cluster'
![pcaMetricsByCluster](https://user-images.githubusercontent.com/112977394/196703998-cd22d9f5-6cf2-4b12-bdbf-16d4b5274a7c.png)

#### Playlist Links
I may change the privacy of the playlists over time so you will need the links to access them. I do not plan to update these playlists at any point but I will be implementing a better clustering solution at some point.

Here are the 7 playlists that were generated from 1929 songs:

- [Playlist 1](https://open.spotify.com/playlist/7EqhbZpWL2bTsl9bYprD5K?si=e7f5399e57174f8e&pt=12ec58d4377c767b39ec00240c12b466)
- [Playlist 2](https://open.spotify.com/playlist/2UjwUlCtMSG5fJqCIUduGb?si=209a9aa128c44168&pt=6a7b668e2915ced615aeeadd45682b79)
- [Playlist 3](https://open.spotify.com/playlist/0LOQHsLS4Ah8qoGEocD2BV?si=464f7d648d3540f2&pt=11064f5efa5ff0877cad71dc363b4370)
- [Playlist 4](https://open.spotify.com/playlist/58zj05l9BBQ7qRF5aZAdJs?si=9b46cf11371440a5&pt=5dbfc33d43751bab5a6585aa7af69f65)
- [Playlist 5](https://open.spotify.com/playlist/2k1O2u8wcWzcfaHjBPBdKo?si=b3a438c17b624043&pt=389dc5a3f1b9268fda20d5a64e183bc5)
- [Playlist 6](https://open.spotify.com/playlist/06YL9wvAiCBQPYSCN1NPkW?si=cf0890c4c4ed4f35&pt=15fcfce0c20dc4dd3d625aa5e1103b5e)
- [Playlist 7](https://open.spotify.com/playlist/1xKk6ZFGqlJ8mBoL9fAKhm?si=ad6d7292e2974fb6)



