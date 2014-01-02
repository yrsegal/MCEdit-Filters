#### Change Block Data ####
# Filter for MCEdit by destruc7i0n with a little help of jgierer12 :)
# Based off of many of jgierer12's Filters
# http://youtube.com/TheDestruc7i0n

displayName = "Set Block Data Value"

inputs = (
	("One Block To Change Data Only: ", "blocktype"),
	("Use Only One Block: ", True),
	("Block Data For One Block: ", 1), 
	("Change All Blocks In Region To A Data: ", False),
	("Block Data Value: ", 1),
	("Please Only Select One Option!", "label"),
)

def perform(level, box, options):
	oneBlockOnly = options["One Block To Change Data Only: "].ID
	oneBlockOnlyTF = options["Use Only One Block: "]
	oneBlockOnlyData = options["Block Data For One Block: "]
	changeAllBlocksTF = options["Change All Blocks In Region To A Data: "]
	changeAllBlocksData = options["Block Data Value: "]
	
	if oneBlockOnlyTF == True and changeAllBlocksTF == True:
		raise Exception('Only check one box between "Use Only One Block" and "Change All Blocks In Region To A Data"')
 
	for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
				if oneBlockOnlyTF == True and changeAllBlocksTF == False and level.blockAt(x, y, z) == oneBlockOnly:
					level.setBlockDataAt(x, y, z, oneBlockOnlyData)
				elif changeAllBlocksTF == True and oneBlockOnlyTF == False:
					level.setBlockDataAt(x, y, z, changeAllBlocksData)

	level.markDirtyBox(box)
		