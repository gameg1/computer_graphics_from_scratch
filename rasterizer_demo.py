import sys
sys.path.append('../')
from Renderer.Rasterizer.rasterizer import *
from Renderer.Rasterizer.objects import *
from settings import *
from pyray import *
import math






# Window set up
init_window(WIDTH, HEIGHT, "Rasterizer Demo")

s2 = 1.0 / math.sqrt(2)
# Camera Info
Camera_pos:Vector3 = Vector3(-3, 1, 2) # X, Y, Z - At origin point
Camera_rotation = Make_OY_Rotation_matrix(-30)
Camera_clipping_planes = [
    Plane(Vector3(  0,   0,  1), -1), # Near
    Plane(Vector3( s2,   0, s2),  0), # Left
    Plane(Vector3(-s2,   0, s2),  0), # Right
    Plane(Vector3(  0, -s2, s2),  0), # Top
    Plane(Vector3(  0,  s2, s2),  0), # Bottom
]

camera = Camera_ras(Camera_pos, Camera_rotation, Camera_clipping_planes)


scene = [Instance(Cube, Vector3(-1.5, 0,     7), Identity4x4, 0.75),
         Instance(Cube, Vector3(1.25, 2.5, 7.5), Make_OY_Rotation_matrix(195)),
         Instance(Cube, Vector3(   0,   0, -10), Make_OY_Rotation_matrix(195))
         ]





def main():

    #for object in scene:
    #    print(object.transform)
    # Runs per frame
    while not window_should_close():
        begin_drawing()
        clear_background(WHITE)
        Render_scene(scene=scene, camera = camera)

        #draw_line_ras(Vector2(-100,200), Vector2(200, -50), RED) # Debug line

        # End render
        end_drawing()

    close_window()

# === Rasterizer ===


if __name__ == "__main__":
    main()