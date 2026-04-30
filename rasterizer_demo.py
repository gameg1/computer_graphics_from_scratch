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
Camera_pos:Vector3 = Vector3(-3, 1, 2) # X, Y, Z - At origin point
Camera_rotation = Make_OY_Rotation_matrix(-30)
#Camera_vector:Vector3 = Vector3(0, 0, 1) # Unit vector pointing towards Z+



scene = [Cube_3d(Vector3(-1.5, 0, 7), 0.75, Identity4x4),
         Cube_3d(Vector3(1.25, 2.5, 7.5),  1, Make_OY_Rotation_matrix(195)), # Cube 2 is looking like a rectangle
         ]



def main():

    #for object in scene:
    #    print(object.transform)
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
    Camera_Matrix = Multiply_MM4(transposed(Camera_rotation), Make_Translation_Matrix(vector3_negate(Camera_pos)))
    for object in scene:
        transform = Multiply_MM4(Camera_Matrix, object.transform)
        Render_instance(object, transform)


def Render_instance(instance, transform):
    projected:list[Vector2] = []
    for V in instance.verts:
        VertexH = Vector4(V.x, V.y, V.z, 1)

        projected.append(project_vertex(Muliply_MV(transform, VertexH)))
    
    for T in instance.Tris:
        Render_triangle(T, projected)


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