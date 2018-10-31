from epbtools.baseobject import BaseObject

class Device(BaseObject):
	"device class, under group"
	def __init__(self,**kwargs):
		super(Device, self).__init__(**kwargs)
		self._properties['Extra']=[0,0]
		self._properties['Position']=[0,0,0]
		self._setProperties(kwargs)

	def getProp(self,Property):
		return self._properties[Property];

	def setProp(self,Property,newValue):
		self._properties[Property]=newValue

	def convertLocationFromPacked():
		pass

	def convertLocationToPacked():
		pass
