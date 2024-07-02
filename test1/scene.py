import numpy as np
import utils
import time_integrator
from mesh import Vert, Edge

class Scene:
    verts: list[Vert] = []
    edges: list[Edge] = []
    h: float
    tol: float
    gravity: list[float]
    def __init__(self, path: str, m: float, k: float, gravity: list[float], h: float, tol: float, initial_stretch = 1.0):
        mesh_data = utils.read_json(path)
        for vert in mesh_data["verts"]:
            self.verts.append(Vert(vert, [0.0, 0.0, 0.0], m))
        for edge in mesh_data["edges"]:
            edge: list[int]
            diff = self.verts[edge[0]].x - self.verts[edge[1]].x
            self.edges.append(Edge(edge, k, np.linalg.norm(diff, ord=2)))
        for v in self.verts:
            v.x[0] *= initial_stretch
        self.h = h
        self.tol = tol
        self.gravity = gravity

    def step_forward(self):
        time_integrator.step_forward(self.verts, self.edges, self.gravity, self.h, self.tol)