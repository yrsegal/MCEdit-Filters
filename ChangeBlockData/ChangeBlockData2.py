#### Change Block Data ####
# Filter for MCEdit by destruc7i0n with a little help of jgierer12 :)
# Based off of many of jgierer12's Filters
# http://youtube.com/TheDestruc7i0n

import pymclevel
import random

displayName = "Set Block Data Value"

inputs = (
        ("One Block To Change Data Only: ", "blocktype"),
		("Use Only One Block: ", True),
		("Block Data For One Block: ", 1), 
		("Change All Blocks In Region To A Data: ", False),
		("Block Data Value: ", 1),
		("Please Only Select One Option!", "label"),
		("Diversify It!", False) 
)

def perform(level, box, options):
    oneBlockOnly = options["One Block To Change Data Only: "]
    oneBlockOnlyTF = options["Use Only One Block: "]
    oneBlockOnlyData = options["Block Data For One Block: "]
    changeAllBlocksTF = options["Change All Blocks In Region To A Data: "]
    changeAllBlocksData = options["Block Data Value: "]
	deversifyIt = options["Diversify It!"]
		
    if oneBlockOnlyTF == True and changeAllBlocksTF == True and diversifyIt == True:
		raise Exception('Only check one box!')
	
	if diversifyIt == True and changeAllBlocksTF == False and oneBlockOnlyTF == False: 
		diversifyIt = 1
	else:
		continue
	
    for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
			
				if oneBlockOnlyTF == True and changeAllBlocksTF == False and level.blockAt(x, y, z) == oneBlockOnly:
					level.setBlockDataAt(x, y, z, oneBlockOnlyData) 
				elif changeAllBlocksTF == True and oneBlockOnlyTF == False
					level.setBlockDataAt(x, y, z, changeAllBlocksData) 
					diversify(x,y,z, diversifyIt) 
					
def diversify(x,y,z, diversifyIt): 
	for x in xrange(box.minx, box.maxx):
					for z in xrange(box.minz, box.maxz):
							for y in xrange(box.miny, box.maxy):
									if diversifyIt == 1 and level.blockAt(x, y, z) == 35:
											level.setBlockDataAt(x, y, z, random.randint(0,15))
					elif diversifyIt == 1 and level.blockAt(x, y, z) == 95:
											level.setBlockDataAt(x, y, z, random.randint(0,15))
					elif diversifyIt == 1 and level.blockAt(x, y, z) == 159:
											level.setBlockDataAt(x, y, z, random.randint(0,15))
					elif diversifyIt == 1 and level.blockAt(x, y, z) == 160:
											level.setBlockDataAt(x, y, z, random.randint(0,15))
					elif diversifyIt == 1 and level.blockAt(x, y, z) == 171:
											level.setBlockDataAt(x, y, z, random.randint(0,15))
			
		level.markDirtyBox(box)