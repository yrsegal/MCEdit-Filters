########## Randomize Chests by jgierer12 ###########
# for Beatmeup50
# Randomizes the slot of items in a chest

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
import random


containers = [
	("Chest", 27, " - Chests"),
	("MinecartChest", 27, " - Chest Minecarts"),
	("Hopper", 5, " - Hoppers"),
	("MinecartHopper", 5, " - Hopper Minecarts"),
	("Dispenser", 9, " - Dispensers"),
	("Dropper", 9, " - Droppers"),
]

displayName = "Randomize Chests"

inputs = (
	("Include: (If checked, all will be included)", True),
	(" - Chests", True),
	(" - Chest Minecarts", True),
	(" - Hoppers", True),
	(" - Hopper Minecarts", True),
	(" - Dispensers", True),
	(" - Droppers", True),
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
	
def tileEntityAt(x, y, z):
	chunk = getChunk(x, z)
	if chunk == None:
		return 0
	return chunk.tileEntityAt(x, y, z)
	
########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	randomizes = getRandomizes(level, box, options)
	changeIDs(level, box, options, randomizes)

def changeIDs(level, box, options, randomizes):
	for (bposX, bposZ, chestBlock, itemsTag, slotCount, isTile) in randomizes:

		occupiedSlots = []
		for itemTag in itemsTag:
			randomSlot = random.randrange(1, slotCount)

			while  randomSlot in occupiedSlots:
				randomSlot = random.randrange(1, slotCount)

			occupiedSlots.append(randomSlot)

			chunk = getChunk(bposX, bposZ)

			if isTile:
				entities = chunk.TileEntities
			else:
				entities = chunk.Entities

			for ent in entities:
				if ent == chestBlock:
					for itm in ent["Items"]:
						if itm == itemTag:
							itm["Slot"].value = randomSlot

			chunk.dirty = True

def getSlotCount(entID):
	for (ID, slotCount, called) in containers:
		if entID == ID:
			return slotCount

def getIncludedIDs(options):
	includedIDs = []
	for option in options:
		for (ID, slotCount, called) in containers: 
			if option == called or options["Include: (If checked, all will be included)"]:
				includedIDs.append(ID)

	return includedIDs

def getRandomizes(level, box, options):
	randomizes = []

	for (chunk, slices, point) in level.getChunkSlices(box):
		for tile in chunk.TileEntities:
			x = tile["x"].value
			y = tile["y"].value
			z = tile["z"].value
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				includedIDs = getIncludedIDs(options)
				if tile["id"].value in includedIDs:
					slotCount = getSlotCount(tile["id"].value)
					randomizes.append((x, z, tile, tile["Items"].value, slotCount, True))
		
		for ent in chunk.Entities:
			x = int(ent["Pos"][0].value-0.5)
			y = int(ent["Pos"][1].value)
			z = int(ent["Pos"][2].value-0.5)
			
			if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
				includedIDs = getIncludedIDs(options)
				if tile["id"].value in includedIDs:
					slotCount = getSlotCount(tile["id"].value)
					randomizes.append((x, z, ent, ent["Command"].value, slotCount, False))

	return randomizes