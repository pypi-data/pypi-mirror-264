import numpy as np

def euclidian_distance(x: np.ndarray, y: np.ndarray) -> float:
    """
    Menghitung jarak euclidean antara dua vektor.

    Parameters:
    x (np.ndarray): Vektor pertama.
    y (np.ndarray): Vektor kedua.

    Returns:
    float: Jarak euclidean antara dua vektor.
    """
    delta = x - y
    square = delta ** 2
    return np.sqrt(np.sum(square))


def kuadrat_jarak(x:np.ndarray,y:np.ndarray)->float:
    """
    Menghitung kuadrat dari jarak Euclidean antara dua vektor.

    Parameters:
    x (np.ndarray): Vektor pertama.
    y (np.ndarray): Vektor kedua.

    Returns:
    float: Kuadrat dari jarak Euclidean antara x dan y.
    """
    return euclidian_distance(x,y)**2