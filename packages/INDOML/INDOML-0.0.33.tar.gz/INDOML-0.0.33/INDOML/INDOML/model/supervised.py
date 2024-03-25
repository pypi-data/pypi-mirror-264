import numpy as np
from ..graph.tree import TreeNode

class DecisionTree(TreeNode):
    """Kelas untuk membangun dan menggunakan pohon keputusan.

    Parameters:
    - depth (int): Kedalaman maksimum dari pohon keputusan. Default: 2

    Attributes:
    - __depth (int): Kedalaman maksimum dari pohon keputusan.
    - __tree (TreeNode): Pohon keputusan yang dibangun.
    - __label (np.ndarray): Label hasil prediksi.
    - root: Akar pohon keputusan.

    Methods:
    - calculate_gini(y): Menghitung nilai Gini impurity dari suatu set data.
    - calculate_split_info(X, y, feature, value): Menghitung nilai split info dari suatu pemisah.
    - calculate_gain_ratio(X, y, feature, value): Menghitung nilai Gain Ratio dari suatu pemisah.
    - split_data(X, y, feature, value): Memisahkan data berdasarkan suatu fitur dan nilai pemisah.
    - find_best_split(X, y, min_fitur=0, max_fitur=None): Mencari pemisah terbaik berdasarkan nilai Gain Ratio.
    - build_tree(X, y, depth=0, max_depth=None, max_feature=None, min_fitur=0): Membangun pohon keputusan secara rekursif.
    - fit(X, y, max_feature=None, min_fitur=0): Melatih model menggunakan data training.
    - fit_predict(X, y, max_feature=None, min_fitur=0): Melatih model dan melakukan prediksi pada data training.
    - predict(X): Melakukan prediksi pada data baru.
    - predict_tree(node, sample): Memprediksi label untuk sampel menggunakan pohon keputusan.
    - score_accuracy(y_pred, y_true): Menghitung akurasi prediksi.

    """

    def __init__(self, depth: int = 2):
        self.__depth = depth
        self.__tree: TreeNode = None
        self.__label: np.ndarray = None
        self.root = None

    @property
    def label(self):
        pass

    @property
    def tree(self):
        pass

    @tree.getter
    def tree__(self):
        return self.__tree

    @label.getter
    def label__(self):
        return self.__label

    def calculate_gini(self, y):
        # Menghitung nilai Gini impurity dari suatu set data
        classes, counts = np.unique(y, return_counts=True)
        probabilities = counts / len(y)
        gini = 1 - np.sum(probabilities**2)
        return gini

    def calculate_split_info(self, X: np.ndarray, y: np.ndarray, feature, value):
        # Menghitung nilai split info dari suatu pemisah
        m = len(y)
        X_left, y_left, X_right, y_right = self.split_data(X, y, feature, value)
        p_left = len(y_left) / m
        p_right = len(y_right) / m

        if p_left == 0 or p_right == 0:
            return 0
        split_info = -p_left * np.log2(p_left) - p_right * np.log2(p_right)
        return split_info

    def calculate_gain_ratio(self, X: np.ndarray, y: np.ndarray, feature, value):
        # Menghitung nilai Gain Ratio dari suatu pemisah
        gini_before = self.calculate_gini(y)
        m = len(y)

        X_left, y_left, X_right, y_right = self.split_data(X, y, feature, value)

        gini_left = self.calculate_gini(y_left)
        gini_right = self.calculate_gini(y_right)

        gini_after = (len(y_left) / m) * gini_left + (len(y_right) / m) * gini_right

        split_info = self.calculate_split_info(X, y, feature, value)

        if split_info == 0:
            return 0

        gain_ratio = (gini_before - gini_after) / split_info
        return gain_ratio

    def split_data(self, X: np.ndarray, y: np.ndarray, feature, value):
        # Memisahkan data berdasarkan suatu fitur dan nilai pemisah
        mask = X[:, feature] <= value
        X_left, y_left = X[mask], y[mask]
        X_right, y_right = X[~mask], y[~mask]
        return X_left, y_left, X_right, y_right

    def find_best_split(self, X: np.ndarray, y: np.ndarray, min_fitur=0, max_fitur=None):
        # Mencari pemisah terbaik berdasarkan nilai Gain Ratio
        m, n = X.shape
        best_gain_ratio = 0
        best_feature = None
        best_value = None
        if max_fitur == None:
            fitur = [i for i in range(n)]
        else:
            if min_fitur != 0:
                max_fitur = np.random.randint(min_fitur, max_fitur)
            fitur = np.random.choice(n, size=max_fitur, replace=False)

        for feature in fitur:
            unique_values = np.unique(X[:, feature])
            for value in unique_values:
                gain_ratio = self.calculate_gain_ratio(X, y, feature, value)

                if gain_ratio > best_gain_ratio:
                    best_gain_ratio = gain_ratio
                    best_feature = feature
                    best_value = value

        return best_feature, best_value

    def build_tree(self, X: np.ndarray, y: np.ndarray, depth=0, max_depth=None, max_feature=None, min_fitur=0):
        # Membangun pohon keputusan secara rekursif
        if depth == max_depth or len(np.unique(y)) == 1:
            # Jika mencapai kedalaman maksimum atau semua label sama, buat leaf node
            return TreeNode(result=np.bincount(y).argmax())

        best_feature, best_value = self.find_best_split(X, y, min_fitur, max_feature)
        if depth == 0:
            self.root = best_feature

        if best_feature is None:
            # Jika tidak dapat menemukan pemisah, buat leaf node
            return TreeNode(result=np.bincount(y).argmax())

        X_left, y_left, X_right, y_right = self.split_data(X, y, best_feature, best_value)

        left_subtree = self.build_tree(X_left, y_left, depth + 1, max_depth, max_feature, min_fitur)
        right_subtree = self.build_tree(X_right, y_right, depth + 1, max_depth, max_feature, min_fitur)

        return TreeNode(feature=best_feature, value=best_value, left=left_subtree, right=right_subtree)

    def fit(self, X: np.ndarray, y: np.ndarray, max_feature=None, min_fitur=0):
        """Melatih model menggunakan data training.

        Parameters:
        - X (np.ndarray): Data training.
        - y (np.ndarray): Label training.
        - max_feature (int): Jumlah fitur maksimum yang digunakan dalam mencari pemisah terbaik. Default: None
        - min_fitur (int): Jumlah fitur minimum yang digunakan dalam mencari pemisah terbaik. Default: 0

        """
        self.__tree = self.build_tree(X, y, max_depth=self.__depth, max_feature=max_feature, min_fitur=min_fitur)
        label = []
        for sam in X:
            label.append(self.predict_tree(self.__tree, sam))

        self.__label = np.array(label)

    def fit_predict(self, X: np.ndarray, y: np.ndarray, max_feature=None, min_fitur=0):
        """Melatih model dan melakukan prediksi pada data training.

        Parameters:
        - X (np.ndarray): Data training.
        - y (np.ndarray): Label training.
        - max_feature (int): Jumlah fitur maksimum yang digunakan dalam mencari pemisah terbaik. Default: None
        - min_fitur (int): Jumlah fitur minimum yang digunakan dalam mencari pemisah terbaik. Default: 0

        Returns:
        - np.ndarray: Label hasil prediksi.

        """
        self.fit(X, y, max_feature, min_fitur)
        return self.__label

    def predict(self, X: np.ndarray):
        """Melakukan prediksi pada data baru.

        Parameters:
        - X (np.ndarray): Data baru yang akan diprediksi.

        Returns:
        - np.ndarray: Label hasil prediksi.

        """
        if len(X.shape) == 1:
            return self.predict_tree(self.__tree, X)
        else:
            label = []
            for sam in X:
                label.append(self.predict_tree(self.__tree, sam))
            return np.array(label)

    def predict_tree(self, node, sample):
        """Memprediksi label untuk sampel menggunakan pohon keputusan.

        Parameters:
        - node (TreeNode): Node saat ini dalam pohon keputusan.
        - sample: Sampel yang akan diprediksi.

        Returns:
        - int: Label hasil prediksi.

        """
        if node.result is not None:
            return node.result

        if sample[node.feature] <= node.value:
            return self.predict_tree(node.left, sample)
        else:
            return self.predict_tree(node.right, sample)

    def score_accuracy(self, y_pred: np.ndarray, y_true: np.ndarray):
        """Menghitung akurasi prediksi.

        Parameters:
        - y_pred (np.ndarray): Label hasil prediksi.
        - y_true (np.ndarray): Label yang sebenarnya.

        Returns:
        - float: Akurasi prediksi.

        """
        true = 0
        for i in range(len(y_pred)):
            if y_pred[i] == y_true[i]:
                true += 1

        return true / len(y_pred)


class RegresiLinear:
    """
    Kelas RegresiLinear digunakan untuk melakukan regresi linear.
    """

    def __init__(self):
        self.__weight = 0
        self.__reg = None
    
    @property
    def reg(self):
        """
        Properti reg digunakan untuk mengakses nilai regresi yang telah dihitung.
        """
        pass

    @reg.getter
    def reg_(self):
        return self.__reg
    
    def fit(self,x:np.ndarray,y:np.ndarray):
        """
        Metode fit digunakan untuk melatih model regresi linear.

        Parameters:
            x (np.ndarray): Array 2D yang berisi fitur-fitur.
            y (np.ndarray): Array 1D yang berisi target.

        Raises:
            np.linalg.LinAlgError: Jika matriks tidak dapat diinvers.
        """
        x_T = np.transpose(x)
        multiply = x_T @ x 
        try:
            inverse = np.linalg.inv(multiply)
            self.__weight = inverse @ x_T @ y
        except np.linalg.LinAlgError:
            print("Matriks tidak dapat diinvers.")
        
    def fit_predict(self, x:np.ndarray, y:np.ndarray):
        """
        Metode fit_predict digunakan untuk melatih model dan mengembalikan hasil regresi.

        Parameters:
            x (np.ndarray): Array 2D yang berisi fitur-fitur.
            y (np.ndarray): Array 1D yang berisi target.

        Returns:
            np.ndarray: Array 1D yang berisi hasil regresi.
        """
        self.fit(x,y)
        self.__reg = x @ self.__weight
        return self.__reg
    
    def predict(self, x:np.ndarray):
        """
        Metode predict digunakan untuk melakukan prediksi menggunakan model yang telah dilatih.

        Parameters:
            x (np.ndarray): Array 2D yang berisi fitur-fitur.

        Returns:
            np.ndarray: Array 1D yang berisi hasil prediksi.
        """
        return x @ self.__weight



    
