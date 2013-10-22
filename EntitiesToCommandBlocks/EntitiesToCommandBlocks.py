########## Entities to Command Blocks by jgierer12 ###########
# for BilboLovesRedstone
# Converts all entities in the selection to a command block

########## VERSION 1.1 ###########
# Fixed a bug: [MAJOR] Filter won't work if there are TileEntities in the way


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





displayName = "Entities to Command Blocks"

inputs = (
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
	global GlobalLevel
	GlobalLevel = level

	spawns = getSpawns(level, box, options)
	createCmdBlocks(level, box, options, spawns)

def createCmdBlocks(level, box, options, spawns):
	for (eposX, eposY, eposZ, entity) in spawns:
		dataTags = tagCode(entity)
		command = "/summon "+entity["id"].value+" ~ ~ ~ "+dataTags
		command = command[:len(command)-1]

		level.setBlockAt(eposX, eposY, eposZ, 137) # Command Block

		chunk = getChunk(eposX, eposZ)
		for tileEntitie in chunk.TileEntities:
			if tileEntitie["x"].value == eposX and tileEntitie["y"].value == eposY and tileEntitie["z"].value == eposZ:
				chunk.TileEntities.remove(tileEntitie)

		cmd = cmdBlock((eposX, eposY, eposZ), command)
		chunk.TileEntities.append(cmd)
		chunk.dirty = True

		



def getSpawns(level, box, options):
	spawns = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		
		for ent in chunk.Entities:
			x = int(ent["Pos"][0].value-0.5)
			y = int(ent["Pos"][1].value)
			z = int(ent["Pos"][2].value-0.5)
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				spawns.append((x, y, z, ent))

	return spawns

def tagCode(nbt):
	if type(nbt) is TAG_Compound:
		tags = []
		for subTag in nbt.value:
			tags.append(tagCode(subTag))
		if nbt.name:
			return nbt.name+":{"+"".join(tags)+"},"
		else:
			return "{"+"".join(tags)+"},"

	elif type(nbt) is TAG_List:
		tags = []
		for subTag in nbt.value:
			tags.append(tagCode(subTag))

		if nbt.name:
			return nbt.name+":["+"".join(tags)+"],"

		else:
			return "["+"".join(tags)+"],"

	else:
		if nbt.name:
			return nbt.name+":"+str(nbt.value)+","

		else:
			return str(nbt.value)+","

def cmdBlock((x, y, z), command):
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)

	return control