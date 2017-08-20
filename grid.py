class Grid(object):
	"object that holds the layout of a 3D voxel structure"
	def __init__(self):
		self._grid=dict()
		self._lcorner=[0,0,0]
		self._hcorner=[0,0,0]
		self._number=0
		self._bounded=1

	def getSize(self):
		if (self._bounded==0):
			self.compact()
		return (self._hcorner[0]-self._lcorner[0]+1,self._hcorner[1]-self._lcorner[1]+1,self._hcorner[2]-self._lcorner[2]+1)

	def getNumber(self):
		return self._number

	size=property(getSize)

	number=property(getNumber)

	def getKeys(self):
		return self._grid.keys()

	def delAll(self):
		keys= dict.fromkeys(self._grid.keys())
		print(len(keys))
		for key in keys:
			self.delBlock(key)

	def getBlock(self,location):
		if (type(location)==list):
			location=tuple(location)
		return self._grid.get(location)

	def putBlock(self,newLocation,newBlock):
		if (type(newLocation)==list):
			newLocation=tuple(newLocation)
		if (self._grid.get(newLocation)==None):
			self._number+=1
		self._grid[newLocation]=newBlock
		for k in range(len(newLocation)):
			if (newLocation[k]<self._lcorner[k]):
				self._lcorner[k]=newLocation[k]
			if (newLocation[k]>self._hcorner[k]):
				self._hcorner[k]=newLocation[k]

	def delBlock(self,location):
		if (type(location)==list):
			location=tuple(location)
		if (self._grid.get(location)!=None):
			self._grid.pop(location)
			self._number-=1
			for k in range(len(location)):
				if (location[k]==self._lcorner[k]):
					self._bounded=0
					return
				if (location[k]==self._hcorner[k]):
					self._bounded=0
					return

	def listAllBlocks(self):
		keys=dict.fromkeys(self._grid.keys())
		for key in keys:
			self.getBlock(key).listProperties()

	# change a particular property for *all* blocks
	# be careful with this!
	def changeAllBlockProperty(self,prop,newValue):
		keys=dict.fromkeys(self._grid.keys())
		for key in keys:
			self.getBlock(key).setProp(prop,newValue)

	# change a particular property for all blocks with a property matching the specified condition
	def changeAllBlockPropertyConditional(self,conditionalProperty,condition,prop,newValue):
		keys=dict.fromkeys(self._grid.keys())
		for key in keys:
			curBlock=self.getBlock(key)
			if curBlock.getProp(conditionalProperty)==condition:
				curBlock.setProp(prop,newValue)

	def getBlockProperty(self,location,prop):
		if (type(location)==list):
			location=tuple(location)
		block=self.getBlock(location)
		return block.getProp(prop)

	def changeBlockProperty(self,location,prop,newValue):
		if (type(location)==list):
			location=tuple(location)
		block=self.getBlock(location)
		block.setProp(prop,newValue)

	def getAllBlocksWithProperty(self,prop):
		pass

	# change a particular property for only the faces of any block with a property matching the specified condition
	def changeAllBlockFacePropertyConditional(self,conditionalProperty,condition,prop,newValue):
		keys=dict.fromkeys(self._grid.keys())
		for key in keys:
			curBlock=self.getBlock(key)
			curProp=curBlock.getProp(conditionalProperty)
			if (type(curProp)==list):
				faceslist=[0,0,0,0,0,0]
				for k in range(len(curProp)):
					if (curProp[k]==condition):
						faceslist[k]=1
				modProp=curBlock.getProp(prop)
				for k in range(len(faceslist)):
					if (faceslist[k]==1):
						modProp[k]=newValue
				curBlock.setProp(prop,modProp)



# reset the locations of the corners of the grid
# don't call this too often, since it is O(n), but it still has to go through the entire dictionary
	def compact(self):
		lower=[0,0,0]
		upper=[0,0,0]
		for key in self._grid.keys():
			lower[0]=min(lower[0],key[0])
			lower[1]=min(lower[1],key[1])
			lower[2]=min(lower[2],key[2])
			upper[0]=max(upper[0],key[0])
			upper[1]=max(upper[1],key[1])
			upper[2]=max(upper[2],key[2])
		self._lcorner=lower
		self._hcorner=upper
		self._bounded=1
