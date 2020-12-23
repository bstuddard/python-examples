from sklearn.cluster import KMeans
import numpy as np
import pandas as pd

def cluster_houses(input_data):
    """Cluster housing data using KMeans

    Args:
        input_data (dict): api request data containing houses to be clustered

    Returns:
        list: list of dict objects containing row and cluster group
    """
    data = pd.DataFrame.from_dict(input_data).to_numpy()
    kmeans = KMeans(n_clusters=3, random_state=42).fit(data)
    return [{'row': (i+1), 'group': label} for i, label in enumerate(kmeans.labels_)]