import numpy as np

def train_val_split(x:np.ndarray, y:np.ndarray, val_size=0.2, random_state=None):
    """
    Memisahkan data menjadi data latih dan data validasi.

    Parameters:
        x (np.ndarray): Array numpy yang berisi fitur-fitur data.
        y (np.ndarray): Array numpy yang berisi label-label data.
        val_size (float): Ukuran data validasi sebagai proporsi dari keseluruhan data. Default: 0.2.
        random_state (int): Seed untuk menghasilkan angka acak. Default: None.

    Returns:
        Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]: Tuple yang berisi data latih dan data validasi
        dalam urutan X_train, X_val, y_train, y_val.
    """
    if random_state is not None:
        np.random.seed(random_state)

    data_size = len(x)
    val_size = int(val_size * data_size)

    indices = np.random.permutation(data_size)
    train_indices, val_indices = indices[val_size:], indices[:val_size]

    X_train, X_val = x[train_indices], x[val_indices]
    y_train, y_val = y[train_indices], y[val_indices]

    return X_train, X_val, y_train, y_val