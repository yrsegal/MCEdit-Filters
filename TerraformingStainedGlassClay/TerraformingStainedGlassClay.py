#### Terraforming Stained Glass/Clay ####
# Filter for MCEdit by CrushedPixel, modified by destruc7i0n and jgierer12
# http://youtube.com/CrushedPixel
# http://youtube.com/TheDestruc7i0n

displayName = "Natural Blocks to Stained Glass/Clay"

inputs = (
	("Replace Blocks with: ", ("Stained Glass", "Stained Clay")),
	("Delete Blocks that can't be replaced", False),
)

stainedGlassColors = {
	80: 0, # white
	#: 1, # orange
	#: 2, # magenta
	174: 3, # lblue
	12: 4, 24: 4, # yellow
	2: 5, # lime
	#: 6, # pink
	17: 7, 88: 7, # gray
	#: 8, # lgray
	1: 9, # cyan
	#: 10, # purple
	49: 11, # blue
	3: 12, # brown
	18: 13, # green
	87: 14, # red
	7: 15, 49: 15 # black
}

normalGlassColors = [
	4
]

stainedClayColors = {
	80: 0, # white
	#: 1, # orange
	#: 2, # magenta
	#: 3, # lblue
	12: 4, 24: 4, # yellow
	2: 5, # lime
	#: 6, # pink
	17: 7, 88: 7, # gray
	#: 8, # lgray
	1: 9, # cyan
	#: 10, # purple
	49: 11, # blue
	3: 12, # brown
	18: 13, # green
	87: 14, # red
	#: 15 # black
}

normalClayColors = [
	4
]

def perform(level, box, options):
	if options["Replace Blocks with: "] == "Stained Glass":
		stainedBlock = 95
		normalBlock = 82

		stainedColors = stainedGlassColors
		normalColors = normalGlassColors

	else:
		stainedBlock = 159
		normalBlock = 172

		stainedColors = stainedClayColors
		normalColors = normalClayColors

	for x in xrange(box.minx, box.maxx):
		for y in xrange(box.miny, box.maxy):
			for z in xrange(box.minz, box.maxz):
				replaced = False

				for block in normalColors:
					if block == level.blockAt(x, y, z):
						level.setBlockAt(x, y, z, normalBlock)
						level.setBlockDataAt(x, y, z, 0)

						replaced = True

						break

				if replaced == False:
					for block in stainedColors:
						if block == level.blockAt(x, y, z):
							level.setBlockAt(x, y, z, stainedBlock)
							level.setBlockDataAt(x, y, z, stainedColors[block])

							replaced = True

							break

				if replaced == False and options["Delete Blocks that can't be replaced"]:
					level.setBlockAt(x, y, z, 0)
					level.setBlockDataAt(x, y, z, 0)

	level.markDirtyBox(box)
