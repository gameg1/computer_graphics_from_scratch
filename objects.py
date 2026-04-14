from vector import *
from rasterizer import draw_line, project_vertex
import pygame

class sphere:
    def __init__(self, pos:vector3, radius:float, color:pygame.Color, specular:int = -1, reflective:float = 0.0):
        self.pos = pos
        self.radius = radius
        self.color:pygame.Color = color
        self.specular = specular
        self.reflective = reflective

    def normal(self, position:vector3):
        return (position - self.pos)/vector3.magnitude(position - self.pos)

class cube_3d:
    def __init__(self, vAf:vector3, vBf:vector3, vCf:vector3, vDf:vector3, vAb:vector3, vBb:vector3, vCb:vector3, vDb:vector3):
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

    def draw(self, color= pygame.Color(255, 255, 255)):
        # Front face
        draw_line(project_vertex(self.vAf), project_vertex(self.vBf),pygame.Color(0, 0, 255))
        draw_line(project_vertex(self.vBf), project_vertex(self.vCf),pygame.Color(0, 0, 255))
        draw_line(project_vertex(self.vCf), project_vertex(self.vDf),pygame.Color(0, 0, 255))
        draw_line(project_vertex(self.vDf), project_vertex(self.vAf),pygame.Color(0, 0, 255))

        # Back face

        draw_line(project_vertex(self.vAb), project_vertex(self.vBb), pygame.Color(255, 0, 0))
        draw_line(project_vertex(self.vBb), project_vertex(self.vCb), pygame.Color(255, 0, 0))
        draw_line(project_vertex(self.vCb), project_vertex(self.vDb), pygame.Color(255, 0, 0))
        draw_line(project_vertex(self.vDb), project_vertex(self.vAb), pygame.Color(255, 0, 0))

        # Front to back lines
        draw_line(project_vertex(self.vAf), project_vertex(self.vAb), pygame.Color(0, 255, 0))
        draw_line(project_vertex(self.vBf), project_vertex(self.vBb), pygame.Color(0, 255, 0))
        draw_line(project_vertex(self.vCf), project_vertex(self.vCb), pygame.Color(0, 255, 0))
        draw_line(project_vertex(self.vDf), project_vertex(self.vAb), pygame.Color(0, 255, 0))



class light:
    AMBIENT = 0
    POINT = 1
    DIRECTIONAL = 2
    def __init__(self, type:int, intensity:float, vec3:vector3 = vector3(0,0,0)):
        self.type:int = type
        self.intensity:float = intensity
        if type == 1:
            self.position:vector3 = vec3
        elif type == 2:
            self.direction:vector3 = vec3