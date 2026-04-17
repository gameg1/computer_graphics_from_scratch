import sys
sys.path.append('../')
from pyray import *
from settings import *
from Renderer.Raytracer.objects import *
import math


def canvas_to_viewport(x:int, y:int):
    """Returns a Vector3 from a canvas x, y co-ordernents to viewport x, y, x"""
    return Vector3(x * (VIEWPORT_WIDTH / WIDTH), y * (VIEWPORT_HIGHT / HEIGHT), VIEWPORT_DISTANCE)

def trace_ray(O:Vector3, d:Vector3, t_min, t_max, scene, recursion_depth = 0, background_color = Color(0, 0, 0, 255))->Color:
    closest_sphere, closest_t = closest_intersection(O, d, t_min = t_min, t_max = t_max, scene = scene)
    if closest_sphere == None:
        return background_color

 

    point = vector3_add(O, vector3_multiply_scalar(d, closest_t))  # Compute intersection
    normal = vector3_subtract(point, closest_sphere.pos)
    normal = vector3_divide_scalar(normal, vector3_length(normal)) 
    intensity = compute_lighting(point, normal, vector3_negate(d), closest_sphere.specular, scene)
    local_color = Color(min(255,int(closest_sphere.color.r * intensity)), min(255,int(closest_sphere.color.g * intensity)), min(255,int(closest_sphere.color.b * intensity)), 255)

    # If we hit hte recusion limit or the object is not reglective, we're done
    r = closest_sphere.reflective
    if recursion_depth <= 0 or r <=0:
        return local_color
    
    # Compute hte reflected color
    R = reflect_ray(vector3_negate(d), normal = normal)

    reflected_color:Color = trace_ray(point, R, 0.001,  math.inf, scene, recursion_depth - 1, background_color = background_color)
    try:
        rc_r = reflected_color[0]
        rc_g = reflected_color[1]
        rc_b = reflected_color[2]
        return Color(int(local_color.r * (1 - r) + rc_r * r), int(local_color.g * (1 - r) + rc_g * r), int(local_color.b * (1 - r) + rc_b * r), 255)
    except TypeError:
        pass
    try:
        rc_r, rc_g, rc_b, rc_a = reflected_color
        return Color(int(local_color.r * (1 - r) + rc_r * r), int(local_color.g * (1 - r) + rc_g * r), int(local_color.b * (1 - r) + rc_b * r), 255)
    except TypeError:
        pass
    return Color(int(local_color.r * (1 - r) + reflected_color.r * r), int(local_color.g * (1 - r) + reflected_color.g * r), int(local_color.b * (1 - r) + reflected_color.b * r), 255)

def vector3_multiply_scalar(v:Vector3, scalar:float)->Vector3:
    return Vector3(v.x * scalar, v.y * scalar, v.z * scalar)   

def vector3_divide_scalar(v:Vector3, scalar:float)->Vector3:
    return Vector3(v.x / scalar, v.y / scalar, v.z / scalar)

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

def intersect_ray_sphere(O:Vector3, D:Vector3, sphere:sphere):
    r = sphere.radius
    CO = vector3_subtract(O, sphere.pos)
    
    a = vector3_length_sqr(D)
    b = 2 * vector3_dot_product(CO, D)
    c = vector3_length_sqr(CO) - r*r

    discriminant = b*b - 4*a*c
    if discriminant < 0:
        return (math.inf, math.inf)
    
    t1 = (-b + math.sqrt(discriminant)) / (2 * a)
    t2 = (-b - math.sqrt(discriminant)) / (2 * a)

    return t1, t2

def compute_lighting(point:Vector3, normal:Vector3, V:Vector3, specular:int, scene):
    i:float = 0.0
    lights = scene["lights"]
    objects = scene["objects"]
    for light in lights:
        if light.type == light.AMBIENT:
            i += light.intensity
        else:
            if light.type == light.POINT:
                L = vector3_subtract(light.position, point)
                t_max = 1
            elif light.type == light.DIRECTIONAL:
                L = light.direction
                t_max = math.inf
            
            # Shadow check
            shadow_sphere, shadow_t = closest_intersection(point, L, 0.001, t_max, scene=scene)
            if shadow_sphere != None: continue
            
            # Diffuse
            n_dot_l = vector3_dot_product(normal, L)
            if n_dot_l > 0:
                i += light.intensity * n_dot_l / (vector3_length(normal) * vector3_length(L))
            
            # Specular
            if specular != -1:
                reflection:Vector3 = vector3_subtract(vector3_multiply_scalar(normal, vector3_dot_product(normal, L) * 2), L)
                r_dot_v = vector3_dot_product(reflection, V)
                if r_dot_v > 0:

                    i += light.intensity * math.pow(r_dot_v/ (vector3_length(reflection)*vector3_length(V)), specular)

    return i

def multiplyMV(mat, vec):
    result = [0, 0, 0]
    vec = [vec.x, vec.y, vec.z]

    for i in range(3):
        for j in range(3):
            result[i] += vec[j] * mat[i][j]

    return Vector3(result[0], result[1], result[2])

def reflect_ray(ray:Vector3, normal:Vector3)->Vector3:

    return vector3_subtract(vector3_multiply_scalar(normal, vector3_dot_product(ray, normal)* 2), ray)


# function ReflectRay(ray, normal) {
#   return sub(mult(normal, mult(2 * dot_product(v1, v2):float)),v1)
#   return v2.mul(2*v1.dot(v2)).sub(v1);
#   return 2 * normal:vec * dot(normal, ray):float - ray