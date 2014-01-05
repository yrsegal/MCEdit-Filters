#### Convert Rainbow Blocks ####
# Filter for MCEdit by destruc7i0n
# http://youtube.com/TheDestruc7i0n

displayName = "Convert Rainbow Blocks"

Blocks = {
	"Wool": 0,
	"Clay": 1,
	"Carpet": 2,
	"Glass": 3,
	"Pane": 4,
}
        
inputs = (
	("Find:", ("Wool", "Clay", "Carpet", "Glass", "Pane")),
	("Convert to:", ("Wool", "Clay", "Carpet", "Glass", "Pane")),
)

def perform(level, box, options):
	f = options["Find:"]
	c = options["Convert to:"]
	
	for x in xrange(box.minx, box.maxx):
		for z in xrange(box.minz, box.maxz):
			for y in xrange(box.miny, box.maxy):

				if f == "Wool" and level.blockAt(x, y, z) == 35:
					if c == "Clay":
						level.setBlockAt(x, y, z, 159)

					if c == "Carpet":
						level.setBlockAt(x, y, z, 171)

					if c == "Glass":
						level.setBlockAt(x, y, z, 95)

					if c == "Pane":
						level.setBlockAt(x, y, z, 160)

				if f == "Clay" and level.blockAt(x, y, z) == 159:
					if c == "Wool":
						level.setBlockAt(x, y, z, 35)

					if c == "Carpet":
						level.setBlockAt(x, y, z, 171)

					if c == "Glass":
						level.setBlockAt(x, y, z, 95)

					if c == "Pane":
						level.setBlockAt(x, y, z, 160)

				if f == "Carpet" and level.blockAt(x, y, z) == 171:
					if c == "Wool":
						level.setBlockAt(x, y, z, 35)

					if c == "Clay":
						level.setBlockAt(x, y, z, 159)

					if c == "Glass":
						level.setBlockAt(x, y, z, 95)

					if c == "Pane":
						level.setBlockAt(x, y, z, 160)

				if f == "Glass" and level.blockAt(x, y, z) == 95:
					if c == "Wool":
						level.setBlockAt(x, y, z, 35)

					if c == "Clay":
						level.setBlockAt(x, y, z, 159)

					if c == "Carpet":
						level.setBlockAt(x, y, z, 171)

					if c == "Pane":
						level.setBlockAt(x, y, z, 160)   

				if f == "Pane" and level.blockAt(x, y, z) == 160:
					if c == "Wool":
						level.setBlockAt(x, y, z, 35)

					if c == "Clay":
						level.setBlockAt(x, y, z, 159)

					if c == "Carpet":
						level.setBlockAt(x, y, z, 171)

					if c == "Glass":
						level.setBlockAt(x, y, z, 95)

	level.markDirtyBox(box)
