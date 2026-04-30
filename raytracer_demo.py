import sys
sys.path.append('../')
from Renderer.Raytracer.raytracer import *
from Renderer.Raytracer.objects import *
from settings import *
from pyray import *
import math

# TODO: Seperate the raytracer software and the objects with the scene.




# Window set up
init_window(WIDTH, HEIGHT, "Raytracer_demo")
set_target_fps(60)
# Camera Info
Camera_pos:Vector3 = Vector3(0, 0, 0) # X, Y, Z - At origin point

Camera_rotation = [
    [0.7071, 0, -0.7071],
    [     0, 1,       0],
    [0.7071, 0,  0.7071],
]
Camera_vector:Vector3 = Vector3(0, 0, 1) # Unit vector pointing towards Z+

        
# Set up the envioment
BACKGROUND_COLOR = BLACK # Black
scene = {
        "objects":[
        sphere(Vector3(0, -1, 3), 1, Color(255, 0 , 0, 255), 500, 0.2),            # Sphere 1
        sphere(Vector3(2, 0, 4), 1, Color(0, 0, 255, 255), 500, 0.3),              # Sphere 2
        sphere(Vector3(-2, 0, 4), 1, Color(0, 255, 0, 255), 10, 0.4),              # Sphere 3
        sphere(Vector3(0, -5001, 0), 5000, Color(255, 255, 0, 255), 1000, 0.5)     # Sphere 4 - The floor
        ],
        "lights":
        [
        light(light.AMBIENT, 0.2),                       # Ambient light
        light(light.POINT, 0.6, Vector3(2, 1, 0)),       # Point light
        light(light.DIRECTIONAL, 0.2, Vector3(1, 4, 4)), # Directional light
        ]
        }




def main():


    # Runs per frame
    while not window_should_close():
        begin_drawing()
        clear_background(BACKGROUND_COLOR)
        # Determine which square on the grid corresponds to this square on the canvas
        
        for canvas_x in range(-WIDTH // 2, WIDTH //2 ):
            for canvas_y in range(-HEIGHT // 2, HEIGHT // 2):

                #direction:Vector3 = multiplyMV(Camera_rotation, canvas_to_viewport(canvas_x, canvas_y))
                direction:Vector3 = canvas_to_viewport(canvas_x, canvas_y)
                # Converts each pixel on the canvas (canvas_x and canvas_y) to a 3d point on the viewport (viewport_x, viewport_y, viewport_z)
                # Determine the color seen through that grid square
                pixel_color:Color = trace_ray(Camera_pos, direction, 1, math.inf,scene = scene, recursion_depth = 3 , background_color = BACKGROUND_COLOR)
                
                # Paint the square with that color
                x = WIDTH // 2 + canvas_x
                y = HEIGHT // 2 - canvas_y
                #draw_pixel(x, y, GREEN)
                draw_pixel(x, y, pixel_color)
                #print(pixel_color.r, pixel_color.g, pixel_color.b, pixel_color.a)
        #draw_text("Hello world", 190, 200, 20, VIOLET)
        for x in range(WIDTH):
            draw_pixel(x, x, RED)
        # End render
        end_drawing()
    close_window()

if __name__ == "__main__":
    main()