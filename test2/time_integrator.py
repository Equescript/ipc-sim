import copy
from cmath import inf

import numpy as np
import numpy.linalg as LA
import scipy.sparse as sparse
from scipy.sparse.linalg import spsolve

import InertiaEnergy
import MassSpringEnergy

from mesh import Vert, Edge

def step_forward(verts: list[Vert], e, v, l2, k, h, tol) -> tuple[list[Vert], list[list[int]]]:
    # x_tilde = x + v * h     # implicit Euler predictive position
    # x_n = copy.deepcopy(x)
    for v in verts:
        v.x_tilde = v.x + v.v * h
        v.x_prev = v.x
        v.x_n = v.x

    # Newton loop
    iter = 0
    E_last = IP_val(verts, e, l2, k, h)
    p = search_dir(verts, e, l2, k, h)
    while LA.norm(p, inf) / h > tol:
        print('Iteration', iter, ':')
        print('residual =', LA.norm(p, inf) / h)

        # line search
        alpha = 1
        while IP_val_with_p(verts, alpha * p, e, l2, k, h) > E_last:
            alpha /= 2
        print('step size =', alpha)

        # x += alpha * p
        for v in verts:
            v.x_prev = v.x
        E_last = IP_val(verts, e, l2, k, h)
        p = search_dir(verts, e, l2, k, h)
        iter += 1

    for v in verts:
        v.v = (v.x - v.x_n) / h   # implicit Euler velocity update
    return [verts, v]

def IP_val(verts: list[Vert], e, l2, k, h):
    return InertiaEnergy.val(verts) + h * h * MassSpringEnergy.val(verts, e, l2, k)     # implicit Euler

def IP_val_with_p(verts: list[Vert], p, e, l2, k, h):
    for i, v in enumerate(verts):
        v.x = v.x_prev + p[i]
    return IP_val(verts, e, l2, k, h)

def IP_grad(verts: list[Vert], e, l2, k, h):
    return InertiaEnergy.grad(verts) + h * h * MassSpringEnergy.grad(verts, e, l2, k)   # implicit Euler

def IP_hess(verts: list[Vert], e, l2, k, h):
    IJV_In = InertiaEnergy.hess(verts)
    IJV_MS = MassSpringEnergy.hess(verts, e, l2, k)
    IJV_MS[2] *= h * h    # implicit Euler
    IJV = np.append(IJV_In, IJV_MS, axis=1)
    H = sparse.coo_matrix((IJV[2], (IJV[0], IJV[1])), shape=(len(verts) * 3, len(verts) * 3)).tocsr()
    return H

def search_dir(verts: list[Vert], e, l2, k, h):
    projected_hess = IP_hess(verts, e, l2, k, h)
    reshaped_grad = IP_grad(verts, e, l2, k, h).reshape(len(verts) * 3, 1)
    return spsolve(projected_hess, -reshaped_grad).reshape(len(verts), 3)