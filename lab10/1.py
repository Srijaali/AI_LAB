import numpy as np
import matplotlib.pyplot as mtp
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder

# Load data
df = pd.read_csv('Mall_Customers.csv')

# Drop CustomerID and encode Gender
x = df.drop(columns=["CustomerID"])
le = LabelEncoder()
x["Gender"] = le.fit_transform(x['Gender'])

# Elbow Method
wcss_list = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init="k-means++", random_state=42)
    kmeans.fit(x)
    wcss_list.append(kmeans.inertia_)

mtp.plot(range(1, 11), wcss_list)
mtp.title("The Elbow Method (No Scaling)")
mtp.xlabel("Number of clusters (k)")
mtp.ylabel("WCSS")
mtp.show()

# KMeans without scaling
kmeans_no_scale = KMeans(n_clusters=5, random_state=42)
y_predict_no_scale = kmeans_no_scale.fit_predict(x)

mtp.figure(figsize=(8, 5))
colors = ['blue', 'green', 'red', 'black', 'purple']
for i in range(5):
    mtp.scatter(
        x[y_predict_no_scale == i]["Annual Income (k$)"],
        x[y_predict_no_scale == i]["Spending Score (1-100)"],
        s=100, c=colors[i], label=f"Cluster {i+1}"
    )

mtp.title("Clusters of Customers (Without Scaling)")
mtp.xlabel("Annual Income (k$)")
mtp.ylabel("Spending Score (1-100)")
mtp.legend()
mtp.show()

x_scaled = x.drop(columns=["Age"])
scaler = StandardScaler()
scaled_features = scaler.fit_transform(x_scaled)

final_scaled_data = pd.concat([x["Age"].reset_index(drop=True), 
                               pd.DataFrame(scaled_features, columns=x_scaled.columns)], axis=1)

kmeans_scaled = KMeans(n_clusters=5, random_state=42)
y_predict_scaled = kmeans_scaled.fit_predict(final_scaled_data)

x["Cluster_Scaled"] = y_predict_scaled

mtp.figure(figsize=(8, 5))
for i in range(5):
    cluster_data = x[x["Cluster_Scaled"] == i]
    mtp.scatter(
        cluster_data["Annual Income (k$)"],
        cluster_data["Spending Score (1-100)"],
        s=100, c=colors[i], label=f"Cluster {i+1}"
    )

mtp.title("Clusters of Customers (With Scaling except Age)")
mtp.xlabel("Annual Income (k$)")
mtp.ylabel("Spending Score (1-100)")
mtp.legend()
mtp.show()
