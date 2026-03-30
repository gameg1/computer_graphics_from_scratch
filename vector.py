import math

class vector3:
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"
    def __add__(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return vector3(self.x + other.x, self.y + other.y, self.z + other.z)
    
    def __sub__(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if isinstance(other, float):
            return vector3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, int):
            return vector3(self.x * other, self.y * other, self.z * other)
        return NotImplemented
    
    def __truediv__(self, other):
        if isinstance(other, vector3):
            return vector3(self.x / other.x, self.y / other.y, self.z / other.z)
        elif isinstance(other, float):
            return vector3(self.x / other, self.y / other, self.z / other)
        return NotImplemented
    
    def __neg__(self):
        return vector3(-self.x, -self.y, -self.z)

    def dot_product(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def magnitude(self) -> float:
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalized(self):
        return self / self.magnitude()
    

def multiplyMV(mat, vec):
    result = [0, 0, 0]
    vec = [vec.x, vec.y, vec.z]

    for i in range(3):
        for j in range(3):
            result[i] += vec[j] * mat[i][j]

    return vector3(result[0], result[1], result[2])