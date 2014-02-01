#### Entities to Command Blocks ####
# Filter for MCEdit by jgierer12, suggested by BilboLovesRedstone


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




displayName = "Command Blocks to Command Block Structures"

inputs = [
	(
		("Instructions", "title"),

		("Step I: Select a region with command blocks", "label"),
		("Step II: Select the region where the Command Blocks are generated", "label"),
	),

	(
		("General", "title"),

		("Step: ", ("I", "II")),
	),
]

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

	global cmdBlocks

	if options["Step: "] == "I":
		cmdBlocks = getCmdBlocks(level, box, options)

		if cmdBlocks == []:
			cmdBlocks = None;
			raise Exception("Please select an area with cmd blocks!")

	else:
		if cmdBlocks:
			createCmdBlock(level, box, options, cmdBlocks)

		else:
			raise Exception("Please select an area with cmd blocks first!")

def createCmdBlock(level, box, options, cmdBlocks):
	x = box.minx
	y = box.miny
	z = box.minz

	for (eposX, eposY, eposZ, entity) in cmdBlocks:

		level.setBlockAt(x, y, z, 137) # Command Block
		cmd = cmdBlock((x, y, z), command[:len(command)-1])
		chunk = getChunk(x, z)
		chunk.TileEntities.append(cmd)
		chunk.dirty = True

		if x+1 < box.maxx:
			x = x+1
		elif z+1 < box.maxz:
			z = z+1
			x = box.minx
		elif y+2 < box.maxy:
			y = y+2
			x = box.minx
			z = box.minz
		else:
			raise Exception("Your selection is too small!")

def getCmdBlocks(level, box, options):
	cmdBlocks = []
	
	for (chunk, slices, point) in level.getChunkSlices(box):
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command = t["Command"].value
						chunk.dirty = True
				
	return cmdBlocks
	
def cmdBlock((x, y, z), command):
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)

	return control
