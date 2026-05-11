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
# Camera_vector:Vector3 = Vector3(0, 0, 1) # Unit vector pointing towards Z+



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
        Render_scene(scene=scene)

        #draw_line_ras(Vector2(-100,200), Vector2(200, -50), RED) # Debug line

        # End render
        end_drawing()

    close_window()

# === Rasterizer ===
def Transfrom_and_clip(planes:list[Plane], object:Object, scale:float, transform:Mat4x4):
    # Transform the bounding sphere, and attempt early discard.
    center = Muliply_MV(transform, Vector4(object.bound_center.x, object.bound_center.y, object.bound_center.z, 1))
    radius = object.bound_radius * scale
    for P in planes:
        distance = Signed_distance(P, Vector3(center.x, center.y, center.z))
        #print(distance)
        #print(-radius)
        if distance < -radius:
            return None

    # Apply modelview transfrom
    vertices = []
    for V in object.vertices:
        tf = Muliply_MV(transform, Vector4(V.x, V.y, V.z, 1))
        vertices.append(Vector3(tf.x, tf.y, tf.z))
    
    # Clip the entire model against each successive plane.
    triangles = object.tris
    for P in planes:
        new_triangles = []
        for T in triangles:
            Clip_Triangle(T, P, new_triangles, vertices)
        triangles = new_triangles
    
    return Object(vertices, triangles, Vector3(0, 0, 0), bound_radius= object.bound_radius)

def Clip_Triangle(triangle:list, plane:Plane, triangles:list[list], vertices:list[Vector3]):
    #print(triangle)
    #print("pass")
    d0:Vector3 = vertices[triangle[0]]
    d1:Vector3 = vertices[triangle[1]]
    d2:Vector3 = vertices[triangle[2]]

    in0:bool = Signed_distance(plane, d0) > 0
    in1:bool = Signed_distance(plane, d1) > 0
    in2:bool = Signed_distance(plane, d2) > 0

    in_count = in0 + in1 + in2

    if in_count == 3: # All positive
        triangles.append(triangle)
    elif in_count == 0: # All Negitive
        pass
    elif in_count == 1: # One positive
        if in0 == True: # d0 positive
            A = d0
            B = d1
            C = d2
            T1 = triangle[0]
        elif in1 == True: # d1 positive
            A = d1
            B = d2
            C = d0
            T1 = triangle[1]
        else:             # d2 positive
            A = d2
            B = d0
            C = d1
            T1 = triangle[2]
        # Calculate new Vertices
        B_new:Vector3 = Intersection(A, B, plane)
        C_new:Vector3 = Intersection(A, C, plane)
        # Add to the list
        vertices.append(B_new)
        vertices.append(C_new)
        # Create new triangle that lists new vertices
        triangles.append([T1, len(vertices)-2, len(vertices)-1, triangle[3]])
    else: # Two positive
        if in2 == False: # d2 False
            A = d0
            B = d1
            C = d2
            T1 = triangle[0]
            T2 = triangle[1]
        elif in0 == False: # d0 False
            A = d1
            B = d2
            C = d0
            T1 = triangle[1]
            T2 = triangle[2]
        else:   # d1 False
            A = d2
            B = d0
            C = d1
            T1 = triangle[2]
            T2 = triangle[0]
        if (in0 == False) and (in1 == False) and (in2 == False):
            print("all in's are false")
        # Calculate new Vertices
        A_new = Intersection(A, C, plane)
        B_new = Intersection(B, C, plane)
        # Add to the list
        vertices.append(A_new)
        vertices.append(B_new)
        # Create new triangles that lists the new vertices
        triangles.append([             T1, T2, len(vertices)-2, triangle[3]])
        triangles.append([len(vertices)-2, T2, len(vertices)-1, triangle[3]])

def Intersection(A:Vector3, B:Vector3, plane:Plane)-> Vector3:
    D = plane.distance
    N = plane.normal
    T = -D - vector3_dot_product(N, A) / vector3_dot_product(N, vector3_subtract(B, A))
    if T > 1:
        print("T is above 1")
        exit(1)
    elif T < 0:
        print("T smaller than 0")
        exit(2)
    Q:Vector3 = vector3_add(A, vector3_multiply(Vector3(T, T, T),vector3_subtract(A, B)))

    return Q


def Signed_distance(plane:Plane, vertex:Vector3):
    normal:Vector3 = plane.normal
    return vector3_dot_product(normal, vertex) + plane.distance
    #return (vertex.x * normal.x) + (vertex.y * normal.y) + (vertex.z * normal.z) + plane.distance


def Render_scene(scene:list[Instance]):
    Camera_Matrix = Multiply_MM4(transposed(Camera_rotation), Make_Translation_Matrix(vector3_negate(Camera_pos)))
    for inst in scene:
        transform = Multiply_MM4(Camera_Matrix, inst.transform)
        clipped =  Transfrom_and_clip(Camera_clipping_planes, inst.object, inst.scale, transform)
        if clipped !=None:
            Render_model(clipped)

def Render_model(object:Object):
    projected:list[Vector2] = []
    for V in object.vertices:
        projected.append(project_vertex(V))
    
    for T in object.tris:
        Render_triangle(T, projected)

def Render_triangle(T, projected:list[Vector2]):
    #print(type(T))
    #print(T)
    #print(T[0])
    #print(projected)
    tri = Triangle(
        projected[T[0]],#P0
        projected[T[1]],#P1
        projected[T[2]],#P2
        T[3], #Color
    ).draw()

if __name__ == "__main__":
    main()