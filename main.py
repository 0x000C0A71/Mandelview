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

	complement = {
		0: 1,
		1: 0,
		2: 3,
		3: 2
	}


verticies = [
	(-1.0, -1.0,   0.0, 0.0),
	(-1.0,  1.0,   0.0, 1.0),
	( 1.0, -1.0,   1.0, 0.0),
	( 1.0,  1.0,   1.0, 1.0)
]

tris = [
	(0, 1, 2),
	(1, 2, 3)
]


vShader = GLShader.Shader()
vShader.loadFromFile("Standart.vsh")
vShader.shaderType = GL_VERTEX_SHADER

fShader = GLShader.Shader()
fShader.loadFromFile("Standart.fsh")
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
layout.bind(vBuffer)


glBindVertexArray(0)
glUseProgram(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)



u_pos = glGetUniformLocation(shaderprogramID, "u_pos")
u_scale = glGetUniformLocation(shaderprogramID, "u_scale")
u_mode = glGetUniformLocation(shaderprogramID, "u_mode")
u_quadPos = glGetUniformLocation(shaderprogramID, "u_quadPos")
u_quadScale = glGetUniformLocation(shaderprogramID, "u_quadScale")



glUseProgram(shaderprogramID)
glUniform4f(u_pos, 0.0, 0.0, 0.0, 0.0)
glUniform1f(u_scale, 3.0)
glUniform1i(u_mode, 0)
glUniform2f(u_quadPos, 0.0, 0.0)
glUniform2f(u_quadScale, 1.0, 1.0)
glBindVertexArray(VAO)

# draw mesh
def draw(pos, scale, mode, renderComplement):
	glUniform4f(u_pos, pos[0], pos[1], pos[2], pos[3])
	glUniform1f(u_scale, scale[mode])

	glUniform2f(u_quadPos, 0.0, 0.0)
	glUniform2f(u_quadScale, 1.0, 1.0)
	glUniform1i(u_mode, mode)

	glDrawElements(GL_TRIANGLES, len(tris) * 3, GL_UNSIGNED_INT, None)

	if renderComplement:
		glUniform2f(u_quadPos, 0.75, 0.75)
		glUniform2f(u_quadScale, 0.25, 0.25)
		glUniform1i(u_mode, Modes.complement[mode])
		glUniform1f(u_scale, scale[Modes.complement[mode]])

		glDrawElements(GL_TRIANGLES, len(tris) * 3, GL_UNSIGNED_INT, None)

	pygame.display.flip()


pos = [0.0, 0.0, 0.0, 0.0]
scale = [3.0, 3.0, 3.0, 3.0]
mode = 0
speed = 0.1
renderComplement = False

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
			if event.key == pygame.K_RETURN:
				pos = [0.0, 0.0, 0.0, 0.0]
			if event.key == pygame.K_c:
				renderComplement = not(renderComplement)
	keys = pygame.key.get_pressed()

	if keys[pygame.K_w]:
		pos[Modes.axis[mode][1]] += 0.01*speed*scale[mode]
	if keys[pygame.K_s]:
		pos[Modes.axis[mode][1]] -= 0.01*speed*scale[mode]
	if keys[pygame.K_d]:
		pos[Modes.axis[mode][0]] += 0.01*speed*scale[mode]
	if keys[pygame.K_a]:
		pos[Modes.axis[mode][0]] -= 0.01*speed*scale[mode]

	if keys[pygame.K_UP]:
		pos[Modes.axis[mode][3]] -= 0.01*speed*scale[Modes.complement[mode]]
	if keys[pygame.K_DOWN]:
		pos[Modes.axis[mode][3]] += 0.01*speed*scale[Modes.complement[mode]]
	if keys[pygame.K_RIGHT]:
		pos[Modes.axis[mode][2]] -= 0.01*speed*scale[Modes.complement[mode]]
	if keys[pygame.K_LEFT]:
		pos[Modes.axis[mode][2]] += 0.01*speed*scale[Modes.complement[mode]]

	if keys[pygame.K_e]:
		if keys[pygame.K_LSHIFT] and renderComplement:
			scale[Modes.complement[mode]] -= 0.1*speed*scale[Modes.complement[mode]]
		else:
			scale[mode] -= 0.1*speed*scale[mode]
	if keys[pygame.K_q]:
		if keys[pygame.K_LSHIFT] and renderComplement:
			scale[Modes.complement[mode]] += 0.1*speed*scale[Modes.complement[mode]]
		else:
			scale[mode] += 0.1*speed*scale[mode]

	draw(pos, scale, mode, renderComplement)

print(pos, scale)