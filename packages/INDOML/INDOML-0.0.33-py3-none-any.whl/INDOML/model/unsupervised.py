"""
Kumpulan algoritma unsupervised learning
"""
import numpy as np
import seaborn as sns
from ..matematika.distance import euclidian_distance,kuadrat_jarak

class Kmeans:
    """
    Implementasi algoritma K-Means untuk pengelompokan data tanpa supervisi.

    Parameters:
    - cluster (int): Jumlah cluster yang diinginkan. Default: 2.
    - inital_centroid (None or dict): Pusat-pusat awal untuk setiap cluster. Jika None, pusat-pusat awal akan diinisialisasi secara acak. Default: None.
    - limit_loop (int): Batas iterasi maksimum. Default: 300.
    - konvergen (None or int): Jumlah iterasi yang diperlukan untuk mencapai konvergensi. Jika None, tidak ada konvergensi yang diperlukan. Default: None.
    - random_state (int): Seed untuk menghasilkan angka acak. Default: 2.
    """

    def __init__(self, cluster: int = 2, inital_centroid=None, limit_loop: int = 300, konvergen=None, random_state: int = 2):
        self.__cluster = cluster
        self.__inital_centroid = inital_centroid
        self.__limit_loop = limit_loop
        self.__historycentroid = {}
        self.__konvergen = konvergen
        self.__random_state = random_state
        self.__cluster_fit = None
        self.__inersia = None
        self.__x = None
        self.__label = None

    @property
    def inersia(self):
        """
        Getter untuk mengakses nilai inersia dari model K-Means.

        Returns:
        - inersia (float): Nilai inersia dari model K-Means.
        """
        pass

    @property
    def label(self):
        """
        Getter untuk mengakses label hasil pengelompokan data.

        Returns:
        - label (np.ndarray): Array numpy berisi label hasil pengelompokan data.
        """
        pass

    def sethistory_centroid(self, loop, list_centroid):
        """
        Menyimpan pusat-pusat centroid pada iterasi tertentu.

        Parameters:
        - loop: Nomor iterasi.
        - list_centroid: Daftar pusat-pusat centroid pada iterasi tersebut.
        """
        self.__historycentroid[loop] = list_centroid

    def history_centroid(self) -> dict:
        """
        Mengembalikan dictionary yang berisi daftar pusat-pusat centroid pada setiap iterasi.

        Returns:
        - historycentroid (dict): Dictionary yang berisi daftar pusat-pusat centroid pada setiap iterasi.
        """
        return self.__historycentroid

    def fit_predict(self, x: np.ndarray) -> np.ndarray:
        """
        Melakukan pengelompokan data menggunakan model K-Means dan mengembalikan label hasil pengelompokan.

        Parameters:
        - x (np.ndarray): Array numpy berisi data yang akan dikelompokkan.

        Returns:
        - predict (np.ndarray): Array numpy berisi label hasil pengelompokan data.
        """
        self.__x = x
        self.fit(x)
        predict = [None for _ in range(len(x))]
        for key3 in self.__cluster_fit.keys():
            for index in self.__cluster_fit[key3]:
                predict[index] = key3
        self.__label = np.array(predict)
        return np.array(predict)

    def fit(self, x: np.ndarray):
        """
        Melakukan proses training model K-Means.

        Parameters:
        - x (np.ndarray): Array numpy berisi data yang akan digunakan untuk training.
        """
        self.__x = x
        np.random.seed(self.__random_state)
        if self.__inital_centroid == None:
            self.__inital_centroid = {}
            for i in range(self.__cluster):
                centroid = x[np.random.choice(x.shape[0], 1, replace=False)]
                self.__inital_centroid[i] = list(centroid)
        loop = 0
        konv = 0
        while loop < self.__limit_loop:
            cluster = {}
            for i in range(self.__cluster):
                cluster[i] = []
            self.sethistory_centroid(loop, self.__inital_centroid)
            for index, value in enumerate(x):
                cls = None
                jrk = None
                for key in self.__inital_centroid.keys():
                    jarak = euclidian_distance(value, np.array(self.__inital_centroid[key]))
                    if jrk == None or jarak <= jrk:
                        jrk = jarak
                        cls = key
                cluster[cls].append(index)
            update_centroid = {}

            for key2 in cluster.keys():
                if len(cluster[key2]) != 0:
                    init = x[cluster[key2][0]].copy()
                    for rec in cluster[key2][1:]:
                        init += x[rec].copy()
                    init = init / len(cluster[key2])
                else:
                    init = list(x[np.random.choice(x.shape[0], 1, replace=False)])

                update_centroid[key2] = list(init)

            if konv == self.__konvergen:
                break

            if update_centroid == self.__inital_centroid:
                konv += 1
            else:
                self.__inital_centroid = update_centroid
            loop += 1

        self.__cluster_fit = cluster

    @inersia.getter
    def inersia_(self):
        """
        Getter untuk mengakses nilai inersia dari model K-Means.

        Returns:
        - inersia (float): Nilai inersia dari model K-Means.
        """
        total = 0

        for key in self.__cluster_fit.keys():
            centroid = self.__inital_centroid[key]
            for rec in self.__cluster_fit[key]:
                total += kuadrat_jarak(self.__x[rec], np.array(centroid))
        self.__inersia = total
        return self.__inersia

    @label.getter
    def label__(self):
        """
        Getter untuk mengakses label hasil pengelompokan data.

        Returns:
        - label (np.ndarray): Array numpy berisi label hasil pengelompokan data.
        """
        return self.__label

class DBscan:
    """
    Implementasi algoritma DBSCAN (Density-Based Spatial Clustering of Applications with Noise).

    Parameters:
    - eps (float): Jarak maksimum antara dua sampel agar dianggap tetangga.
    - minpts (int): Jumlah minimum sampel dalam radius eps agar suatu sampel dianggap sebagai core point.

    Attributes:
    - label (numpy.ndarray): Label hasil klasterisasi setelah pemanggilan metode `fit_predict`.
    - jarak (list): Daftar jarak antara setiap pasangan sampel yang dihitung selama pemanggilan metode `fit`.

    Methods:
    - fit(x: np.ndarray): Melakukan klasterisasi pada data x.
    - fit_predict(x: np.ndarray) -> np.ndarray: Melakukan klasterisasi pada data x dan mengembalikan label hasil klasterisasi.
    """

    def __init__(self, eps: float, minpts: int):
        self.__eps = eps
        self.__minpts = minpts
        self.__cluster = {}
        self.__label = None
        self.__jarak = []

    @property
    def label(self):
        """
        Properti label untuk mengakses label hasil klasterisasi.

        Returns:
        - label (numpy.ndarray): Label hasil klasterisasi.
        """
        return self.__label

    @property
    def jarak(self):
        """
        Properti jarak untuk mengakses daftar jarak antara setiap pasangan sampel yang dihitung selama pemanggilan metode `fit`.

        Returns:
        - jarak (list): Daftar jarak antara setiap pasangan sampel.
        """
        return self.__jarak

    def fit(self, x: np.ndarray):
        """
        Melakukan klasterisasi pada data x.

        Parameters:
        - x (np.ndarray): Data yang akan dikelompokkan.

        Returns:
        - None
        """
        cluster = 1
        visited = []
        unvisited = [i for i in range(len(x))]
        noise = []
        N = []
        while len(unvisited) != 0:
            init = np.random.choice(unvisited, 1, replace=False)[0]
            visited.append(init)
            unvisited.remove(init)
            elemen = []
            for index, value in enumerate(x):
                if index != init:
                    jarak = euclidian_distance(x[init], value)
                    self.__jarak.append(jarak)
                    if jarak <= self.__eps:
                        N.append(index)

            if len(N) >= self.__minpts:
                elemen.append(init)
            else:
                N = []
                noise.append(init)

            while len(N) > 0:

                if N[0] not in visited:
                    visited.append(N[0])
                    unvisited.remove(N[0])
                el2 = []
                for idx2, value in enumerate(x):
                    if N[0] != idx2:
                        jarak = euclidian_distance(x[N[0]], value)
                        self.__jarak.append(jarak)
                        if jarak <= self.__eps:
                            el2.append(idx2)
                if len(el2) >= self.__minpts:
                    for j in el2:
                        if j not in visited and j not in N and j not in noise:
                            N.append(j)

                found = False
                for lst in self.__cluster.values():

                    if N[0] in lst:
                        found = True
                        break
                if not found:
                    elemen.append(N[0])

                N.pop(0)

            if len(elemen) > 0:
                self.__cluster[cluster] = elemen
                cluster += 1
        self.__cluster[-1] = noise

    def fit_predict(self, x: np.ndarray) -> np.ndarray:
        """
        Melakukan klasterisasi pada data x dan mengembalikan label hasil klasterisasi.

        Parameters:
        - x (np.ndarray): Data yang akan dikelompokkan.

        Returns:
        - label (numpy.ndarray): Label hasil klasterisasi.
        """
        self.fit(x.copy())
        predict = [None for _ in range(len(x))]
        for key in self.__cluster.keys():
            for index in self.__cluster[key]:
                predict[index] = key
        self.__label = np.array(predict)
        return self.__label

    @label.getter
    def label_(self):
        """
        Properti label_ untuk mengakses label hasil klasterisasi.

        Returns:
        - label (numpy.ndarray): Label hasil klasterisasi.
        """
        return self.__label

    @jarak.getter
    def jarak_(self):
        """
        Properti jarak_ untuk mengakses daftar jarak antara setiap pasangan sampel yang dihitung selama pemanggilan metode `fit`.

        Returns:
        - jarak (list): Daftar jarak antara setiap pasangan sampel.
        """
        return self.__jarak

    
                    

                





                

            

            




    

    
