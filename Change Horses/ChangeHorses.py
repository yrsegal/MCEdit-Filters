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

displayName = 'Change Horses In MCEdit'

inputs = [
    (	
		("Horse Type To Change To", ("Normal Horse","Donkey Horse", "Mule Horse", "Zombie Horse", "Skeleton Horse")),
		("Changing Horses won't apply Saddles, Horse Armor, or Donkey Chests.", "label"),
		("You may not be able to apply these after changement, so tame and apply first.", "label"),
		("Main", "title"),
	),
	
	(
		("Bred: ", False),
		("Chested: ", False),
		("Reproduced: ", False),
		("Tamed: ", False),
		("Use A Temper Value", False),
		("Temper Value: ", (0, 0, 100)),
		("Use Owner Name? ", False),
		("Owner Name: ", "string"),
		("Saddle: ", False),
		("Extra Options", "title"),
	),
]
	
def perform(level, box, options):
    global GlobalLevel
    GlobalLevel = level
    
    horsetype = options["Horse Type To Change To"]
    bred = options["Bred: "]
    chested = options["Chested: "]
    repro = options["Reproduced: "]
    tame = options["Tamed: "]
    tempervalue = options["Temper Value: "]
    tempervalueTF = options["Use A Temper Value"]
    ownernameTF = options["Use Owner Name? "]
    ownername = options["Owner Name: "]
    saddle = options["Saddle: "]
            
    for (chunk, slices, point) in level.getChunkSlices(box):
    	for e in chunk.Entities:
    		x = e['Pos'][0].value
    		y = e['Pos'][1].value
    		z = e['Pos'][2].value
                
    if (x,y,z) in box:
    	if e["id"].value == "EntityHorse" and horsetype == "Normal Horse":
    		e["Type"] = TAG_Int(0)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and horsetype == "Donkey Horse":
    	    e["Type"] = TAG_Int(1)
    	    chunk.dirty = True
    	if e["id"].value == "EntityHorse" and horsetype == "Mule Horse":
    		e["Type"] = TAG_Int(2)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and horsetype == "Zombie Horse":
    		e["Type"] = TAG_Int(3)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and horsetype == "Skeleton Horse":
    		e["Type"] = TAG_Int(4)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and bred == True:
    		e["Bred"] = TAG_Byte(1)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and chested == True:
    		e["ChestedHorse"] = TAG_Byte(1)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and repro == True:
    		e["HasReproduced"] = TAG_Byte(1)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and tame == True:
    		e["Tame"] = TAG_Byte(1)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and tempervalueTF == True:
    		e["Temper"] = TAG_String(tempervalue)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and ownernameTF == True:
    		e["OwnerName"] = TAG_String(ownername)
    		chunk.dirty = True
    	if e["id"].value == "EntityHorse" and saddle == True:
    		e["Saddle"] = TAG_Byte(1)
    		chunk.dirty = True
