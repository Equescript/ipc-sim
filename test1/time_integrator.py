from cmath import inf
import numpy as np
import numpy.linalg as LA
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

import InertiaEnergy, MassSpringEnergy, GravityEnergy
from mesh import Vert, Edge

def step_forward(verts: list[Vert], edges: list[Edge], gravity: list[float], h: float, tol: float):
    for v in verts:
        v.x_tilde = v.x + v.v * h
        v.x_prev = v.x
        v.x_n = v.x

    # Newton loop
    iter = 0
    E_last = IP_val(verts, edges, gravity, h)
    p = search_dir(verts, edges, gravity, h)
    while LA.norm(p, inf) / h > tol:
        print('Iteration', iter, ':')
        # line search
        alpha = 1
        while IP_val_with_p(verts, alpha * p, edges, gravity, h) > E_last:
            alpha /= 2
        print('step size =', alpha)

        for v in verts:
            v.x_prev = v.x
        E_last = IP_val(verts, edges, gravity, h)
        p = search_dir(verts, edges, gravity, h)
        iter += 1

    for v in verts:
        v.v = (v.x - v.x_n) / h

def IP_val(verts: list[Vert], edges: list[Edge], gravity: list[float], h: float) -> float:
    return InertiaEnergy.val(verts) + h * h * (MassSpringEnergy.val(verts, edges) + GravityEnergy.val(verts, gravity))

def IP_val_with_p(verts: list[Vert], p: np.ndarray, edges: list[Edge], gravity: list[float], h: float) -> float:
    # assert len(p) == 3 * len(verts)
    for i, v in enumerate(verts):
        v.x = v.x_prev + p[i] # np.array([p[i*3], p[i*3+1], p[i*3+2]])
    return IP_val(verts, edges, gravity, h)

def IP_grad(verts: list[Vert], edges: list[Edge], gravity: list[float], h: float) -> np.ndarray:
    return InertiaEnergy.grad(verts) + h * h * (MassSpringEnergy.grad(verts, edges) + GravityEnergy.grad(verts, gravity))

def IP_hess(verts: list[Vert], edges: list[Edge], h: float):
    IJV_In = InertiaEnergy.hess(verts)
    IJV_MS = MassSpringEnergy.hess(verts, edges)
    IJV_MS[2] *= h * h    # implicit Euler
    IJV = np.append(IJV_In, IJV_MS, axis=1)
    H = sparse.coo_matrix((IJV[2], (IJV[0], IJV[1])), shape=(len(verts) * 3, len(verts) * 3)).tocsr()
    return H

def search_dir(verts: list[Vert], edges: list[Edge], gravity: list[float], h: float) -> np.ndarray:
    projected_hess = IP_hess(verts, edges, h)
    reshaped_grad = IP_grad(verts, edges, gravity, h).reshape(len(verts) * 3, 1)
    return spsolve(projected_hess, -reshaped_grad).reshape(len(verts), 3)