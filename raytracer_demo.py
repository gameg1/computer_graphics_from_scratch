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
Camera_pos:vector3 = vector3(3, 0, 1) # X, Y, Z - At origin point
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
        sphere(vector3(0, -1, 3), 1, (255, 0 , 0), 500, 0.2),            # Sphere 1
        sphere(vector3(2, 0, 4), 1, (0, 0, 255), 500, 0.3),              # Sphere 2
        sphere(vector3(-2, 0, 4), 1, (0, 255, 0), 10, 0.4),              # Sphere 3
        sphere(vector3(0, -5001, 0), 5000, (255, 255, 0), 1000, 0.5)     # Sphere 4 - The floor
        ],
        "lights":
        [
        light(light.AMBIENT, 0.2),                       # Ambient light
        light(light.POINT, 0.6, vector3(2, 1, 0)),       # Point light
        light(light.DIRECTIONAL, 0.2, vector3(1, 4, 4)), # Directional light
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

        # Determine which square on the grid corresponds to this square on the canvas
        for canvas_x in range(-(WIDTH // 2), WIDTH // 2, 2):
            for canvas_y in range(-(HEIGHT // 2), HEIGHT // 2, 2):

                # Converts each pixel on the canvas (canvas_x and canvas_y) to a 3d point on the viewport (viewport_x, viewport_y, viewport_z)
                direction:vector3 = multiplyMV(Camera_rotation, canvas_to_viewport(canvas_x, canvas_y))
                # Determine the colo0r seen through that grid square
                color = trace_ray(Camera_pos, direction, 1, math.inf,scene = scene, recursion_depth= 3 , background_color = BACKGROUND_COLOR)

                # Paint the square with that color
                draw_pixel(canvas_x, canvas_y, color, screen = screen)

        # End render
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()