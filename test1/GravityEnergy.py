import numpy as np
from mesh import Vert

def val(verts: list[Vert], gravity: list[float]) -> float:
    sum = 0.0
    for v in verts:
        sum += -v.m * v.x.dot(gravity)
    return sum

def grad(verts: list[Vert], gravity: list[float]):
    g = np.array([gravity] * len(verts))
    for i, v in enumerate(verts):
        g[i] *= -v.m
    return g

# Hessian is 0