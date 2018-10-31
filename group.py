from epbtools.baseobject import BaseObject

class Group(BaseObject):
	"block class"
	def __init__(self,**kwargs):
		super(Group, self).__init__(**kwargs)
		self._properties['Extra']=0
		self._properties['Devices']=None
		self._setProperties(kwargs)

	def getProp(self,Property):
		return self._properties[Property];

	def setProp(self,Property,newValue):
		self._properties[Property]=newValue
