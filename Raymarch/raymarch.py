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

import numpy as np



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





def getForwardVector(rot):
	vec = (0, 1, 0)
	vec = (
		vec[0],
		vec[1]*np.cos(rot[0]) - vec[2]*np.sin(rot[0]),
		vec[1]*np.sin(rot[0]) + vec[2]*np.cos(rot[0])
	)
	vec = (
		vec[0]*np.cos(rot[1]) - vec[1]*np.sin(rot[1]),
		vec[0]*np.sin(rot[1]) + vec[1]*np.cos(rot[1]),
		vec[2]
	)
	return vec

def getRightVector(rot):
	vec = (1, 0, 0)
	vec = (
		vec[0],
		vec[1]*np.cos(rot[0]) - vec[2]*np.sin(rot[0]),
		vec[1]*np.sin(rot[0]) + vec[2]*np.cos(rot[0])
	)
	vec = (
		vec[0]*np.cos(rot[1]) - vec[1]*np.sin(rot[1]),
		vec[0]*np.sin(rot[1]) + vec[1]*np.cos(rot[1]),
		vec[2]
	)
	return vec

def getUpVector(rot):
	vec = (0, 0, 1)
	vec = (
		vec[0],
		vec[1]*np.cos(rot[0]) - vec[2]*np.sin(rot[0]),
		vec[1]*np.sin(rot[0]) + vec[2]*np.cos(rot[0])
	)
	vec = (
		vec[0]*np.cos(rot[1]) - vec[1]*np.sin(rot[1]),
		vec[0]*np.sin(rot[1]) + vec[1]*np.cos(rot[1]),
		vec[2]
	)
	return vec



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
layout.bind(vBuffer)


glBindVertexArray(0)
glUseProgram(0)
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)



u_pos = glGetUniformLocation(shaderprogramID, "u_pos")
u_scale = glGetUniformLocation(shaderprogramID, "u_scale")
u_mode = glGetUniformLocation(shaderprogramID, "u_mode")
u_rot = glGetUniformLocation(shaderprogramID, "u_rot")
u_quadScale = glGetUniformLocation(shaderprogramID, "u_quadScale")



glUseProgram(shaderprogramID)
glUniform3f(u_pos, 0.0, -2.0, 1.0)
glUniform1f(u_scale, 3.0)
glUniform1i(u_mode, 0)
glUniform2f(u_rot, 0.0, 0.0)
glUniform2f(u_quadScale, 1.0, 1.0)
glBindVertexArray(VAO)

# draw mesh
def draw(pos, scale, mode, renderComplement, rot):
	glUniform3f(u_pos, *pos)
	glUniform2f(u_rot, *rot)

	glDrawElements(GL_TRIANGLES, len(tris) * 3, GL_UNSIGNED_INT, None)


	pygame.display.flip()


pos = [-1.885765387718606, -1.102795742013073, 1.0850171033470117]
scale = 3.0
mode = 0
rot = [0.0, 0.0]
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
			if event.key == pygame.K_c:
				renderComplement = not(renderComplement)
	keys = pygame.key.get_pressed()

	fwv = getForwardVector(rot)
	rv = getRightVector(rot)
	uv = getUpVector(rot)

	if keys[pygame.K_w]:
		pos[0] += 0.01*scale*fwv[0]
		pos[1] += 0.01*scale*fwv[1]
		pos[2] += 0.01*scale*fwv[2]
	if keys[pygame.K_s]:
		pos[0] -= 0.01*scale*fwv[0]
		pos[1] -= 0.01*scale*fwv[1]
		pos[2] -= 0.01*scale*fwv[2]
	if keys[pygame.K_d]:
		pos[0] += 0.01*scale*rv[0]
		pos[1] += 0.01*scale*rv[1]
		pos[2] += 0.01*scale*rv[2]
	if keys[pygame.K_a]:
		pos[0] -= 0.01*scale*rv[0]
		pos[1] -= 0.01*scale*rv[1]
		pos[2] -= 0.01*scale*rv[2]

	if keys[pygame.K_e]:
		pos[0] += 0.01*scale*uv[0]
		pos[1] += 0.01*scale*uv[1]
		pos[2] += 0.01*scale*uv[2]
	if keys[pygame.K_q]:
		pos[0] -= 0.01*scale*uv[0]
		pos[1] -= 0.01*scale*uv[1]
		pos[2] -= 0.01*scale*uv[2]

	if keys[pygame.K_UP]:
		rot[0] += 0.01*scale
	if keys[pygame.K_DOWN]:
		rot[0] -= 0.01*scale

	if keys[pygame.K_LEFT]:
		rot[1] += 0.01*scale
	if keys[pygame.K_RIGHT]:
		rot[1] -= 0.01*scale


	"""
	if keys[pygame.K_e]:
		if keys[pygame.K_LSHIFT] and renderComplement:
			scale[Modes.complement[mode]] -= 0.1*scale[Modes.complement[mode]]
		else:
			scale[mode] -= 0.1*scale[mode]
	if keys[pygame.K_q]:
		if keys[pygame.K_LSHIFT] and renderComplement:
			scale[Modes.complement[mode]] += 0.1*scale[Modes.complement[mode]]
		else:
			scale[mode] += 0.1*scale[mode]"""


	draw(pos, scale, mode, renderComplement, rot)

print(pos, scale)