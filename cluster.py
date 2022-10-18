""" 
This file will implement Principal Component Analysis (PCA) on the data set and use K-Means Clustering
to cluster the data set in such a way that we can produce playlists in the playlist.py file. There are
a number of possible methodologies and I have gone into some detail in the comments below and in
the README.md file on GitHub.

Note : At the time of writing there is an issue with the Spotify API that causes the SPI value to be 
returned as 0 for a significant number of tracks. This is a known issue and is being worked on by
Spotify. As a result, the 'popularity' values have not been used at any point for any analysis 
which mainly effects the visualisation of the clusters that can be made. This is something I will 
revisit in future to produce better representations of the data.

Note 2: I have tried to be consistent in using 'features' to mean the audio feature 
values produced by Spotify's machine learning algorithm and 'metrics' to any metric that has 
been generated via PCA. However, there may be times that I have used both interchangeably - 
this is NOT INTENTIONAL. The most egregious case of this is my choice of naming 
dfTrackMetrics which of course refers to a dataframe containing only the audio features.
Similarly, 'partition' and 'cluster' should be treated as the same thing.

Advance apologies for my inconsistencies in writing.

"""

from credentials import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import image
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
import plotly.express as px
from requests.exceptions import ReadTimeout
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from yellowbrick.cluster import KElbowVisualizer

"""
Import the csv file and store as a pandas dataframe. 

"""

dataReader = pd.read_csv(filePath, chunksize = 500, iterator = True)
dfTrackData = pd.concat(dataReader, ignore_index = True)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

"""
Start by restricting our dataset to only the features that we can use for analysis and model 
building. Any high level overview will probably be unnecessary due to the chaotic nature of 
my spotify library.

The data also needs to be standardised such that each of our features has a mean of 
0 and standard deviation of 1. This is done to ensure that the features are on the same scale 
and that the model is not biased towards any particular feature.

"""


infoMetrics = ['trackName', 'artistName', 'trackID', 'trackURI', 'duration (min)']
dfTrackInfo = dfTrackData[infoMetrics]
dfTrackMetrics = dfTrackData.drop(columns = infoMetrics)

scaler = StandardScaler()
trackMetricsSTD = scaler.fit_transform(dfTrackMetrics)
dfTrackMetricsSTD = pd.DataFrame(trackMetricsSTD, columns = dfTrackMetrics.columns)

""" 
We can now use PCA to reduce the dimensionality of our dataset. This is done to reduce the
effective complexity of our model and to reduce the number of features that we need to 
consider. This will also help us to visualise our data in 2D. Some information will be lost 
by reducing the dimensionality of our dataset however by computing the best possible subset 
of our features by considering the variance of each feature, we can ensure that our 
approximation is 'good'.

"""

pca = PCA()
pca.fit(trackMetricsSTD)

"""
The variance ratio is used to determine how impactful each of our features is on 
the variance distribution of our dataset.  

"""
evr = pca.explained_variance_ratio_

figure = plt.figure(figsize = (10, 10))
plt.plot(range(1, len(dfTrackMetrics.columns)+1), evr.cumsum(), marker = 'o', linestyle = '--')
plt.xlabel('Number of Features')
plt.ylabel('Cumulative Explained Variance')
fig = plt.savefig(folderLoc + '/cumVarPlot.png')

"""
Generally a cumulative variance ratio of 0.8 is considered to be a good approximation however 
due to having a massive dataset a value of 0.9 will be used to compute the optimal number of 
features to use.

"""

for i, expVar in enumerate(evr.cumsum()):
    if expVar > 0.8:
        pcaMetrics = i + 1
        #print(pcaMetrics)
        break

""" 
The above code has determined that the ideal number of features to use is 8. A new PCA object 
was instantiated with components parameter = 8 to give us the best possible subset of our 
data with 8 different data points derived from our initial 12 - these are the new metrics we 
will use for any further analysis.

The next task is to determine the optimal number of clusters for a k-mean clustering 
algorithm; this will be done algorithmically with the elbow method. THe within-cluster sum of 
squares (wcss) metric will be used to determine the 'density' of each partition. The optimal 
cluster number can then be computed by considering the graph of WCSS against partitions to 
find the 'elbow' of the graph.

"""

pca = PCA(n_components = pcaMetrics)
pca.fit(trackMetricsSTD)
pcaScores = pca.transform(trackMetricsSTD)

visualiser = KElbowVisualizer(KMeans(init = 'k-means++'), k = (1, 20), timings = False)
visualiser.fit(pcaScores)
#visualiser.show()
numClusters = visualiser.elbow_value_
kmeansPCA = KMeans(n_clusters = numClusters, init = 'k-means++', random_state = 42)
kmeansPCA.fit(pcaScores)

"""
The above code has determined that the optimal number of clusters is 7 and now we can apply 
the k-means clustering algorithm wrt (with respect to) the 8 new metrics that we derived to 
cluster our entire dataset. The clusters can then be added back to the original dataframe.

"""

dfPcaKMeans = pd.concat([dfTrackMetrics.reset_index(drop = True), pd.DataFrame(pcaScores)], axis = 1)
dfPcaKMeans.columns.values[(-1*pcaMetrics):] = ['Metric ' + str(i+1) for i in range(pcaMetrics)]
dfPcaKMeans['Cluster'] = kmeansPCA.labels_

"""
The original dataframe can now be saved into a new CSV file which can be used to generate the 
clustered playlists in the playlists.py file. The merged dataframe can now be used to produce 
some visualisations on each of the clusters to further understand the data. 
""" 

dfTrackData['Cluster'] = dfPcaKMeans['Cluster'] + 1
dfTrackData['Metric 1'] = dfPcaKMeans['Metric 1']
dfTrackData['Metric 2'] = dfPcaKMeans['Metric 2']
dfTrackData['Metric 3'] = dfPcaKMeans['Metric 3']
dfTrackData['Metric 4'] = dfPcaKMeans['Metric 4']
dfTrackData['Metric 5'] = dfPcaKMeans['Metric 5']
dfTrackData['Metric 6'] = dfPcaKMeans['Metric 6']
dfTrackData['Metric 7'] = dfPcaKMeans['Metric 7']
dfTrackData['Metric 8'] = dfPcaKMeans['Metric 8']

dfTrackData.to_csv(folderLoc + '/clusteredData.csv')

"""
The data can now be clustered wrt any pair of each of the new metrics or each of 
the original audio features. As an example the data will be visualised as metric 1 : metric 
2 and metric 3 : metric 4. Feel free to try out different combinations of metrics to see how
relevant each metric is within each cluster. 

"""

fig = px.scatter(dfTrackData, x = 'Metric 1', y = 'Metric 2', color = 'Cluster', hover_data = ['trackName', 'artistName'])
plt.xlabel('Metric 1')
plt.ylabel('Metric 2')
fig.write_image(folderLoc + '/metric1Metric2.png')
fig.write_html(folderLoc + '/metric1Metric2.html')
#fig.show()
fig = px.scatter(dfTrackData, x = 'energy', y = 'danceability', color = 'Cluster', hover_data = ['trackName', 'artistName'])
plt.xlabel('Energy')
plt.ylabel('Danceability')
fig.write_image(folderLoc + '/energyDanceability.png')
fig.write_html(folderLoc + '/energyDanceability.html') 
#fig.show()
fig = px.scatter(dfTrackData, x = 'acousticness', y = 'speechiness', color = 'Cluster', hover_data = ['trackName', 'artistName'])
plt.xlabel('Acousticness')
plt.ylabel('Speechiness')
fig.write_image(folderLoc + '/acousticnessSpeechiness.png')
fig.write_html(folderLoc + '/acousticnessSpeechiness.html')
#fig.show()

""" 
Another type of visualisation that is of interest to me is an intra-cluster spread of the 
original audio features. This can be done by computing the mean of each audio feature for 
each cluster and then plotting the mean of each audio feature against the cluster number. 
This will give us a visualisation of how each audio feature is distributed within each 
cluster. The cluster chart has been broken up into two for easier viewing.

It's expected that the charts wrt our original features should produce visualisations that 
look very similar. This is because broadly speaking the songs in my library are not very 
diverse and so the clusters are not very distinct.

By creating charts that visualise the clusters wrt the PCA metrics, we can expect to see 
more distinct differences between each cluster.

Note: The charts below are not that useful due to the issues with SPI returns mentioned in 
Note 2. I will revisit this in the future. Also the plots that have been made with plotly 
express have proved to be somewhat unreliable and so I will recommend you use Seaborn if you
decided to produce any yourself.

"""

def makeFig(df, clusterNum):
    fig = go.Figure()
    cmap = cm.get_cmap('tab20')
    angles = list(df.columns[18:])
    angles.append(angles[0])

    layoutDict = dict(radialaxis = dict(visible = True, range = [0, 1]))
    subset = df[df['Cluster'] == clusterNum]
    data = [np.mean(subset[col]) for col in angles]
    data.append(data[0])

    fig.add_trace(go.Scatterpolar(r = data, fill = 'toself', theta = angles, mode = 'lines', name = 'Cluster ' + str(clusterNum), line_color ='rgba' + str(cmap(clusterNum/7))))   
    
    fig.update_layout(polar = layoutDict)
    fig.update_traces()
    return fig

clusterFigs = make_subplots(rows = 4, cols = 3, specs = [[{'type': 'polar'}]*3 for i in range(4)])
for i in range(7):
    for t in makeFig(dfTrackData, i + 1).data:
        rownum = i%4 + 1
        clusterFigs.append_trace(t, row = rownum, col = (i)%3 + 1)
        fig.update_layout(polar = dict(radialaxis = dict(visible = True, range = [0, 1], showticklabels = False), angularaxis = dict(showticklabels = False)), showlegend = False )  
#clusterFigs.show()