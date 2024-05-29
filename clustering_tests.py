import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score, adjusted_rand_score

df = pd.read_csv("~/CentraCare/CentraCareIsolation_CLEANED.csv", index_col=0)

data = df.copy()
df = None
for column in ["Diabetes", "Depression", "Alcoholism", "CHF", "COPD", "HTN"]:
    binarized_column = data[column].apply(lambda x: 1 if isinstance(x, str) else 0)
    data[column] = binarized_column

for column in ["Tobacco Use", "vape_user"]:
    binarized_column = data[column].apply(lambda x: 1 if (x=="Yes" or x=="Y") else 0)
    data[column] = binarized_column

clustering_data = data[["Diabetes", "Depression", "HTN", "Tobacco Use", "Isolation_YN"]]
clustering_data = clustering_data.fillna(clustering_data.mean())
clustering_data = clustering_data.to_numpy()

cluster_range = range(2, 11)

# Initialize lists to store scores
silhouette_scores = []
variance_ratios = []

# Perform hierarchical clustering for each number of clusters
for n_clusters in cluster_range:
    print(n_clusters)
    # Perform hierarchical clustering
    linkage_matrix = linkage(clustering_data, method='ward')
    labels = fcluster(linkage_matrix, t=n_clusters, criterion='maxclust')

    
    # Compute silhouette score
    silhouette_scores.append(silhouette_score(clustering_data, labels))
    
    # Compute variance ratio criterion
    variance_ratios.append(calinski_harabasz_score(clustering_data, labels))

print(silhouette_scores)
print(variance_ratios)