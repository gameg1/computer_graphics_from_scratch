import sys
sys.path.append('../')
from Renderer.Rasterizer.rasterizer import *
from Renderer.Rasterizer.objects import *
from pyray import *
from settings import *






# Window set up
init_window(WIDTH, HEIGHT, "Rasterizer Demo")

# Camera Info
Camera_pos:Vector3 = Vector3(0, 0, 0) # X, Y, Z - At origin point
Camera_rotation = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
]
Camera_vector:Vector3 = Vector3(0, 0, 1) # Unit vector pointing towards Z+



cube:cube_3d = cube_3d(
Vector3(-2, -0.5, 5),
Vector3(-2,  0.5, 5),
Vector3(-1,  0.5, 5),
Vector3(-1, -0.5, 5),
Vector3(-2, -0.5, 6),
Vector3(-2,  0.5, 6),
Vector3(-1,  0.5, 6),
Vector3(-1, -0.5, 6),
)


def main():

    # Runs per frame
    while not window_should_close():
        begin_drawing()
        # # Determine which square on the grid corresponds to this square on the canvas
        # for canvas_x in range(-(WIDTH // 2), WIDTH // 2, 2):
        #     for canvas_y in range(-(HEIGHT // 2), HEIGHT // 2, 2):
        #         pass

        # draw_shaded_triangle(vector3(-200, -250, 0.0), vector3(200, 50, 0.0), vector3(20, 250, 1.0),color=(0, 255, 0))
        # draw_wireframe_triange(vector2(-200, -250), vector2(200, 50), vector2(20, 250),color=(255, 255, 255))
        cube.draw()


        # End render
        end_drawing()

    close_window()

if __name__ == "__main__":
    main()