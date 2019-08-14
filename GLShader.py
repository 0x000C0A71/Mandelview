

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.arrays import vbo


from ctypes import *

import numpy as np

class Shader:
	def __init__(self, source = "", shaderType = None, compiled = None):
		self.source = source
		self.shaderType = shaderType
		self.compiled = compiled

	def loadFromFile(self, filename):
		with open(filename, "r") as file:
			self.source = file.read()




def CompileShader(shader):
	shaderID = glCreateShader(shader.shaderType)
	glShaderSource(shaderID, shader.source)
	glCompileShader(shaderID)

	result = glGetShaderiv(shaderID, GL_COMPILE_STATUS)
	if result == GL_FALSE:
		length = glGetShaderiv(shaderID, GL_INFO_LOG_LENGTH)
		message = glGetShaderInfoLog(shaderID)
		raise SyntaxError("Shader Compile failed while compiling " + str(shader.shaderType) + "\nOpenGL Message: " + str(message))
		glDeleteShader(shaderID)

		return None

	shader.compiled = shaderID
	return shaderID

def CreateShader(shaders = []):
	program = glCreateProgram()

	compiledShaders = []
	for shader in shaders:
		if shader.compiled == None:
			cShader = CompileShader(shader)
			if cShader != None:
				compiledShaders.append(cShader)
				glAttachShader(program, cShader)

		else:
			compiledShaders.append(shader.compiled)
			glAttachShader(program, shader.compiled)

	glLinkProgram(program)
	glValidateProgram(program)

	for shader in compiledShaders:
		if shader != None:
			glDeleteShader(shader)

	return program