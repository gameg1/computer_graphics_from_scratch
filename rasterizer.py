from raytracer import *
from vector import *
from objects import *
import pygame
import pygame.gfxdraw
import math

# TODO: Seperate the raytracer software and the objects with the scene.

WIDTH = 600
HEIGHT = 600
pygame.init()


# Window set up
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Camera Info
Camera_pos:vector3 = vector3(0, 0, 1) # X, Y, Z - At origin point
Camera_rotation = [
    [0.7071, 0, -0.7071],
    [     0, 1,       0],
    [0.7071, 0,  0.7071],
]
Camera_vector:vector3 = vector3(0, 0, 1) # Unit vector pointing towards Z+

        
# Set up the envioment
BACKGROUND_COLOR = pygame.Color(0, 0, 0)
scene = {
        "objects":[
        ],
        "lights":
        [
        ]
        }




def main():

    clock = pygame.time.Clock()
    running = True
    # Runs per frame
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # # Determine which square on the grid corresponds to this square on the canvas
        # for canvas_x in range(-(WIDTH // 2), WIDTH // 2, 2):
        #     for canvas_y in range(-(HEIGHT // 2), HEIGHT // 2, 2):
        #         pass

        draw_line(vector2(-200, -100), vector2(240,120))
        draw_line(vector2(-50, -200), vector2(60, 240), (255, 0, 0))



        # End render
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_line(P0:vector2, P1:vector2, color:pygame.Color = (255, 255, 255)): # Default - White
    if abs(P1.x - P0.x) > abs(P1.y - P0.y):
        # Line is more horizontal
        # make sure that x0 < x1
        if P0.x > P1.x:
            P0, P1 = P1, P0
        ys = interpolate(P0.x, P0.y, P1.x, P1.y)
        for x in range(P0.x, P1.x):
            draw_pixel(x, ys[x-P0.x], color, screen)
    else:
        # Line is more vertical
        # Make sure y0 < y1:
        if P0.y > P1.y:
            P0, P1 = P1, P0
        xs = interpolate(P0.y, P0.x, P1.y, P1.x)
        for y in range(P0.y, P1.y):
            draw_pixel(xs[y - P0.y], y, color, screen)

def interpolate(i0:int, d0:float, i1:int, d1:float):
    """Linear interpolates from d0 to d1 in i1 - 10 steps"""
    if i0 == i1:
        return [d0]
    values=[]
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(i0, i1):
        values.append(d)
        d = d + a
    return values

if __name__ == "__main__":
    main()