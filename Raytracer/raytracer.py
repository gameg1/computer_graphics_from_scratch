import pygame
from settings import *
from Raytracer.objects import *
from vector import *


def draw_pixel(x, y, color:pygame.Color):
    """Draws a pixel to the screen with 0,0 being the center of the screen"""
    Screen_X = int((WIDTH /2) + x)
    Screen_Y = int((HEIGHT /2) - y)
    r, g, b = clamp(color[0]), clamp(color[1]), clamp(color[2])


    pygame.gfxdraw.pixel(pygame.display.get_surface(), Screen_X, Screen_Y, (r, g, b))

def canvas_to_viewport(x:int, y:int):
    """Returns a vector3 from a canvas x, y co-ordernents to viewport x, y, x"""
    return vector3(x * (VIEWPORT_WIDTH / WIDTH), y * (VIEWPORT_HIGHT / HEIGHT), VIEWPORT_DISTANCE)

def trace_ray(O:vector3, d:vector3, t_min, t_max, scene, recursion_depth = 0, background_color = pygame.Color(0, 0, 0)):
    closest_sphere, closest_t = closest_intersection(O, d, t_min = t_min, t_max = t_max, scene = scene)
    if closest_sphere == None:
        return background_color
    

    point = O + d * closest_t  # Compute intersection
    normal = closest_sphere.normal(point)
    normal = normal.normalized()
    intensity = compute_lighting(point, normal, -d, closest_sphere.specular, scene)
    r, g, b = closest_sphere.color
    local_color = pygame.Color(clamp(int(r * intensity)), clamp(int(g * intensity)), clamp(int(b * intensity)))

    # If we hit hte recusion limit or the object is not reglective, we're done
    r = closest_sphere.reflective
    if recursion_depth <= 0 or r <=0:
        return local_color
    
    # Compute hte reflected color
    R = reflect_ray(-d, normal = normal)
    reflected_color = trace_ray(point, R, 0.001,  math.inf, scene, recursion_depth - 1, background_color)

    
    return pygame.Color(int(local_color.r * (1 - r) + reflected_color.r * r), int(local_color.g * (1 - r) + reflected_color.g * r), int(local_color.b * (1 - r) + reflected_color.b * r))


def closest_intersection(O, direction, t_min, t_max, scene:dict)-> tuple[sphere, float]:
    closest_t = math.inf
    closest_sphere:sphere = None
    objects = scene["objects"]
    for object in objects:
        t1, t2 = intersect_ray_sphere(O, direction, object)
        if t1 < closest_t and t_min < t1 < t_max:
            closest_t = t1
            closest_sphere = object
        if t2 < closest_t and t_min < t2 < t_max:
            closest_t = t2
            closest_sphere = object
    
    return closest_sphere, closest_t

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

def compute_lighting(point:vector3, normal:vector3, V:vector3, specular:int, scene):
    i:float = 0.0
    lights = scene["lights"]
    objects = scene["objects"]
    for light in lights:
        if light.type == light.AMBIENT:
            i += light.intensity
        else:
            if light.type == light.POINT:
                L = light.position - point
                t_max = 1
            elif light.type == light.DIRECTIONAL:
                L = light.direction
                t_max = math.inf
            
            # Shadow check
            shadow_sphere, shadow_t = closest_intersection(point, L, 0.001, t_max, scene=scene)
            if shadow_sphere != None: continue
            
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

def reflect_ray(ray:vector3, normal:vector3):
    return (normal * 2) * normal.dot_product(ray) - ray

def clamp (n:int):
    if n < 0:
        return 0
    elif n > 255:
        return 255
    else:
        return n