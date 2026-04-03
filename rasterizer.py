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

def draw_line(P0,P1, color:pygame.Color = (255, 255, 255)): # Default - White
    dx = P1.x - P0.x
    dy = P1.y - P0.y
    if abs(dx) > abs(dy):
        # Line is more horizontal
        # make sure that x0 < x1
        if P0.x > P1.x:
            P0, P1 = P1, P0
        a = dy / dx
        y = P0.y
        for x in range(P0.x, P1.x):
            draw_pixel(x, y, color, screen)
            y = y + a
    else:
        # Line is more vertical
        # Make sure y0 < y1:
        if P0.y > P1.y:
            P0, P1 = P1, P0
        a = dy / dx
        x = P0.x
        for y in range(P0.y, P1.y):
            draw_pixel(x, y, color, screen)


if __name__ == "__main__":
    main()