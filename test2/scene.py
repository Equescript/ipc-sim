import utils
import time_integrator
from mesh import Vert, Edge

class Scene:
    verts: list[Vert] = []
    edges: list[Edge] = []
    h: float
    tol: float
    def __init__(self, path: str, m: float, k: float, l: float, h: float, tol: float):
        mesh_data = utils.read_json(path)
        for vert in mesh_data["verts"]:
            self.verts.append(Vert(vert, [0.0, 0.0, 0.0], m))
        for edge in mesh_data["edges"]:
            self.edges.append(Edge(edge, k, l))
        self.h = h
        self.tol = tol

    def step_forward(self):
        time_integrator.step_forward(self.verts, self.edges, self.h, self.tol)