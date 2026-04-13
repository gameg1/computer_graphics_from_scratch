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
Camera_pos:vector3 = vector3(0, 0, 0) # X, Y, Z - At origin point
Camera_rotation = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
Camera_vector:vector3 = vector3(0, 0, 1) # Unit vector pointing towards Z+

        
# Set up the envioment
BACKGROUND_COLOR = pygame.Color(255, 255, 255)
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

        draw_shaded_triangle(vector3(-200, -250, 0.0), vector3(200, 50, 0.0), vector3(20, 250, 1.0),color=(0, 255, 0))
        draw_wireframe_triange(vector2(-200, -250), vector2(200, 50), vector2(20, 250),color=(255, 255, 255))



        # End render
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_line(P0:vector2, P1:vector2, color:pygame.Color = (0, 0, 0)): # Default - black
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

def draw_wireframe_triange(P0:vector2, P1:vector2, P2:vector2, color):
    draw_line(P0, P1, color)
    draw_line(P1, P2, color)
    draw_line(P2, P0, color)

def draw_filled_triangle(P0:vector2, P1:vector2, P2:vector2, color):
    """
    for each norizontal line y between the triangle's top and bottom:
        compute x_left and x_right for this y
        draw_line(x_left, y, x_right, y, color)
    """
    # Sort triangle point's by hight (y)
    if P1.y < P0.y: P1, P0 = P0, P1
    if P2.y < P0.y: P2, P0 = P0, P2
    if P2.y < P1.y: P2, P1 = P1, P2

    # Compute the x coordinates of the tiangle edges
    x01:list = interpolate(P0.y, P0.x, P1.y, P1.x)
    x12:list = interpolate(P1.y, P1.x, P2.y, P2.x)
    x02:list = interpolate(P0.y, P0.x, P2.y, P2.x)

    # Concatenate the short sides

    x01.pop()
    x012 = x01 + x12

    # Determine which is left and which is right
    middle = math.floor(len(x02) / 2)
    if x02[middle] < x012[middle]:
        x_left = x02
        x_right = x012
    else:
        x_left = x012
        x_right = x02
    
    # Draw the horizontal segments
    
    for y in range(P0.y, P2.y):
        #print(f"y:{y}, P0.y:{P0.y}, dif:{y - P0.y}, x_right_lenth:{len(x_right)}")

        for x in range(int(x_left[y - P0.y]), int(x_right[y - P0.y])):
            draw_pixel(x, y, color, screen)

def draw_shaded_triangle(P0:vector3, P1:vector3, P2:vector3, color:pygame.Color):
    # Simular to draw_filled_triangle but uses vec3's to store a value H in the Z direction, ranging from 0 to 1.
    
    # Sort the points so that P0.y <= P1.y <= P2.y
    if P1.y < P0.y: P1, P0 = P0, P1
    if P2.y < P0.y: P2, P0 = P0, P1
    if P2.y < P1.y: P2, P1 = P1, P2

    # Compute the x coordinates and h values of the triangle edges
    x01 = interpolate(P0.y, P0.x, P1.y, P1.x)
    h01 = interpolate(P0.y, P0.z, P1.y, P1.z)

    x12 = interpolate(P1.y, P1.x, P2.y, P2.x)
    h12 = interpolate(P1.y, P1.z, P2.y, P2.z)

    x02 = interpolate(P0.y, P0.x, P2.y, P2.x)
    h02 = interpolate(P0.y, P0.z, P2.y, P2.z)

    # Concatenate the short sides
    x01.pop()
    x012 = x01 + x12

    h01.pop()
    h012 = h01 + h12

    # Determine which is left and which is right
    m = math.floor(len(x012)/2)
    if x02[m] < x012[m]:
        x_left = x02
        h_left = h02

        x_right = x012
        h_right = h012
    else:
        x_left = x012
        h_left = h012

        x_right = x02
        h_right = h02

    # Draw the horizontal segments
    for y in range(P0.y, P2.y -1):
        x_l = int(x_left[y - P0.y])
        x_r = int(x_right[y - P0.y])
        h_segment = interpolate(x_l, h_left[y - P0.y],x_r, h_right[y - P0.y])
        for x in range(x_l, x_r):
            r,g,b = color
            shaded_r = int(r * h_segment[x - x_l])
            shaded_g = int(g * h_segment[x - x_l])
            shaded_b = int(b * h_segment[x - x_l])
            #print(shaded_r, shaded_g, shaded_b)
            shaded_color = pygame.Color(shaded_r, shaded_g, shaded_b)
            draw_pixel(x ,y, shaded_color, screen=screen)

def interpolate(i0:int, d0:float, i1:int, d1:float)->list[float]:
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