from epbtools.baseobject import BaseObject

class Blueprint(BaseObject):
	"blueprint class"
	def __init__(self,**kwargs):
		super(Blueprint,self).__init__(**kwargs)
		self._properties['Version']=18 # latest version, need to keep updating
		self._properties['Type']=8
		self._properties['Width']=1
		self._properties['Height']=1
		self._properties['Length']=1
		self._properties['Grid']=None
		self._properties['Build']=0
		self._properties['CreatorID']=0
		self._properties['CreatorName']=""
		self._properties['CurrentUserID']=0
		self._properties['CurrentUserName']=""
		self._properties['Blocks']=0
		self._properties['Lights']=0
		self._properties['Devices']=0
		self._properties['Triangles']=0
		self._properties['Class']=1
		self._properties['Groups']=None
		self._setProperties(kwargs)
		self.updateClass()

	def updateClass(self):
		self._properties['Class']=max(round((self._properties["Devices"]*.01+self._properties["Lights"]*.05+self._properties["Triangles"]*0.00025)/3),1)


	# TODO: fix lazy getter/setters
	def getProp(self,Property):
		return self._properties[Property];

	def setProp(self,Property,newValue):
		self._properties[Property]=newValue

	def listGroups(self):
		if (self._properties["Groups"] is not None):
			for group in self._properties["Groups"]:
				group.listProperties()
