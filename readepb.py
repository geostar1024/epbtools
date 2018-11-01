from epbtools.utility import *
from epbtools.grid import Grid
from epbtools.blueprint import Blueprint
from epbtools.block import Block
from epbtools.group import Group
from epbtools.device import Device
from .player import Player

import datetime as dt

import sys
assert sys.version_info >= (3,6)

blocks={4:"Fuel Tank (T2)",46:"Core",147:"L Steel",1:"CV Cockpit 1",150:"L Hardened Steel",156:"L Combat Steel",144:"Concrete",141:"Wood",206:"Grow Plot",160:"L Truss",51:"L Stairs",934:"CV RCS T2",125:"S Steel",383:"S Hardened Steel",456:"SV Thruster S",81:"Admin Core (Player)",197:"L Armored Door",104:"Window Blocks L",10:"Large Generator (T2)",22:"Gravity Generator",11:"Fuel Tank (T2)",24:"Light",17:"Cargo Box",116:"Walkway & Railing",201:"CV Thruster S"}

#shipdict={0:"Voxel",2:"BA",4:"SV",8:"CV",16:"HV"}

rotations={1:"+y,+z",9:"+x,+z"}

def readepb(filename,blockDataLen=4,damageDataLen=2,colorDataLen=4,textureDataLen=8,symbolDataLen=4,symbolrotationDataLen=4,debug=False):


	# new blueprint object
	blueprint=Blueprint(name="Test")

	fpr=open(filename,"rb")

	# get magic file descriptor
	magic=fpr.read(4)
	if debug:
		print("magic: ",binascii.hexlify(magic))

	blueprint.version=unpack("i",fpr.read(4))[0]

	if debug:
		print("version: ",blueprint.version)


	# ship type is just one character

	blueprint.set_type_from_raw(unpack("c",fpr.read(1))[0][0])

	if debug:
		print("structure type: %s" % blueprint.type.name)

	# ship dimensions are stored little-endian!
	blueprint.dimensions=(unpack("i",fpr.read(4))[0],unpack("i",fpr.read(4))[0],unpack("i",fpr.read(4))[0])

	if debug:
		print("dimensions: "+str(blueprint.dimensions))

	# not sure about these
	unknown_1=[]
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])
	unknown_1.append(unpack("i",fpr.read(4))[0])

	if debug:
		print(unknown_1)

	fpr.read(1)

	# loction 0x30: same for 20 bytes
	unknown_2=[]
	unknown_2.append(unpack("i",fpr.read(4))[0])
	unknown_2.append(unpack("i",fpr.read(4))[0])
	unknown_2.append(unpack("i",fpr.read(4))[0])
	unknown_2.append(unpack("i",fpr.read(4))[0])
	unknown_2.append(unpack("i",fpr.read(4))[0])

	if debug:
		print(unknown_2)

	# not sure about this
	unknown_3=unpack("i",fpr.read(4))[0]

	if debug:
		print(unknown_3)

	# location 0x47: same for 60 bytes
	unknown_4=[]
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])
	unknown_4.append(unpack("i",fpr.read(4))[0])

	if debug:
		print(unknown_4)

	# always 5
	unknown_5=unpack("c",fpr.read(1))[0][0]
	if debug:
		print(f"always 5: {unknown_5}")

	# next 8 bytes seem to be a timestamp, though oddly represented
	# the following formula can be used to convert it:
	#  - replace last byte with 0x00
	#  - unpack the 8 bytes to an unsigned 64-bit integer and divide by 1e7
	#  - add to the epoch given in the blueprint file

	timestamp_raw=fpr.read(8)
	blueprint.datetime=dt.timedelta(seconds=unpack("Q",timestamp_raw[0:7]+b'\x00')[0]/1e7)+Blueprint.EPOCH

	print(unpack("Q",timestamp_raw[0:7]+b'\x00')[0])

	print(int((blueprint.datetime-Blueprint.EPOCH).total_seconds()*1e7))

	if debug:
		print(f"timestamp: {blueprint.datetime}")

	# location 0x8D: same for 11 bytes
	unknown_7=fpr.read(9)

	if debug:
		print(unknown_7)

	blueprint.game_build=unpack("h",fpr.read(2))[0]

	# always the same
	unknown_8=fpr.read(3)

	if debug:
		print(unknown_8)

	# next section is the steam ID and steam username for the original creator and current maker in ASCII
	# there are 4 fields, prefixed in order by 0x0B, 0x0A, 0x0D, 0x0C
	# then an empty 4 bytes (0x0000 0x0000) before each text field

	id_field_1=unpack("c",fpr.read(1))[0][0]

	fpr.read(4)

	# next is a length-first string for the steam ID of the last modifier
	steamidlen=unpack(">i",fpr.read(4))[0]

	steamid=fpr.read(steamidlen).decode()

	#blueprint.setProp("CreatorID",steamid)

	id_field_2=unpack("c",fpr.read(1))[0][0]
	fpr.read(4)

	# next is a length-first string for the steam name of the creator
	steamnamelen=unpack(">i",fpr.read(4))[0]

	steamname=fpr.read(steamnamelen).decode()

	#blueprint.setProp("CreatorName",steamname)

	blueprint.creator=Player(steamid,steamname)

	if debug:
		print("Original creator: "+str(blueprint.creator))

	# steam id and name of the current blueprint maker
	id_field_3=unpack("c",fpr.read(1))[0][0]
	fpr.read(4)

	# next is a length-first string for the steam ID of the current blueprint maker
	steamidlen2=unpack(">i",fpr.read(4))[0]

	steamid2=fpr.read(steamidlen2).decode()

	#blueprint.setProp("CurrentUserID",steamid2)

	id_field_4=unpack("c",fpr.read(1))[0][0]
	fpr.read(4)

	# next is a length-first string for the steam name of the current blueprint maker
	# length is big-endian
	steamnamelen2=unpack(">i",fpr.read(4))[0]

	steamname2=fpr.read(steamnamelen2).decode()

	blueprint.user=Player(steamid2,steamname2)

	#blueprint.setProp("CurrentUserName",steamname2)

	if debug:
		print("Last modified by: %s in build %d" % (str(blueprint.user),blueprint.game_build))

	# region between steamid fields and block/device list
	# there's something in the first 3 bytes . . .

	unknown_9=[]
	unknown_9.append(fpr.read(3))

	# seem empty
	unknown_9.append(fpr.read(4))
	unknown_9.append(fpr.read(4))

	if debug:
		print(unknown_9)

	# extra fields as of version 20
	if blueprint.version>=20:
		# empty

		v20_unknown_1=fpr.read(4)

		# 0x0005
		v20_unknown_2=fpr.read(2)

		# varies; unknown why
		v20_unknown_3=fpr.read(2)

		# always 0x8080
		v20_unknown_4=fpr.read(2)

		# varies; unknown why
		v20_unknown_5=fpr.read(2)

		# unknown, but seems to be zero for now
		v20_unknown_6=fpr.read(4)

		# unknown
		v20_unknown_7=fpr.read(1)

		if debug:
			print(v20_unknown_1)
			print(f"always 0x0005: {v20_unknown_2}")
			print(v20_unknown_3)
			print(f"always 0x8080: {v20_unknown_4}")
			print(v20_unknown_5)
			print(v20_unknown_6)
			print(v20_unknown_7)

	# number of lights
	blueprint.lights=unpack("i",fpr.read(4))[0]

	if debug:
		print("number of lights: %d" % blueprint.lights)

	#blueprint.setProp("Lights",numlights)
	unknown_10=unpack("i",fpr.read(4))[0]

	if debug:
		print(unknown_10)

	# number of devices
	blueprint.devices=unpack("i",fpr.read(4))[0]

	if debug:
		print("number of devices: %d" % blueprint.devices)

	#blueprint.setProp("Devices",numdevices)

	unknown_11=unpack("i",fpr.read(4))[0]

	if debug:
		print(unknown_11)

	# number of blocks (little-endian)
	blueprint.blocks=unpack("i",fpr.read(4))[0]

	if debug:
		print("number of blocks: %d" % blueprint.blocks)

	#blueprint.setProp("Blocks",numblocks)

	unknown_11=unpack("i",fpr.read(4))[0]

	if debug:
		print(unknown_11)

	# number of triangles (little-endian)
	blueprint.triangles=unpack("i",fpr.read(4))[0]

	if debug:
		print("number of triangles: %d" % blueprint.triangles)

	#blueprint.setProp("Triangles",numtris)

	# now we can compute Eleon's class size
	blueprint.update_eleon_class_size()

	if debug:
		print("eleon class size: %0.2f"%(blueprint.eleon_class_size))

	# number of block/device types (little-endian 16-bit)
	blocktypenum=unpack("h",fpr.read(2))[0]

	if debug:
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

		if debug:
			print("%20s (%03d): %d" % (blocks.get(curblock),curblock,curblocknum))

	blueprint.block_type_list=devicetypelist

	# block list seems to always be terminated by 4 if version<21
	# 5 now as of version 21
	block_terminator=unpack("c",fpr.read(1))[0][0]
	if debug:
		print(f"I'll be block ... {block_terminator}")

	# next section is present or not depending on if there are any groups
	# if this is greater than zero, then there are groups to process
	numgroups=unpack("h",fpr.read(2))[0]

	if debug:
		print("number of groups: %d"%(numgroups))
	if (numgroups>0):
		groups=[]
		# process the groups
		for k in range(0,numgroups):
			# names are a length-first string and then the name characters
			# this time, the length is 1 byte instead of 4
			curgroupnamelen=unpack("c",fpr.read(1))[0][0]
			groups.append(Group(name=fpr.read(curgroupnamelen).decode()))


			# next byte is uncertain; could be that the group was automatically created and hasn't been modified
			# as of version 21, this is a word; not sure of endian-ness
			# for auto-created groups, it is 0x0001

			byte_buf=[]
			next_byte=0
			while next_byte != b'\xff':
				next_byte=fpr.read(1)
				if next_byte!=b'\xff':
					byte_buf.append(next_byte)

			byte_buf=b''.join(byte_buf)

			# all blueprints before version 21 and a few early version 21 blueprints
			if len(byte_buf)==1:
				groups[k].set_type_from_raw(unpack("c",byte_buf)[0][0])

			# most version 21+ blueprints
			if len(byte_buf)==2:
				groups[k].set_type_from_raw(unpack("h",byte_buf)[0])

			# these next 2 bytes are how many devices are in a group
			curnumdevices=unpack("h",fpr.read(2))[0]
			#print("  devices: %d" % curnumdevices)
			#print("  device list:")
			if (curnumdevices>0):
				curdevicelist=[]
				for j in range(0,curnumdevices):
					curdata=fpr.read(5)
					#print(curdata)
					#print(binascii.hexlify(curdata))
					# each device gets at least 5 bytes:
					#   3 bytes that are a packed location
					#   4th byte is always 0x80
					#   last byte is a name length, 0 if no custom name
					namelength=unpack("c",bytes([curdata[4]]))[0][0]
					if namelength>0:
						# read the name!
						curdevicelist.append(Device(name=fpr.read(namelength).decode()))
						#print("%s" % curdevicelist[j].name)
					else:
						curdevicelist.append(Device())
					curdevicelist[j].location=tuple(curdata[0:3])
				groups[k].devices=curdevicelist
				#print(groups[k])
				#print(curdata[0:2])
				#curdevice=unpack(">h",curdata[0:2])[0]
				#curdevicelist.append(curdevice)
				#print(curdevice)
				#print("    %s (%d): %d" % (blocks.get(devicetypelist[curdevice][0]),devicetypelist[curdevice][0],(devicetypelist[curdevice])[1]))
				#fpr.read(3)
			blueprint.groups=groups
	# these bytes always seem to be empty
	fpr.read(2)

	start=fpr.tell()

	fpr.close()

	# unzip the block data
	unzipped=pkzipread(filename,start)

	# process the block data
	# all block data is now in this data structure
	blueprint.grid=readBlockData(unzipped,blueprint.dimensions)

	# the blueprint has been read
	return blueprint


def readBlockData(unzipped,dimensions,blockDataLen=4,damageDataLen=2,colorDataLen=4,textureDataLen=8,symbolDataLen=4,symbolrotationDataLen=4,debug=False):

	width=dimensions[0]
	height=dimensions[1]
	length=dimensions[2]

	# first 4 bytes are how many bytes of position data there are
	# this will be the same for all future bit arrays that are encounted
	positionDataLen=unpack("i",unzipped[0:4])[0]

	# get the bit array of blocks
	positionDataString=processbitarray(unzipped[4:4+positionDataLen])

	if debug:
		print(positionDataString)

	# get the number of blocks
	numBlocks=positionDataString.count('1')

	if debug:
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

