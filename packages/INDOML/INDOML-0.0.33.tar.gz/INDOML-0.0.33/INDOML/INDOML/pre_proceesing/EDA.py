import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
sns.set()

class Visualisasi:
    """
    Kelas untuk visualisasi data dengan konstruktor dataframe pandas.
    """

    def __init__(self, data):
        """
        Inisialisasi objek Visualisasi dengan data.

        Parameters:
        - data (pandas.DataFrame): Dataframe pandas yang akan divisualisasikan.
        """
        self.__data = data
    
    def setData(self, data):
        """
        Mengatur data yang akan divisualisasikan.

        Parameters:
        - data (pandas.DataFrame): Dataframe pandas yang akan divisualisasikan.
        """
        self.__data = data
    
    def getData(self):
        """
        Mengembalikan data yang akan divisualisasikan.

        Returns:
        - data (pandas.DataFrame): Dataframe pandas yang akan divisualisasikan.
        """
        return self.__data
    
    def distribusi(self):
        """
        Menampilkan distribusi untuk setiap kolom dalam bentuk histogram.
        """
        num_kolom = len(self.__data.columns)
        num_rows = (num_kolom + 4) // 5
        num_rows = min(15, num_rows)

        fig, axes = plt.subplots(num_rows, 5, figsize=(30, 20))
    
        for i, kolom in enumerate(self.__data.columns):
            row = i // 5
            col = i % 5
            sns.histplot(self.__data[kolom], kde=True, ax=axes[row, col])
    
        for i in range(num_kolom, num_rows * 5):
            row = i // 5
            col = i % 5
            fig.delaxes(axes[row, col])
    
        fig.suptitle('Distribusi untuk Setiap Kolom', y=1.02)

        plt.tight_layout()
        plt.show()

    def box_plot(self, kolom):
        """
        Menampilkan box plot untuk kolom tertentu.

        Parameters:
        - kolom (str): Nama kolom yang akan divisualisasikan.
        """
        sns.set(rc={'figure.figsize': (38, 10)})
        melted_data = pd.melt(self.__data, value_vars=kolom, var_name="variabel", value_name="value")
        ax = sns.boxplot(x="variabel", y="value", data=melted_data)
        ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
        plt.show()
    
    def scatter(self, kolom):
        """
        Menampilkan scatter plot untuk setiap kolom terhadap kolom tertentu.

        Parameters:
        - kolom (str): Nama kolom yang akan divisualisasikan.
        """
        num_kolom = len(self.__data.columns)
        num_rows = (num_kolom + 4) // 5
        num_rows = min(15, num_rows)

        fig, axes = plt.subplots(num_rows, 5, figsize=(30, 20))

        for i, colu in enumerate(self.__data.columns):
            row = i // 5
            col = i % 5
            axes[row, col].scatter(x=self.__data[colu], y=self.__data[kolom])
            axes[row, col].set_xlabel(colu)

        for i in range(num_kolom, num_rows * 5):
            row = i // 5
            col = i % 5
            fig.delaxes(axes[row, col])
    
        fig.suptitle(f'Scatter plot untuk Setiap Kolom terhadap {kolom}', y=1.02)

        plt.tight_layout()
        return plt
    
    def heatmapkor(self):
        """
        Menampilkan heatmap korelasi antar kolom.
        """
        korelasi = self.__data.corr()
        plt.figure(figsize=(8, 6))
        sns.heatmap(korelasi, annot=True, cmap='coolwarm', linewidths=.5)

        plt.title('Heatmap Korelasi')
        plt.show()
    
    def regplot(self, colom_x):
        """
        Menampilkan regplot untuk setiap kolom terhadap kolom tertentu.

        Parameters:
        - colom_x (str): Nama kolom yang akan menjadi sumbu x dalam regplot.
        """
        fig, axes = plt.subplots(1, len(self.__data.columns), figsize=(15, 5))

        for index, y in enumerate(self.__data.columns):
            sns.regplot(x=colom_x, y=y, data=self.__data, ci=None, ax=axes[index])
        
        plt.tight_layout()
        plt.show()

    

    
class Skalasisasi:
    """
    Kelas untuk melakukan skalasisasi data.

    Metode:
    - minmax_scaler: Melakukan skalasisasi menggunakan metode Min-Max Scaler.
    - standar_scaler: Melakukan skalasisasi menggunakan metode Standar Scaler.
    """

    def __init__(self, data):
        self.__data = data.copy()
    
    def minmax_scaler(self):
        """
        Melakukan skalasisasi menggunakan metode Min-Max Scaler.

        Returns:
        Data yang telah di-skalasisasi menggunakan metode Min-Max Scaler.
        """
        kolom = self.__data.columns
        data = self.__data.copy()
        for col in kolom:
            maksimal = data[col].max()
            minimum = data[col].min()
            delta = maksimal - minimum
            data[col] = data[col].apply(lambda x: abs((x - minimum)) / delta)
        
        return data
    
    def standar_scaler(self):
        """
        Melakukan skalasisasi menggunakan metode Standar Scaler.

        Returns:
        Data yang telah di-skalasisasi menggunakan metode Standar Scaler.
        """
        kolom = self.__data.columns
        data = self.__data.copy()
        for col in kolom:
            mean = data[col].mean()
            std = data[col].std()
            data[col] = data[col].apply(lambda x: (x - mean) / std)
        
        return data

def visual_data(tipe:str,data:np.ndarray,Label:np.ndarray,ruang:int=2,legend:list=None):
    """
    Menampilkan visualisasi data menggunakan plot scatter dengan menggunakan PCA (Principal Component Analysis).

    Parameters:
    tipe (str): Tipe data yang akan divisualisasikan.
    data (np.ndarray): Data yang akan divisualisasikan.
    Label (np.ndarray): Label untuk setiap data.
    ruang (int, optional): Jumlah dimensi yang diinginkan setelah menggunakan PCA. Default adalah 2.
    legend (list, optional): Daftar label untuk legenda. Default adalah None.

    Returns:
    None
    """
    data = data.copy()
    pca = PCA(n_components=ruang)
    data = pca.fit_transform(data)
    df = pd.DataFrame(data=data, columns=[f"PCA{i+1}" for i in range(ruang)])
    df['label'] = list(Label)
    print(df)

    scatter = plt.scatter(df['PCA1'], df['PCA2'], c=df['label'], cmap='viridis', s=80)

    plt.title(f'Plot Clustering {tipe} ')
    plt.xlabel('PCA 1')
    plt.ylabel('PCA 2')

    # Menambahkan legenda
    if legend:
        plt.legend(handles=scatter.legend_elements()[0], labels=legend, title='Klaster', loc='upper right')
    else:
        plt.legend(*scatter.legend_elements(), title='Klaster', loc='upper right')
    plt.show()


