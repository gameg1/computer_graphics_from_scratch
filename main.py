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
        return vector3(self.x + other.x, self.y + other.y, self.x + other.x)
    
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

    def dot_product(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def magnitude(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)
    
    def normalized(self):
        return self / self.magnitude()

class sphere:
    def __init__(self, pos:vector3, radius:float, color:tuple[int, int, int]):
        self.pos = pos
        self.radius = radius
        self.color = color

    def normal(self, position:vector3):
        return (position - self.pos)/vector3.magnitude(position - self.pos)

class light:
    def __init__(self, type:str, intensity:float, vec3:vector3 = vector3(0,0,0)):
        if type not in ["ambient", "point", "directional"]:
            return NotImplemented
        self.type:str = type
        self.intensity:float = intensity
        if type == "point":
            self.position:vector3 = vec3
        elif type == "directional":
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
BACKGROUND_COLOR = (255, 255, 255)
scene_objects = [
        sphere(vector3(0, -1, 3), 1, (255, 0 , 0)), # Sphere 1
        sphere(vector3(2, 0, 4), 1, (0, 0, 255)),   # Sphere 2
        sphere(vector3(-2, 0, 4), 1, (0, 255, 0)),  # Sphere 3
        sphere(vector3(0, -5001, 0), 5000, (255, 255, 0))
        ]
scene_lights = [
        light("ambient", 0.2),                      # Ambient light
        light("point", 0.6, vector3(2, 1, 0)),      # Point light
        light("directional", 0.2, vector3(1, 4, 4)) # Directional light
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

def draw_pixel(x, y, color:tuple[int, int, int]):
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
    closest_sphere = None
    for sphere in scene_objects:
        t1, t2 = intersect_ray_sphere(O, d, sphere)
        if t1 < closest_t and t_min < t1 < t_max:
            closest_t = t1
            closest_sphere = sphere
        if t2 < closest_t and t_min < t2 < t_max:
            closest_t = t2
            closest_sphere = sphere
    if closest_sphere == None:
        return BACKGROUND_COLOR
    
    point = O + d * closest_t  # Compute intersection
    normal = closest_sphere.normal(point)
    normal = normal.normalized()
    #print(closest_sphere.color)
    #print(compute_lighting(point, normal))
    r, g, b = closest_sphere.color
    c_light = compute_lighting(point, normal)
    r = int(r * c_light)
    g = int(g * c_light)
    b = int(b * c_light)
    return (r, g, b)
    
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

def compute_lighting(point:vector3, normal:vector3):
    i:float = 0.0
    for light in scene_lights:
        if light.type == "ambient":
            i += light.intensity
        else:
            if light.type == "point":
                L = light.position - point
            else:
                L = light.direction
            # Check here if something goes wrong - indentation
            n_dot_l = vector3.dot_product(normal, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l / (normal.magnitude() * L.magnitude())
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