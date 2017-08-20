from epbtools.baseobject import BaseObject

class Block(BaseObject):
	"block class"
	def __init__(self,**kwargs):
		super(Block, self).__init__(**kwargs)
		self._properties['Type']=None
		self._properties['Rotation']=None
		self._properties['SubType']=None
		self._properties['Damage']=None
		self._properties['Color']=None
		self._properties['Texture']=None
		self._properties['Symbol']=None
		self._properties['SymbolPage']=0
		self._properties['SymbolRotation']=None
		self._setProperties(kwargs)

	def getProp(self,Property):
		return self._properties[Property];

	def setProp(self,Property,newValue):
		self._properties[Property]=newValue
