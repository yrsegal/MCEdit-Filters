#### Command Block To Command Block Structure ####
# Filter for MCEdit by destruc7i0n 
# Puts all the command blocks in the region into a structure that can activate them 
# heavily based off of jgierer12's Create Wireless Screen Filter (http://is.gd/CWSJG12)

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

		("Step I; Select: Select a region with command blocks", "label"),
		("Step II; Generate: Select the region where the Command Blocks are generated", "label"),
		("(Go to the 'General' Tab to select the step; Select or Generate)", "label"),
	),

	(
		("General", "title"),

		("Step: ", ("Select", "Generate")),
	),
	
	(
		("Dev", "title"),
		
		("(Still A Work In Progress Page!)", "label"),
		("Print Commands After Selection", True),
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

	global commandBlocks

	if options["Step: "] == "Select":
		command = command, commandBlocks = getCommandBlocks(level, box, options)

		if commandBlocks == []:
			commandBlocks = None;
			raise Exception("Please select an area with command blocks!")

	else:
		if commandBlocks:
			if box.maxx-box.minx < 4:
				raise Exception("The selection must be at least 3 blocks deep (x dimension)")
			elif box.maxz-box.minz < 5:
				raise Exception("The selection must be at least 5 blocks wide (z dimension)")

			createCmdBlocks(level, box, options, commandBlocks, command)
		else:
			raise Exception("Please select an area with cmd blocks first!")

def createCmdBlocks(level, box, options, commandBlocks, command):

	i = 0

	x = box.minx
	y = box.miny
	z = box.minz

	level.setBlockAt(x, y+2, z, 159) # Block
	level.setBlockDataAt(x, y+2, z, 5) # Block Data
	chunk = getChunk(x, z)
	chunk.dirty = True

	rsLen = 0
	direction = True

	for command in commandBlocks:
		newPos = getNewPos(x, y, z, box, level, rsLen, direction)
		x = newPos[0]
		y = newPos[1]
		z = newPos[2]

		rsLen = newPos[3]
		direction = newPos[4]

		level.setBlockAt(x, y+2, z, 55) # Redstone Dust

		level.setBlockAt(x, y+1, z, 137) # Command Block
		chunk = getChunk(x, z)
		commandBlock = cmdBlock(x, y+1, z, command)
		chunk.TileEntities.append(commandBlock)
		chunk.dirty = True

		i = i+1

def getCommandBlocks(level, box, options):
	commandBlocks = []
	command = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		
		for t in chunk.TileEntities:
			x = t["x"].value
			y = t["y"].value
			z = t["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				if t["id"].value == "Control":
					command = t["Command"].value
					if options["Print Commands After Selection"] == True:
						print("Command At: " +str(x)+"(x)"+" "+str(y)+"(y)"+" "+str(z)+ "(z)" + " " +"is: " + command + "													")

	return(command, commandBlocks)
	
def cmdBlock(x, y, z, command):
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command["Command"].value)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)

	return control

def getNewPos(x, y, z, box, level, rsLen, direction):
	rsLen = rsLen+1

	if direction == True:

		if z < box.maxz-3:
			z = z+1

			if rsLen >= 16:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 2) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z+1

		else:
			direction = False

			rsLen = 2

			level.setBlockAt(x, y+1, z+1, 159) # Block
			level.setBlockDataAt(x, y+1, z+1, 9) # Block Data

			level.setBlockAt(x, y+2, z+1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z+1, 2) # Repeater Data

			level.setBlockAt(x, y+3, z+1, 159) # Block
			level.setBlockDataAt(x, y+3, z+1, 9) # Block Data

			level.setBlockAt(x, y+4, z+1, 55) # Redstone Dust
			chunk = getChunk(x, z+1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z+2, 159) # Block
			level.setBlockDataAt(x, y+2, z+2, 9) # Block Data

			level.setBlockAt(x, y+3, z+2, 55) # Redstone Dust
			chunk = getChunk(x, z+2)
			chunk.dirty = True

			y = y+3

	else:

		if z > box.minz+3:
			z = z-1

			if rsLen >= 16:
				rsLen = 0

				level.setBlockAt(x, y+1, z, 159) # Block
				level.setBlockDataAt(x, y+1, z, 9) # Block Data

				level.setBlockAt(x, y+2, z, 93) # Repeater
				level.setBlockDataAt(x, y+2, z, 0) # Repeater Data
				chunk = getChunk(x, z)
				chunk.dirty = True

				z = z-1

		else:
			direction = True

			rsLen = 2

			level.setBlockAt(x, y+1, z-1, 159) # Block
			level.setBlockDataAt(x, y+1, z-1, 9) # Block Data

			level.setBlockAt(x, y+2, z-1, 93) # Repeater
			level.setBlockDataAt(x, y+2, z-1, 0) # Repeater Data

			level.setBlockAt(x, y+3, z-1, 159) # Block
			level.setBlockDataAt(x, y+3, z-1, 9) # Block Data

			level.setBlockAt(x, y+4, z-1, 55) # Redstone Dust
			chunk = getChunk(x, z-1)
			chunk.dirty = True

			level.setBlockAt(x, y+2, z-2, 159) # Block
			level.setBlockDataAt(x, y+2, z-2, 9) # Block Data

			level.setBlockAt(x, y+3, z-2, 55) # Redstone Dust
			chunk = getChunk(x, z-2)
			chunk.dirty = True

			y = y+3

	if y+3 > box.maxy:
		raise Exception("The selection must be higher (y dimension)")

	return (x, y, z, rsLen, direction)