from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Settings import Settings
import random
import glm
import colorsys
import numpy as np
RED = glm.vec3(1.0, 0.0, 0.0)
GREEN = glm.vec3(0.0, 1.0, 0.0)
BLUE = glm.vec3(0.0, 0.0, 1.0)
WHITE = glm.vec3(1.0, 1.0, 1.0)
YELLOW = glm.vec3(1.0, 1.0, 0)

class Body:
    def __init__(self, position, velocity, r, mass, color):
        self.pos = position #glm.vec3(position)
        self.v = velocity #glm.vec3(velocity)
        self.r = r
        self.mass = mass
        self.color = color

    def show_info(self):
        print(f"Position: ({self.pos}), velocity:({self.v}), radius:{self.r}, mass:{self.mass}, color:{self.color}")


    def update_position(self):
        self.pos += self.v * Settings.TIME_STEP


def Mini_solar_system():
    sun_mass = 1000.0
    sun_radius = 4.0

    # Distance from the Sun's surface (not from center), to improve visual clarity
    planet_visual_distances = {
        "Mercury": (5, 0.3, glm.vec3(1.0, 1.0, 1.0)),
        "Venus":   (8, 0.5, glm.vec3(1.0, 0.8, 0.0)),
        "Earth":   (12, 0.7, glm.vec3(0.0, 0.0, 1.0)),
        "Mars":    (15, 0.6, glm.vec3(1.0, 0.0, 0.0)),
        "Jupiter": (22, 1.4, glm.vec3(1.0, 1.0, 0.0)),
        "Saturn":  (27, 1.2, glm.vec3(1.0, 0.9, 0.0)),
        "Uranus":  (30, 1.0, glm.vec3(0.5, 0.5, 1.0)),
        "Neptune": (34, 1.0, glm.vec3(0.0, 0.0, 1.0))
    }

    # Create solar system with scaled distances
    solar_system = [
        Body(position=glm.vec3(0, 0, 0), velocity=glm.vec3(0, 0, 0), r=sun_radius, mass=sun_mass, color=YELLOW),  # Sun
    ]
   
    # Add planets with non-realistic visual distances
    for name, (offset_from_surface, radius, color) in planet_visual_distances.items():
        distance = sun_radius + offset_from_surface
        orbital_velocity = np.sqrt(Settings.GRAVITY * sun_mass / distance)
        velocity = glm.vec3(0, orbital_velocity, 0)  # Orbiting in the y-direction
        position = glm.vec3(distance, 0, 0)          # Along x-axis

        solar_system.append(Body(position=position, velocity=velocity, r=radius, mass=1.0, color=color))
        
    return solar_system


def generate_figure_8_pattern():
    import numpy as np

    scale = 12.0 
    velocity_scale = np.sqrt(scale)

    pos1 = glm.vec3(0.97000436, -0.24308753, 0) * scale
    pos2 = glm.vec3(-0.97000436, 0.24308753, 0) * scale
    pos3 = glm.vec3(0, 0, 0)

    base_vel1 = glm.vec3(0.466203685, 0.43236573, 0)
    base_vel2 = glm.vec3(0.466203685, 0.43236573, 0)
    base_vel3 = glm.vec3(-0.93240737, -0.86473146, 0)

    gravity_scale = np.sqrt(0.5)
    vel1 = base_vel1 * gravity_scale * velocity_scale
    vel2 = base_vel2 * gravity_scale * velocity_scale
    vel3 = base_vel3 * gravity_scale * velocity_scale

    r = 1.0
    mass = scale * scale

    figure8_scenario = [
        Body(position=pos1, velocity=vel1, r=r, mass=mass, color=glm.vec3(1, 0, 0)),
        Body(position=pos2, velocity=vel2, r=r, mass=mass, color=glm.vec3(0, 1, 0)),
        Body(position=pos3, velocity=vel3, r=r, mass=mass, color=glm.vec3(0, 0, 1)),
    ]

    return figure8_scenario


def generate_random_bodies(num_bodies=None):
    if num_bodies is None:
        num_bodies = random.randint(10, 20)

    bodies = []
    for _ in range(num_bodies):
        position = glm.vec3(random.uniform(-10, 10),
                       random.uniform(-10, 10),
                       random.uniform(-10, 10))
        velocity = glm.vec3(random.uniform(-2, 2),
                            random.uniform(-2, 2),
                            random.uniform(-2, 2))
        r = random.uniform(0.2, 1.5)
        mass = random.uniform(20, 400)
        color = glm.vec3(0.9, 0, 0)
        
        h = random.random()
        s = random.uniform(0.7, 1.0)
        v = random.uniform(0.7, 1.0)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        color = glm.vec3(r, g, b)

        bodies.append(Body(position, velocity, r, mass, color))

    return bodies
