import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, LabelEncoder
import matplotlib.pyplot as mtp
import numpy as np


# Sample data
data = {
    'vehicle_serial_no': [5, 3, 8, 2, 4, 7, 6, 10, 1, 9],
    'mileage': [150000, 120000, 250000, 80000, 100000, 220000, 180000, 300000, 75000, 280000],
    'fuel_efficiency': [15, 18, 10, 22, 20, 12, 16, 8, 24, 9],
    'maintenance_cost': [5000, 4000, 7000, 2000, 3000, 6500, 5500, 8000, 1500, 7500],
    'vehicle_type': ['SUV', 'Sedan', 'Truck', 'Hatchback', 'Sedan', 'Truck', 'SUV', 'Truck', 'Hatchback', 'SUV']
}

df = pd.DataFrame(data)

df = df.drop('vehicle_serial_no', axis=1)

le = LabelEncoder()
df['vehicle_type'] = le.fit_transform(df['vehicle_type'])

x = df[['mileage','fuel_efficiency','maintenance_cost','vehicle_type']]

wcss_list = []

for i in range(1,11):
    kmeans = KMeans(n_clusters=i,init='k-means++',random_state=42)
    kmeans.fit(x)
    wcss_list.append(kmeans.inertia_)

mtp.plot(range(1,11),wcss_list)
mtp.show()

kmeans_no = KMeans(n_clusters=3,init='k-means++',random_state=42)
before_scale = kmeans_no.fit_predict(x)

mtp.figure(figsize=(8, 5))
for i in range(3):
    mtp.scatter(
        df[before_scale == i]["mileage"],
        df[before_scale == i]["fuel_efficiency"],
        s=100, label=f"Cluster {i+1}"
    )
mtp.title("Clusters of Vehicles (Without Scaling)")
mtp.xlabel("Mileage")
mtp.ylabel("Fuel Efficiency")
mtp.legend()
mtp.show()
 
y = df[['mileage','fuel_efficiency','maintenance_cost']]
scalar = StandardScaler()
scaled = scalar.fit_transform(y)

kmeans_scaled = KMeans(n_clusters=3, random_state=42)
clusters = kmeans_scaled.fit_predict(scaled)

df['Cluster'] = clusters

mtp.figure(figsize=(8, 5))
mtp.scatter(scaled[:, 0], scaled[:, 1], c=clusters, cmap='viridis', s=100)
mtp.title('K-means Clustering (k=3)')
mtp.colorbar(label='Cluster')
mtp.show()

print(df)
