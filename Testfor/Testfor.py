#### Testfor ####
# Filter for MCEdit by jgierer12
# Some parts taken from WumpaCraft's TestForBlockRange Filter: http://www.youtube.com/watch?v=X_bbtMerur0

# -*- coding: utf-8 -*-

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
from pymclevel import MCSchematic
import mcplatform
import pymclevel
from pymclevel import TileEntity

displayName = "Testfor"

inputs = (
    ("For use in Snapshot 14w02a and newer", False),
    ("/testforblock", True),
    ("/testfor", False),
    ("Delete Block After Placement", False),
    ("Output Command", False),
    ("Output Command, pre co-ords:", "string"),
    ("Output Command, post co-ords:", "string"),
    ("To make the command have nothing before/after the co-ords, type 'n/a'", "label"),
)

########## Fast data access ##########
from pymclevel import ChunkNotPresent
GlobalChunkCache = {}
GlobalLevel = None


def getChunk(x, z):
    global GlobalChunkCache
    global GlobalLevel
    chunkCoords = (x >> 4, z >> 4)
    if chunkCoords not in GlobalChunkCache:
        try:
            GlobalChunkCache[chunkCoords] = GlobalLevel.getChunk(x >> 4, z >> 4)
        except ChunkNotPresent:
            return None

    return GlobalChunkCache[chunkCoords]


def blockAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.Blocks[x % 16][z % 16][y]


def dataAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.Data[x % 16][z % 16][y]


def tileEntityAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.tileEntityAt(x, y, z)


def setBlockAt(x, y, z, block):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    chunk.Blocks[x % 16][z % 16][y] = block


def setDataAt(x, y, z, data):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    chunk.Data[x % 16][z % 16][y] = data


def markDirty((minx, maxx), (minz, maxz)):
    for x in xrange(minx, maxx):
        for z in xrange(minz, maxz):
            chunk = getChunk(x, z)
            if chunk is None:
                return 0
            chunk.dirty = True

########## End fast data access ##########


def perform(level, box, options):
    global GlobalLevel
    GlobalLevel = level

    doTestforblock = options["/testforblock"]
    doTestfor = options["/testfor"]
    useSnapshot = options["For use in Snapshot 14w02a and newer"]
    delete = options["Delete Block After Placement"]
    output = options["Output Command"]
    outputPre = options["Output Command, pre co-ords:"]

    if outputPre[-1] == " ":
        outputPre = outputPre[:-1]
    if outputPre.lower() == "n/a":
        outputPre = ""

    outputPost = options["Output Command, post co-ords:"]

    if outputPost[0] == " ":
        outputPost = outputPost[1:]
    if outputPost.lower() == "n/a":
        outputPost = ""

    if doTestforblock is False and doTestfor is False:
        raise Exception("Please select at least one option!")

    rsx = 0
    rsy = 1
    rsz = 0

    count = 0
    height = 0

    testforBlocksEntities = []

    if doTestforblock:
        for x in xrange(box.minx, box.maxx):
            for y in xrange(box.miny, box.maxy):
                for z in xrange(box.minz, box.maxz):
                    if blockAt(x, y, z) != 0:
                        testforBlocksEntities.append((((x, y, z), blockAt(x, y, z), dataAt(x, y, z), tileEntityAt(x, y, z)), True))

    if doTestfor:
        for (chunk, slices, point) in level.getChunkSlices(box):
            for ent in chunk.Entities:
                x = int(ent["Pos"][0].value-0.5)
                y = int(ent["Pos"][1].value)
                z = int(ent["Pos"][2].value-0.5)

                if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
                    testforBlocksEntities.append((((x, y, z), ent), False))

    if testforBlocksEntities == []:
        raise Exception("The selection is empty!")

    if useSnapshot is False and doTestfor:
        raise Exception("/testfor won't work with Entities in your version of Minecraft. Please switch to Snapshot 14w02a or newer or disable the /testfor option!")

    testblocktotal = len(testforBlocksEntities)

    #Get X Dimension
    if testblocktotal >= 15:
        schemX = 15
    else:
        schemX = testblocktotal

    #Get Y Dimension
    if testblocktotal >= 90:
        schemY = 18
    else:
        schemY = ((((testblocktotal-1)//15)+1)*3)

    #Get Z Dimension
    schemZ = (((((testblocktotal-1)//90)+1)*6)-1)

    newSchematic = pymclevel.MCSchematic((schemX, schemY, schemZ))

    for (entity, isBlock) in testforBlocksEntities:
        newSchematic.setBlockAt(rsx, rsy, rsz, 137)
####go from here using newSchematic
        CmdBlock = TileEntity.Create("Control")
        TileEntity.setpos(CmdBlock, (rsx, rsy, rsz))

        bx = entity[0][0]
        by = entity[0][1]
        bz = entity[0][2]

        if isBlock:
            cmd = "/testforblock " + str(bx) + " " + str(by) + " " + str(bz) + " " + str(entity[1]) + " " + str(entity[2]) + " " + str(tagCodeTestfor(entity[3]))

        else:
            cmd = "/testfor @e " + str(tagCodeTestfor(entity[1]))

        cmd = cmd[:len(cmd)-1]
        CmdBlock["Command"] = TAG_String(cmd)

        newSchematic.TileEntities.append(CmdBlock)

        newSchematic.setBlockAt(rsx, rsy+1, rsz, 55)
        newSchematic.setBlockAt(rsx, rsy-1, rsz+1, 42)
        newSchematic.setBlockAt(rsx, rsy, rsz+1, 149)
        newSchematic.setBlockDataAt(rsx, rsy, rsz+1, 2)
        newSchematic.setBlockAt(rsx, rsy-1, rsz+2, 42)
        newSchematic.setBlockAt(rsx, rsy, rsz+2, 93)
        newSchematic.setBlockDataAt(rsx, rsy, rsz+2, 2)
        newSchematic.setBlockAt(rsx, rsy, rsz+3, 42)

        if output is False:
            newSchematic.setBlockAt(rsx, rsy+1, rsz+3, 55)

            if delete is True:
                newSchematic.setBlockAt(rsx, rsy+1, rsz+3, 137)

                CmdBlock = TileEntity.Create("Control")
                TileEntity.setpos(CmdBlock, (rsx, rsy+1, rsz+3))
                cmd = "setblock " + str(bx) + " " + str(by) + " " + str(bz) + " 0 0 replace"
                CmdBlock["Command"] = TAG_String(cmd)

                newSchematic.TileEntities.append(CmdBlock)

        if output is True:
            newSchematic.setBlockAt(rsx, rsy+1, rsz+3, 137)

            CmdBlock = TileEntity.Create("Control")
            TileEntity.setpos(CmdBlock, (rsx, rsy+1, rsz+3))
            cmd = outputPre + " " + str(bx) + " " + str(by) + " " + str(bz) + " " + outputPost
            CmdBlock["Command"] = TAG_String(cmd)

            newSchematic.TileEntities.append(CmdBlock)

            if delete is True:
                newSchematic.setBlockAt(rsx, rsy, rsz+4, 137)

                CmdBlock = TileEntity.Create("Control")
                TileEntity.setpos(CmdBlock, (rsx, rsy, rsz+4))
                cmd = "setblock " + str(bx) + " " + str(by) + " " + str(bz) + " 0 0 replace"
                CmdBlock["Command"] = TAG_String(cmd)

                newSchematic.TileEntities.append(CmdBlock)

        if count >= 14:
            rsy += 3
            rsx -= 14
            count = 0
            height +=1

            if height >= 6:
                rsy -= 18
                rsz += 6
                height = 0
        else:
            rsx += 1
            count += 1

    schematicFile = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
    newSchematic.saveToFile(schematicFile)


def tagCodeTestfor(nbt):
    if nbt is None:
        return None

    if type(nbt) is TAG_Compound:
        tags = []
        for subTag in nbt.value:
            tags.append(tagCodeTestfor(subTag))

        if nbt.name:
            return nbt.name+":{"+"".join(tags)+"},"

        else:
            return "{"+"".join(tags)+"},"

    elif type(nbt) is TAG_List:
        tags = []
        for subTag in nbt.value:
            tags.append(tagCodeTestfor(subTag))

        if nbt.name:
            return nbt.name+":["+"".join(tags)+"],"

        else:
            return "["+"".join(tags)+"],"

    elif type(nbt) is TAG_Byte:
        return nbt.name+":"+str(nbt.value)+"b,"

    elif type(nbt) is TAG_Short:
        return nbt.name+":"+str(nbt.value)+"s,"

    elif type(nbt) is TAG_Long:
        return nbt.name+":"+str(nbt.value)+"l,"

    elif type(nbt) is TAG_Double:
        return nbt.name+":"+str(nbt.value)+"d,"

    else:
        if nbt.name:
            return nbt.name+":"+str(nbt.value)+","

        else:
            return str(nbt.value)+","
