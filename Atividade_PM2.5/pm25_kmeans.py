import pandas as pd
import numpy as np
from scipy import stats
from sklearn import preprocessing
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

def pearsonr_ci(x,y,alpha=0.05):
   r, p = stats.pearsonr(x, y)
   r_z = np.arctanh(r)
   se = 1 / np.sqrt(x.size - 3)
   z = stats.norm.ppf(1 - alpha / 2)
   lo_z, hi_z = r_z - z * se, r_z + z * se
   lo, hi = np.tanh((lo_z, hi_z))
   return r, p, lo, hi

psra = pd.read_csv('PM25.csv')
df = pd.DataFrame(psra, columns=['year', 'month', 'DEWP', 'TEMP', 'PRES', 'Iws', 'Is', 'Ir'])

print('\nCorrelation:')
print(psra.corr())

# Teste se r está compreendido entre lo e hi
df_columns = df.columns

for i in df_columns:
   for j in df_columns:
      if (i == j):
         continue
      # validade da correlacao
      r, p, lo, hi = pearsonr_ci(df[i],df[j],0.05)
      if ((r>=lo and r<=hi) and (hi-r) < (r-lo)):
         print(i, j, "Correlação positiva")

df_normalizado = pd.get_dummies(psra)

x = df_normalizado.values
min_max_scaler = preprocessing.MinMaxScaler()
x_scaled = min_max_scaler.fit_transform(x)
df_final = pd.DataFrame(x_scaled)
df_final.columns = df_normalizado.columns

kmeans = KMeans(n_clusters=4).fit(df_final)
centroids = kmeans.cluster_centers_
print(centroids)

plt.scatter(df_final['DEWP'], df_final['TEMP'], c=kmeans.labels_.astype(float), s=50, alpha=0.5)
plt.scatter(centroids[:, 0], centroids[:, 1], c='red', s=50)
plt.show()

