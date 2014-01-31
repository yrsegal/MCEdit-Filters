#### Speech Bubbles ####
# Filter for MCEdit by jgierer12, idea by SimplySarc

from pymclevel.schematic import MCSchematic
import mcplatform

from pymclevel import TAG_Int
from pymclevel import TAG_String
from pymclevel import TAG_Compound
from mceutils import showProgress

displayName = "Speech Bubbles"

inputs = (
    ("Text:", ("string", "value=Text")),
    ("Particles:", ("dripWater", "dripLava")),
    ("Display at:", ("string", "value=@p")),
    ("Distance to Entity:", 2),
    ("Direction:", ("-X -> +X", "+X -> -X", "-Z -> +Z", "+Z -> -Z")),
    ("For information about Emoticons and custom Symbols visit <url>", "label")
)


def perform(level, box, options):
    showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    global GlobalLevel
    GlobalLevel = level

    text = options["Text:"]
    particleType = options["Particles:"]
    entitySelector = options["Display at:"]
    dy = options["Distance to Entity:"]
    direction = options["Direction:"]

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    characters = {
        "A": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0.2), (0.1, 0.4), (0.2, 0.2), (0.2, 0.4), (0.3, 0), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3)], 0.4, 0.5),
        "B": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0.1), (0.3, 0.3)], 0.4, 0.5),
        "C": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.4)], 0.3, 0.5),
        "D": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.4), (0.3, 0.1), (0.3, 0.1), (0.3, 0.3)], 0.4, 0.5),
        "E": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4)], 0.3, 0.5),
        "F": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.1, 0.4), (0.2, 0.2), (0.2, 0.4)], 0.3, 0.5),
        "G": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.1), (0.2, 0.4)], 0.3, 0.5),
        "H": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.2, 0.2), (0.3, 0), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3), (0.3, 0.4)], 0.4, 0.5),
        "I": PGroup([(0, 0), (0, 0.4), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.1, 0.3), (0.1, 0.4), (0.2, 0), (0.2, 0.4)], 0.3, 0.5),
        "J": PGroup([(0, 0.1), (0, 0.4), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.1), (0.2, 0.2), (0.2, 0.3),  (0.2, 0.4)], 0.3, 0.5),
        "K": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.2, 0.1), (0.2, 0.2), (0.3, 0), (0.3, 0.4)], 0.4, 0.5),
        "L": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.2, 0)], 0.3, 0.5),
        "M": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.3), (0.2, 0.2), (0.3, 0.3), (0.4, 0), (0.4, 0.1), (0.4, 0.2), (0.4, 0.3), (0.4, 0.4)], 0.5, 0.5),
        "N": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.3), (0.2, 0.2), (0.3, 0.1), (0.4, 0), (0.4, 0.1), (0.4, 0.2), (0.4, 0.3), (0.4, 0.4)], 0.5, 0.5),
        "O": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.4), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3)], 0.4, 0.5),
        "P": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.1, 0.4), (0.2, 0.2), (0.2, 0.4), (0.3, 0.3)], 0.4, 0.5),
        "Q": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.4), (0.2, 0.1), (0.2, 0.4), (0.3, 0), (0.3, 0.2), (0.3, 0.3)], 0.4, 0.5),
        "R": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.1, 0.4), (0.2, 0.2), (0.2, 0.4), (0.3, 0), (0.3, 0.1), (0.3, 0.3)], 0.4, 0.5),
        "S": PGroup([(0, 0), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.1), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.1), (0.2, 0.2), (0.2, 0.4)], 0.3, 0.5),
        "T": PGroup([(0, 0.4), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.1, 0.3), (0.1, 0.4), (0.2, 0.4)], 0.3, 0.5),
        "U": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.2, 0), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3), (0.3, 0.4)], 0.4, 0.5),
        "V": PGroup([(0, 0.1), (0, 0.3), (0, 0.4), (0.1, 0.1), (0.2, 0), (0.3, 0.1), (0.4, 0.2), (0.4, 0.3), (0.4, 0.4)], 0.5, 0.5),
        "W": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.1), (0.2, 0.2), (0.3, 0.1), (0.4, 0), (0.4, 0.1), (0.4, 0.2), (0.4, 0.3), (0.4, 0.4)], 0.5, 0.5),
        "X": PGroup([(0, 0), (0, 0.4), (0.1, 0.1), (0.1, 0.3), (0.2, 0.2), (0.3, 0.1), (0.3, 0.3), (0.4, 0), (0.4, 0.4)], 0.5, 0.5),
        "Y": PGroup([(0, 0.4), (0.1, 0.3), (0.2, 0), (0.2, 0.1), (0.2, 0.2), (0.3, 0.3), (0.4, 0.4)], 0.5, 0.5),
        "Z": PGroup([(0, 0), (0, 0.1), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0), (0.3, 0.3), (0.3, 0.4)], 0.4, 0.5),

        "a": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.2), (0.2, 0), (0.2, 0.1), (0.2, 0.2)], 0.3, 0.3),
        "b": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.2, 0), (0.2, 0.2), (0.3, 0.1)], 0.4, 0.5),
        "c": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.2), (0.2, 0), (0.2, 0.2)], 0.3, 0.3),
        "d": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.2), (0.2, 0), (0.2, 0.2), (0.3, 0), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3), (0.3, 0.4)], 0.4, 0.5),
        "e": PGroup([(0, 0.1), (0, 0.2), (0.1, 0), (0.1, 0.1), (0.1, 0.3), (0.2, 0), (0.2, 0.2)], 0.3, 0.4),
        "f": PGroup([(0, -0.2), (0, -0.1), (0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.1, 0.4), (0.2, 0.4)], 0.3, 0.5),
        "g": PGroup([(0, 0.1), (0.1, -0.2), (0.1, 0), (0.1, 0.2), (0.2, -0.2), (0.2, -0.1), (0.2, 0), (0.2, 0.1)], 0.3, 0.3),
        "h": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.2), (0.2, 0.2), (0.3, 0), (0.3, 0.1)], 0.4, 0.5),
        "i": PGroup([(0, 0), (0, 0.1), (0, 0.3)], 0.1, 0.4),
        "j": PGroup([(0, -0.2), (0.1, -0.2), (0.1, -0.1), (0.1, 0), (0.1, 0.1), (0.1, 0.3)], 0.2, 0.4),
        "k": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0.1), (0.2, 0), (0.2, 0.2)], 0.3, 0.5),
        "l": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0)], 0.2, 0.5),
        "m": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0.1, 0.2), (0.2, 0), (0.2, 0.1), (0.3, 0.2), (0.4, 0), (0.4, 0.1)], 0.5, 0.3),
        "n": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0.1, 0.2), (0.2, 0), (0.2, 0.1)], 0.3, 0.3),
        "o": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.2), (0.2, 0.1)], 0.3, 0.3),
        "p": PGroup([(0, -0.2), (0, -0.1), (0, 0), (0, 0.1), (0, 0.2), (0.1, 0), (0.1, 0.2), (0.2, 0.1)], 0.3, 0.3),
        "q": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.2), (0.2, -0.2), (0.2, -0.1), (0.2, 0), (0.2, 0.1), (0.2, 0.2)], 0.3, 0.3),
        "r": PGroup([(0, 0), (0, 0.1), (0, 0.2), (0.1, 0.2)], 0.2, 0.3),
        "s": PGroup([(0, 0), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.2, 0.2)], 0.3, 0.3),
        "t": PGroup([(0, 0.2), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.1, 0.3), (0.1, 0.4), (0.2, 0.2)], 0.3, 0.5),
        "u": PGroup([(0, 0.1), (0, 0.2), (0.1, 0), (0.2, 0), (0.2, 0.1), (0.2, 0.2)], 0.3, 0.3),
        "v": PGroup([(0, 0.1), (0, 0.2), (0.1, 0), (0.2, 0.1), (0.2, 0.2)], 0.3, 0.3),
        "w": PGroup([(0, 0.1), (0, 0.2), (0.1, 0), (0.2, 0.1), (0.3, 0), (0.4, 0.1), (0.4, 0.2)], 0.5, 0.3),
        "x": PGroup([(0, 0), (0, 0.2), (0.1, 0.1), (0.2, 0), (0.2, 0.2)], 0.3, 0.3),
        "y": PGroup([(0, 0.1), (0, 0.2), (0.1, -0.2), (0.1, 0), (0.2, -0.2), (0.2, -0.1), (0.2, 0), (0.2, 0.1), (0.2, 0.2)], 0.3, 0.3),
        "z": PGroup([(0, 0.2), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.2, 0)], 0.3, 0.3),

        "0": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0), (0.3, 0.4), (0.4, 0.1), (0.4, 0.2), (0.4, 0.3)], 0.5, 0.5),
        "1": PGroup([(0, 0), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.1), (0.1, 0.2), (0.1, 0.3), (0.1, 0.4), (0.2, 0), (0.2, 0.4)], 0.3, 0.5),
        "2": PGroup([(0, 0), (0, 0.1), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.3)], 0.3, 0.5),
        "3": PGroup([(0, 0), (0, 0.2), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0.1), (0.2, 0.3)], 0.3, 0.5),
        "4": PGroup([(0, 0.2), (0.1, 0.1), (0.1, 0.3), (0.2, 0.1), (0.2, 0.4), (0.3, 0), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3)], 0.4, 0.5),
        "5": PGroup([(0, 0), (0, 0.2), (0, 0.3), (0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0.1), (0.2, 0.4)], 0.3, 0.5),
        "6": PGroup([(0, 0.1), (0, 0.2), (0, 0.3), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0.1)], 0.4, 0.5),
        "7": PGroup([(0, 0), (0, 0.1), (0, 0.4), (0.1, 0.2), (0.1, 0.4), (0.2, 0.3), (0.2, 0.4)], 0.3, 0.5),
        "8": PGroup([(0, 0.1), (0, 0.3), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0.1), (0.3, 0.3)], 0.4, 0.5),
        "9": PGroup([(0, 0.3), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0), (0.2, 0.2), (0.2, 0.4), (0.3, 0.1), (0.3, 0.2), (0.3, 0.3)], 0.4, 0.5),

        ".": PGroup([(0, 0)], 0.1, 0.1),
        ",": PGroup([(0, -0.1), (0, 0)], 0.1, 0.1),
        ":": PGroup([(0, 0), (0, 0.2)], 0.1, 0.3),
        "!": PGroup([(0, 0), (0, 0.2), (0, 0.3), (0, 0.4)], 0.1, 0.3),
        "?": PGroup([(0, 0.4), (0.1, 0), (0.1, 0.2), (0.1, 0.4), (0.2, 0.2), (0.2, 0.3), (0.2, 0.4)], 0.3, 0.5),

        "_": PGroup([(0, 0), (0.1, 0), (0.2, 0)], 0.3, 0.1)
    }

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    customSymbols = {
        ":)": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.3, 0), (0.4, 0), (0.4, 0.4), (0.5, 0.1)], 0.6, 0.5),
        ":(": PGroup([(0, 0), (0.1, 0.1), (0.1, 0.4), (0.2, 0.1), (0.3, 0.1), (0.4, 0.1), (0.4, 0.4), (0.5, 0)], 0.6, 0.5),
        ":|": PGroup([(0, 0.1), (0.1, 0.1), (0.1, 0.4), (0.2, 0.1), (0.3, 0.1), (0.4, 0.1), (0.4, 0.4), (0.5, 0.1)], 0.6, 0.5),
        ":D": PGroup([(0, 0.1), (0, 0.2), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.3, 0), (0.4, 0), (0.4, 0.4), (0.5, 0.1), (0.5, 0.2)], 0.6, 0.5),
        ";)": PGroup([(0, 0.1), (0.1, 0), (0.1, 0.4), (0.2, 0), (0.2, 0.4), (0.3, 0), (0.4, 0), (0.4, 0.4), (0.5, 0.1)], 0.6, 0.5),
    }

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    width = 0.0
    word = ""
    particles = []

    i = 0
    for letter in text:
        i += 1

        if letter != " ":
            word += letter

        if letter == " " or i == len(text):
            try:
                pGroupSymbol = customSymbols[word]
                for particle in pGroupSymbol.particles:
                    particles.append((particle[0] + width, particle[1]))
                width += pGroupSymbol.totalWidth + 0.2

            except:
                for character in word:
                    try:
                        pGroupCharacter = characters[character]
                        for particle in pGroupCharacter.particles:
                            particles.append((particle[0] + width, particle[1]))
                        width += pGroupCharacter.totalWidth + 0.1

                    except:
                        pGroupUnknown = characters["_"]
                        for particle in pGroupUnknown.particles:
                            particles.append((particle[0] + width, particle[1]))
                        width += pGroupUnknown.totalWidth + 0.1
            word = ""

            if letter == " ":
                width += 0.4

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    commands = []
    textStart = 0.0 - width/2

    for particlePosition in particles:
        if direction == "-X -> +X":
            command = "/particle " + particleType + " ~" + str(textStart + particlePosition[0]) + " ~" + str(dy + particlePosition[1]) + " ~ 0 0 0 0 10 " + entitySelector

        elif direction == "+X -> -X":
            command = "/particle " + particleType + " ~" + str(-1*(textStart + particlePosition[0])) + " ~" + str(dy + particlePosition[1]) + " ~ 0 0 0 0 10 " + entitySelector

        elif direction == "-Z -> +Z":
            command = "/particle " + particleType + " ~ ~" + str(dy + particlePosition[1]) + " ~" + str(textStart + particlePosition[0]) + " 0 0 0 0 10 " + entitySelector

        elif direction == "+Z -> -Z":
            command = "/particle " + particleType + " ~ ~" + str(dy + particlePosition[1]) + " ~" + str(-1*(textStart + particlePosition[0])) + " 0 0 0 0 10 " + entitySelector

        commands.append(command)

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    if len(commands) > 15:
        totalZ = 15
        totalX = int(len(commands)/15) + 1
    else:
        totalZ = len(commands)
        totalX = 1

    schematic = MCSchematic((totalX, 2, totalZ))

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    x = 0
    z = 0
    for command in commands:
        schematic.TileEntities.append(AddCommandBlock(schematic, x, 0, z, command))
        schematic.setBlockAt(x, 0, z, 137)
        schematic.setBlockAt(x, 1, z, 55)

        if z < 14:
            z += 1
        else:
            x += 1
            z = 0

    #showProgress("SpeechBubbles Filter", progressIterator(), cancel=True)
    schematicFile = mcplatform.askSaveFile(mcplatform.lastSchematicsDir or mcplatform.schematicsDir, "Save Schematic As...", "", "Schematic\0*.schematic\0\0", ".schematic")
    schematic.saveToFile(schematicFile)


class PGroup:
    def __init__(self, particles, totalWidth, totalHeigth):
        self.particles = particles
        self.totalWidth = totalWidth


def AddCommandBlock(schematic, x, y, z, command):
    control = TAG_Compound()
    control["Command"] = TAG_String(command)
    control["id"] = TAG_String(u'Control')
    control["CustomName"] = TAG_String(u'@')
    control["SuccessCount"] = TAG_Int(0)
    control["x"] = TAG_Int(x)
    control["y"] = TAG_Int(y)
    control["z"] = TAG_Int(z)
    return control


def progressIterator():
    # yield (0.0, "Defining variables")
    # yield (0.1, "Defining models for characters")
    # yield (0.3, "Defining models for custom symbols")
    # yield (0.4, "Converting text to particles")
    # yield (0.6, "Creating commands")
    # yield (0.7, "Defining schematic")
    # yield (0.8, "Creating Command Blocks")
    # yield (0.9, "Saving schematic")

    yield "Defining variables"
    yield "Defining models for characters"
    yield "Defining models for custom symbols"
    yield "Converting text to particles"
    yield "Creating commands"
    yield "Defining schematic"
    yield "Creating Command Blocks"
    yield "Saving schematic"
