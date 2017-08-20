from epbtools.utility import *
from epbtools.grid import Grid
from epbtools.blueprint import Blueprint
from epbtools.block import Block

blocks={4:"Fuel Tank (T2)",46:"Core",147:"L Steel",1:"CV Cockpit 1",150:"L Hardened Steel",156:"L Combat Steel",144:"Concrete",141:"Wood",206:"Grow Plot",160:"L Truss",51:"L Stairs",934:"CV RCS T2",125:"S Steel",383:"S Hardened Steel",456:"SV Thruster S",81:"Admin Core (Player)",197:"L Armored Door",104:"Window Blocks L",10:"Large Generator (T2)",22:"Gravity Generator",11:"Fuel Tank (T2)",24:"Light",17:"Cargo Box",116:"Walkway & Railing",201:"CV Thruster S"}

shipdict={2:"BA",4:"SV",8:"CV",16:"HV"}

rotations={1:"+y,+z",9:"+x,+z"}

def readepb(filename,blockDataLen=4,damageDataLen=2,colorDataLen=4,textureDataLen=8,symbolDataLen=4,symbolrotationDataLen=4):


	# new blueprint object
	blueprint=Blueprint(Name="Test")

	fpr=open(filename,"rb")


	ftype=fpr.read(5)

	# ship type is stored big-endian
	shipType=unpack(">i",fpr.read(4))[0]

	blueprint.setProp("Type",shipType)

	print("ship type: %s" % shipdict.get(shipType))

	# ship dimensions are stored little-endian!
	width=unpack("i",fpr.read(4))[0]
	height=unpack("i",fpr.read(4))[0]
	length=unpack("i",fpr.read(4))[0]
	print("width:\t%d\nheight:\t%d\nlength:\t%d" % (width,height,length))

	blueprint.setProp("Width",width)
	blueprint.setProp("Height",height)
	blueprint.setProp("Length",length)

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

	blueprint.setProp("Build",build)

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

	blueprint.setProp("CreatorID",steamid)

	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)

	# next is a length-first string for the steam name of the creator
	steamnamelen=unpack(">i",fpr.read(4))[0]

	steamname=fpr.read(steamnamelen).decode()

	blueprint.setProp("CreatorName",steamname)

	print("Original creator: %s (%s)" % (steamname,steamid))

	# steam id and name of the current blueprint maker
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)

	# next is a length-first string for the steam ID of the current blueprint maker
	steamidlen2=unpack(">i",fpr.read(4))[0]

	steamid2=fpr.read(steamidlen2).decode()

	blueprint.setProp("CurrentUserID",steamid2)

	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)

	# next is a length-first string for the steam name of the current blueprint maker
	steamnamelen2=unpack(">i",fpr.read(4))[0]

	steamname2=fpr.read(steamnamelen2).decode()

	blueprint.setProp("CurrentUserName",steamname2)

	print("Last modified by: %s (%s) in build %d" % (steamname2,steamid2,build))

	# region between steamid fields and block/device list
	# there's something in the first 3 bytes . . .

	fpr.read(3)

	# seem empty
	fpr.read(4)
	fpr.read(4)


	# number of lights
	numlights=unpack("i",fpr.read(4))[0]
	print("number of lights: %d" % numlights)

	blueprint.setProp("Lights",numlights)

	print(unpack("i",fpr.read(4))[0])

	# number of devices
	numdevices=unpack("i",fpr.read(4))[0]
	print("number of devices: %d" % numdevices)

	blueprint.setProp("Devices",numdevices)

	print(unpack("i",fpr.read(4))[0])


	# number of blocks (little-endian)
	numblocks=unpack("i",fpr.read(4))[0]
	print("number of blocks: %d" % numblocks)

	blueprint.setProp("Blocks",numblocks)


	print(unpack("i",fpr.read(4))[0])

	# number of triangles (little-endian)
	numtris=unpack("i",fpr.read(4))[0]
	print("number of triangles: %d" % numtris)

	blueprint.setProp("Triangles",numtris)



	# number of block/device types (little-endian 16-bit)
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

		# get the subtype
		cursubtype=unpack("c",fpr.read(1))[0][0]

		# block amount is little-endian!
		curblocknum=unpack("i",fpr.read(4))[0]
		devicetypelist.append([curblock,cursubtype,curblocknum])
		print("%20s (%03d): %d" % (blocks.get(curblock),curblock,curblocknum))

	blueprint.setProp("BlockList",devicetypelist)

	# block list seems to always be terminated by 4
	print(unpack("c",fpr.read(1))[0][0])

	# next section is present or not depending on if there are any groups
	# if this is greater than zero, then there are groups to process
	numgroups=unpack("h",fpr.read(2))[0]

	if (numgroups>0):
		print(numgroups)
		# process the groups
		for k in range(0,numgroups):
			# names are a length-first string and then the name characters
			# this time, the length is 1 byte instead of 4
			curgroupnamelen=unpack("c",fpr.read(1))[0][0]
			curgroupname=fpr.read(curgroupnamelen).decode()
			print("%s: " % curgroupname)

			# next byte is uncertain; could be that the group was automatically created and hasn't been modified
			print("  status: %d" % unpack("c",fpr.read(1))[0][0])

			# next byte is always 0xFF
			fpr.read(1)

			# these next 2 bytes are how many devices are in a group
			curnumdevices=unpack("h",fpr.read(2))[0]
			print("  devices: %d" % curnumdevices)
			print("  device list:")
			curdevicelist=[]
			for j in range(0,curnumdevices):
				curdata=fpr.read(5)
				#print(curdata)
				#print(binascii.hexlify(curdata))
				# each device gets at least 5 bytes:
				#   3 bytes unknown
				#   4th byte is always 0x80
				#   last byte is a name length, 0 if no custom name
				namelength=unpack("c",bytes([curdata[4]]))[0][0]
				if namelength>0:
					# read the name!
					curdevicename=fpr.read(namelength).decode()
					print("%s" % curdevicename)
				#print(curdata[0:2])
				#curdevice=unpack(">h",curdata[0:2])[0]
				#curdevicelist.append(curdevice)
				#print(curdevice)
				#print("    %s (%d): %d" % (blocks.get(devicetypelist[curdevice][0]),devicetypelist[curdevice][0],(devicetypelist[curdevice])[1]))
				#fpr.read(3)

	# these bytes always seem to be empty
	fpr.read(2)

	start=fpr.tell()

	fpr.close()

	# unzip the block data
	unzipped=pkzipread(filename,start)

	# process the block data
	# all block data is now in this data structure
	blueprint.setProp("Grid",readBlockData(unzipped,blueprint))

	# the blueprint has been read
	return blueprint


def readBlockData(unzipped,blueprint,blockDataLen=4,damageDataLen=2,colorDataLen=4,textureDataLen=8,symbolDataLen=4,symbolrotationDataLen=4):

	width=blueprint.getProp("Width")
	height=blueprint.getProp("Height")
	length=blueprint.getProp("Length")

	# first 4 bytes are how many bytes of position data there are
	# this will be the same for all future bit arrays that are encounted
	positionDataLen=unpack("i",unzipped[0:4])[0]

	# get the bit array of blocks
	positionDataString=processbitarray(unzipped[4:4+positionDataLen])
	print(positionDataString)

	# get the number of blocks
	numBlocks=positionDataString.count('1')

	print("number of blocks: "+str(numBlocks))

	# to save on memory, the blocks are stored in a dict, with a tuple of (x,y,z) as the key
	#   the benefit here is that the grid can be easily resized using negative values and an offset for each dim

	# initialize the block array
	blockarray=Grid()

	# the main workhorse function
	# takes in the data to be processed as well as the size of the blueprint, the field width
	#   and the helper function used to further process the data
	extractBitarrayData(unzipped[4+positionDataLen:4+positionDataLen+numBlocks*blockDataLen],width,height,length,positionDataString,blockDataLen,blockarray,handleBlock)

	# extract damage states
	# same procedure as above, with a different helper function
	damagestart=4+positionDataLen+numBlocks*blockDataLen
	damageDataString=processbitarray(unzipped[damagestart+4:damagestart+4+positionDataLen])
	numDamaged=damageDataString.count('1')

	if (numDamaged>0):
		extractBitarrayData(unzipped[damagestart+4+positionDataLen:damagestart+4+positionDataLen+numDamaged*damageDataLen],width,height,length,damageDataString,damageDataLen,blockarray,handleDamage)

	# extract colors
	# same procedure as above, with a different helper function
	colorstart=damagestart+4+numDamaged*damageDataLen+2+positionDataLen
	colorDataString=processbitarray(unzipped[colorstart+4:colorstart+4+positionDataLen])
	numColored=colorDataString.count('1')

	if (numColored>0):
		extractBitarrayData(unzipped[colorstart+4+positionDataLen:colorstart+4+positionDataLen+numColored*colorDataLen],width,height,length,colorDataString,colorDataLen,blockarray,handleColor)

	# extract textures
	# same procedure as above, with a different helper function
	texturestart=colorstart+4+numColored*colorDataLen+positionDataLen
	textureDataString=processbitarray(unzipped[texturestart+4:texturestart+4+positionDataLen])
	numTextured=textureDataString.count('1')

	if (numTextured>0):
		extractBitarrayData(unzipped[texturestart+4+positionDataLen:texturestart+4+positionDataLen+numTextured*textureDataLen],width,height,length,textureDataString,textureDataLen,blockarray,handleTexture)

	# symbols are handled somewhat differently than textures
	# the array for each block is 32 bits, with the last 4 bits being used to select the page of symbols
	# note that the null symbol for all but the first page will cause an entry to be created for that block
	symbolstart=texturestart+4+numTextured*textureDataLen+positionDataLen
	symbolDataString=processbitarray(unzipped[symbolstart+4:symbolstart+4+positionDataLen])
	numSymboled=symbolDataString.count('1')

	if (numSymboled>0):
		extractBitarrayData(unzipped[symbolstart+4+positionDataLen:symbolstart+4+positionDataLen+numSymboled*symbolDataLen],width,height,length,symbolDataString,symbolDataLen,blockarray,handleSymbol)

	# there's another data segment that is also for the symbols, which stores rotations
	# an entry is only made if a symbol is rotated on that block,
	#   but then persists until that block is removed, even if the symbol is removed
	#   note also that the rotation of the null symbol is stored (but there's no corresponding symbol entry)
	symbolrotationstart=symbolstart+4+numSymboled*symbolDataLen+positionDataLen
	symbolrotationDataString=processbitarray(unzipped[symbolrotationstart+4:symbolrotationstart+4+positionDataLen])
	numRotatedSymbol=symbolrotationDataString.count('1')

	if (numRotatedSymbol>0):
		extractBitarrayData(unzipped[symbolrotationstart+4+positionDataLen:symbolrotationstart+4+positionDataLen+numRotatedSymbol*symbolrotationDataLen],width,height,length,symbolrotationDataString,symbolrotationDataLen,blockarray,handleSymbolRotation)

	# there always seems to be 12 empty bytes at the end, so we just ignore them
	return blockarray


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

# handles initial processing of blocks
def handleBlock(x,y,z,curData,blockarray):
	curBlock=Block(Name=blocks.get(curData[0]),Type=curData[0],Rotation=curData[1],SubType=unpack(">H",curData[2:4])[0])
	#print(curBlock.listProperties())
	blockarray.putBlock((x,y,z),curBlock)

# handles extracting color data
def handleColor(x,y,z,curData,blockarray):
	colors=[]
	curBlock=blockarray.getBlock((x,y,z))
	blocktype=curBlock.getProp("Type")

	processedData=processbitarray(curData)

	# now extract the colors for the 6 faces
	for k in range(6):
		colors.append(int(processedData[k*5:k*5+5][::-1],2))

	# see if block type is not a device
	if (blocktype!=141 and blocktype!=144 and blocktype!=150 and blocktype!=156 and blocktype!=1):
		colors=[colors[0]]*6

	curBlock.setProp("Color",colors)

# handles extracting texture data
def handleTexture(x,y,z,curData,blockarray):
	textures=[]
	processedData=processbitarray(curData)

	# now extract the textures for the 6 faces
	for k in range(6):
		textures.append(int(processedData[k*6:k*6+6][::-1],2))
	blockarray.getBlock((x,y,z)).setProp("Texture",textures)

# handles extracting damage states
def handleDamage(x,y,z,curData,blockarray):
	blockarray.getBlock((x,y,z)).setProp("Damage",unpack("H",curData)[0])

def handleSymbol(x,y,z,curData,blockarray):
	symbols=[]
	curBlock=blockarray.getBlock((x,y,z))

	processedData=processbitarray(curData)

	for k in range(6):
		symbols.append(int(processedData[k*5:k*5+5][::-1],2))

	symbolpage=int(processedData[30:32][::-1],2)

	curBlock.setProp("Symbol",symbols)
	curBlock.setProp("SymbolPage",symbolpage)

def handleSymbolRotation(x,y,z,curData,blockarray):
	symbolrotations=[]

	curBlock=blockarray.getBlock((x,y,z))

	processedData=processbitarray(curData)

	for k in range(6):
		symbolrotations.append(int(processedData[k*5:k*5+5][::-1],2))

	curBlock.setProp("SymbolRotation",symbolrotations)

# function to read and extract a single file from PKZIP data
def pkzipread(filename,start=0,end=0):
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


