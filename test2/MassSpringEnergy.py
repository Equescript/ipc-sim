import numpy as np
import utils

from mesh import Vert, Edge

def val(verts: list[Vert], e: list[list[int]], l2, k):
    sum = 0.0
    for i in range(0, len(e)):
        diff = verts[e[i][0]].x - verts[e[i][1]].x
        sum += l2[i] * 0.5 * k[i] * (diff.dot(diff) / l2[i] - 1) ** 2
    return sum

def grad(verts: list[Vert], e: list[list[int]], l2, k):
    g = np.array([[0.0, 0.0, 0.0]] * len(verts))
    for i in range(0, len(e)):
        diff = verts[e[i][0]].x - verts[e[i][1]].x
        g_diff = 2 * k[i] * (diff.dot(diff) / l2[i] - 1) * diff
        g[e[i][0]] += g_diff
        g[e[i][1]] -= g_diff
    return g

def hess(verts: list[Vert], e: list[list[int]], l2, k):
    IJV = [[0] * (len(e) * 36), [0] * (len(e) * 36), np.array([0.0] * (len(e) * 36))]
    for i in range(0, len(e)):
        diff = verts[e[i][0]].x - verts[e[i][1]].x
        H_diff = 2 * k[i] / l2[i] * (2 * np.outer(diff, diff) + (diff.dot(diff) - l2[i]) * np.identity(3))
        H_local = utils.make_PSD(np.block([[H_diff, -H_diff], [-H_diff, H_diff]]))
        # add to global matrix
        for nI in range(0, 2):
            for nJ in range(0, 2):
                indStart = i * 36 + (nI * 2 + nJ) * 9
                for r in range(0, 3):
                    for c in range(0, 3):
                        IJV[0][indStart + r * 3 + c] = e[i][nI] * 3 + r
                        IJV[1][indStart + r * 3 + c] = e[i][nJ] * 3 + c
                        IJV[2][indStart + r * 3 + c] = H_local[nI * 3 + r, nJ * 3 + c]
    return IJV
