#[79,81,76,102,107,102,103,21,27,23,19]
import numpy as np
from sklearn.cluster import MeanShift, estimate_bandwidth

'''
#x = [1,1,5,6,1,5,10,22,23,23,50,51,51,52,100,112,130,500,512,600,12000,12230]
x = [79,79,79,78]
X = np.array(zip(x,np.zeros(len(x))), dtype=np.int)
bandwidth = estimate_bandwidth(X, quantile=0.5)
ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
print n_clusters_

for k in range(n_clusters_):
    my_members = labels == k
    print "cluster {0}: {1}".format(k, X[my_members, 0])
'''

def cluster(x):
	X = np.array(zip(x,np.zeros(len(x))), dtype=np.int)
	bandwidth = estimate_bandwidth(X, quantile=1)
	ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
	ms.fit(X)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)
	#print n_clusters_
	return n_clusters_