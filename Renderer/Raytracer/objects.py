from vector import *
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