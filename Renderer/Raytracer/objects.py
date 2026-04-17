from pyray import *

def vector3_divide_scalar(v:Vector3, scalar:float)->Vector3:
    return Vector3(v.x / scalar, v.y / scalar, v.z / scalar)

class sphere:
    def __init__(self, pos:Vector3, radius:float, color:Color, specular:int = -1, reflective:float = 0.0):
        self.pos:Vector3 = pos
        self.radius = radius
        self.color:Color = color
        self.specular = specular
        self.reflective = reflective
    def normal(self, position:Vector3)->Vector3:
        return vector3_divide_scalar(vector3_subtract(position, self.pos),vector3_length(vector3_subtract(position, self.pos)))


class light:
    AMBIENT = 0
    POINT = 1
    DIRECTIONAL = 2
    def __init__(self, type:int, intensity:float, vec3:Vector3 = Vector3(0,0,0)):
        self.type:int = type
        self.intensity:float = intensity
        if type == 1:
            self.position:Vector3 = vec3
        elif type == 2:
            self.direction:Vector3 = vec3