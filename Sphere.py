from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import glm 


def load_shader(vertex_path, fragment_path):
    with open(vertex_path, 'r') as f:
        vertex_src = f.read()
    with open(fragment_path, 'r') as f:
        fragment_src = f.read()
    
    return compileProgram(
        compileShader(vertex_src, GL_VERTEX_SHADER),
        compileShader(fragment_src, GL_FRAGMENT_SHADER)
    )


def create_sphere(radius=1, sectors=32, stacks=32):
    vertices = []
    normals = []
    indices = []

    for i in range(stacks + 1):
        stack_angle = np.pi / 2 - i * (np.pi / stacks) 
        xy = radius * np.cos(stack_angle)
        z = radius * np.sin(stack_angle)

        for j in range(sectors + 1):
            sector_angle = j * (2 * np.pi / sectors)
            x = xy * np.cos(sector_angle)
            y = xy * np.sin(sector_angle)

            vertices.extend([x, y, z])
            normals.extend([x / radius, y / radius, z / radius])

    for i in range(stacks):
        for j in range(sectors):
            first = i * (sectors + 1) + j
            second = first + sectors + 1

            indices.extend([first, second, first + 1])
            indices.extend([second, second + 1, first + 1])

    return np.array(vertices, dtype=np.float32), np.array(normals, dtype=np.float32), np.array(indices, dtype=np.uint32)


def setup_sphere_vao():
    vertices, normals, indices = create_sphere()

    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    VBO = glGenBuffers(2)
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, normals.nbytes, normals, GL_STATIC_DRAW)
    
    EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)
    
    glBindVertexArray(0)
    return VAO, len(indices)


def draw_sphere(body, shader, VAO, index_count):
    glUseProgram(shader)

    model = glm.mat4(1.0)
    model = glm.translate(model, body.pos)
    model = glm.scale(model, glm.vec3(body.r))  
    glUniformMatrix4fv(glGetUniformLocation(shader, "model"), 1, GL_FALSE, glm.value_ptr(model))
    glUniform3fv(glGetUniformLocation(shader, "objectColor"), 1, glm.value_ptr(body.color))

    glBindVertexArray(VAO)
    glDrawElements(GL_TRIANGLES, index_count, GL_UNSIGNED_INT, None)
    