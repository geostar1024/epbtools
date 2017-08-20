class BaseObject(object):
	"minimal basic object"
	def __init__(self,**kwargs):
		self._properties=dict()
		self._properties['Name']=""
		self._setProperties(kwargs)

	def _setProperties(self,newProperties):
		for key in newProperties:
			if key in self._properties:
				self._properties[key]=newProperties[key]

	def getName(self):
		return self._properties.get('Name')

	def setName(self,newName):
		self._properties['Name']=newName

	def isType(self,testType):
		return isinstance(self,testType)

	def listProperties(self):
		print(self._properties)

	def getTypeName(self):
		return type(self).__name__
