import sys
sys.path.append('../')
from Renderer.Rasterizer.rasterizer import *
from Renderer.Rasterizer.objects import *
from settings import *
from pyray import *
import math






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



scene = [Cube_3d(Vector3(-1.5, 0, 7)),
         Cube_3d(Vector3(1.25, 2, 7.5)),
         ]



def main():

    # Runs per frame
    while not window_should_close():
        begin_drawing()
        #clear_background(WHITE)
        Render_scene(scene=scene)

        #draw_line_ras(Vector2(-100,200), Vector2(200, -50), RED) # Debug line

        # End render
        end_drawing()

    close_window()

def Render_scene(scene:list):
    for i in scene:
        Render_instance(i)


def Render_instance(instance):
    projected:list[Vector2] = []
    for V in instance.verts:
        V_new = Apply_Transform(V, instance.transfrom)
        projected.append(project_vertex(V_new))
    
    for T in instance.Tris:
        Render_triangle(T, projected)

def Apply_Transform(vertex, transform):
    scaled = Scale(vertex, transform["scale"])
    rotated = Rotate(scaled, transform["rotation"])
    translated = Translate(rotated, transform["position"])
    return translated

def Scale(v, scale):
    pass
def Rotate(v, rotation):
    pass
def Translate(v, translate):
    pass
def Render_triangle(T:list, projected:list[Vector2]):
    #print(type(T.P0))
    #print(projected)
    tri = Triangle(
        projected[T[0]],#P0
        projected[T[1]],#P1
        projected[T[2]],#P2
        T[3], #Color
    ).draw()

if __name__ == "__main__":
    main()