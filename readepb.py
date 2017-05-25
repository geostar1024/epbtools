from struct import *

blocks={558:"Core",403:"L Steel",257:"CV Cockpit 1",406:"L Hardened Steel",412:"L Combat Steel",934:"CV RCS T2",381:"S Steel",383:"S Hardened Steel",456:"SV Thruster S"}

shipdict={2:"BA",4:"SV",8:"CV",16:"HV"}

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
	
	# seem to be different for every ship; some kind of id?
	print(unpack("h",fpr.read(2))[0])
	print(unpack("h",fpr.read(2))[0])
	print(unpack("h",fpr.read(2))[0])
	
	# location 0x8D: same for 11 bytes
	print("")
	fpr.read(11)
	
	# different for some reason
	print(unpack("h",fpr.read(2))[0])
	
	# always the same
	print("")
	fpr.read(3)
	
	# next section is the steam ID and steam username for the original creator and current maker in ASCII
	# there are 4 fields, prefixed in order by 0x0B, 0x0A, 0x0D, 0x0C
	# then an empty 4 bytes (0x0000 0x0000) before each text field
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam ID of the creator
	steamidlen=unpack(">i",fpr.read(4))[0]
	print("steam ID of creator length: %d" % steamidlen)
	
	steamid=fpr.read(steamidlen)
	print("steam ID of creator: %s" % steamid)
	
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam name of the creator
	steamnamelen=unpack(">i",fpr.read(4))[0]
	print("steam ID of creator length: %d" % steamnamelen)
	
	steamname=fpr.read(steamnamelen)
	print("steam ID of creator: %s" % steamname)
	
	# steam id and name of the current blueprint maker
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam ID of the current blueprint maker
	steamidlen2=unpack(">i",fpr.read(4))[0]
	print("steam ID of current length: %d" % steamidlen2)
	
	steamid2=fpr.read(steamidlen2)
	print("steam ID of current: %s" % steamid2)
	
	
	print(unpack("c",fpr.read(1))[0][0])
	fpr.read(4)
	
	# next is a length-first string for the steam name of the current blueprint maker
	steamnamelen2=unpack(">i",fpr.read(4))[0]
	print("steam ID of current length: %d" % steamnamelen2)
	
	steamname2=fpr.read(steamnamelen2)
	print("steam name of current: %s" % steamname2)
	
	# region between steamid fields and block/device list
	# there's something in the first 3 bytes . . .
	
	fpr.read(3)
	
	# seem empty
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	
	
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
		curblock=unpack("h",fpr.read(2))[0]
		devicetypelist.append(curblock)
		
		# block amount is little-endian!
		curblocknum=unpack("i",fpr.read(4))[0]
		print("%16s (%04d): %d" % (blocks.get(curblock),curblock,curblocknum))
	
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
		

	# block and group list section terminated by 5 bytes: 0x0000 0x0003 0x04
	
	fpr.read(5)
	
	# section header and footer for grid has the following format:
	#   0x1400 0x0000 0x0800 <3 bytes> 0x4A <12 bytes> 0x0100 0x0000
	# part of this is the length of the grid data, as indicated below
	
	print(unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0])
	print(unpack("c",fpr.read(1))[0][0],unpack("c",fpr.read(1))[0][0],unpack("c",fpr.read(1))[0][0])
	fpr.read(1)
	print(unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0])
	
	# length of grid data in bytes
	gridlen=unpack("i",fpr.read(4))[0]
	print("length of grid (bytes): %d" % gridlen)
	
	# another 2 integers
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	
	# start of grid proper indicated by 0x30
	fpr.read(1)
	
	printgrid=0
	# read gridlen number of bytes
	for k in range(0,gridlen):
		if (printgrid):
			print(k,hex(unpack("c",fpr.read(1))[0][0]))
		else:
			fpr.read(1)
	
	# end of grid indicated by 0x504b 0x0102 0x1400
	fpr.read(6)
	
	# section header repeats as a footer
	print(unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0])
	print(unpack("c",fpr.read(1))[0][0],unpack("c",fpr.read(1))[0][0],unpack("c",fpr.read(1))[0][0])
	fpr.read(1)
	print(unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0])
	
	# length of grid data in bytes
	gridlen=unpack("i",fpr.read(4))[0]
	print("length of grid (bytes): %d" % gridlen)
	
	# another 2 integers
	print(unpack("i",fpr.read(4))[0])
	print(unpack("i",fpr.read(4))[0])
	
	# footer is always 0x00 0x0000 0x0000 0x0000 0x0000 0x0000 0x0000 0x0030 0x504B 0x0506 0x0000 0x0000 0x0100 0x0100 0x2F00 0x0000 (but maybe check it anyway)
	fpr.read(31)
	
	# last 6 bytes of file always different, usually ending with 0x0000 0x0000
	# maybe some kind of size indicator? (empirically, larger blueprints have larger values)
	print(unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0],unpack("h",fpr.read(2))[0])

	# that's it!
