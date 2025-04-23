from imgui.integrations.pygame import PygameRenderer
from OpenGL.GL import *
from OpenGL.GLU import *
from pygame.locals import *
from Body import *
from Camera import *
from Sphere import*
from Settings import Settings
from Gui import *
from Physic import *
import pygame
import glm 


def main():
    pygame.init()
    pygame.display.set_mode(
        (Settings.SCREEN_WIDTH, Settings.SCREEN_HEIGHT),
        pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE
    )
    pygame.display.set_caption("N body problem 3D")
    
    clock = pygame.time.Clock()
    running = True
    
    shader = load_shader("shaders/vertex_shader.glsl", 
                         "shaders/fragment_shader.glsl")
    
    
    camera = Camera(shader)
    light_pos = glm.vec3(10.0, 10.0, 10.0)
    light_dir = glm.normalize(glm.vec3(-1.0, -1.0, -1.0))

    view_pos = camera.position
    light_color = glm.vec3(1.0, 1.0, 1.0)
    
    glUseProgram(shader)
    #glUniform3fv(glGetUniformLocation(shader, "lightPos"), 1, glm.value_ptr(light_pos))
    glUniform3fv(glGetUniformLocation(shader, "lightDir"), 1, glm.value_ptr(light_dir))
    glUniform3fv(glGetUniformLocation(shader, "viewPos"), 1, glm.value_ptr(view_pos))
    glUniform3fv(glGetUniformLocation(shader, "lightColor"), 1, glm.value_ptr(light_color))
    
    
    VAO, index_count = setup_sphere_vao()
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)
    

    #   RANDOM BODIES
    bodies = generate_random_bodies(80)
    
    gui = Gui()
    
    while running:       
        glClearColor(0.1, 0.1, 0.1, 1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if gui.process_event(event):
                camera.handle_event(event)
        gui.process_input()

        camera.update()
        camera.apply(shader)
       
        for body in bodies:
            draw_sphere(body, shader, VAO, index_count)     
            body.update_position()

        step(bodies)
        detect_collisions(bodies)

        gui.render() 
        Settings.update_settings(gui.gravity, gui.time_step, gui.dampening)  

        if gui.generate_bodies:
            bodies = generate_random_bodies(gui.num_bodies)
            gui.generate_bodies = False

        if gui.demo_figure_8_pattern:
            bodies = generate_figure_8_pattern()
            gui.demo_figure_8_pattern = False

        if gui.demo_Mini_solar_system:
            bodies = Mini_solar_system()
            gui.demo_Mini_solar_system = False
        

        pygame.display.flip()
        clock.tick(100)
        
    pygame.quit()

if __name__ == "__main__":
    main()
