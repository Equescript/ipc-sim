import json
import numpy as np
import numpy.linalg as LA

def make_PSD(hess):
    [lam, V] = LA.eigh(hess)    # Eigen decomposition on symmetric matrix
    # set all negative Eigenvalues to 0
    for i in range(0, len(lam)):
        lam[i] = max(0, lam[i])
    return np.matmul(np.matmul(V, np.diag(lam)), np.transpose(V))

def read_json(file_path: str):
    with open(file_path, 'r') as json_file:
        json_data = json.load(json_file)
        json_file.close()
        return json_data
