from Renderer.Rasterizer.rasterizer import *
from pyray import *

class cube_3d:
    def __init__(self, vAf:Vector3, vBf:Vector3, vCf:Vector3, vDf:Vector3, vAb:Vector3, vBb:Vector3, vCb:Vector3, vDb:Vector3):
        # The four front vertices
        self.vAf = vAf
        self.vBf = vBf
        self.vCf = vCf
        self.vDf = vDf

        # The four back vertices
        self.vAb = vAb
        self.vBb = vBb
        self.vCb = vCb
        self.vDb = vDb

    def draw(self, color= Color(255, 255, 255, 255)):
        # Front face
        draw_line_ras(project_vertex(self.vAf), project_vertex(self.vBf),Color(0, 0, 255, 255))
        draw_line_ras(project_vertex(self.vBf), project_vertex(self.vCf),Color(0, 0, 255, 255))
        draw_line_ras(project_vertex(self.vCf), project_vertex(self.vDf),Color(0, 0, 255, 255))
        draw_line_ras(project_vertex(self.vDf), project_vertex(self.vAf),Color(0, 0, 255, 255))

        # Back face

        draw_line_ras(project_vertex(self.vAb), project_vertex(self.vBb), Color(255, 0, 0, 255))
        draw_line_ras(project_vertex(self.vBb), project_vertex(self.vCb), Color(255, 0, 0, 255))
        draw_line_ras(project_vertex(self.vCb), project_vertex(self.vDb), Color(255, 0, 0, 255))
        draw_line_ras(project_vertex(self.vDb), project_vertex(self.vAb), Color(255, 0, 0, 255))

        # Front to back lines
        draw_line_ras(project_vertex(self.vAf), project_vertex(self.vAb), Color(0, 255, 0, 255))
        draw_line_ras(project_vertex(self.vBf), project_vertex(self.vBb), Color(0, 255, 0, 255))
        draw_line_ras(project_vertex(self.vCf), project_vertex(self.vCb), Color(0, 255, 0, 255))
        draw_line_ras(project_vertex(self.vDf), project_vertex(self.vDb), Color(0, 255, 0, 255))

class triangle_wireframe:
    def __init__(self, P0:Vector2, P1:Vector2, P2:Vector2, color:Color):
        self.P0 = P0
        self.P1 = P1
        self.P2 = P2
        self.color = Color
    
    def draw(self):
        draw_line_ras(self.P0, self.P1, self.color)
        draw_line_ras(self.P1, self.P2, self.color)
        draw_line_ras(self.P2, self.P0, self.color)

class triangle_filled:
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

class triangle_shaded:
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