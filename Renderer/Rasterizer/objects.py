import Renderer.Rasterizer.rasterizer as ras
from pyray import *
import math



        
        


Cube_verts = [
            Vector3( 1,  1,  1),
            Vector3(-1,  1,  1),
            Vector3(-1, -1,  1),
            Vector3( 1, -1,  1),
            Vector3( 1,  1, -1),
            Vector3(-1,  1, -1),
            Vector3(-1, -1, -1),
            Vector3( 1, -1, -1),
            ]
Cube_tris = [
            [0, 1, 2, RED],
            [0, 2, 3, RED],
            [4, 0, 3, GREEN],
            [4, 3, 7, GREEN],
            [5, 4, 7, BLUE],
            [5, 7, 6, BLUE],
            [1, 5, 6, YELLOW],
            [1, 6, 2, YELLOW],
            [4, 5, 1, PURPLE],
            [4, 1, 0, PURPLE],
            [2, 6, 7, SKYBLUE],
            [2, 7, 3, SKYBLUE],
            ]
Cube = ras.Object(Cube_verts, Cube_tris, Vector3(0, 0, 0), math.sqrt(3))