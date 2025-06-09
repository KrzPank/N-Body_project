import glm
from Settings import Settings
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Body import *


def detect_collisions(bodies):
    n = len(bodies)
    
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = bodies[i], bodies[j]
            
            distance_vector = p2.pos - p1.pos
            distance = glm.length(distance_vector)

            if distance <= (p1.r + p2.r):
                normal = glm.normalize(distance_vector)
                
                relative_velocity = p2.v - p1.v
                velocity_along_normal = glm.dot(relative_velocity, normal)

                t_mass = p1.mass + p2.mass

                if velocity_along_normal <= 0: 
                    impulse = -2 * velocity_along_normal / t_mass
                    overlap = (p1.r + p2.r) - distance
                    correction_factor = overlap / t_mass

                    p1.pos -= correction_factor * p2.mass * normal
                    p2.pos += correction_factor * p1.mass * normal

                    p1.v += impulse * p2.mass * -normal * Settings.DAMPENING
                    p2.v -= impulse * p1.mass * -normal * Settings.DAMPENING
            

def apply_gravity(bodies):
    n = len(bodies)
    accelerations = [glm.vec3(0.0) for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = bodies[i], bodies[j]
            distance_vector = p2.pos - p1.pos
            distance = glm.length(distance_vector)

            normalized_direction = glm.normalize(distance_vector)
            a_gravity = Settings.GRAVITY / (distance ** 2)
            acceleration = normalized_direction * a_gravity

            accelerations[i] += acceleration * p2.mass
            accelerations[j] -= acceleration * p1.mass

    return accelerations



def step(bodies):
    accelerations = apply_gravity(bodies)

    for i, body in enumerate(bodies):
        body.v += accelerations[i] * Settings.TIME_STEP
        body.pos += body.v * Settings.TIME_STEP
