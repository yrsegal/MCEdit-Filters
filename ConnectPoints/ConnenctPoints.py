#### Connect Points ####
# Filter for MCEdit by jgierer12, suggested by SlinkyThePanda


from __future__ import division
from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_String
from pymclevel import TAG_Int_Array
from pymclevel import TAG_Float
from pymclevel import TAG_Long
import math



displayName = "Connect Points"

inputs = (
	("connect", "blocktype"),
	("with", "blocktype"),
)

########## Fast data access ##########
from pymclevel import ChunkNotPresent
GlobalChunkCache = {}
GlobalLevel = None

def getChunk(x, z):
	global GlobalChunkCache
	global GlobalLevel
	chunkCoords = (x>>4, z>>4)
	if chunkCoords not in GlobalChunkCache:
		try:
			GlobalChunkCache[chunkCoords] = GlobalLevel.getChunk(x>>4, z>>4)
		except ChunkNotPresent:
			return None

	return GlobalChunkCache[chunkCoords]

def blockAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Blocks[x%16][z%16][y]

def dataAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.Data[x%16][z%16][y]

def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

def setBlockAt(x, y, z, block):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Blocks[x%16][z%16][y] = block

def setDataAt(x, y, z, data):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	chunk.Data[x%16][z%16][y] = data

def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)

########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	blocks = getBlocks(box, options)

	connect(level, options, blocks)

def getBlocks(box, options):
	blocks = []

	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.maxy-1, box.miny-1, -1):
				if blockAt(x, y, z) == options["connect"].ID and dataAt(x, y, z) == options["connect"].blockData:
					blocks.append((x, y, z))

	if len(blocks) > 2:
		raise Exception("There are more than 2 Blocks with the ID "+str(options["connect"].ID)+" and the Data Value "+str(options["connect"].blockData)+"!")
	elif len(blocks) < 2:
		raise Exception("There are less than 2 Blocks with the ID "+str(options["connect"].ID)+" and the Data Value "+str(options["connect"].blockData)+"!")

	return blocks

def connect(level, options, blocks):
	x1 = blocks[0][0]
	y1 = blocks[0][1]
	z1 = blocks[0][2]

	x2 = blocks[1][0]
	y2 = blocks[1][1]
	z2 = blocks[1][2]

	totalX = x2-x1
	totalY = y2-y1
	totalZ = z2-z1

	if totalX >= 0:
		facX = 1
	else:
		facX = -1

	if totalY >= 0:
		facY = 1
	else:
		facY = -1

	if totalZ >= 0:
		facZ = 1
	else:
		facZ = -1

	totalX = abs(totalX)
	totalY = abs(totalY)
	totalZ = abs(totalZ)

	if totalX >= totalY and totalX >= totalZ:
		total1 = totalX
		total2 = totalY
		total3 = totalZ
		case = 1
	elif totalY >= totalX and totalY >= totalZ:
		total1 = totalY
		total2 = totalX
		total3 = totalZ
		case = 2
	else:
		total1 = totalZ
		total2 = totalX
		total3 = totalY
		case = 3

	line = []

	for new1 in xrange(1, total1):
		new2 = total2*(new1/total1)
		new3 = total3*(new1/total1)

		line.append((int(new1), int(new2), int(new3)))

	for (b1, b2, b3) in line:
		if case == 1:
			bX = blocks[0][0]+b1*facX
			bY = blocks[0][1]+b2*facY
			bZ = blocks[0][2]+b3*facZ
		elif case == 2:
			bX = blocks[0][0]+b2*facX
			bY = blocks[0][1]+b1*facY
			bZ = blocks[0][2]+b3*facZ
		else:
			bX = blocks[0][0]+b2*facX
			bY = blocks[0][1]+b3*facY
			bZ = blocks[0][2]+b1*facZ

		level.setBlockAt(bX, bY, bZ, options["with"].ID)
		level.setBlockDataAt(bX, bY, bZ, options["with"].blockData)
		getChunk(bX, bZ).dirty = True
