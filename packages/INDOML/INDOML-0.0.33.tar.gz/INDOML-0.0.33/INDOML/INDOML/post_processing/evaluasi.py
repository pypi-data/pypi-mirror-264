import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics import silhouette_score
from random import sample
sns.set()

def elbow_method(model, start_cluster:int, end_cluster:int, data:np.ndarray):
    """
    Metode elbow digunakan untuk menentukan jumlah optimal dari cluster dalam algoritma clustering.
    
    Parameters:
        - model (objek model clustering): Model clustering yang digunakan.
        - start_cluster (int): Jumlah cluster awal yang akan dievaluasi.
        - end_cluster (int): Jumlah cluster akhir yang akan dievaluasi.
        - data (np.ndarray): Data yang akan digunakan untuk clustering.
    """
    x = []
    y = []

    for x_ in range(start_cluster, end_cluster):
        k = model(x_)
        k.fit(data)
        insersia = k.inersia_
        x.append(x_)
        y.append(insersia)
    
    plt.plot(x, y, marker='o', linestyle='--')
    plt.title("Optimal Jumlah Cluster")
    plt.xlabel("cluster")
    plt.ylabel("Sum Square Error")
    plt.tight_layout()
    plt.show()

def hopkins_statistik(x:np.ndarray,n_neighbors:int=2):
    """
    Menghitung statistik Hopkins untuk mengukur kecenderungan data untuk berkelompok.

    Parameters:
    x (np.ndarray): Array data yang akan dievaluasi.
    n_neighbors (int, optional): Jumlah tetangga terdekat yang akan digunakan dalam perhitungan. Defaultnya adalah 2.

    Returns:
    float: Nilai statistik Hopkins.

    """
    n = len(x)
    nei = NearestNeighbors(n_neighbors=n_neighbors).fit(x)

    sli = sample(range(0,n,1),n)
    rand_data = [x[i] for i in sli]
    u_distances = nei.kneighbors(x, n_neighbors=n_neighbors)[0][:, -1]
    w_distances = nei.kneighbors(rand_data, n_neighbors=n_neighbors)[0][:, -1]

    hop = np.sum(u_distances)/(np.sum(u_distances)+np.sum(w_distances))

    return hop

def visual_silhoutte(model, start_cluster:int, end_cluster:int, data:np.ndarray):
    """
    Menampilkan grafik Silhouette Score untuk berbagai jumlah cluster.

    Parameters:
        model (function): Fungsi untuk membuat model clustering.
        start_cluster (int): Jumlah cluster awal.
        end_cluster (int): Jumlah cluster akhir.
        data (np.ndarray): Data yang akan digunakan untuk clustering.

    Returns:
        None
    """
    no_cluster = []
    siluette_score = []
    for n in range(start_cluster, end_cluster):
        k = model(n)
        k.fit_predict(data)
        label = k.label__
        siluette_score.append(silhouette_score(data, label))
        no_cluster.append(n)
    
    plt.plot(no_cluster, siluette_score, marker='o', linestyle='--')
    plt.title("Optimal Jumlah Cluster")
    plt.xlabel("cluster")
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.show()

def visual_silhoutte_dbms(model,title:str,xlabel:str,start:int,end:int,step:int,data:np.ndarray,minpts:int=None,epsilon:int=None):
    no_cluster = []
    siluette_score = []
    if epsilon and not minpts:
        for n in range(start,end,step):
            k = model(epsilon,n)
            k.fit_predict(data)
            label = k.label_
            siluette_score.append(silhouette_score(data,label))
            no_cluster.append(n)
    elif minpts and not epsilon:
        while start!=end:
            k = model(start,minpts)
            k.fit_predict(data)
            label = k.label_
            siluette_score.append(silhouette_score(data,label))
            no_cluster.append(start)
            start += step
    
    plt.plot(no_cluster,siluette_score,marker='o',linestyle='--')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel("Silhouette Score")
    plt.tight_layout()
    plt.show()

def silhoutte_skor(label:np.ndarray,data:np.ndarray):
    return silhouette_score(data,label)


def mean_absolute_error(y_true:np.ndarray,y_pred:np.ndarray):
    """
    Menghitung rata-rata kesalahan absolut antara nilai yang sebenarnya (y_true) dan nilai yang diprediksi (y_pred).

    Parameters:
    y_true (np.ndarray): Array numpy yang berisi nilai yang sebenarnya.
    y_pred (np.ndarray): Array numpy yang berisi nilai yang diprediksi.

    Returns:
    float: Rata-rata kesalahan absolut antara y_true dan y_pred.
    """
    delta = y_pred - y_true
    absolut = np.abs(delta)
    total = np.sum(absolut)
    return total/len(y_true)

def mean_square_error(y_true:np.ndarray,y_pred:np.ndarray):
    """
    Menghitung mean square error antara nilai yang sebenarnya (y_true) dan nilai yang diprediksi (y_pred).

    Parameters:
    y_true (np.ndarray): Array numpy yang berisi nilai yang sebenarnya.
    y_pred (np.ndarray): Array numpy yang berisi nilai yang diprediksi.

    Returns:
    float: Nilai mean square error antara y_true dan y_pred.
    """
    delta = (y_pred - y_true)**2
    total = np.sum(delta)
    return total/len(y_true)

def root_mean_square_eroor(y_true:np.ndarray,y_pred:np.ndarray):
    """
    Menghitung akar mean square error (RMSE) antara nilai sebenarnya (y_true) dan nilai prediksi (y_pred).

    Parameters:
    y_true (np.ndarray): Array numpy yang berisi nilai sebenarnya.
    y_pred (np.ndarray): Array numpy yang berisi nilai prediksi.

    Returns:
    np.ndarray: Akar mean square error (RMSE) antara y_true dan y_pred.
    """
    mse = mean_square_error(y_true,y_pred)
    return np.sqrt(mse)

def mean_percentage_error(y_true:np.ndarray,y_pred:np.ndarray):
    """
    Menghitung rata-rata persentase kesalahan antara nilai yang sebenarnya (y_true) dan nilai yang diprediksi (y_pred).

    Parameters:
    y_true (np.ndarray): Array numpy berisi nilai yang sebenarnya.
    y_pred (np.ndarray): Array numpy berisi nilai yang diprediksi.

    Returns:
    float: Rata-rata persentase kesalahan antara y_true dan y_pred.
    """
    delta = (y_pred - y_true)/y_pred
    absolut = np.abs(delta)
    total = np.sum(absolut)
    return (total/len(y_pred))*100