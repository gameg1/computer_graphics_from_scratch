from settings import *
from pyray import *
import math
#from. import objects
# TODO: Fix circular imports

# === Classes ===
class Mat4x4:
    def __init__ (self, data):
        self.data = data

class Plane:
    def __init__(self, normal:Vector3, distance:float):
        self.normal = normal
        self.distance = distance

class Camera_ras:
    def __init__(self, pos:Vector3, rotation:Mat4x4, clipping_planes:list[Plane]):
        self.pos = pos
        self.rotation = rotation
        self.clipping_planes = clipping_planes



#=== Mat 4x4 math ===



Identity4x4:Mat4x4 = Mat4x4([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1],])

def Make_OY_Rotation_matrix(degrees):
    cos = math.cos(degrees*math.pi/180.0)
    sin = math.sin(degrees*math.pi/180.0)
    return Mat4x4([[cos, 0, -sin, 0],
                   [  0, 1,    0, 0],
                   [sin, 0,  cos, 0],
                   [  0, 0,    0, 1],])

def Make_Translation_Matrix(translation:Vector3):
    return Mat4x4([[1, 0, 0, translation.x],
                   [0, 1, 0, translation.y],
                   [0, 0, 1, translation.z],
                   [0, 0, 0,             1],])

def Make_Scaling_Matrix(scale:float):
    return Mat4x4([[scale,      0,     0, 0],
                   [     0, scale,     0, 0],
                   [     0,     0, scale, 0],
                   [     0,     0,     0, 1],])

def Muliply_MV(matrix:Mat4x4, V:Vector4):
    result =[0, 0, 0, 0]
    vec = [V.x, V.y, V.z, V.w]

    for i in range(4):
        for j in range(4):
            result[i] += matrix.data[i][j]*vec[j]
    
    return Vector4(result[0], result[1], result[2], result[3])

def Multiply_MM4(matA:Mat4x4, matB:Mat4x4):
    result = Mat4x4([[0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],
                     [0, 0, 0, 0],])
    
    for i in range(4):
        for j in range(4):
            for k in range(4):
                result.data[i][j] += matA.data[i][k] * matB.data[k][j]
    
    return result

def transposed(mat:Mat4x4):
    result = Mat4x4([[1, 0, 0, 0],
                     [0, 1, 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1],])
    
    for i in range(4):
        for j in range(4):
            result.data[i][j] = mat.data[j][i]

    return result

# === Triangles ===
class Triangle:
    def __init__(self, P0:Vector2, P1:Vector2, P2:Vector2, color:Color):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.color = color
    
    def draw(self):
        draw_line_ras(self.P0, self.P1, self.color)
        draw_line_ras(self.P1, self.P2, self.color)
        draw_line_ras(self.P2, self.P0, self.color)

class Triangle_filled:
    def __init__(self, P0:Vector2, P1:Vector2, P2:Vector2, color:Color):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.color = color
    
    def draw(self):
        """
        for each norizontal line y between the triangle's top and bottom:
            compute x_left and x_right for this y
            draw_line(x_left, y, x_right, y, color)
        """
        # Sort triangle point's by hight (y)
        if self.P1.y < self.P0.y: self.P1, self.P0 = self.P0, self.P1
        if self.P2.y < self.P0.y: self.P2, self.P0 = self.P0, self.P2
        if self.P2.y < self.P1.y: self.P2, self.P1 = self.P1, self.P2

        # Compute the x coordinates of the tiangle edges
        x01:list = interpolate(self.P0.y, self.P0.x, self.P1.y, self.P1.x)
        x12:list = interpolate(self.P1.y, self.P1.x, self.P2.y, self.P2.x)
        x02:list = interpolate(self.P0.y, self.P0.x, self.P2.y, self.P2.x)

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
        
        for y in range(int(self.P0.y), int(self.P2.y)-1):
            #print(f"y:{y}, P0.y:{P0.y}, dif:{y - P0.y}, x_right_lenth:{len(x_right)}")
            for x in range(int(x_left[int(y - self.P0.y)]), int(x_right[int(y - self.P0.y)])):
                draw_pixel_ras(x, y, self.color)

class Triangle_shaded:
    def __init__(self, P0:Vector3, P1:Vector3, P2:Vector3, color:Color):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.color = color

    def draw(self):
        # Simular to draw_filled_triangle but uses vec3's to store a value H in the Z direction, ranging from 0 to 1.
        
        # Sort the points so that P0.y <= P1.y <= P2.y
        if self.P1.y < self.P0.y: self.P1, self.P0 = self.P0, self.P1
        if self.P2.y < self.P0.y: self.P2, self.P0 = self.P0, self.P1
        if self.P2.y < self.P1.y: self.P2, self.P1 = self.P1, self.P2

        # Compute the x coordinates and h values of the triangle edges
        x01 = interpolate(self.P0.y, self.P0.x, self.P1.y, self.P1.x)
        h01 = interpolate(self.P0.y, self.P0.z, self.P1.y, self.P1.z)

        x12 = interpolate(self.P1.y, self.P1.x, self.P2.y, self.P2.x)
        h12 = interpolate(self.P1.y, self.P1.z, self.P2.y, self.P2.z)

        x02 = interpolate(self.P0.y, self.P0.x, self.P2.y, self.P2.x)
        h02 = interpolate(self.P0.y, self.P0.z, self.P2.y, self.P2.z)

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
        for y in range(self.P0.y, self.P2.y -1):
            x_l = int(x_left[y - self.P0.y])
            x_r = int(x_right[y - self.P0.y])
            h_segment = interpolate(x_l, h_left[y - self.P0.y], x_r, h_right[y - self.P0.y])
            for x in range(x_l, x_r):
                r,g,b = self.color
                shaded_r = int(r * h_segment[x - x_l])
                shaded_g = int(g * h_segment[x - x_l])
                shaded_b = int(b * h_segment[x - x_l])
                #print(shaded_r, shaded_g, shaded_b)
                shaded_color = Color(shaded_r, shaded_g, shaded_b, 255)
                draw_pixel_ras(x, y, shaded_color)

# == Objects & Instances ===

class Object:
    def __init__(self, vertices:list[Vector3], tris:list[list], bound_center, bound_radius):
        self.vertices = vertices
        self.tris = tris
        self.bound_center = bound_center
        self.bound_radius = bound_radius


class Instance:
    def __init__(self, object:Object, position, rotation:Mat4x4 = Identity4x4, scale:float = 1.0):
        self.object = object
        self.position = position
        self.rotation = rotation
        self.scale = scale
        self.transform:Mat4x4 = Multiply_MM4(Make_Translation_Matrix(self.position), Multiply_MM4(self.rotation, Make_Scaling_Matrix(self.scale)))

# === Rasterizer ===

def draw_pixel_ras(x:int, y:int, color:Color):
    """Draws a pixel to the screen with 0,0 being the center of the screen"""
    Screen_X = int((WIDTH /2) + x)
    Screen_Y = int((HEIGHT /2) - y)
    #print(color)
    #print(type(color))
    draw_pixel(Screen_X, Screen_Y, color)

def viewport_to_canvas(x, y):
    return Vector2(int(x * WIDTH/VIEWPORT_WIDTH),int( y*HEIGHT/VIEWPORT_HIGHT))

def project_vertex(v:Vector3):
    return viewport_to_canvas(v.x * VIEWPORT_DISTANCE / v.z, v.y * VIEWPORT_DISTANCE / v.z)

def draw_line_ras(P0:Vector2, P1:Vector2, color:Color = (0, 0, 0, 255)): # Default - black
    if abs(P1.x - P0.x) > abs(P1.y - P0.y):
        # Line is more horizontal
        # make sure that x0 < x1
        if P0.x > P1.x:
            P0, P1 = P1, P0
        ys = interpolate(P0.x, P0.y, P1.x, P1.y)
        for x in range(int(P0.x), int(P1.x)):
            draw_pixel_ras(x, ys[int(x-P0.x)], color)
    else:
        # Line is more vertical
        # Make sure y0 < y1:
        if P0.y > P1.y:
            P0, P1 = P1, P0
        xs = interpolate(P0.y, P0.x, P1.y, P1.x)
        for y in range(int(P0.y), int(P1.y)):
            draw_pixel_ras(xs[int(y - P0.y)], y, color)

def draw_shaded_triangle(P0:Vector3, P1:Vector3, P2:Vector3, color:Color):
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
            shaded_color = Color(shaded_r, shaded_g, shaded_b, 255)
            draw_pixel_ras(x, y, shaded_color)

def interpolate(i0:int, d0:float, i1:int, d1:float)->list[float]:
    """Linear interpolates from d0 to d1 in i1 - 10 steps"""
    if i0 == i1:
        return [d0]
    values=[]
    a = (d1 - d0) / (i1 - i0)
    d = d0
    for i in range(int(i0), int(i1)):
        values.append(d)
        d = d + a
    return values

# New stuff to fix

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


def Render_scene(scene:list[Instance], camera:Camera_ras):
    Camera_Matrix = Multiply_MM4(transposed(camera.rotation), Make_Translation_Matrix(vector3_negate(camera.pos)))
    for inst in scene:
        transform = Multiply_MM4(Camera_Matrix, inst.transform)
        clipped =  Transfrom_and_clip(camera.clipping_planes, inst.object, inst.scale, transform)
        if clipped !=None:
            Render_model(clipped)

def Render_model(object:Object):
    projected:list[Vector2] = []
    for V in object.vertices:
        projected.append(project_vertex(V))
    
    for T in object.tris:
        Render_triangle(T, projected)

def Render_triangle(T, projected:list[Vector2]):
    tri = Triangle_filled(
        projected[T[0]],#P0
        projected[T[1]],#P1
        projected[T[2]],#P2
        T[3], #Color
    ).draw()