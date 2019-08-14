
from OpenGL.GL import *

from ctypes import *

import numpy as np




class vertAttrib:
	def __init__(self, typeGL, typeC, size = 1, needNormalisation = GL_FALSE):
		self.typeGL = typeGL
		self.typeC = typeC
		self.size = size
		self.needNormalisation = needNormalisation
		self.pointerOffset = 0
		self.width = 0

	def update(self):
		self.width = sizeof(self.typeC) * self.size

class Layout:
	def __init__(self, attribs = []):
		self.attribs = list(attribs)
		self.stride = 0

	def addAttribF(self, size, needNormalisation = GL_FALSE):
		newAttrib = vertAttrib(GL_FLOAT, c_float, size, needNormalisation)
		self.attribs.append(newAttrib)

	def update(self):
		offset = 0
		for attrib in self.attribs:
			attrib.update()
			attrib.pointerOffset = offset
			offset += attrib.width
		self.stride = offset

	def bind(self, vBuffer):
		self.update()
		for i, attrib in enumerate(self.attribs):
			glEnableVertexAttribArray(i)
			glVertexAttribPointer(i, attrib.size, attrib.typeGL, attrib.needNormalisation, self.stride, vBuffer + attrib.pointerOffset)
