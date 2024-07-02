import numpy as np

class Vert:
    x: np.ndarray[float]
    x_tilde: np.ndarray[float]
    x_prev: np.ndarray[float]
    x_n: np.ndarray[float]
    v: np.ndarray[float]
    m: float
    is_DBC: bool
    def __init__(self, x: list[float], v: list[float], m: float, is_DBC: bool = False):
        self.x = np.array(x)
        self.x_tilde = np.array(x)
        self.x_prev = np.array(x)
        self.x_n = np.array(x)
        self.v = np.array(v)
        self.m = m
        self.is_DBC = is_DBC

class Edge:
    verts: tuple[int, int]
    k: float
    l: float
    l_squared: float
    def __init__(self, verts: tuple[int, int], k: float, l: float):
        self.verts = verts
        self.k = k
        self.l = l
        self.l_squared = l * l