
class Subarray:
	def __init__(self, parent, fi, ti):
		self.parent = parent
		self.fi = fi
		self.ti = ti

	def _getArray(self):
		return self.parent.array[self.fi:self.ti]

	def __repr__(self):
		return str(self._getArray())

	def _index_localToGlobal(self, index):
		gIndex = index + self.fi
		if gIndex >= self.ti:
			raise IndexError("list index out of range")


class LArray:
	def __init__(self, array = []):
		self.array = list(array)

	def __repr__(self):
		return str(self.array)

	def generateSubarray(self, fromIndex = 0, toIndex = 0):
		newSub = Subarray(self, fromIndex, toIndex)



test = LArray([1,2,3,4])
print(test)
a = [1,2,3]
print(a[3])
