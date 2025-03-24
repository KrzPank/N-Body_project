import pygame
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Body import *


pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

GRAVITY = 0.5
TIME_STEP = 0.01
DAMPENING = 0.85

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), DOUBLEBUF|OPENGL)
pygame.display.set_caption("N body problem 3D")


def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_COLOR_MATERIAL)
    
    light_position = [1, 1, 1, 0]  # Directional light
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    
    ambient_light = [0.2, 0.2, 0.2, 1.0]
    diffuse_light = [0.8, 0.8, 0.8, 1.0]
    specular_light = [1.0, 1.0, 1.0, 1.0]
    
    glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_light)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_light)
    glLightfv(GL_LIGHT0, GL_SPECULAR, specular_light)



def draw_sphere(body):
    glPushMatrix()
    glTranslatef(body.x, body.y, body.z)
    color = pygame.Color(body.color)  # Ensure it's a pygame.Color instance
    glColor3f(color.r / 255.0, color.g / 255.0, color.b / 255.0)
    quadric = gluNewQuadric()
    gluQuadricNormals(quadric, GLU_SMOOTH)
    gluSphere(quadric, body.r, 32, 32)
    glPopMatrix()


def main():
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45, (SCREEN_WIDTH / SCREEN_HEIGHT), 0.1, 175.0)
    glMatrixMode(GL_MODELVIEW)
    glTranslatef(0.0, 0.0, -35)

    setup_lighting()
    
    ''' VERTICAL AND HORIZONTAL ORBITS
    bodies = [
        Body(0, 0, -5, 3, 0, 0, 0.4, 3, RED),
        Body(0, 0, 5, 0, 0, 0, 1, 300, RED), 
        Body(0, 4, 0, -3, 0, 0, 0.3, 1, BLUE)
    ]
    '''

    ''' ORBIT STEAL SCENARIO
    mass = 200
    bodies = [
    Body(-12, 0, 0, 0.347, 0.532, 0, 1.2, mass, WHITE),  # Left body
    Body(12, 0, 0, 0.347, 0.532, 0, 1.2, mass, WHITE),  # Right body
    Body(0, 0, 0, -2 * 0.347, -2 * 0.532, 0, 1.2, mass, WHITE)   # Center body
    ]

    '''

    '''
    mass = 400
    bodies = [
    Body(-9, 0, 0, 0.347, 1.532, 0, 1, mass, WHITE),  # Left body
    Body(9, 0, 0, 0.347, 1.532, 0, 1, mass, WHITE),  # Right body
    Body(0, 0, 0, -2 * 0.347, -2 * 1.532, 0, 1, mass, WHITE)   # Center body
    ]
    '''


    #''' RANDOM BODIES GENERATION
    bodies = generate_random_bodies()
    for body in bodies:
        print(f"Body at ({body.x}, {body.y}, {body.z}) with velocity ({body.v_x}, {body.v_y}, {body.v_z}), radius {body.r}, mass {body.mass}, color {body.color}")
    #'''

    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(GREY)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        step(bodies)
        detect_collisions(bodies)

        for body in bodies:
            body.update_position()
            draw_sphere(body)
        
        pygame.display.flip()
        clock.tick(60) 
        
    pygame.quit()

if __name__ == "__main__":
    main()