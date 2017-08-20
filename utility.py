from struct import *
import zipfile
import io
import binascii
import math
import random
import datetime

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


# need to flip each byte in the bitmask around
def processbitarray(data):
	datastring=""
	DataLen=len(data)
	for k in range(DataLen):
		curbyte=bin(unpack("c",data[k:k+1])[0][0])[2:].zfill(8)[-1::-1]
		datastring=datastring+curbyte
	return datastring
