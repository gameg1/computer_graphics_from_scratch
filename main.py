import pygame
import pygame.gfxdraw
import math



WIDTH = 600
HEIGHT = 600
pygame.init()

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

class sphere:
    def __init__(self, pos:vector3, radius:float, color:pygame.Color, specular:int = -1):
        self.pos = pos
        self.radius = radius
        self.color:pygame.Color = color
        self.specular = specular

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
# Window set up
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Camera Info
Camera_pos:vector3 = vector3(0, 0, 0) # X, Y, Z - At origin point
Camera_vector:vector3 = vector3(0, 0, 1) # Unit vector pointing towards Z+

# Viewport Info
viewport_width = 1
viewport_height = 1
viewport_distance = 1

        
# Set up the envioment
BACKGROUND_COLOR = pygame.Color(255, 255, 255)
scene_objects = [
        sphere(vector3(0, -1, 3), 1, (255, 0 , 0), 500),            # Sphere 1
        sphere(vector3(2, 0, 4), 1, (0, 0, 255), 500),              # Sphere 2
        sphere(vector3(-2, 0, 4), 1, (0, 255, 0), 10),              # Sphere 3
        sphere(vector3(0, -5001, 0), 5000, (255, 255, 0), 1000)     # Sphere 4 - The floor
        ]
scene_lights = [
        light(light.AMBIENT, 0.2),                       # Ambient light
        light(light.POINT, 0.6, vector3(2, 1, 0)),       # Point light
        light(light.DIRECTIONAL, 0.2, vector3(1, 4, 4)), # Directional light
        ]



def main():

    clock = pygame.time.Clock()
    running = True
    # Runs per frame
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Determine which square on the grid corresponds to this square on the canvas
        for canvas_x in range(-(WIDTH // 2), WIDTH // 2):
            for canvas_y in range(-(HEIGHT // 2), HEIGHT // 2):

                # Converts each pixel on the canvas (canvas_x and canvas_y) to a 3d point on the viewport (viewport_x, viewport_y, viewport_z)
                direction:vector3 = canvas_to_viewport(canvas_x, canvas_y)
                # Determine the colo0r seen through that grid square
                color = trace_ray(Camera_pos, direction, 1, math.inf)

                # Paint the square with that color
                draw_pixel(canvas_x, canvas_y, color)
                
                pass

        # End render
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def draw_pixel(x, y, color:pygame.Color):
    """Draws a pixel to the screen with 0,0 being the center of the screen"""
    Screen_X = int((WIDTH /2) + x)
    Screen_Y = int((HEIGHT /2) - y)
    r, g, b = clamp(color[0]), clamp(color[1]), clamp(color[2])


    pygame.gfxdraw.pixel(screen, Screen_X, Screen_Y, (r, g, b))

def canvas_to_viewport(x:int, y:int):
    """Returns a vector3 from a canvas x, y co-ordernents to viewport x, y, x"""
    return vector3(x * (viewport_width / WIDTH), y * (viewport_height / HEIGHT), viewport_distance)

def trace_ray(O:vector3, d:vector3, t_min, t_max):
    closest_t = math.inf
    closest_sphere:sphere = None
    for object in scene_objects:
        t1, t2 = intersect_ray_sphere(O, d, object)
        if t1 < closest_t and t_min < t1 < t_max:
            closest_t = t1
            closest_sphere = object
        if t2 < closest_t and t_min < t2 < t_max:
            closest_t = t2
            closest_sphere = object
    if closest_sphere == None:
        return BACKGROUND_COLOR
    
    point = O + d * closest_t  # Compute intersection
    normal = closest_sphere.normal(point)
    normal = normal.normalized()
    intensity = compute_lighting(point, normal, -d, closest_sphere.specular)
    r, g, b = closest_sphere.color
    return pygame.Color(clamp(int(r * intensity)), clamp(int(g * intensity)), clamp(int(b * intensity)))
    
def intersect_ray_sphere(O:vector3, D:vector3, sphere:sphere):
    r = sphere.radius
    CO = O - sphere.pos

    a = vector3.dot_product(D, D)
    b = 2 * vector3.dot_product(CO, D)
    c = vector3.dot_product(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return (math.inf, math.inf)
    
    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return t1, t2

def compute_lighting(point:vector3, normal:vector3, V:vector3, specular:int):
    i:float = 0.0
    for light in scene_lights:
        if light.type == light.AMBIENT:
            i += light.intensity
        else:
            if light.type == light.POINT:
                L = light.position - point
            elif light.type == light.DIRECTIONAL:
                L = light.direction
            # Diffuse
            n_dot_l = vector3.dot_product(normal, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l / (normal.magnitude() * L.magnitude())
            
            # Specular
            if specular != -1:
                reflection:vector3 = (normal * 2) * vector3.dot_product(normal, L) - L
                r_dot_v = vector3.dot_product(reflection, V)
                if r_dot_v > 0:
                    i += light.intensity * math.pow(r_dot_v / ((reflection.magnitude()) * (V.magnitude())), specular)

    return i


def clamp (n:int):
    if n < 0:
        return 0
    elif n > 255:
        return 255
    else:
        return n
if __name__ == "__main__":
    main()