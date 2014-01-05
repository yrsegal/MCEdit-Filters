#### Tiny Structure Spawner ####
# Filter for MCEdit by CrushedPixel, modified by jgierer12
# http://www.youtube.com/user/CrushedPixel

from pymclevel import TAG_List
from pymclevel import TAG_Byte
from pymclevel import TAG_Int
from pymclevel import TAG_Compound
from pymclevel import TAG_Short
from pymclevel import TAG_Double
from pymclevel import TAG_Float
from pymclevel import TAG_String
from pymclevel import TAG_Long
from pymclevel import TAG_Int_Array
 
displayName = "Tiny Structure Spawner"
 
inputs = (
        ("Spawner's Relative Position:", "label"),
        ("dx", 0),
        ("dy", 10),
        ("dz", 0),
        ("Spawn Entities",True),
        ("Create Spawner", True),
        ("Create Deleter", True),
        ("Include Air Blocks", False),
)
 
def perform(level,box,options):
        dx = options["dx"]
        dy = options["dy"]
        dz = options["dz"]
        cr = options["Create Spawner"]
        cd = options["Create Deleter"]
        iab = options["Include Air Blocks"]
       
        if dx == 0:
                rsx = (box.maxx + box.minx) / 2
        if dy == 0:
                rsy = (box.maxy + box.miny) / 2
        if dz == 0:
                rsz = (box.maxz + box.minz) / 2
               
        if dx < 0:
                rsx = box.minx + dx - 5
        if dy < 0:
                rsy = box.miny + dy - 2
        if dz < 0:
                rsz = box.minz + dz - 5
       
        if dx > 0:
                rsx = box.maxx + dx + 5
        if dy > 0:
                rsy = box.maxy + dy + 5
        if dz > 0:
                rsz = box.maxz + dz + 2
       
        if cr:
                createStructure(rsx,rsy,rsz,level,1)
       
        if cd:
                createStructure(rsx-3,rsy,rsz,level,0)

        minecartCount = 0       
        for x in xrange(box.minx,box.maxx):
                for y in xrange(box.miny,box.maxy):
                        for z in xrange(box.minz,box.maxz):
                                id = level.blockAt(x,y,z)
                                data = level.blockDataAt(x,y,z)
                                te = level.tileEntityAt(x,y,z)
                               
                                if x < 0:
                                        blockx = x-1
                                else:
                                        blockx = x
                                       
                                if z < 0:
                                        blockz = z
                                else:
                                        blockz = z+1
                               
                                if id != 1000 and iab == True:
                                        if cr:
                                                minecartCount = createCartBlock(rsx,rsy-1,rsz-3,level,1,blockx,y,blockz-1,id,data,te,minecartCount) #Create-Mode
                                        if cd:
                                                minecartCount = createCartBlock(rsx-3,rsy-1,rsz-3,level,0,blockx,y,blockz-1,id,data,te,minecartCount) #Destroy-Mode
 
                                if id != 0 and iab == False:
                                        if cr:
                                                minecartCount = createCartBlock(rsx,rsy-1,rsz-3,level,1,blockx,y,blockz-1,id,data,te,minecartCount) #Create-Mode
                                        if cd:
                                                minecartCount = createCartBlock(rsx-3,rsy-1,rsz-3,level,0,blockx,y,blockz-1,id,data,te,minecartCount) #Destroy-Mode
                                               
        if options["Spawn Entities"]:
                for (chunk, slices, point) in level.getChunkSlices(box):       
                        for entity in chunk.Entities:
                                x = int(entity["Pos"][0].value-0.5)
                                y = int(entity["Pos"][1].value)
                                z = int(entity["Pos"][2].value-0.5)
                               
                                if x >= box.minx and x < box.maxx and y >= box.miny and y < box.maxy and z >= box.minz and z < box.maxz:
                                        ent = str(entity)
                                        ent = CleanTAG(ent)            
                                        minecartCount = createCartEntity(rsx,rsy-1,rsz-3,level,entity["Pos"][0].value, entity["Pos"][1].value, entity["Pos"][2].value, entity["id"].value, ent, minecartCount)
               
               
                                               
def CleanTAG(te):
        tileEntity = te
       
        while '  ' in tileEntity:
                tileEntity = tileEntity.replace('  ', ' ')
       
        tileEntity = tileEntity.replace("\"", '')
        tileEntity = tileEntity.replace("(", '')
        tileEntity = tileEntity.replace(")", '')
        tileEntity = tileEntity.replace("TAG_List", '')
        tileEntity = tileEntity.replace("TAG_Byte", '')
        tileEntity = tileEntity.replace("TAG_Short", '')
        tileEntity = tileEntity.replace("TAG_Int", '')
        tileEntity = tileEntity.replace("TAG_Long", '')
        tileEntity = tileEntity.replace("TAG_Float", '')
        tileEntity = tileEntity.replace("TAG_Double", '')
        tileEntity = tileEntity.replace("TAG_String", '')
        tileEntity = tileEntity.replace("TAG_Byte_Array", '')
        tileEntity = tileEntity.replace("TAG_Int_Array", '')
        tileEntity = tileEntity.replace("TAG_Compound", '')
        tileEntity = tileEntity.replace("u'", '')
        tileEntity = tileEntity.replace("'", '')
        tileEntity = tileEntity.replace("\n", '')
        tileEntity = tileEntity.replace("{ ", '{')
        tileEntity = tileEntity.replace("[ ", '[')
        tileEntity = tileEntity.replace(", ", ',')
        tileEntity = tileEntity.replace(",}", '}')
        tileEntity = tileEntity.replace(",]", ']')
       
        return tileEntity

def createSlime(cartx,carty,cartz,chunk):
        slime = TAG_Compound()

        slime["Size"] = TAG_Int(-3)
        slime["Invulnerable"] = TAG_Byte(1)

        slime["UUIDLeast"] = TAG_Long(-7988352983206307739)
        motion = TAG_List()
        motion.append(TAG_Double(0.0))
        motion.append(TAG_Double(-0.0))
        motion.append(TAG_Double(0.0))
        slime["Motion"] = motion
        slime["CustomName"] = TAG_String(u'12')
        slime["OnGround"] = TAG_Byte(0)
        slime["UUIDMost"] = TAG_Long(1404135178162750390)
        slime["Dimension"] = TAG_Int(0)
        slime["Air"] = TAG_Short(300)
        slime["id"] = TAG_String(u'Slime')
        pos = TAG_List()
        pos.append(TAG_Double(cartx+0.5))
        pos.append(TAG_Double(carty+0.5))
        pos.append(TAG_Double(cartz+0.5))
        slime["Pos"] = pos
        slime["PortalCooldown"] = TAG_Int(0)
        slime["Fire"] = TAG_Short(-1)
        slime["FallDistance"] = TAG_Float(0.0)
        rotation = TAG_List()
        rotation.append(TAG_Float(0.0))
        rotation.append(TAG_Float(0.0))
        slime["Rotation"] = rotation

        chunk.Entities.append(slime)
 
def createCartEntity(cartx,carty,cartz,level,ex,ey,ez,eid,e,minecartCount):
        if e != None:
                e = str(e)
                e = CleanTAG(e)
        else:
                e = ''
       
        minecartCommandBlock = TAG_Compound()
       
        minecartCommandBlock["Command"] = TAG_String(u'/summon '+str(eid)+' '+str(ex)+' '+str(ey)+' '+str(ez)+' '+e)
       
        minecartCommandBlock["UUIDLeast"] = TAG_Long(-7988352983206307739)
        minecartCommandBlock["TrackOutput"] = TAG_Byte(1)
        motion = TAG_List()
        motion.append(TAG_Double(0.0))
        motion.append(TAG_Double(-0.0))
        motion.append(TAG_Double(0.0))
        minecartCommandBlock["Motion"] = motion
        minecartCommandBlock["CustomName"] = TAG_String(u'CP')
        minecartCommandBlock["OnGround"] = TAG_Byte(0)
        minecartCommandBlock["UUIDMost"] = TAG_Long(1404135178162750390)
        minecartCommandBlock["Dimension"] = TAG_Int(0)
        minecartCommandBlock["Air"] = TAG_Short(300)
        minecartCommandBlock["id"] = TAG_String(u'MinecartCommandBlock')
        pos = TAG_List()
        pos.append(TAG_Double(cartx+0.5))
        pos.append(TAG_Double(carty+0.5))
        pos.append(TAG_Double(cartz+0.5))
        minecartCommandBlock["Pos"] = pos
        minecartCommandBlock["PortalCooldown"] = TAG_Int(0)
        minecartCommandBlock["Fire"] = TAG_Short(-1)
        minecartCommandBlock["SuccessCount"] = TAG_Int(1)
        minecartCommandBlock["FallDistance"] = TAG_Float(0.0)
        rotation = TAG_List()
        rotation.append(TAG_Float(0.0))
        rotation.append(TAG_Float(0.0))
        minecartCommandBlock["Rotation"] = rotation
        minecartCommandBlock["Invulnerable"] = TAG_Byte(0)
 
        chunk = level.getChunk(cartx/16,cartz/16)
        chunk.Entities.append(minecartCommandBlock)

        if minecartCount == 19:
                createSlime(cartx,carty,cartz,chunk)

                minecartCount = 0

        else:
                minecartCount += 1

        chunk.dirty = True

        return minecartCount
       
def createCartBlock(cartx,carty,cartz,level,mode,blockx,blocky,blockz,id,data,te,minecartCount):
        if te != None:
                te = str(te)
                te = CleanTAG(te)
        else:
                te = ''
       
        minecartCommandBlock = TAG_Compound()
        if mode == 1:
                minecartCommandBlock["Command"] = TAG_String(u'/setblock '+str(blockx)+' '+str(blocky)+' '+str(blockz)+' '+str(id)+' '+str(data)+' replace'+' '+te)
        else:
                minecartCommandBlock["Command"] = TAG_String(u'/setblock '+str(blockx)+' '+str(blocky)+' '+str(blockz)+' 0'+' 0'+' replace')
        minecartCommandBlock["UUIDLeast"] = TAG_Long(-7988352983206307739)
        minecartCommandBlock["TrackOutput"] = TAG_Byte(1)
        motion = TAG_List()
        motion.append(TAG_Double(0.0))
        motion.append(TAG_Double(-0.0))
        motion.append(TAG_Double(0.0))
        minecartCommandBlock["Motion"] = motion
        minecartCommandBlock["CustomName"] = TAG_String(u'CP')
        minecartCommandBlock["OnGround"] = TAG_Byte(0)
        minecartCommandBlock["UUIDMost"] = TAG_Long(1404135178162750390)
        minecartCommandBlock["Dimension"] = TAG_Int(0)
        minecartCommandBlock["Air"] = TAG_Short(300)
        minecartCommandBlock["id"] = TAG_String(u'MinecartCommandBlock')
        pos = TAG_List()
        pos.append(TAG_Double(cartx+0.5))
        pos.append(TAG_Double(carty+0.5))
        pos.append(TAG_Double(cartz+0.5))
        minecartCommandBlock["Pos"] = pos
        minecartCommandBlock["PortalCooldown"] = TAG_Int(0)
        minecartCommandBlock["Fire"] = TAG_Short(-1)
        minecartCommandBlock["SuccessCount"] = TAG_Int(1)
        minecartCommandBlock["FallDistance"] = TAG_Float(0.0)
        rotation = TAG_List()
        rotation.append(TAG_Float(0.0))
        rotation.append(TAG_Float(0.0))
        minecartCommandBlock["Rotation"] = rotation
        minecartCommandBlock["Invulnerable"] = TAG_Byte(0)
 
        chunk = level.getChunk(cartx/16,cartz/16)
        chunk.Entities.append(minecartCommandBlock)

        if minecartCount == 19:
                createSlime(cartx,carty,cartz,chunk)

                minecartCount = 0

        else:
                minecartCount += 1

        chunk.dirty = True

        return minecartCount
       
 
       
def createStructure(rsx,rsy,rsz,level,mode):
        level.setBlockAt(rsx + -1, rsy + -1, rsz + 1, 77)
        level.setBlockDataAt(rsx + -1, rsy + -1, rsz + 1, 2)
       
        chunk = level.getChunk((rsx-1)/16,(rsz+1)/16)
       
        if mode == 1:
                level.setBlockAt(rsx + -1, rsy + 1, rsz + 1, 68)
                level.setBlockDataAt(rsx + -1, rsy + 1, rsz + 1, 4)
                sign = signTileEntity(rsx -1, rsy+1, rsz+1, '==============','Spawn','Structure','==============')
                chunk.TileEntities.append(sign)
        else:
                level.setBlockAt(rsx + -1, rsy + 1, rsz + 1, 68)
                level.setBlockDataAt(rsx + -1, rsy + 1, rsz + 1, 4)
                sign = signTileEntity(rsx -1, rsy+1, rsz+1, '==============','Delete','Structure','==============')
                chunk.TileEntities.append(sign)
               
        level.setBlockAt(rsx + 0, rsy + -2, rsz + -3, 1)
        level.setBlockAt(rsx + 0, rsy + -2, rsz + 0, 1)
        level.setBlockAt(rsx + 0, rsy + -1, rsz + -3, 157)
        level.setBlockAt(rsx + 0, rsy + -1, rsz + -2, 75)
        level.setBlockDataAt(rsx + 0, rsy + -1, rsz + -2, 4)
        level.setBlockAt(rsx + 0, rsy + -1, rsz + -1, 1)
        level.setBlockAt(rsx + 0, rsy + -1, rsz + 0, 93)
        level.setBlockDataAt(rsx + 0, rsy + -1, rsz + 0, 8)
        level.setBlockAt(rsx + 0, rsy + -1, rsz + 1, 1)
        level.setBlockAt(rsx + 0, rsy + 0, rsz + -1, 55)
        level.setBlockDataAt(rsx + 0, rsy + 0, rsz + -1, 14)
        level.setBlockAt(rsx + 0, rsy + 0, rsz + 0, 1)
        level.setBlockAt(rsx + 0, rsy + 0, rsz + 1, 76)
        level.setBlockDataAt(rsx + 0, rsy + 0, rsz + 1, 5)
        level.setBlockAt(rsx + 0, rsy + 1, rsz + 0, 55)
        level.setBlockDataAt(rsx + 0, rsy + 1, rsz + 0, 15)
        level.setBlockAt(rsx + 0, rsy + 1, rsz + 1, 1)
 
def signTileEntity(x, y, z, text1, text2, text3, text4):
        sign = TAG_Compound()
        sign["id"] = TAG_String(u'Sign')
        sign["Text1"] = TAG_String(text1)
        sign["Text2"] = TAG_String(text2)
        sign["Text3"] = TAG_String(text3)
        sign["Text4"] = TAG_String(text4)
        sign["x"] = TAG_Int(x)
        sign["y"] = TAG_Int(y)
        sign["z"] = TAG_Int(z)
 
        return sign