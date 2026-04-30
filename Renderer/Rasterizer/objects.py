from Renderer.Rasterizer.rasterizer import *
from pyray import *


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
        self.color = Color
    
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
        
        for y in range(self.P0.y, self.P2.y):
            #print(f"y:{y}, P0.y:{P0.y}, dif:{y - P0.y}, x_right_lenth:{len(x_right)}")

            for x in range(int(x_left[y - self.P0.y]), int(x_right[y - self.P0.y])):
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

class Cube_3d:
    # Vertices

    A = Vector3( 1,  1,  1)
    B = Vector3(-1,  1,  1)
    C = Vector3(-1, -1,  1)
    D = Vector3( 1, -1,  1)
    E = Vector3( 1,  1, -1)
    F = Vector3(-1,  1, -1)
    G = Vector3(-1, -1, -1)
    H = Vector3( 1, -1, -1)

    verts = [
                A,
                B,
                C,
                D,
                E,
                F,
                G,
                H,
            ]

    # triangles

    Tris = [
        [0, 1, 2, RED],
        [0, 2, 3, RED],
        [4, 0, 3, GREEN],
        [4, 3, 7, GREEN],
        [5, 4, 7, BLUE],
        [5, 7, 6, BLUE],
        [1, 5, 6, YELLOW],
        [1, 6, 2, YELLOW],
        [4, 5, 1, PURPLE],
        [4, 1, 0, PURPLE],
        [2, 6, 7, SKYBLUE],
        [2, 7, 3, SKYBLUE]
            ]


    def __init__(self, pos:Vector3 = Vector3(0, 0, 0), scale:float = 1, rotation:Mat4x4 = Identity4x4): 
        self.pos = pos
        self.rotation = rotation
        self.scale = scale
        self.transform:Mat4x4 = Multiply_MM4(Make_Translation_Matrix(self.pos), Multiply_MM4(self.rotation, Make_Scaling_Matrix(self.scale)))
        
        
