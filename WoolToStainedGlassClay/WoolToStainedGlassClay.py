# MCEdit Filter by CrushedPixel Changed A Bit By destruc7i0n  
# http://youtube.com/CrushedPixel
# http://youtube.com/TheDestruc7i0n

displayName = "Wool to Stained Glass/Clay"

inputs = (
	("Replace Wool with: ", ("Stained Glass", "Stained Clay")),
)

def perform(level, box, options):
	replaceWith = options["Replace Wool with: "]
	
	for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):

				if replaceWith == "Stained Glass" and level.blockAt(x, y, z) == 35:
					level.setBlockAt(x, y, z, 95)    
				elif replaceWith == "Stained Clay" and level.blockAt(x, y, z) == 35:
					level.setBlockAt(x, y, z, 159)
					
	level.markDirtyBox(box)
