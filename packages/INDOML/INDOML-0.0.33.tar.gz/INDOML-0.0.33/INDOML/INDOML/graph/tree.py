import numpy as np

class TreeNode:
    """
    Representasi dari simpul dalam pohon keputusan.

    Args:
        feature (optional): Fitur pemisah untuk simpul ini.
        value (optional): Nilai pemisah untuk simpul ini.
        result (optional): Hasil jika simpul ini adalah simpul daun.
        left (optional): Sub-pohon kiri (nilai kurang dari atau sama dengan pemisah).
        right (optional): Sub-pohon kanan (nilai lebih dari pemisah).
    """

    def __init__(self, feature=None, value=None, result=None, left=None, right=None):
        self.feature = feature
        self.value = value
        self.result = result
        self.left = left
        self.right = right

    