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
from pymclevel.nbt import *

displayName = 'Change Horses In MCEdit'
inputs = [
	(	
		("Horse Type To Change", ("Normal Horse","Donkey Horse", "Mule Horse", "Zombie Horse", "Skeleton Horse")),
		("Changing Horses won't apply Saddles, Horse Armor, or Donkey Chests.", "label"),
		("You may not be able to apply these after changement, so tame and apply first.", "label"),
		("Main", "title"),
	),
	
	(
		("Bred: ", ("Yes", "No")),
		("Chested: ", ("Yes", "No")),
		("Reproduced: ", ("Yes", "No")),
		("Tamed: ", ("Yes", "No")),
		("Temper Value: ", 0,0,100),
		("Owner Name: ", "string"),
		("Saddle: ", ("Yes", "No")),
		("Extra Options", "title"),
	),
]
	
def perform(level, box, options):
    
    horsetype = options["Horse Type To Change"]
        
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