########## Change Repeater Delay by jgierer12 ###########
# for destruc7i0n
# Changes the delay of every repeater in the selection

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

displayName = "Change Repeater Delay"

inputs = (
	("Method: ", ("Set", "Add", "Subtract")),
	("Value: ", 1),
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
	
########## End fast data access ##########

def perform(level, box, options):
	method = options["Method: "]
	value = options["Value: "]

	global GlobalLevel
	GlobalLevel = level

	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.maxy-1, box.miny-1, -1):
				block = blockAt(x, y, z)
				if block == 93 or block == 94:
					data = getData(dataAt(x, y, z), method, value)
					level.setBlockDataAt(x, y, z, data)

def getData(data, method, value):
	if method == "Set":
		if data == 0 or data == 4 or data == 8 or data == 12:
			data = ((value-1)*4)+0
		if data == 1 or data == 5 or data == 9 or data == 13:
			data = ((value-1)*4)+1
		if data == 2 or data == 6 or data == 10 or data == 14:
			data = ((value-1)*4)+2
		if data == 3 or data == 7 or data == 11 or data == 15:
			data = ((value-1)*4)+3

		while data >= 16:
			data = data-4

	elif method == "Add":
		data = data+(value*4)

		while data >= 16:
			data = data-4

	else:
		data = data-(value*4)

		while data <= -1:
			data = data+4

	return data
