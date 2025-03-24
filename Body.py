import pygame
import random
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
import pygame.math
from main import GRAVITY, TIME_STEP, DAMPENING


WHITE = pygame.Color(255, 255, 255)
BLACK = pygame.Color(0,0,0)
GREY = pygame.Color(30, 30, 30)
YELLOW = pygame.Color(255, 255, 102)
BROWN = pygame.Color(141, 47, 11)
RED = pygame.Color(220, 0, 0)
BLUE = pygame.Color(14, 120, 205)


class Body:
    def __init__(self, x, y, z, v_x, v_y, v_z, r, mass, color):
        self.x = x
        self.y = y
        self.z = z
        self.v_x = v_x
        self.v_y = v_y
        self.v_z = v_z
        self.r = r
        self.mass = mass
        self.color = color

    def update_position(self):
        self.x += self.v_x * TIME_STEP
        self.y += self.v_y * TIME_STEP
        self.z += self.v_z * TIME_STEP




def detect_collisions(bodies):
    n = len(bodies)
    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = bodies[i], bodies[j]
            
            distance_vector = pygame.math.Vector3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
            distance = distance_vector.length()

            #print(f"Distance between bodies {i} and {j}: {distance}")
            #print(f"Sum of radii: {p1.r + p2.r}")
            
            if distance <= (p1.r + p2.r):
                normal = distance_vector.normalize()
                
                relative_velocity = pygame.math.Vector3(p2.v_x - p1.v_x, p2.v_y - p1.v_y, p2.v_z - p1.v_z)
                velocity_along_normal = relative_velocity.dot(normal)

                if velocity_along_normal < 0: 
                    impulse = -2 * velocity_along_normal / (p1.mass + p2.mass)
                    overlap = (p1.r + p2.r) - distance
                    correction_factor = (overlap) / (p1.mass + p2.mass)

                    #print(f"Distance between bodies before correction: {distance}")
                    #print(f"Sum of radii: {p1.r + p2.r}")
                    #print(f"correction factor:{correction_factor}")

                    p1.x -= correction_factor * p2.mass * normal.x
                    p1.y -= correction_factor * p2.mass * normal.y
                    p1.z -= correction_factor * p2.mass * normal.z
                    p2.x += correction_factor * p1.mass * normal.x
                    p2.y += correction_factor * p1.mass * normal.y
                    p2.z += correction_factor * p1.mass * normal.z

                    p1.v_x += impulse * p2.mass * -normal.x * DAMPENING
                    p1.v_y += impulse * p2.mass * -normal.y * DAMPENING
                    p1.v_z += impulse * p2.mass * -normal.z * DAMPENING
                    p2.v_x -= impulse * p1.mass * -normal.x * DAMPENING
                    p2.v_y -= impulse * p1.mass * -normal.y * DAMPENING
                    p2.v_z -= impulse * p1.mass * -normal.z * DAMPENING

                    #dv = pygame.math.Vector3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
                    #d  = dv.length()
                    #print(f"Distance between bodies after correction: {d}")
                
                

def apply_gravity(bodies):
    n = len(bodies)
    accelerations = [(0, 0, 0) for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            p1, p2 = bodies[i], bodies[j]
            distance_vector = pygame.math.Vector3(p2.x - p1.x, p2.y - p1.y, p2.z - p1.z)
            distance = distance_vector.length()

            if distance == 0:
                continue

            normalized_direction = distance_vector / distance
            a_gravity = GRAVITY / pow(distance, 2)
            
            acceleration = normalized_direction * a_gravity

            # Update accelerations
            ax1, ay1, az1 = accelerations[i]
            ax2, ay2, az2 = accelerations[j]
            
            accelerations[i] = (ax1 + acceleration.x * p2.mass, ay1 + acceleration.y * p2.mass, az1 + acceleration.z * p2.mass)
            accelerations[j] = (ax2 - acceleration.x * p1.mass, ay2 - acceleration.y * p1.mass, az2 - acceleration.z * p1.mass)

    return accelerations

def step(bodies):
    accelerations = apply_gravity(bodies)

    for i, body in enumerate(bodies):
        ax, ay, az = accelerations[i]

        # Update velocity
        body.v_x += ax * TIME_STEP
        body.v_y += ay * TIME_STEP
        body.v_z += az * TIME_STEP

        # Update position
        body.update_position()


def generate_random_bodies(num_bodies=None):
    if num_bodies is None:
        num_bodies = random.randint(10, 20)

    bodies = []
    for _ in range(num_bodies):
        x = random.uniform(-10, 10)
        y = random.uniform(-10, 10)
        z = random.uniform(-10, 10)
        v_x = random.uniform(-1, 1)
        v_y = random.uniform(-1, 1)
        v_z = random.uniform(-1, 1)
        r = random.uniform(0.1, 1.5)
        mass = random.uniform(1, 300)
        color = pygame.Color(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        )

        bodies.append(Body(x, y, z, v_x, v_y, v_z, r, mass, color))

    return bodies

