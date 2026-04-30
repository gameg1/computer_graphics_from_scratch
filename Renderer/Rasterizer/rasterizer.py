from settings import *
from pyray import *
import math

#=== Mat 4x4 math ===

class Mat4x4:
    def __init__ (self, data):
        self.data = data

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

#=== End of Mat 4x4 math ===

def draw_pixel_ras(x:int, y:int, color:Color):
    """Draws a pixel to the screen with 0,0 being the center of the screen"""
    Screen_X = int((WIDTH /2) + x)
    Screen_Y = int((HEIGHT /2) - y)

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