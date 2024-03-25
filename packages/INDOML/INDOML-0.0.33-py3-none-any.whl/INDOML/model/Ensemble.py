import numpy as np
from statistics import mode
from .supervised import DecisionTree,RegresiLinear
from ..datamanipulasi.fold import train_val_split

class Bagging:
    """
    Kelas Bagging digunakan untuk melakukan ensemble learning dengan metode Bagging.
    Bagging adalah teknik ensemble learning yang menggabungkan beberapa model yang sama
    jenisnya untuk meningkatkan performa prediksi.

    Parameters:
    - model: objek model yang akan digunakan untuk melakukan prediksi.
    - n_model: jumlah model yang akan digunakan dalam ensemble (default: 5).
    - random_state: seed untuk mengontrol randomness dalam pemilihan data (default: None).

    Methods:
    - fit(x, y): Melakukan training pada model dengan data x dan label y.
    - fit_predict(x, y): Melakukan training pada model dengan data x dan label y, dan mengembalikan hasil prediksi.
    - score_accuracy(y_pred, y_true): Menghitung akurasi prediksi berdasarkan hasil prediksi (y_pred) dan label sebenarnya (y_true).
    """

    def __init__(self, model, n_model: int = 5, random_state: int = None):
        self.__model = model
        self.__label: np.ndarray = None
        self.__random_state = random_state
        self.__n_model = n_model
    
    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Melakukan training pada model dengan data x dan label y.

        Parameters:
        - x: array numpy yang berisi data training.
        - y: array numpy yang berisi label data training.
        """
        if self.__random_state:
            np.random.seed(self.__random_state)
        record_x = [i for i in range(len(x))]
        predict_model = []

        for i in range(self.__n_model):
            data_x = []
            data_y = []
            for _ in range(len(x)):
                rd_c = np.random.choice(record_x, 1, replace=True)
                data_x.append(x[rd_c])
                data_y.append(int(y[rd_c]))
            
            data_x = np.array(data_x).reshape(x.shape)
            data_y = np.array(data_y)
            obj = self.__model
            obj.fit(data_x, data_y)
            predict_model.append(obj)
            pred = obj.predict(x)
            print(
                f"model-{i+1} akurasi : {self.score_accuracy(pred, y)}"
            )

        
        predict = []
        for data in x:
            temp_predict = []
            for m in predict_model:
                temp_predict.append(m.predict(data))
            
            predict.append(mode(temp_predict))


        
        self.__label = np.array(predict)
    
    def fit_predict(self, x: np.ndarray, y: np.ndarray):
        """
        Melakukan training pada model dengan data x dan label y, dan mengembalikan hasil prediksi.

        Parameters:
        - x: array numpy yang berisi data training.
        - y: array numpy yang berisi label data training.

        Returns:
        - label hasil prediksi.
        """
        self.fit(x, y)
        return self.__label
    
    def score_accuracy(self, y_pred: np.ndarray, y_true: np.ndarray):
        """
        Menghitung akurasi prediksi berdasarkan hasil prediksi (y_pred) dan label sebenarnya (y_true).

        Parameters:
        - y_pred: array numpy yang berisi hasil prediksi.
        - y_true: array numpy yang berisi label sebenarnya.

        Returns:
        - akurasi prediksi.
        """
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true / len(y_pred)


class Boosting:
    """
    Kelas Boosting digunakan untuk melakukan ensemble learning dengan metode Boosting.
    """

    def __init__(self,model, n_model:int = 5,random_state:int=None):
        """
        Inisialisasi objek Boosting.

        Parameters:
        - model: Objek model yang akan digunakan dalam ensemble learning.
        - n_model: Jumlah model yang akan digunakan dalam ensemble learning. Default: 5.
        - random_state: Seed untuk mengatur random state. Default: None.
        """
        self.__model = model
        self.__n_model = n_model
        self.__random_state = random_state
        self.__label = None
    
    def fit(self,x:np.ndarray,y:np.ndarray):
        """
        Melakukan fitting model dengan data training.

        Parameters:
        - x: Array numpy berisi data training.
        - y: Array numpy berisi label data training.
        """
        sample_weight = np.ones(len(x))/len(x)

        if self.__random_state :
            np.random.seed(self.__random_state)
        predict_model = []
        weight_model = []
        final_prediksi = None

        for i in range(self.__n_model):
            selected_indices = np.random.choice(len(x), size=len(x), p=sample_weight)
            data_x = [x[i] for i in selected_indices]
            data_y = [y[i] for i in selected_indices]
            data_x = np.array(data_x)
            data_y = np.array(data_y)
            obj = self.__model
            obj.fit(data_x,data_y)
            predict_model.append(obj)
            prediksi = obj.predict(x)
            error = np.sum(sample_weight * (prediksi != y))
            model_weight = 0.5 * np.log((1 - error) / error)
            weight_model.append(model_weight)
            sample_weight *= np.exp(-model_weight * y * prediksi)
            sample_weight /= np.sum(sample_weight)
            if final_prediksi == None:
                final_prediksi = model_weight*prediksi
            else:
                final_prediksi += model_weight*prediksi
            
            print(
                f"model-{i+1} akurasi : {self.score_accuracy(prediksi,y)}"
            )
            
        self.__label = np.argmax(final_prediksi,axis=1)
    
    def fit_predict(self,x:np.ndarray,y:np.ndarray):
        """
        Melakukan fitting model dengan data training dan mengembalikan label hasil prediksi.

        Parameters:
        - x: Array numpy berisi data training.
        - y: Array numpy berisi label data training.

        Returns:
        - Array numpy berisi label hasil prediksi.
        """
        self.fit(x,y)
        return self.__label

    def score_accuracy(self,y_pred:np.ndarray,y_true:np.ndarray):
        """
        Menghitung akurasi prediksi.

        Parameters:
        - y_pred: Array numpy berisi label hasil prediksi.
        - y_true: Array numpy berisi label sebenarnya.

        Returns:
        - Nilai akurasi prediksi.
        """
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true/len(y_pred)

class RandomForest:
    """
    Implementasi kelas RandomForest untuk melakukan pembelajaran dan prediksi menggunakan metode Random Forest.

    Parameters:
    - max_feature (int): Jumlah fitur maksimum yang akan dipertimbangkan saat membangun setiap pohon keputusan dalam ensemble.
    - min_fitur (int, optional): Jumlah fitur minimum yang akan dipertimbangkan saat membangun setiap pohon keputusan dalam ensemble. Default: 0.
    - max_depth (int): Kedalaman maksimum setiap pohon keputusan dalam ensemble.
    - random_state (int, optional): Seed untuk menghasilkan angka acak. Default: None.
    - n_tree (int): Jumlah pohon keputusan dalam ensemble.

    Attributes:
    - label: Label hasil prediksi setelah melakukan pembelajaran.
    - tree: Daftar pohon keputusan dalam ensemble.

    Methods:
    - fit(x, y, nama_fitur=None): Melakukan pembelajaran pada data x dan label y.
    - fit_predict(x, y, nama_fitur=None): Melakukan pembelajaran pada data x dan label y, serta mengembalikan hasil prediksi.
    - predict(x): Melakukan prediksi pada data x.
    - score_accuracy(y_pred, y_true): Menghitung akurasi prediksi berdasarkan hasil prediksi (y_pred) dan label sebenarnya (y_true).
    """

    def __init__(self, max_feature: int, min_fitur: int = 0, max_depth: int = 2, random_state: int = None, n_tree: int = 3):
        self.__max_depth = max_depth
        self.__random_state = random_state
        self.__n_tree = n_tree
        self.__tree = []
        self.__label = None
        self.__max_feature = max_feature
        self.__min_fitur = min_fitur
    
    @property
    def label(self):
        """
        Getter untuk atribut label.

        Returns:
        - label: Label hasil prediksi setelah melakukan pembelajaran.
        """
        pass

    @label.getter
    def label__(self):
        return self.__label

    @property
    def tree(self):
        """
        Getter untuk atribut tree.

        Returns:
        - tree: Daftar pohon keputusan dalam ensemble.
        """
        pass

    @tree.getter
    def tree__(self):
        return self.__tree
    
    def fit(self, x: np.ndarray, y: np.ndarray, nama_fitur: list = None):
        """
        Melakukan pembelajaran pada data x dan label y menggunakan metode Random Forest.

        Parameters:
        - x (np.ndarray): Data fitur untuk pembelajaran.
        - y (np.ndarray): Label yang sesuai dengan data fitur.
        - nama_fitur (list, optional): Nama fitur untuk keperluan informasi tambahan. Default: None.
        """
        if self.__random_state:
            np.random.seed(self.__random_state)
        record_x = [i for i in range(len(x))]

        for i in range(self.__n_tree):
            # boosting data
            data_x = []
            data_y = []
            data_terpilih = []
            for _ in range(len(x)):
                rd_c = np.random.choice(record_x, 1, replace=True)
                
                data_x.append(x[rd_c])
                data_y.append(int(y[rd_c]))
            data_x = np.array(data_x).reshape(x.shape)
            data_y = np.array(data_y)
            obj = DecisionTree(self.__max_depth)
            obj.fit(data_x, data_y, self.__max_feature, self.__min_fitur)
            self.__tree.append(obj)
            data_x_oob = np.array([x[i] for i in range(len(x)) if i not in data_terpilih])
            data_y_oob = np.array([y[i] for i in range(len(x)) if i not in data_terpilih])
            
            pred = obj.predict(data_x_oob)
            if nama_fitur is not None:
                print(
                f"model-{i+1} akurasi : {self.score_accuracy(pred, data_y_oob)} dan OOB error : {1 - self.score_accuracy(pred, data_y_oob)} , kolom root : {nama_fitur[obj.root]}"
                )
            else:
                print(
                    f"model-{i+1} akurasi : {self.score_accuracy(pred, data_y_oob)} dan OOB error : {1 - self.score_accuracy(pred, data_y_oob)}"
                )
        

    def fit_predict(self, x: np.ndarray, y: np.ndarray, nama_fitur=None):
        """
        Melakukan pembelajaran pada data x dan label y menggunakan metode Random Forest, serta mengembalikan hasil prediksi.

        Parameters:
        - x (np.ndarray): Data fitur untuk pembelajaran.
        - y (np.ndarray): Label yang sesuai dengan data fitur.
        - nama_fitur (list, optional): Nama fitur untuk keperluan informasi tambahan. Default: None.

        Returns:
        - label: Label hasil prediksi setelah melakukan pembelajaran.
        """
        self.fit(x, y, nama_fitur)

        predict = []
        for data in x:
            temp_predict = []
            for m in self.__tree:
                temp_predict.append(m.predict(data))
            
            predict.append(mode(temp_predict))

        self.__label = np.array(predict)
        return self.__label
    
    def predict(self, x: np.ndarray):
        """
        Melakukan prediksi pada data x menggunakan metode Random Forest.

        Parameters:
        - x (np.ndarray): Data fitur untuk prediksi.

        Returns:
        - label: Label hasil prediksi.
        """
        predict = []
        for data in x:
            temp_predict = []
            for m in self.__tree:
                temp_predict.append(m.predict(data))
            
            predict.append(mode(temp_predict))

        self.__label = np.array(predict)
        return self.__label
    

    def score_accuracy(self, y_pred: np.ndarray, y_true: np.ndarray):
        """
        Menghitung akurasi prediksi berdasarkan hasil prediksi (y_pred) dan label sebenarnya (y_true).

        Parameters:
        - y_pred (np.ndarray): Hasil prediksi.
        - y_true (np.ndarray): Label sebenarnya.

        Returns:
        - accuracy: Akurasi prediksi.
        """
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true / len(y_pred)

class Stacking:
    """
    Kelas Stacking digunakan untuk melakukan ensemble stacking pada model-model yang diberikan.

    Parameters:
    - base_model (list): List dari model-model dasar yang akan digunakan dalam stacking.
    - meta_model: Model yang akan digunakan untuk melakukan prediksi pada data hasil stacking.
    - val_size (float): Ukuran validasi yang akan digunakan dalam pembagian data train dan validation.
    - random_state: Seed untuk mengontrol randomness dalam pembagian data train dan validation.

    Attributes:
    - label: Label hasil prediksi dari model stacking.

    Methods:
    - fit(x, y): Melakukan training pada model stacking menggunakan data x dan label y.
    - fit_predict(x, y): Melakukan training pada model stacking menggunakan data x dan label y, dan mengembalikan hasil prediksi.
    - predict(x): Melakukan prediksi menggunakan model stacking pada data x.
    - score_accuracy(y_pred, y_true): Menghitung akurasi dari prediksi model stacking.

    """

    def __init__(self, base_model: list, meta_model, val_size=0.2, random_state=None):
        self.__base_model = base_model
        self.__meta_model = meta_model
        self.__label = None
        self.__val_size = val_size
        self.__random_state = random_state
    
    @property
    def label(self):
        """
        Properti label untuk mengakses hasil prediksi dari model stacking.

        Returns:
        - label: Hasil prediksi dari model stacking.

        """
        pass

    @label.getter
    def label__(self):
        return self.__label
    
    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Melakukan training pada model stacking menggunakan data x dan label y.

        Parameters:
        - x (np.ndarray): Data input untuk training.
        - y (np.ndarray): Label untuk training.

        """
        X_train, X_val, y_train, y_val = train_val_split(x, y, self.__val_size, self.__random_state)
        pred_base_model = []
        for m in self.__base_model:
            pred = m.fit_predict(X_train, y_train)
            print(f"Model {m.name} akurasi : {self.score_accuracy(pred, y_train)}")
            pred_base_model.append(m.predict(X_val))
            
        
        data_train_meta = np.column_stack(pred_base_model)
        prediksi = self.__meta_model.fit_predict(data_train_meta, y_val)
        self.__label = prediksi
    
    def fit_predict(self, x: np.ndarray, y: np.ndarray):
        """
        Melakukan training pada model stacking menggunakan data x dan label y, dan mengembalikan hasil prediksi.

        Parameters:
        - x (np.ndarray): Data input untuk training.
        - y (np.ndarray): Label untuk training.

        Returns:
        - label: Hasil prediksi dari model stacking.

        """
        self.fit(x, y)
        return self.__label
    
    def predict(self, x: np.ndarray):
        """
        Melakukan prediksi menggunakan model stacking pada data x.

        Parameters:
        - x (np.ndarray): Data input untuk prediksi.

        Returns:
        - prediksi: Hasil prediksi dari model stacking.

        """
        pred_base_model = []
        for m in self.__base_model:
            pred = m.predict(x)
            pred_base_model.append(pred)
            
        data_train_meta = np.column_stack(pred_base_model)
        prediksi = self.__meta_model.predict(data_train_meta)
        
        return prediksi
        

    def score_accuracy(self, y_pred: np.ndarray, y_true: np.ndarray):
        """
        Menghitung akurasi dari prediksi model stacking.

        Parameters:
        - y_pred (np.ndarray): Hasil prediksi dari model stacking.
        - y_true (np.ndarray): Label yang sebenarnya.

        Returns:
        - akurasi: Akurasi dari prediksi model stacking.

        """
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1
        
        return true / len(y_pred)
                

class BoostingRegressi:
    """
    Kelas BoostingRegressi digunakan untuk melakukan boosting pada model regresi.
    """

    def __init__(self, learning_rate: float = 0.2, n_estimator=10):
        """
        Inisialisasi objek BoostingRegressi.

        Parameters:
        - learning_rate (float): Tingkat pembelajaran untuk setiap model regresi. Default: 0.2.
        - n_estimator (int): Jumlah estimator (model regresi) yang akan digunakan dalam boosting. Default: 10.
        """
        self.__learning_rate = learning_rate
        self.__n_estimator = n_estimator
        self.__model = []
        self.__mean_target = None
        self.__y = None
    
    @property
    def model(self):
        """
        Properti model digunakan untuk mengakses daftar model regresi yang telah dilatih.

        Returns:
        - list: Daftar model regresi.
        """
        pass

    @model.getter
    def model_(self):
        return self.__model

    
    def fit(self, x: np.ndarray, y: np.ndarray):
        """
        Melatih model regresi dengan menggunakan data x dan y.

        Parameters:
        - x (np.ndarray): Data fitur yang akan digunakan untuk melatih model.
        - y (np.ndarray): Data target yang akan digunakan untuk melatih model.
        """
        self.__mean_target = np.mean(y)
        self.__y = y
        prediksi = np.full_like(y, np.mean(y))

        for _ in range(self.__n_estimator):
            residual = y - prediksi
            linear_model = RegresiLinear()
            linear_model.fit(x, residual)
            
            prediksi += self.__learning_rate * linear_model.predict(x)
            self.__model.append(linear_model)
    
    def fit_predict(self, x: np.ndarray, y: np.ndarray):
        """
        Melatih model regresi dengan menggunakan data x dan y, kemudian melakukan prediksi.

        Parameters:
        - x (np.ndarray): Data fitur yang akan digunakan untuk melatih model dan melakukan prediksi.
        - y (np.ndarray): Data target yang akan digunakan untuk melatih model.

        Returns:
        - np.ndarray: Hasil prediksi.
        """
        self.fit(x, y)
        pred = np.full_like(y, self.__mean_target)
        for mod in self.__model:
            pred += (self.__learning_rate * mod.predict(x))
        return pred

    def predict(self, x: np.ndarray):
        """
        Melakukan prediksi menggunakan model regresi yang telah dilatih.

        Parameters:
        - x (np.ndarray): Data fitur yang akan digunakan untuk melakukan prediksi.

        Returns:
        - np.ndarray: Hasil prediksi.
        """
        pred = np.full_like(x, shape=(x.shape[0],), fill_value=self.__mean_target)
        for mod in self.__model:
            pred += (self.__learning_rate * mod.predict(x))
        if len(x.shape) == 1:
            pred = pred[0]
        return pred
    



        











            
            
            


            





        
