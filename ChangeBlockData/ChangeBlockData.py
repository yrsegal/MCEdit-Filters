#### Change Block Data ####
# Filter for MCEdit by destruc7i0n, modified by jgierer12
# Based off of many of jgierer12's Filters
# http://youtube.com/TheDestruc7i0n

import pymclevel
import random

displayName = "Set Block Data Value"

inputs = (
	("Only change Data of this Block: ", "blocktype"),
	("(Set to air to change data of all Blocks in the selection)", "label"),
	("Block Data Value: ", 0),
	("Diversify It!", False),
)

canDiversify = [35, 95, 159, 160, 171]

def perform(level, box, options):
	changeBlock = options["Only change Data of this Block: "].ID
	data = options["Block Data Value: "]
	diversifyIt = options["Diversify It!"]
	
	for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
				block = level.blockAt(x, y, z)
				
				if (changeBlock != 0 and block == changeBlock) or changeBlock == 0:
					level.setBlockDataAt(x, y, z, data)

				if diversifyIt and block in canDiversify:
					level.setBlockDataAt(x, y, z, random.randint(0,15))

	level.markDirtyBox(box)
