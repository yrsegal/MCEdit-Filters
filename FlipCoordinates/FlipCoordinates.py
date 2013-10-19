########## Flip Coordinates by jgierer12 ###########
# for magib1
# Flips relative coordinates in command blocks ("-" -> "+", "+" -> "-")

########## VERSION 1.0 ###########


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



commands = [
	("setblock", 2),
	("testforblock", 2),
	("tp", 2),
	("playsound", 4),
	("spawnpoint", 3),
	("summon", 3),
]

displayName = "Flip Coordinates"

inputs = (
	("Include Command Blocks", True),
	("Include Command Block Minecarts", True),
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
	
########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	changes = getChanges(level, box, options)
	flipCoordinates(level, box, options, changes)

def flipCoordinates(level, box, options, changes):
	for (bposX, bposZ, oldCommand, isTile, cmdBlock) in changes:
		oldCommandArray = oldCommand.split()

		wordIndex = 0
		newCommandArray = []
		for word in oldCommandArray:
			for (command, XCoordIndex) in commands:
				if word == command or word == "/"+command:
					XCoord = oldCommandArray[wordIndex+XCoordIndex]
					print XCoord
					YCoord = oldCommandArray[wordIndex+XCoordIndex+1]
					print YCoord
					ZCoord = oldCommandArray[wordIndex+XCoordIndex+2]
					print ZCoord

					if XCoord[0] == "~":
						XCoord = "~"+str(int(XCoord[1:])*(-1))
					if YCoord[0] == "~":
						YCoord = "~"+str(int(YCoord[1:])*(-1))
					if ZCoord[0] == "~":
						ZCoord = "~"+str(int(ZCoord[1:])*(-1))

					oldCommandArray[wordIndex+XCoordIndex] = XCoord
					oldCommandArray[wordIndex+XCoordIndex+1] = YCoord
					oldCommandArray[wordIndex+XCoordIndex+2] = ZCoord

			newCommandArray.append(word)

			wordIndex = wordIndex+1

		newCommand = " ".join(newCommandArray)

		chunk = getChunk(bposX, bposZ)

		if isTile:
			entities = chunk.TileEntities
		else:
			entities = chunk.Entities

		for ent in entities:
			if ent == cmdBlock:
				ent["Command"].value = newCommand

		chunk.dirty = True




def getChanges(level, box, options):
	changes = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		for tile in chunk.TileEntities:
			x = tile["x"].value
			y = tile["y"].value
			z = tile["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and "Command" in tile and options["Include Command Blocks"]:
				changes.append((x, z, tile["Command"].value, True, tile))
		
		for ent in chunk.Entities:
			x = int(ent["Pos"][0].value-0.5)
			y = int(ent["Pos"][1].value)
			z = int(ent["Pos"][2].value-0.5)
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz and "Command" in ent and options["Include Command Block Minecarts"]:
				changes.append((x, z, ent["Command"].value, False, ent))

	return changes