# Mass-Spring Solids Simulation

import numpy as np  # numpy for linear algebra
import pygame       # pygame for visualization
pygame.init()

from scene import Scene
from mesh import Vert

# simulation setup
side_len = 1
rho = 1000  # density of square
k = 1e5     # spring stiffness
initial_stretch = 1.4
n_seg = 4   # num of segments per side of the square
h = 0.004   # time step size in s
gravity = [0.0, -9.81, 0.0]
# m = rho * side_len * side_len / ((n_seg + 1) * (n_seg + 1))  # calculate node mass evenly
m = 20

path = "D:\\Code\\ComputerGarphics\\IPC\\ipc-sim\\test1\\square_mesh_2x2x2.json"
scene = Scene(path, m, k, gravity, h, 1e-2, initial_stretch)

# simulation with visualization
resolution = np.array([900, 900])
offset = resolution / 2
scale = 200
def screen_projection(v: Vert):
    return [offset[0] + scale * v.x[0], resolution[1] - (offset[1] + scale * v.x[1])]

time_step = 0
screen = pygame.display.set_mode(resolution)
running = True
while running:
    # run until the user asks to quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    print('### Time step', time_step, '###')

    # fill the background and draw the square
    screen.fill((255, 255, 255))
    for e in scene.edges:
        pygame.draw.aaline(screen, (0, 0, 255), screen_projection(scene.verts[e.verts[0]]), screen_projection(scene.verts[e.verts[1]]))
    for v in scene.verts:
        pygame.draw.circle(screen, (0, 0, 255), screen_projection(v), 0.1 * side_len / n_seg * scale)

    pygame.display.flip()   # flip the display

    # step forward simulation and wait for screen refresh
    print("scene.step_forward()")
    scene.step_forward()
    time_step += 1
    pygame.time.wait(int(h * 1000))

pygame.quit()