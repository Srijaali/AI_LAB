import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

student_ids = [f'S{1000+i}' for i in range(200)]
gpas = np.round(np.random.normal(3.0, 0.5, 200).clip(1.0, 4.0), 2)
study_hours = np.round(np.random.normal(15, 5, 200).clip(5, 30), 1)
attendance = np.round(np.random.normal(80, 10, 200).clip(50, 100), 1)

# Create DataFrame
df = pd.DataFrame({
    'student_id': student_ids,
    'GPA': gpas,
    'study_hours': study_hours,
    'attendance_rate': attendance
})

features = df[['GPA','study_hours','attendance_rate']]

scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

wcss_list = []

for i in range(1,11):
    kmeans  = KMeans(n_clusters=i,random_state=42)
    kmeans.fit(scaled_features)
    wcss_list.append(kmeans.inertia_)
    
plt.plot(range(1,11),wcss_list)
plt.show()

k = KMeans(n_clusters=4,random_state=42)
clusters = k.fit_predict(scaled_features)

df['Clusters'] = clusters

colors = ['red', 'blue', 'green', 'purple', 'orange', 'brown']
for i in range(3):
    cluster_data = df[df['Clusters'] == i]
    plt.scatter(cluster_data['study_hours'], cluster_data['GPA'], 
                color=colors[i], label=f'Cluster {i}', alpha=0.7)
    
plt.xlabel('Weekly Study Hours')
plt.ylabel('GPA')
plt.title('Student Clusters Based on Study Hours and GPA')
plt.legend()
plt.grid()
plt.show()

print(df)
