import numpy as np
import os
import utils
from mesh import Vert, Edge

def generate(side_length, n_seg, m: float) -> tuple[list[Vert], list[list[int]]]:
    """ # sample nodes uniformly on a square
    x = np.array([[0.0, 0.0, 0.0]] * ((n_seg + 1) ** 2))
    step = side_length / n_seg
    for i in range(0, n_seg + 1):
        for j in range(0, n_seg + 1):
            x[i * (n_seg + 1) + j] = [-side_length / 2 + i * step, -side_length / 2 + j * step, 0.0]

    # connect the nodes with edges
    e = []
    # horizontal edges
    for i in range(0, n_seg):
        for j in range(0, n_seg + 1):
            e.append([i * (n_seg + 1) + j, (i + 1) * (n_seg + 1) + j])
    # vertical edges
    for i in range(0, n_seg + 1):
        for j in range(0, n_seg):
            e.append([i * (n_seg + 1) + j, i * (n_seg + 1) + j + 1])
    # diagonals
    for i in range(0, n_seg):
        for j in range(0, n_seg):
            e.append([i * (n_seg + 1) + j, (i + 1) * (n_seg + 1) + j + 1])
            e.append([(i + 1) * (n_seg + 1) + j, i * (n_seg + 1) + j + 1])

    verts = []
    for vert in x:
        verts.append(Vert(vert, [0.0, 0.0, 0.0], m)) """
    path = "D:\\Code\\ComputerGarphics\\IPC\\ipc-sim\\test1\\square_mesh_2x2x2.json"
    mesh_data = utils.read_json(path)
    verts = []
    e = mesh_data["edges"]
    for vert in mesh_data["verts"]:
        verts.append(Vert(vert, [0.0, 0.0, 0.0], m))
    return (verts, e)

def write_to_file(frameNum, x, n_seg):
    # Check if 'output' directory exists; if not, create it
    if not os.path.exists('output'):
        os.makedirs('output')

    # create obj file
    filename = f"output/{frameNum}.obj"
    with open(filename, 'w') as f:
        # write vertex coordinates
        for row in x:
            f.write(f"v {float(row[0]):.6f} {float(row[1]):.6f} 0.0\n")
        # write vertex indices for each triangle
        for i in range(0, n_seg):
            for j in range(0, n_seg):
                #NOTE: each cell is exported as 2 triangles for rendering
                f.write(f"f {i * (n_seg+1) + j + 1} {(i+1) * (n_seg+1) + j + 1} {(i+1) * (n_seg+1) + j+1 + 1}\n")
                f.write(f"f {i * (n_seg+1) + j + 1} {(i+1) * (n_seg+1) + j+1 + 1} {i * (n_seg+1) + j+1 + 1}\n")