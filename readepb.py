from struct import *
import zipfile
import io
import binascii
import math
import random
import datetime

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

# write a blueprint object to a file
def writeepb(filename,blueprint):

	# write everything but the block data
	writeEPBHeader(filename,blueprint)

	# make the zipped block data
	zipdata=makeBlockData(blueprint)

	fpw=open(filename,"ab")

	# strip off the leading PK because that's how Eleon rolls
	fpw.write(zipdata[2:-1])

	# blueprint file written
	fpw.close()


# writes the header section of an EPB file
# currently overwrites the specified file, so exercise the normal amount of caution
def writeEPBHeader(filename,blueprint):
	fpw=open(filename,"wb+")

	# write EPB identifier
	fpw.write(binascii.unhexlify("45529478"))
	fpw.write(pack("i",17))

	# write the structure type
	fpw.write(binascii.unhexlify(str(blueprint.getProp("Type")).zfill(2)))

	# write the dimensions
	fpw.write(pack("i",blueprint.getProp("Width")))
	fpw.write(pack("i",blueprint.getProp("Height")))
	fpw.write(pack("i",blueprint.getProp("Length")))

	# write something to do with the blueprint revision number
	fpw.write(binascii.unhexlify("01000F00"))

	# write a bunch of unknown data
	# it looks like a bunch of ints, but it's unclear what it represents

	fpw.write(binascii.unhexlify("11000000000000030000000000010000000000000100000E0000000000000300000000000F000000000000030000000000050000000000000100000400000000000002000000000006000000000000040000000000000000000000000007000000000000000009000000"))

	# write an int that signals the start of the timestamp
	fpw.write(pack(">i",5))

	# the exact date time format isn't really clear
	# so, just use 2017-01-01 00:00:00 as the epoch
	# the number below is what it was computed as
	epoch=datetime.datetime(2017,1,1,0,0,0)
	epochnum=59727647703877224

	curdate=datetime.datetime.now()

	# add the difference in time between now and the epoch, multiply by 10^7 and add to the epoch number
	curdatenum=int(epochnum+(curdate-epoch).total_seconds()*1e7)

	# convert to hex and remove the trailing 0x00 and write it
	fpw.write(pack("l",curdatenum)[:-1])
	fpw.write(binascii.unhexlify("88"))

	# write something that might contain a section identifier (for the upcoming steamid section?)
	fpw.write(binascii.unhexlify("000800000000000002"))

	# write the build number
	fpw.write(pack("h",blueprint.getProp("Build")))

	fpw.write(binascii.unhexlify("000000"))

	# write the steamid section
	# first, the original creator id and name
	fpw.write(binascii.unhexlify("0B"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.getProp("CreatorID"))))
	fpw.write(bytes(blueprint.getProp("CreatorID"),"utf8"))

	fpw.write(binascii.unhexlify("0A"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.getProp("CreatorName"))))
	fpw.write(bytes(blueprint.getProp("CreatorName"),"utf8"))

	# then the current user id and name
	fpw.write(binascii.unhexlify("0D"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.getProp("CurrentUserID"))))
	fpw.write(bytes(blueprint.getProp("CurrentUserID"),"utf8"))

	fpw.write(binascii.unhexlify("0C"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.getProp("CurrentUserName"))))
	fpw.write(bytes(blueprint.getProp("CurrentUserName"),"utf8"))

	# next 11 bytes are unknown
	fpw.write(binascii.unhexlify("1000000000000000000000"))

	# write the basic stats of number of lights, devices, triangles, and blocks
	fpw.write(pack("i",blueprint.getProp("Lights")))
	fpw.write(pack("i",0))

	fpw.write(pack("i",blueprint.getProp("Devices")))
	fpw.write(pack("i",0))

	fpw.write(pack("i",blueprint.getProp("Blocks")))
	fpw.write(pack("i",blueprint.getProp("Triangles")))

	# write the block list
	fpw.write(pack("h",len(blueprint.getProp("BlockList"))))
	for block in blueprint.getProp("BlockList"):
		fpw.write(bytes([block[0]]))
		fpw.write(bytes([block[1]]))
		fpw.write(pack("i",block[2]))

	# the block list always ends with 4
	fpw.write(bytes([4]))

	# write groups
	# don't write groups for the moment
	fpw.write(bytes(2))

	# next 2 bytes always seem to be empty
	fpw.write(bytes(2))

	# the header is finished
	fpw.close()



# writes block data to bloom arrays
# blocks, colors, textures, and symbols work correctly
# TODO: groups and signal logic
def makeBlockData(blueprint,blockDataLen=4,damageDataLen=2,colorDataLen=4,textureDataLen=8,symbolDataLen=4,symbolrotationDataLen=4):
	blockarray=blueprint.getProp("Grid")

	#print(blockarray.size,blockarray.number)

	bloomlen=math.ceil(float(blockarray.size[0])*float(blockarray.size[1])*float(blockarray.size[2])/8)
	#print(bloomlen)

	sortedlocs=sorted(blockarray.getKeys(), key=lambda tup: (tup[2],tup[1],tup[0]))
	#print(sortedlocs)

	bloom=getBloom(blockarray,sortedlocs,"Type")

	#print(bloom)

	# get a temporary file
	fpw=io.BytesIO(b"")

	#print(len(bloom))

	bloomlen=pack("i",len(bloom))
	fpw.write(bloomlen+bloom)

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		curType=pack("c",bytes([curBlock.getProp("Type")]))
		curRotation=pack("c",bytes([curBlock.getProp("Rotation")]))
		curSubType=pack(">H",curBlock.getProp("SubType"))
		fpw.write(curType+curRotation+curSubType)

	# write damage
	damageBloom=getBloom(blockarray,sortedlocs,"Damage")
	fpw.write(bloomlen+bytes(damageBloom))

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		if (curBlock.getProp("Damage")!=None):
			fpw.write(pack(">H",curBlock.getProp("Damage")))

	# some kind of separator
	fpw.write(bytes([int("01",16),int("7F",16)]))

	# write color

	colorBloom=getBloom(blockarray,sortedlocs,"Color")
	fpw.write(bloomlen+bytes(colorBloom))

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		if (curBlock.getProp("Color")!=None):
			bitstr=""
			for k in curBlock.getProp("Color"):
				bitstr+=bin(k)[2:].zfill(5)[-1::-1]
			bitstr=bitstr+"".zfill(colorDataLen*8-len(bitstr))
			rbitstr=""
			for k in range(int(len(bitstr)/8)):
				rbitstr=rbitstr+bitstr[8*k:8*k+8][::-1]
			fpw.write(pack(">I",int(rbitstr,2)))

	# write texture

	textureBloom=getBloom(blockarray,sortedlocs,"Texture")
	fpw.write(bloomlen+bytes(textureBloom))

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		if (curBlock.getProp("Texture")!=None):
			bitstr=""
			for k in curBlock.getProp("Texture"):
				bitstr+=bin(k)[2:].zfill(6)[-1::-1]
			bitstr=bitstr+"".zfill(textureDataLen*8-len(bitstr))
			rbitstr=""
			for k in range(int(len(bitstr)/8)):
				rbitstr=rbitstr+bitstr[8*k:8*k+8][::-1]
			fpw.write(pack(">I",int(rbitstr[0:32],2)))
			fpw.write(pack(">I",int(rbitstr[32:64],2)))

	# write symbols

	symbolBloom=getBloom(blockarray,sortedlocs,"Symbol")
	fpw.write(bloomlen+bytes(symbolBloom))

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		if (curBlock.getProp("Symbol")!=None):
			bitstr=""
			#print(curBlock.getProp("Color"))
			for k in curBlock.getProp("Symbol"):
				bitstr+=bin(k)[2:].zfill(5)[-1::-1]
			bitstr=bitstr+"{0:b}".format(curBlock.getProp("SymbolPage")).zfill(2)[::-1]
			rbitstr=""
			for k in range(int(len(bitstr)/8)):
				rbitstr=rbitstr+bitstr[8*k:8*k+8][::-1]
			fpw.write(pack(">I",int(rbitstr,2)))

	# write symbol rotations

	symbolrotationBloom=getBloom(blockarray,sortedlocs,"SymbolRotation")
	fpw.write(bloomlen+bytes(symbolrotationBloom))

	for key in sortedlocs:
		curBlock=blockarray.getBlock(key)
		if (curBlock.getProp("SymbolRotation")!=None):
			bitstr=""
			#print(curBlock.getProp("Color"))
			for k in curBlock.getProp("SymbolRotation"):
				bitstr+=bin(k)[2:].zfill(5)[-1::-1]
			bitstr=bitstr+"".zfill(symbolrotationDataLen*8-len(bitstr))
			rbitstr=""
			for k in range(int(len(bitstr)/8)):
				rbitstr=rbitstr+bitstr[8*k:8*k+8][::-1]
			fpw.write(pack(">I",int(rbitstr,2)))


	# write the 12 empty bytes at the end
	fpw.write(binascii.unhexlify("000000000000000000000000"))

	fpw.seek(0)

	#zipdata=io.BytesIO()

	# create temporary zipfile (has to be done on disk, it seems)
	fpw3=zipfile.ZipFile("0000","w",compression=zipfile.ZIP_DEFLATED)

	fpw2=open("000","wb+")


	fpw2.write(fpw.read(-1))

	fpw.seek(0)

	newdata=fpw.read(-1)
	print(newdata)

	fpw.close()

	fpw3.writestr("0",newdata)

	print(fpw3.testzip())

	fpw3.close()

	fpw3=open("0000","rb")

	zipdata=fpw3.read(-1)

	fpw2.close()
	fpw3.close()

	return zipdata

def printBlocks(blockarray):
	for key in blockarray.getKeys():
		print(blockarray.getBlock(key).listProperties())


def getBloom(blockarray,sortedlocs,field=None):
	size=blockarray.size
	bitstr=[0 for k in range(8*math.ceil(size[0]*size[1]*size[2]/8))]

	for k in sortedlocs:
		bitstr[k[0]+k[1]*size[0]+k[2]*size[0]*size[1]]=int((blockarray.getBlock(k).getProp(field)!=None))

	#print(bitstr)

	ibytes=[]
	for k in range(len(bitstr)//8):
		ibytes.append(int("".join(str(e) for e in bitstr[8*k:8*k+8][-1::-1]),2))

	return bytes(ibytes)


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

# need to flip each byte in the bitmask around
def processbitarray(data):
	datastring=""
	DataLen=len(data)
	for k in range(DataLen):
		curbyte=bin(unpack("c",data[k:k+1])[0][0])[2:].zfill(8)[-1::-1]
		datastring=datastring+curbyte
	return datastring

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

class Blueprint(BaseObject):
	"blueprint class"
	def __init__(self,**kwargs):
		super(Blueprint,self).__init__(**kwargs)
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
		self._properties['Class']=max(round((self._properties["Devices"]*.01*3+self._properties["Lights"]*.05*2+self._properties["Triangles"]*.0001)/6),1)


	# TODO: fix lazy getter/setters
	def getProp(self,Property):
		return self._properties[Property];

	def setProp(self,Property,newValue):
		self._properties[Property]=newValue


