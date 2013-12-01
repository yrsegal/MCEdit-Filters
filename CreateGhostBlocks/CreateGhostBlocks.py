########## Create Ghost Blocks by jgierer12 ###########
# for destruc7i0n


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




displayName = "Create Ghost Blocks"

inputs = (
    ("Command Blocks Relative Position:", "label"),
	("dx", 5),
	("dy", 0),
	("dz", 0),
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
	
########## End fast data access ##########

def perform(level, box, options):
	global GlobalLevel
	GlobalLevel = level

	builds = getBlocks(box)
	createCmdBlock(level, box, options, builds)

def createCmdBlock(level, box, options, builds):	
	# Find redstone/spawner coordinates
	dx = options["dx"]
	dy = options["dy"]
	dz = options["dz"]

	if dx == 0:
		rsx = (box.maxx + box.minx) / 2
	if dy == 0:
		rsy = (box.maxy + box.miny) / 2
	if dz == 0:
		rsz = (box.maxz + box.minz) / 2
		
	if dx < 0:
		rsx = box.minx + dx
	if dy < 0:
		rsy = box.miny + dy
	if dz < 0:
		rsz = box.minz + dz
	
	if dx > 0:
		rsx = box.maxx + dx
	if dy > 0:
		rsy = box.maxy + dy
	if dz > 0:
		rsz = box.maxz + dz

	posX = rsx
	posY = rsy
	posZ = rsz


	level.setBlockAt(posX-1, posY+2, posZ, 137) # Command Block 1
	level.setBlockAt(posX-3, posY+2, posZ, 137) # Command Block 2
	level.setBlockAt(posX-2, posY+2, posZ, 75) # RS Torch
	level.setBlockDataAt(posX-2, posY+2, posZ, 2) # RS Torch Data
	level.setBlockAt(posX-1, posY+2, posZ-1, 69) # Lever
	level.setBlockDataAt(posX-1, posY+2, posZ-1, 12) # Lever Data
	level.setBlockAt(posX, posY+2, posZ, 152) # RS Block
	level.setBlockAt(posX-1, posY+2, posZ+1, 68) # Sign
	level.setBlockDataAt(posX-1, posY+2, posZ+1, 3) # Sign Rotation

	cmd = cmdBlock((posX-1, posY+2, posZ), "/setblock ~1 ~ ~ 152 0 destroy")
	chunk = getChunk(posX-1, posZ)
	chunk.TileEntities.append(cmd)
	chunk.dirty = True
	cmd = cmdBlock((posX-3, posY+2, posZ), "/setblock ~3 ~ ~ 152 0 destroy")
	chunk = getChunk(posX-3, posZ)
	chunk.TileEntities.append(cmd)
	chunk.dirty = True
	sign = signTileEntity(posX-1, posY+2, posZ+1, "Ghost Blocks", "", "Summons", str(len(builds))+" FS")
	chunk = getChunk(posX-1, posZ+1)
	chunk.TileEntities.append(sign)
	chunk.dirty = True

	rsLength = 13
	# Create commands
	for (bposX, bposY, bposZ, bID, bdata) in builds:
		command = "/summon FallingSand "+str(bposX)+" "+str(bposY)+" "+str(bposZ)+" {Time:0,TileID:"+str(bID)+",Data:"+str(bdata)+",Motion:[0.0,0.04,0.0],DropItem:0}"

		# Create Blocks

		level.setBlockAt(posX, posY, posZ, 137) # Command Block
		cmd = cmdBlock((posX, posY, posZ), command)
		if posY == rsy:
			level.setBlockAt(posX, posY+1, posZ, 55) # Redstone 
		chunk = getChunk(posX, posZ)
		chunk.TileEntities.append(cmd)
		chunk.dirty = True
		chunk = getChunk(posX, posZ+1)
		chunk.dirty = True

		if posX-rsx <= rsLength:
			posX = posX+1
		else:
			posX = rsx

			if posY == rsy:
				posY = rsy-1
			else:
				posY = rsy
				posZ = posZ-1
				rsLength = rsLength-1


def getBlocks(box):
	builds = []
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.maxy-1, box.miny-1, -1):
				block = blockAt(x, y, z)
				if block != 0:						
					builds.append((x, y, z, block, dataAt(x, y, z)))

	return builds

def cmdBlock((x, y, z), command):
	control = TAG_Compound()
	control["id"] = TAG_String("Control")
	control["Command"] = TAG_String(command)
	control["x"] = TAG_Int(x)
	control["y"] = TAG_Int(y)
	control["z"] = TAG_Int(z)

	return control

def signTileEntity(x, y, z, text1, text2, text3, text4):
	sign = TAG_Compound()
	sign["id"] = TAG_String("Sign")
	sign["Text1"] = TAG_String(text1)
	sign["Text2"] = TAG_String(text2)
	sign["Text3"] = TAG_String(text3)
	sign["Text4"] = TAG_String(text4)
	sign["x"] = TAG_Int(x)
	sign["y"] = TAG_Int(y)
	sign["z"] = TAG_Int(z)
	
	return sign
