#### Create Boss Display/Countdown ####
# Filter for MCEdit by jgierer12

# -*- coding: utf-8 -*-
# Nasty little unicode symbolses

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

displayName = "Create Boss Display/Countdown"

inputs = [
    (
        (u"Instructions", "title"),

        ##### INSTRUCTIONS #####

        (u"Do this BEFORE using the filter:", "label"),
        (u"\u00B7 Back up the world\012\u00B7 Set the gamerule \"mobGriefing\" to false\012\u00B7 Set the gamerule \"doMobLoot\" to false (Not neccessary but recommended to avoid lag)", "label"),
        (u"", "label"),
        (u"Do this AFTER using the filter:", "label"),
        (u"\u00B7 Read the information printed to the MCEdit Console\012\u00B7 Test the device at least once\012\u00B7 After you successfully tested the device you can delete the backup\012\u00B7 Do NOT reset the gamerule(s) to true!!!\012\u00B7 Do NOT delete or move the holding cell!!!", "label"),
        (u"", "label"),
        (u"Step I:", "label"),
        (u"Select an area the Ender Dragon will go. The filter will automatically find the best spot in your selection. The selection should be the center of the area the countdown/display will be viewable from. There must be at least one column of air blocks in the selection that reaches down to the void! All options will be saved here!", "label"),
        (u"", "label"),
        (u"Step II:", "label"),
        (u"Select an area the Redstone will go. It will be generated at the least x, y and z coordinates of the selection.", "label"),
    ),
    (
        (u"Options", "title"),

        ##### OPTIONS #####

        (u"Step:", (u"I", u"II")),
        (u"Type:", (u"Display", u"Countdown")),
        (u"", "label"),
        (u"Display Name:", ("string", u"value=\u00A7c\u00A7lDisplay")),
        (u"Health Bar (in %)", (100, 1, 100)),
        (u"", "label"),
        (u"Start Countdown at:", 5),
        (u"Countdown Name:", ("string", u"value=\u00A7c\u00A7lCountdown")),
        (u"", "label"),
        (u"Print a detailed log of the filter process to the console", False),
    ),
]

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


def tileEntityAt(x, y, z):
    chunk = getChunk(x, z)
    if chunk is None:
        return 0
    return chunk.tileEntityAt(x, y, z)


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

    step = options["Step:"]
    cirquitType = options["Type:"]
    displayName = options["Display Name:"]
    countdownStart = options["Start Countdown at:"]
    countdownName = options["Countdown Name:"]
    detailedLog = options["Print a detailed log of the filter process to the console"]
    healthBar = options["Health Bar (in %)"]

    global bossDisplayCountdownProperties

    printDetailedLog(["~~~~~ Filter Log ~~~~~", "Step: " + step], detailedLog)

    if step == "I":
        printDetailedLog(["Type: " + cirquitType], detailedLog)

        if cirquitType == "Display":
            printDetailedLog(["Display Name: " + displayName], detailedLog)

            typeSpecific = (healthBar, displayName)
        else:
            printDetailedLog(["Countdown Start: " + str(countdownStart), "Countdown Name: " + countdownName], detailedLog)

            typeSpecific = (countdownStart, countdownName)

        printDetailedLog(["Searching for a valid location for the dragon holding cell..."], detailedLog)

        dragonPos = getDragonPos(box, detailedLog)

        printDetailedLog(["Found a valid location for the dragon holding cell: x = " + str(dragonPos[0]) + ", y = " + str(dragonPos[1]-1) + ", z = " + str(dragonPos[2]), "Generating the dragon holding cell..."], detailedLog)

        generateDragonCell(box, dragonPos)

        printDetailedLog(["Successfully generated the dragon holding cell!", "Writing properties to global variable bossDisplayCountdownProperties..."], detailedLog)

        bossDisplayCountdownProperties = (dragonPos, cirquitType, typeSpecific)

        printDetailedLog(["Successfully wrote properties to global variable bossDisplayCountdownProperties!"], detailedLog)

        printInformation(["", "~~~~~ Information ~~~~~", "The filter has successfully generated the dragon holding cell and saved the settings", "Ready for Step II!"])

        printDetailedLog(["", "~~~~~ Filter Log (cont.) ~~~~~", "Done!"], detailedLog)

    elif bossDisplayCountdownProperties is not None:
        generateRedstone(box, bossDisplayCountdownProperties, detailedLog)

        printDetailedLog(["", "~~~~~ Filter Log (cont.) ~~~~~", "Successfully generated the Redstone!", "Deleting global variable bossDisplayCountdownProperties..."], detailedLog)

        bossDisplayCountdownProperties = None

        printDetailedLog(["Successfully deleted global variable bossDisplayCountdownProperties!", "Done!"], detailedLog)

    else:
        printDetailedLog(["Attempted to run Step II before Step I!", "Raising error message..."], detailedLog)

        raise Exception("You have to run Step I first!")


def printDetailedLog(textList, detailedLog):
    if detailedLog:
        for text in textList:
            try:
                print str(text)

            except Exception, e:
                print ""
                print "~~~~~ Error while printing Filter Log ~~~~~"
                print e
                print ""
                print "This error can be ignored, it didn't affect the filter action!"
                print ""
                print "~~~~~ Filter Log (cont.) ~~~~~"


def printInformation(textList):
    for text in textList:
        try:
            print str(text)
        except Exception, e:
            print ""
            print "~~~~~ Error while printing Information ~~~~~"
            print e
            print ""
            print "This error can be ignored, it didn't affect the filter action!"
            print ""
            print "~~~~~ Information (cont.) ~~~~~"


def getDragonPos(box, detailedLog):
    if box.maxy-box.miny < 3:
        printDetailedLog(["Couldn't find a valid location for the dragon holding cell!", "Raising Error message..."], detailedLog)

        raise Exception("The selection must be at least 3 blocks high!")

    valid = []

    for x in xrange(box.minx+1, box.maxx-1):
        for z in xrange(box.minz+1, box.maxz-1):
            airColumn = True

            for y in xrange(0, box.miny):
                print blockAt(x, y, z)
                if blockAt(x, y, z) != 0:
                    airColumn = False
                    break

            if airColumn:
                valid.append((x, z))

    if valid != []:
        return (valid[0][0], box.miny+1, valid[0][1])

    else:
        printDetailedLog(["Couldn't find a valid location for the dragon holding cell!", "Raising Error message..."], detailedLog)

        raise Exception("There must be at least one column of air blocks in the selection that reaches down to the void!")


def generateDragonCell(box, (x, y, z)):
    setBlockAt(x, y-1, z, 7)  # Bedrock
    setBlockAt(x, y, z, 9)  # Water
    setBlockAt(x+1, y, z, 7)  # Bedrock
    setBlockAt(x-1, y, z, 7)  # Bedrock
    setBlockAt(x, y, z+1, 7)  # Bedrock
    setBlockAt(x, y, z-1, 7)  # Bedrock
    setBlockAt(x, y+1, z, 7)  # Bedrock

    setDataAt(x, y-1, z, 0)
    setDataAt(x, y, z, 0)
    setDataAt(x+1, y, z, 0)
    setDataAt(x-1, y, z, 0)
    setDataAt(x, y, z+1, 0)
    setDataAt(x, y, z-1, 0)
    setDataAt(x, y+1, z, 0)

    markDirty((x-1, x+1), (z-1, z+1))


def generateRedstone(box, (dragonPos, cirquitType, typeSpecific), detailedLog):
    if box.maxx-box.minx < 6 or box.maxy-box.miny < 4 or box.maxz-box.minz < 2:
        printDetailedLog(["Redstone won't fit into the selection!", "Raising Error message..."], detailedLog)

        raise Exception("The selection must be bigger!")

    if cirquitType == "Display":
        healthBar = typeSpecific[0]
        name = typeSpecific[1]
        baseHealth = 1.25*(100/float(healthBar))
        healF = 1.25
    else:
        start = typeSpecific[0]
        name = typeSpecific[1]
        baseHealth = 1.25*start
        healF = baseHealth

    dragonX = dragonPos[0]
    dragonY = dragonPos[1]
    dragonZ = dragonPos[2]

    redstoneX = box.minx
    redstoneY = box.miny
    redstoneZ = box.minz

    printDetailedLog(["Generating the Redstone at x = " + str(redstoneX) + ", y = " + str(redstoneY) + ", z = " + str(redstoneZ) + "..."], detailedLog)

    summonDragon = "/summon EnderDragon "+str(dragonX)+" "+str(dragonY)+" "+str(dragonZ)+" {Riding:{id:Minecart,Invulnerable:1},Attributes:[{Name:generic.maxHealth,Base:"+str(baseHealth)+"}],HealF:"+str(healF)+",CustomeNameVisible:1,CustomName:\""+name+"\"}"
    summonTNT = "/summon PrimedTnt "+str(dragonX)+" "+str(dragonY)+" "+str(dragonZ)
    setblockResetAir = "/setblock "+str(dragonX)+" "+str(dragonY-1)+" "+str(dragonZ)+" minecraft:air"
    setblockResetBedrock = "/setblock "+str(dragonX)+" "+str(dragonY-1)+" "+str(dragonZ)+" minecraft:bedrock"

    printDetailedLog(["Commands:", "Summon Dragon: " + summonDragon, "Summon TNT: " + summonTNT, "Set Air (Reset): " + setblockResetAir, "Set Bedrock (Reset): " + setblockResetBedrock, "Generating Blocks..."], detailedLog)

    AddCommandBlock(redstoneX+1, redstoneY+1, redstoneZ, summonTNT)
    AddCommandBlock(redstoneX+3, redstoneY+1, redstoneZ, setblockResetAir)
    AddCommandBlock(redstoneX+5, redstoneY+1, redstoneZ, setblockResetBedrock)
    AddCommandBlock(redstoneX+1, redstoneY+3, redstoneZ, summonDragon)

    setBlockAt(redstoneX+1, redstoneY+1, redstoneZ+1, 77)
    setDataAt(redstoneX+1, redstoneY+1, redstoneZ+1, 3)
    setBlockAt(redstoneX+1, redstoneY+3, redstoneZ+1, 77)
    setDataAt(redstoneX+1, redstoneY+3, redstoneZ+1, 3)

    AddSign(redstoneX, redstoneY+3, redstoneZ, "Wall", "-X", "", "Summon", "Dragon", "")

    setBlockAt(redstoneX+4, redstoneY, redstoneZ, 159)
    setDataAt(redstoneX+4, redstoneY, redstoneZ, 9)
    setBlockAt(redstoneX+4, redstoneY+1, redstoneZ, 93)
    setDataAt(redstoneX+4, redstoneY+1, redstoneZ, 1)

    if cirquitType == "Display":
        AddSign(redstoneX, redstoneY+1, redstoneZ, "Wall", "-X", "", "Reset", "", "")
        setBlockAt(redstoneX+2, redstoneY, redstoneZ, 159)
        setDataAt(redstoneX+2, redstoneY, redstoneZ, 9)
        setBlockAt(redstoneX+2, redstoneY+1, redstoneZ, 55)
        setDataAt(redstoneX+2, redstoneY+1, redstoneZ, 0)

    else:
        AddSign(redstoneX, redstoneY+1, redstoneZ, "Wall", "-X", "", "Decrease", "Counter", "")
        AddSign(redstoneX+2, redstoneY+1, redstoneZ, "Wall", "-X", "", "Reset", "", "")
        AddSign(redstoneX+2, redstoneY, redstoneZ, "Wall", "-X", u"\u00A74\u26A0 \u00A7cOnly", u"\u00A7cacitvate when", u"\u00A7cthe dragon", u"\u00A7cis dead \u00A74\u26A0")
        setBlockAt(redstoneX+3, redstoneY, redstoneZ, 159)
        setDataAt(redstoneX+3, redstoneY, redstoneZ, 9)

    markDirty((redstoneX, redstoneX+5), (redstoneZ, redstoneZ+1))

    printInformation(["", "~~~~~ Information ~~~~~", "The filter successfully generated the redstone. The first time the dragon gets killed a Portal will propably be generated at around x = " + str(dragonX) + ", y = 63, z = " + str(dragonZ) + "."])


def AddCommandBlock(x, y, z, command):
    global GlobalLevel
    level = GlobalLevel
    chunk = level.getChunk(x/16, z/16)
    te = level.tileEntityAt(x, y, z)
    if te is not None:
        chunk.TileEntities.remove(te)
    control = TAG_Compound()
    control["Command"] = TAG_String(command)
    control["id"] = TAG_String(u'Control')
    control["CustomName"] = TAG_String(u'@')
    control["SuccessCount"] = TAG_Int(0)
    control["x"] = TAG_Int(x)
    control["y"] = TAG_Int(y)
    control["z"] = TAG_Int(z)
    chunk.TileEntities.append(control)
    chunk.dirty = True
    level.setBlockAt(x, y, z, 137)
    level.setBlockDataAt(x, y, z, 0)


def AddSign(x, y, z, signType, direction, text1, text2, text3, text4):
    global GlobalLevel
    level = GlobalLevel
    chunk = level.getChunk(x/16, z/16)
    te = level.tileEntityAt(x, y, z)
    if te is not None:
        chunk.TileEntities.remove(te)
    sign = TAG_Compound()
    sign["id"] = TAG_String("Sign")
    sign["Text1"] = TAG_String(text1)
    sign["Text2"] = TAG_String(text2)
    sign["Text3"] = TAG_String(text3)
    sign["Text4"] = TAG_String(text4)
    sign["x"] = TAG_Int(x)
    sign["y"] = TAG_Int(y)
    sign["z"] = TAG_Int(z)
    chunk.TileEntities.append(sign)
    chunk.dirty = True

    if signType == "Wall":
        level.setBlockAt(x, y, z, 68)
        if direction == "+X":
            level.setBlockDataAt(x, y, z, 5)
        elif direction == "-X":
            level.setBlockDataAt(x, y, z, 4)
        elif direction == "+Z":
            level.setBlockDataAt(x, y, z, 3)
        elif direction == "-Z":
            level.setBlockDataAt(x, y, z, 2)
        else:
            level.setBlockAt(x, y, z, 63)
            level.setBlockDataAt(x, y, z, 0)
    else:
        level.setBlockAt(x, y, z, 63)
        level.setBlockDataAt(x, y, z, 0)
