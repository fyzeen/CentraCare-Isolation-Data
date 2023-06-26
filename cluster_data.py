import pandas as pd
import numpy as np
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.metrics import silhouette_score, calinski_harabasz_score, adjusted_rand_score

df = pd.read_csv("/home/ahmadf/CentraCare/CentraCareIsolation_CLEANED.csv", index_col=0)

data = df.copy()
df = None
for column in ["Diabetes", "Depression", "Alcoholism", "CHF", "COPD", "HTN"]:
    binarized_column = data[column].apply(lambda x: 1 if isinstance(x, str) else 0)
    data[column] = binarized_column

for column in ["Tobacco Use", "vape_user"]:
    binarized_column = data[column].apply(lambda x: 1 if (x=="Yes" or x=="Y") else 0)
    data[column] = binarized_column

clustering_data = data[["Diabetes", "Depression", "HTN", "Tobacco Use", "SocialIntegrationScore"]]
clustering_data = clustering_data.fillna(clustering_data.mean())
clustering_data = clustering_data.to_numpy()


linkage_matrix = linkage(clustering_data, method='ward')
two_cluster_labels = fcluster(linkage_matrix, t=2, criterion='maxclust')
#ten_cluster_labels = fcluster(linkage_matrix, t=10, criterion='maxclust')

pd.DataFrame(two_cluster_labels).to_csv("/home/ahmadf/CentraCare/two_cluster_labels.csv")
#pd.DataFrame(ten_cluster_labels).to_csv("/home/ahmadf/CentraCare/ten_cluster_labels.csv")