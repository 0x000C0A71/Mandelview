import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo

from ctypes import *

import numpy as np
import GLLayout
import GLShader

import time



class Modes:
	MANDELBROT = 0
	JULIA = 1
	XZ = 2
	YW = 3

	axis = {
		0: (0, 1, 2, 3),
		1: (2, 3, 0, 1),
		2: (0, 2, 1, 3),
		3: (1, 3, 0, 2)
	}


verticies = [
	(-1.0, -1.0,   0.0, 0.0,   1.0, 0.0, 0.0),
	(-1.0,  1.0,   0.0, 1.0,   0.0, 1.0, 0.0),
	( 1.0, -1.0,   1.0, 0.0,   0.0, 0.0, 1.0),
	( 1.0,  1.0,   1.0, 1.0,   1.0, 0.0, 0.0)
]

tris = [
	(0, 1, 2),
	(1, 2, 3)
]


vShader = GLShader.Shader()
vShader.loadFromFile("vertex.shader")
vShader.shaderType = GL_VERTEX_SHADER

fShader = GLShader.Shader()
fShader.loadFromFile("fragment.shader")
fShader.shaderType = GL_FRAGMENT_SHADER







# init
pygame.init()

pgScreen = pygame.display.set_mode((600, 600), DOUBLEBUF | OPENGL)

pgClock = pygame.time.Clock()

glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glEnable(GL_BLEND)




# load mesh
VAO = GLuint(0)
glGenVertexArrays(1, VAO)
glBindVertexArray(VAO)



vBuffer = vbo.VBO(np.array(verticies, dtype = "f"))
iBuffer = vbo.VBO(np.array(tris, dtype = np.int32), target = GL_ELEMENT_ARRAY_BUFFER)

shaderprogramID = GLShader.CreateShader([vShader, fShader])


vBuffer.bind()
iBuffer.bind()

layout = GLLayout.Layout()
layout.addAttribF(2)
layout.addAttribF(2)
layout.addAttribF(3)
layout.bind(vBuffer)


glBindVertexArray(0)
glUseProgram(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)



u_color = glGetUniformLocation(shaderprogramID, "u_color")
u_pos = glGetUniformLocation(shaderprogramID, "u_pos")
u_scale = glGetUniformLocation(shaderprogramID, "u_scale")
u_mode = glGetUniformLocation(shaderprogramID, "u_mode")



glUseProgram(shaderprogramID)
glUniform3f(u_color, 1.0, 0.0, 0.0)
glUniform4f(u_pos, 0.0, 0.0, 0.0, 0.0)
glUniform1f(u_scale, 3.0)
glUniform1i(u_mode, 0)
glBindVertexArray(VAO)

# draw mesh
def draw(pos, scale, mode):
	glUniform4f(u_pos, pos[0], pos[1], pos[2], pos[3])
	glUniform1f(u_scale, scale)
	glUniform1i(u_mode, mode)
	glDrawElements(GL_TRIANGLES, len(tris) * 3, GL_UNSIGNED_INT, None)

	pygame.display.flip()


pos = [0.6991911724614522, -0.2917956201051549, 0.0, 0.0]
scale = 3.0
mode = 0

# keep running
isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				mode = (mode + 1)%4
			if event.key == pygame.K_f:
				mode = (mode - 1)%4
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]:
		pos[Modes.axis[mode][1]] += 0.01*scale
	if keys[pygame.K_s]:
		pos[Modes.axis[mode][1]] -= 0.01*scale
	if keys[pygame.K_d]:
		pos[Modes.axis[mode][0]] += 0.01*scale
	if keys[pygame.K_a]:
		pos[Modes.axis[mode][0]] -= 0.01*scale

	if keys[pygame.K_UP]:
		pos[Modes.axis[mode][3]] += 0.01*scale
	if keys[pygame.K_DOWN]:
		pos[Modes.axis[mode][3]] -= 0.01*scale
	if keys[pygame.K_RIGHT]:
		pos[Modes.axis[mode][2]] += 0.01*scale
	if keys[pygame.K_LEFT]:
		pos[Modes.axis[mode][2]] -= 0.01*scale

	if keys[pygame.K_e]:
		scale -= 0.1*scale
	if keys[pygame.K_q]:
		scale += 0.1*scale

	draw(pos, scale, mode)

print(pos, scale)