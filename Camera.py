import pygame
from pygame.locals import *
import math
import glm
from Settings import Settings
from OpenGL.GL import *
from OpenGL.GLU import *


class Camera:
    def __init__(self, shader, position=glm.vec3(0.0, 0.0, 35.0)):
        glMatrixMode(GL_PROJECTION)
        glUseProgram(shader)
        projection = glm.perspective(glm.radians(45), Settings.SCREEN_WIDTH / Settings.SCREEN_HEIGHT, 0.1, 350.0)
        glUniformMatrix4fv(glGetUniformLocation(shader, "projection"), 1, GL_FALSE, glm.value_ptr(projection))
        glMatrixMode(GL_MODELVIEW)

        self.position = position
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)
        self.world_up = glm.vec3(0.0, 1.0, 0.0)

        self.move_speed = 0.6
        self.shift_speed = 3.0
        
        self.sensitivity = 0.06
        self.pitch = 0.0
        self.yaw = -90.0

        self.temp_pos = pygame.mouse.get_pos()
        self.mouse_held = False
        self.keys = {pygame.K_w: False,
                       pygame.K_s: False,
                       pygame.K_a: False, 
                       pygame.K_d: False,
                       pygame.K_SPACE: False, 
                       pygame.K_LCTRL: False,
                       pygame.K_LSHIFT: False}
        
        self.update_vectors()

    def update_vectors(self):
        front = glm.vec3(
            math.cos(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
            math.sin(math.radians(self.pitch)),
            math.sin(math.radians(self.yaw)) * math.cos(math.radians(self.pitch)),
        )
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))


    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def apply(self, shader):
        glUseProgram(shader)
        view_matrix = self.get_view_matrix()
        glUniformMatrix4fv(glGetUniformLocation(shader, "view"), 1, GL_FALSE, glm.value_ptr(view_matrix))
    

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in self.keys:
                self.keys[event.key] = True
        elif event.type == pygame.KEYUP:
            if event.key in self.keys:
                self.keys[event.key] = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.mouse_held = True
                self.temp_pos = pygame.mouse.get_pos()
                pygame.mouse.set_pos((Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2))
                pygame.event.set_grab(True)
                pygame.mouse.set_visible(False)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.mouse_held = False
                pygame.mouse.set_pos(self.temp_pos)
                pygame.event.set_grab(False)
                pygame.mouse.set_visible(True)
        elif event.type == pygame.MOUSEMOTION and self.mouse_held:
            pygame.mouse.set_pos((Settings.SCREEN_WIDTH // 2, Settings.SCREEN_HEIGHT // 2))
            dx, dy = event.rel
            self.yaw += dx * self.sensitivity
            self.pitch -= dy * self.sensitivity
            self.pitch = max(-89, min(89, self.pitch))
            self.update_vectors()
    

    def update(self):
        speed = self.move_speed
        if self.keys[pygame.K_LSHIFT]:
            speed *= self.shift_speed
            
        if self.keys[pygame.K_w]:
            self.position += self.front * speed
        if self.keys[pygame.K_s]:
            self.position -= self.front * speed
        if self.keys[pygame.K_a]:
            self.position -= self.right * speed
        if self.keys[pygame.K_d]:
            self.position += self.right * speed
        if self.keys[pygame.K_SPACE]:
            self.position += self.up * speed
        if self.keys[pygame.K_LCTRL]:
            self.position -= self.up * speed