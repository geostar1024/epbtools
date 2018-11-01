from epbtools.utility import *
from epbtools.grid import Grid
from epbtools.blueprint import Blueprint
from epbtools.block import Block

# write a blueprint object to a file
def writeepb(filename,blueprint):

	# write everything but the block data
	writeEPBHeader(filename,blueprint)

	# make the zipped block data
	zipdata=makeBlockData(blueprint)

	fpw=open(filename,"ab")

	# strip off the leading PK because that's how Eleon rolls
	# actually, could simply be to prevent zip programs from deciding blueprint files are archives
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
	fpw.write(binascii.unhexlify(str(blueprint.type.value).zfill(2)))

	# write the dimensions
	fpw.write(pack("i",blueprint.dimensions[0]))
	fpw.write(pack("i",blueprint.dimensions[1]))
	fpw.write(pack("i",blueprint.dimensions[2]))

	# write something to do with the blueprint revision number
	fpw.write(binascii.unhexlify("01000F00"))

	# write a bunch of unknown data
	# it looks like a bunch of ints, but it's unclear what it represents

	fpw.write(binascii.unhexlify("11000000000000030000000000010000000000000100000E0000000000000300000000000F000000000000030000000000050000000000000100000400000000000002000000000006000000000000040000000000000000000000000007000000000000000009000000"))

	# write an int that signals the start of the timestamp
	fpw.write(pack(">i",5))

	# write timestamp
	# subtract the epoch from the stored datetime and multiply by 10^7
	curdatenum=int((blueprint.datetime-Blueprint.EPOCH).total_seconds()*1e7)

	# convert to hex and remove the trailing 0x00 and write it
	fpw.write(pack("Q",curdatenum)[:-1])
	fpw.write(binascii.unhexlify("88"))

	# write something that might contain a section identifier (for the upcoming steamid section?)
	fpw.write(binascii.unhexlify("000800000000000002"))

	# write the build number
	fpw.write(pack("h",blueprint.game_build))

	fpw.write(binascii.unhexlify("000000"))

	# write the steamid section
	# first, the original creator id and name
	fpw.write(binascii.unhexlify("0B"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(str(blueprint.creator.steam_id))))
	fpw.write(bytes(str(blueprint.creator.steam_id),"utf8"))

	fpw.write(binascii.unhexlify("0A"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.creator.display_name)))
	fpw.write(bytes(blueprint.creator.display_name,"utf8"))

	# then the current user id and name
	fpw.write(binascii.unhexlify("0D"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(str(blueprint.user.steam_id))))
	fpw.write(bytes(str(blueprint.user.steam_id),"utf8"))

	fpw.write(binascii.unhexlify("0C"))
	fpw.write(pack("i",0))
	fpw.write(pack(">i",len(blueprint.user.display_name)))
	fpw.write(bytes(blueprint.user.display_name,"utf8"))

	# next 11 bytes are unknown
	fpw.write(binascii.unhexlify("1000000000000000000000"))

	# write the basic stats of number of lights, devices, triangles, and blocks
	fpw.write(pack("i",blueprint.lights))
	fpw.write(pack("i",0))

	fpw.write(pack("i",blueprint.devices))
	fpw.write(pack("i",0))

	fpw.write(pack("i",blueprint.blocks))
	fpw.write(pack("i",0))
	fpw.write(pack("i",blueprint.triangles))

	# write the block list
	fpw.write(pack("h",len(blueprint.block_type_list)))
	for block in blueprint.block_type_list:
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
	blockarray=blueprint.grid

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
	#print(newdata)

	fpw.close()

	fpw3.writestr("0",newdata)

	print(fpw3.testzip())

	fpw3.close()

	fpw3=open("0000","rb")

	zipdata=fpw3.read(-1)

	fpw2.close()
	fpw3.close()

	return zipdata
