import pygame
import pygame.gfxdraw
import math



WIDTH = 1920
HEIGHT = 1080
pygame.init()

class vector3:
    def __init__(self, x, y ,z):
        self.x = x
        self.y = y
        self.z = z
    
    def __add__(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return vector3(self.x + other.x, self.y + other.y, self.x + other.x)
    
    def __sub__(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return vector3(self.x - other.x, self.y - other.y, self.z - other.z)
    
    def __mul__(self, other):
        if not isinstance(other, int):
            return NotImplemented
        return vector3(self.x * other, self.y * other, self.z * other)
    
    def dot_product(self, other):
        if not isinstance(other, vector3):
            return NotImplemented
        return self.x * other.x + self.y * other.y + self.z * other.z

class sphere:
    def __init__(self, pos:vector3, radius:float, color:tuple[int, int, int]):
        self.pos = pos
        self.radius = radius
        self.color = color

screen = pygame.display.set_mode((WIDTH, HEIGHT))
# Camera Info
Camera_pos:vector3 = vector3(0, 0, 0) # X, Y, Z
Camera_vector:vector3 = vector3(0, 0, 1) # Unit vector pointing towards Z+

# Viewport Info
viewport_width = 1
viewport_height = 1
viewport_distance = 1

        
# Set up the envioment
BACKGROUND_COLOR = (255, 255, 255)
scene = [
        sphere(vector3(0, -1, 3), 1, (255, 0 , 0)),
        sphere(vector3(2, 0, 4), 1, (0, 0, 255)),
        sphere(vector3(-2, 0, 4), 1, (0, 255, 0)),
        ]



def main():

    clock = pygame.time.Clock()
    running = True

    #
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for canvas_x in range(-(WIDTH // 2), WIDTH // 2):
            for canvas_y in range(-(HEIGHT // 2), HEIGHT // 2):
                # Determine which square on the grid corresponds to this square on the canvas

                # Converts each pixel on the canvas (canvas_x and canvas_y) to a 3d point on the viewport (viewport_x, viewport_y, viewport_z)
                distance:vector3 = canvas_to_viewport(canvas_x, canvas_y)
                # Determine the colo0r seen through that grid square
                color = trace_ray(Camera_pos, distance, 1, float("inf"))

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
    return vector3(x * (viewport_width / WIDTH), y * (viewport_height / HEIGHT), viewport_distance)

def trace_ray(O:vector3, d:vector3, t_min, t_max):
    closest_t = float("inf")
    closest_sphere = None
    for sphere in scene:
        t1, t2 = intersect_ray_sphere(O, d, sphere)
        if t1 in [t_min, t_max] and t1 < closest_t:
            closest_t = t1
            closest_sphere = sphere
        if t2 in [t_min, t_max] and t2 < closest_t:
            closest_t = t2
            closest_sphere = sphere
        if closest_sphere == None:
            return BACKGROUND_COLOR
        return closest_sphere.color
    
def intersect_ray_sphere(O:vector3, D:vector3, sphere:sphere):
    r = sphere.radius
    CO = O - sphere.pos

    a = vector3.dot_product(D, D)
    b = 2 * vector3.dot_product(CO, D)
    c = vector3.dot_product(CO, CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return (float("inf"), float("inf"))
    
    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return t1, t2


def ray_equation(camera_pos:vector3, viewport_pos:vector3, amount:int):
    """Takes the cam position and viewport position and gives
    a point along its vector by an amount"""

    point = camera_pos + amount(viewport_pos - camera_pos)
    return point

def sphere_equation(point:tuple,position:tuple, radius:int,):
    point_x, point_y, point_z = point
    
    sphere_x, sphere_y, sphere_z = position


def clamp (n:int):
    if n < 0:
        return 0
    elif n > 255:
        return 255
    else:
        return n
if __name__ == "__main__":
    main()