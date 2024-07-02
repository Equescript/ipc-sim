import numpy as np
import utils
from mesh import Vert, Edge

def val(verts: list[Vert], edges: list[Edge]) -> float:
    sum = 0.0
    for e in edges:
        diff = verts[e.verts[0]].x - verts[e.verts[1]].x
        sum += 0.5 * e.l_squared * e.k * (diff.dot(diff) / e.l_squared - 1) ** 2
    return sum

def grad(verts: list[Vert], edges: list[Edge]):
    g = np.array([[0.0, 0.0, 0.0]] * len(verts))
    for e in edges:
        diff = verts[e.verts[0]].x - verts[e.verts[1]].x
        g_diff = 2 * e.k * (diff.dot(diff) / e.l_squared - 1) * diff
        g[e.verts[0]] += g_diff
        g[e.verts[1]] -= g_diff
    return g

def hess(verts: list[Vert], edges: list[Edge]):
    IJV = [[0] * (len(edges) * 36), [0] * (len(edges) * 36), np.array([0.0] * (len(edges) * 36))]
    for i, e in enumerate(edges):
        diff = verts[e.verts[0]].x - verts[e.verts[1]].x
        H_diff = 2 * e.k / e.l_squared * (2 * np.outer(diff, diff) + (diff.dot(diff) - e.l_squared) * np.identity(3))
        H_local = utils.make_PSD(np.block([[H_diff, -H_diff], [-H_diff, H_diff]]))
        # add to global matrix
        for nI in range(0, 2):
            for nJ in range(0, 2):
                indStart = i * 36 + (nI * 2 + nJ) * 9
                for r in range(0, 3):
                    for c in range(0, 3):
                        IJV[0][indStart + r * 3 + c] = e.verts[nI] * 3 + r
                        IJV[1][indStart + r * 3 + c] = e.verts[nJ] * 3 + c
                        IJV[2][indStart + r * 3 + c] = H_local[nI * 3 + r, nJ * 3 + c]
    return IJV