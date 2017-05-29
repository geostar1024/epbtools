from struct import *
import zipfile
import io
import binascii
import math

blocks={4:"Fuel Tank (T2)",46:"Core",147:"L Steel",1:"CV Cockpit 1",150:"L Hardened Steel",156:"L Combat Steel",144:"Concrete",141:"Wood",206:"Grow Plot",160:"L Truss",51:"L Stairs",934:"CV RCS T2",125:"S Steel",383:"S Hardened Steel",456:"SV Thruster S",81:"Admin Core (Player)",197:"L Armored Door",104:"Window Blocks L"}

shipdict={2:"BA",4:"SV",8:"CV",16:"HV"}

rotations={1:"+y,+z",9:"+x,+z"}

def readepb(filename):


	fpr=open(filename,"rb")

	ftype=fpr.read(5)

	# ship type is stored big-endian
	shipType=unpack(">i",fpr.read(4))[0]

	print("ship type: %s" % shipdict.get(shipType))

	# ship dimensions are stored little-endian!
	width=unpack("i",fpr.read(4))[0]
	height=unpack("i",fpr.read(4))[0]
	length=unpack("i",fpr.read(4))[0]
	print("width:\t%d\nheight:\t%d\nlength:\t%d" % (width,height,length))

	# not sure about these
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	fpr.read(1)

	print("")
	# loction 0x30: same for 20 bytes
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	
	# not sure about this
	print("")
	print(unpack("i",fpr.read(4))[0])
	
	# location 0x47: same for 60 bytes
	print("")
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	
	
	# always 5
	print("")
	print(unpack("c",fpr.read(1))[0][0])
	
	print("")
	
	# seem to be different for every ship; some kind of timestamp, since it always increases?
	print(unpack("h",fpr.read(2))[0])
	print(unpack("h",fpr.read(2))[0])
	print(unpack("h",fpr.read(2))[0])
	
	# location 0x8D: same for 11 bytes
	print("")
	fpr.read(11)
	
	# build version
	build=unpack("h",fpr.read(2))[0]
	
	# always the same
	print("")
	fpr.read(3)
	
	# next section is the steam ID and steam username for the original creator and current maker in ASCII
	# there are 4 fields, prefixed in order by 0x0B, 0x0A, 0x0D, 0x0C
	# then an empty 4 bytes (0x0000 0x0000) before each text field
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam ID of the last modifier
	steamidlen=unpack(">i",fpr.read(4))[0]
	
	steamid=fpr.read(steamidlen).decode()
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam name of the creator
	steamnamelen=unpack(">i",fpr.read(4))[0]
	
	steamname=fpr.read(steamnamelen).decode()
	
	print("Last modified by: %s (%s) in build %d" % (steamname,steamid,build))
	
	# steam id and name of the current blueprint maker
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam ID of the current blueprint maker
	steamidlen2=unpack(">i",fpr.read(4))[0]
	
	steamid2=fpr.read(steamidlen2).decode()
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam name of the current blueprint maker
	steamnamelen2=unpack(">i",fpr.read(4))[0]
	
	steamname2=fpr.read(steamnamelen2).decode()
	
	print("Original creator: %s (%s)" % (steamname2,steamid2))
	
	# region between steamid fields and block/device list
	# there's something in the first 3 bytes . . .
	
	fpr.read(3)
	
	# seem empty
	fpr.read(4)
	fpr.read(4)
	
	
	# number of lights
	numlights=unpack("i",fpr.read(4))[0]
	print("number of lights: %d" % numlights)
	
	print(unpack("i",fpr.read(4))[0])
	
	# number of devices
	numdevices=unpack("i",fpr.read(4))[0]
	print("number of devices: %d" % numdevices)
	
	print(unpack("i",fpr.read(4))[0])
	
	
	# number of blocks (little-endian)
	numblocks=unpack("i",fpr.read(4))[0]
	print("number of blocks: %d" % numblocks)
	
	
	# number of triangles (little-endian)
	numtris=unpack("i",fpr.read(4))[0]
	print("number of triangles: %d" % numtris)
	
	# number of block/device types, stored big-endian
	blocktypenum=unpack("h",fpr.read(2))[0]
	print("block types: %d" % blocktypenum)
	
	# now the blocks themselves are listed
	# the format is 6 bytes total
	#   the first 2 bytes are the block type
	#   the next 4 bytes are an integer, for the amount of this type of block
	
	devicetypelist=[]
		
	# list all the blocks and their number
	for k in range(0,blocktypenum):
		curblock=unpack("c",fpr.read(1))[0][0]
		devicetypelist.append(curblock)
		
		# we don't care about rotation right now; it's in the grid data anyway
		fpr.read(1)
		
		# block amount is little-endian!
		curblocknum=unpack("i",fpr.read(4))[0]
		print("%20s (%03d): %d" % (blocks.get(curblock),curblock,curblocknum))
	
	# block list seems to always be terminated by 4
	print(unpack("c",fpr.read(1))[0][0])
	
	# next section is present or not depending on if there are any groups
	# if this is greater than zero, then there are groups to process
	numgroups=unpack("c",fpr.read(1))[0][0]
	
	if (numgroups>0):
		# process the groups
		for k in range(0,numgroups):
			# names are a length-first string and then the name characters
			# this time, the length is 2 bytes instead of 4 (big-endian!)
			curgroupnamelen=unpack(">h",fpr.read(2))[0]
			curgroupname=fpr.read(curgroupnamelen)
			print("%s: " % curgroupname)
		
			# next byte is uncertain; could be that the group was automatically created and hasn't been modified
			print("  status: %d" % unpack("c",fpr.read(1))[0][0])
		
			# next byte is always 0xFF
			fpr.read(1)
		
			# this byte is how many devices are in a group; the limit is 255
			curnumdevices=unpack("c",fpr.read(1))[0][0]
			print("  devices: %d" % curnumdevices)
			print("  device list:")
			curdevicelist=[]
			for j in range(0,curnumdevices):
				# each device gets 5 bytes:
				#   2 bytes for its position in the list of devices (big-endian!)
				#   3 more unknown
				curdevice=unpack(">h",fpr.read(2))[0]
				curdevicelist.append(curdevice)
				print("    %s" % blocks.get(devicetypelist[curdevice]))
				fpr.read(3)
	
	# these bytes always seem to be empty
	fpr.read(3)
	
	start=fpr.tell()
	
	fpr.close()
	
	unzipped=pkzipread(filename,start)
	
	# first 4 bytes are how many bytes of position data there are
	# this will be the same for all future bit arrays that are encounted
	positionDataLength=unpack("i",unzipped[0:4])[0]
	
	# get the bit array of blocks
	positionDataString=processbitarray(unzipped[4:4+positionDataLength])
	
	# get the number of blocks
	numBlocks=positionDataString.count('1')
	
	print("number of blocks: "+str(numBlocks))
	
	# initialize the block array
	blockarray=[[[0]*length for i in range(height)] for i in range(width)]
	
	# the main workhorse function
	# takes in the data to be processed as well as the size of the blueprint, the field width
	#   and the helper function used to further process the data
	extractBitarrayData(unzipped[4+positionDataLength:4+positionDataLength+numBlocks*4],width,height,length,positionDataString,4,blockarray,handleBlock)
	
	# extract damage states
	# same procedure as above, with a different helper function
	damagestart=4+positionDataLength+numBlocks*4
	damageDataString=processbitarray(unzipped[damagestart+4:damagestart+4+positionDataLength])
	numDamaged=damageDataString.count('1')
	
	if (numDamaged>0):
		extractBitarrayData(unzipped[damagestart+4+positionDataLength:damagestart+4+positionDataLength+numDamaged*2],width,height,length,damageDataString,2,blockarray,handleDamage)
		
	# extract colors
	# same procedure as above, with a different helper function
	colorstart=damagestart+4+numDamaged*2+2+positionDataLength
	colorDataString=processbitarray(unzipped[colorstart+4:colorstart+4+positionDataLength])
	numColored=colorDataString.count('1')
	
	if (numColored>0):
		extractBitarrayData(unzipped[colorstart+4+positionDataLength:colorstart+4+positionDataLength+numColored*4],width,height,length,colorDataString,4,blockarray,handleColor)
		
	# extract textures
	# same procedure as above, with a different helper function
	texturestart=colorstart+4+numColored*4+positionDataLength
	textureDataString=processbitarray(unzipped[texturestart+4:texturestart+4+positionDataLength])
	numTextured=textureDataString.count('1')
		
	if (numTextured>0):
		extractBitarrayData(unzipped[texturestart+4+positionDataLength:texturestart+4+positionDataLength+numTextured*8],width,height,length,textureDataString,8,blockarray,handleTexture)
	
	# iterate through the array and print out all the blocks
	if (0):
		for k in range(width*height*length):
			if (positionDataString[k]=="1"):
				x=k%width
				y=math.floor(k/width)%height
				z=math.floor(k/(width*height))%length
				print(blockarray[x][y][z].listProperties())
	
	# symbols are messed up currently
	# so this is all commented out
	
	#symbolstart=texturestart+4+numTextured*4+1
	
	#symbolDataString=processbitarray(unzipped[symbolstart+4:symbolstart+4+positionDataLength])
	
	#numSymboled=symbolDataString.count('1')
	
	#if (numSymboled>0):
		#extractBitarrayData(unzipped[symbolstart+4+positionDataLength:symbolstart+4+positionDataLength+numSymboled*4],width,height,length,symbolDataString,4,blockarray,handleSymbol)
		#extractBitarrayData(unzipped[symbolstart+2*(4+positionDataLength)+numSymboled*4+1:symbolstart+2*(4+positionDataLength)+numSymboled*4+numSymboled*4],width,height,length,symbolDataString,4,blockarray,handleSymbol)
	
	
	# that's it!
	
# function that iterates through the bitarray it's given, extracts a field of the specified length,
#   and hands it off to a helper function for further processing
def extractBitarrayData(unzipped,width,height,length,bitarray,fieldwidth,blockarray,helperfunction):
	j=0
	
	# loop over all possible blocks
	for k in range(width*height*length):
	
		# compute the block array coordinates
		x=k%width
		y=math.floor(k/width)%height
		z=math.floor(k/(width*height))%length
		
		# if this is data to be extracted, grab it and pass it to the helper function
		if (bitarray[k]=="1"):
			curData=unzipped[fieldwidth*j:fieldwidth*(j+1)]
			helperfunction(x,y,z,curData,blockarray)
			j+=1
		else:
			blockarray[x][y][z]=None

# handles initial processing of blocks
def handleBlock(x,y,z,curData,blockarray):
	curBlock=Block(Name=blocks.get(curData[0]),Type=curData[0],Rotation=curData[1],SubType=unpack(">h",curData[2:4])[0])
	#print(curBlock.listProperties())
	blockarray[x][y][z]=curBlock
	
# handles extracting color data
def handleColor(x,y,z,curData,blockarray):
	colors=[]
	blocktype=blockarray[x][y][z].getProp("Type")
	
	# see if block type is not a device
	if (blocktype==147 or blocktype==150 or blocktype==156):
		processedData=processbitarray(curData)
	
		# now extract the colors for the 6 faces
		for k in range(6):
			colors.append(int(processedData[k*5:k*5+5],2))
	else:
		colors=[unpack("i",curData)[0]]*6
	blockarray[x][y][z].setProp("Color",colors)

# handles extracting texture data
def handleTexture(x,y,z,curData,blockarray):
	textures=[]
	processedData=processbitarray(curData)

	# now extract the textures for the 6 faces
	for k in range(6):
		textures.append(int(processedData[k*6:k*6+6],2))
	blockarray[x][y][z].setProp("Texture",textures)

# handles extracting damage states
def handleDamage(x,y,z,curData,blockarray):
	blockarray[x][y][z].setProp("Damage",unpack("h",curData)[0])
	
def handleSymbol(x,y,z,curData,blockarray):
	print(processbitarray(curData))

# function to read and extract a single file from PKZIP data
def pkzipread(filename,start,end=0):
	fpr=open(filename,"rb")
	
	# get to the right starting point
	fpr.read(start)
	
	# figure out how much to read
	length=end-start
	if (length<0):
		length=-1
	
	# read the data
	zipdata=fpr.read(length)
	
	# close the original file as it won't be needed again
	fpr.close()
	
	# write the data to a virtual temp file	
	# if the first PK is missing, we have to add it back
	if (zipdata[0:1]!=b"PK"):
		tempfile=io.BytesIO(b"PK"+zipdata)
	else:
		tempfile=io.BytesIO(zipdata)
	
	# open the virtual temp file as a zipfile
	zipped=zipfile.ZipFile(tempfile)
	zipnames=zipped.namelist()
	
	# read the uncompressed grid data
	# pick the first file name (should be the only one)
	griddata=zipped.read(zipnames[0])
	
	# TEMPORARY
	# write the data to a real file for further analysis with a hex editor
	fpw=open(zipnames[0],"wb+")
	fpw.write(griddata)
	fpw.close()
	# TEMPORARY
	
	return griddata

# need to flip each byte in the bitmask around
def processbitarray(data):
	datastring=""
	datalength=len(data)
	for k in range(datalength):
		curbyte=bin(unpack("c",data[k:k+1])[0][0])[2:].zfill(8)[-1::-1]
		datastring=datastring+curbyte
	return datastring
	
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
	
class Block(BaseObject):
	"block class"
	def __init__(self,**kwargs):
		super(Block, self).__init__(**kwargs)
		self._properties['Type']=0
		self._properties['Rotation']=0
		self._properties['SubType']=0
		self._properties['Damage']=0
		self._properties['Color']=[0,0,0,0,0,0]
		self._properties['Texture']=[0,0,0,0,0,0]
		self._properties['Symbol']=[0,0,0,0,0,0]
		self._setProperties(kwargs)
		
	def getProp(self,Property):
		return self._properties[Property];
		
	def setProp(self,Property,newValue):
		self._properties[Property]=newValue
		
