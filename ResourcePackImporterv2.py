import os
import json
import sys
import glob
from shutil import copy


def isEven(x):
    even = (x % 2 == 0)
    if even:
        return True
    else:
        return False

def init(namespace):
    modelsPath = os.path.join(namespace, "models")
    texturesPath = os.path.join(namespace, "textures")
    modelsItemPath = os.path.join(modelsPath, "item")
    modelsBlockPath = os.path.join(modelsPath, "block")
    texturesItemPath = os.path.join(texturesPath, "item")
    texturesBlockPath = os.path.join(texturesPath, "block")
    texturesHatPath = os.path.join(texturesItemPath, "hats")
    texturesHandheldPath = os.path.join(texturesItemPath, "handheld")
    modelsHatPath = os.path.join(modelsItemPath, "hats")
    modelsHandheldPath = os.path.join(modelsItemPath, "handheld")
    
    if not os.path.exists(namespace):
        os.mkdir(namespace)

    if not os.path.exists(modelsPath):
        os.mkdir(modelsPath)

    if not os.path.exists(texturesPath):
        os.mkdir(texturesPath)
    
    if not os.path.exists(modelsItemPath):
        os.mkdir(modelsItemPath)

    if not os.path.exists(modelsBlockPath):
        os.mkdir(modelsBlockPath)

    if not os.path.exists(texturesItemPath):
        os.mkdir(texturesItemPath)

    if not os.path.exists(texturesBlockPath):
        os.mkdir(texturesBlockPath)

    if not os.path.exists(texturesHatPath):
        os.mkdir(texturesHatPath)

    if not os.path.exists(texturesHandheldPath):
        os.mkdir(texturesHandheldPath)

    if not os.path.exists(modelsHatPath):
        os.mkdir(modelsHatPath)

    if not os.path.exists(modelsHandheldPath):
        os.mkdir(modelsHandheldPath)

    if not os.path.exists("items.yml"):
        open('items.yml', 'a').close()

def parseJSON(filePath):
    with open(filePath, "r") as file:
        modelData = json.loads(file.read()) # DICT

        textures = json.dumps(modelData["textures"]) # TEXTURES STR

#        print(textures)
        
        textureKeys = []
        texturePaths = []
        temp = ""
        i = -1
        for char in textures:
            if char == '"':
                i+=1
                if not isEven(i):
                    id = i%4
                    if id == 1:
                        textureKeys.append(temp)
                    else:
                        texturePaths.append(temp)
                    temp = ""
            elif isEven(i):
                temp += char

        file.close()
        return textureKeys, texturePaths, modelData

def findModelPath(file):
    fileSearch = "models/**/" + file
    for modelPath in glob.glob(fileSearch, recursive=True):
        return modelPath

def grabInput(namespace):
    jsonFile = input("Enter model's json file: ")
    modelPath = findModelPath(jsonFile)
    if modelPath=="None":
        return False, "", "", "", "", ""
    
    block = input("Is " + jsonFile + " a block or item model? \n0 for item\n1 for block\n")
    isBlock = "block" if block=="1" else "item"

    isHat = ""
    if isBlock=="item":
        hat = input("Is " + jsonFile + " handheld or a hat? \n0 for handheld\n1 for hat\n")
        isHat = "hats" if hat=="1" else "handheld"

    pasteTextureLoc = ""
    pasteJSONLoc = ""

    pasteTextureLoc = os.path.join(isBlock, isHat)
    pasteJSONLoc = os.path.join(namespace, "models", isBlock, isHat, jsonFile)
    return True, modelPath, pasteJSONLoc, pasteTextureLoc, isBlock, isHat
    
def copyTextures(texturePaths, textureDir, textureKeys, modelData, textureDir_short, jsonFileName, namespace):
    for i in range(len(texturePaths)):
        temp = texturePaths[i]
        itemName = os.path.basename(temp)
        temp = "textures/" + temp + ".png"

        if(os.path.exists(temp)):
            copy(temp, textureDir)
            modelData["textures"][textureKeys[i]] =  namespace + ":" + os.path.join(textureDir_short, itemName).replace("\\", "/")
            print("Sucessfully copied " + temp)
        else:
            print("ERROR: CANNOT FIND TEXTURE " + temp + " FROM ORIGINAL FILES!")

        temp += ".mcmeta"

        if(os.path.exists(temp)):
            copy(temp, textureDir)
            print("Successfully copied " + temp)
    
    jsonFilePath = textureDir.replace("textures", "models")
    jsonFilePath = os.path.join(jsonFilePath, jsonFileName)
    with open(jsonFilePath, "w") as write_file:
        json.dump(modelData, write_file)
        print("Successfully saved " + jsonFilePath)

def createEntry(filePath, isBlock, isHat, jsonModelPath):
    with open(filePath, "a") as write_file:
        name = input("What would you like to name this item?")
        write_file.write('\n' + "  " + name + ":")
        write_file.write('\n' + "    display_name: display-name-" + name)
        write_file.write('\n' + "    lore:")
        for i in range(5):
            write_file.write('\n' + "    - 'lore-" + str(i+1) + "-" + name + "'")
        write_file.write('\n' + "    permission: animecraft")
        write_file.write('\n' + "    resource:")
        write_file.write('\n' + "      material: PAPER")
        write_file.write('\n' + "      generate: false")
        write_file.write('\n' + "      model_path: " + jsonModelPath[:-5].replace("\\", "/"))
        if isHat=="hats":
            write_file.write('\n' + "    behaviours:")
            write_file.write('\n' + "      hat: true")

        if isBlock=="block":
            write_file.write('\n' + "    specific_properties:")
            write_file.write('\n' + "      block:")
            write_file.write('\n' + "        placed_model:")
            write_file.write('\n' + "          type: REAL_NOTE")
            write_file.write('\n' + "          break_particles_material: PRISMARINE_BRICKS")

def splitall(path): # https://www.oreilly.com/library/view/python-cookbook/0596001673/ch04s16.html
    allparts = []
    while 1:
        parts = os.path.split(path)
        if parts[0] == path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == path: # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            path = parts[0]
            allparts.insert(0, parts[1])

    collect = False
    finalPath = ""
    for i in range(len(allparts)):
        if allparts[i]=="item" or allparts[i]=="block":
            collect = True
        
        if collect:
            finalPath = os.path.join(finalPath, allparts[i])

    return finalPath

namespace = "animecraft"
init(namespace)

running = True
print("Welcome to ItemsAdder Resource Pack Importer v2")


while running:
    valid, modelPath, pasteJSONLoc, pasteTextureLoc, isBlock, isHat = grabInput(namespace)
    if not valid: 
        print("Input invalid!")
        continue

    #print(modelPath)
    print(pasteJSONLoc)
    #print(pasteTextureLoc)

    textureKeys, texturePaths, modelData = parseJSON(modelPath)

    textureDir = os.path.join(namespace, "textures", pasteTextureLoc)
    copyTextures(texturePaths, textureDir, textureKeys, modelData, pasteTextureLoc, os.path.basename(modelPath), namespace)

    jsonModelPath = splitall(pasteJSONLoc)

    createEntry("items.yml", isBlock, isHat, jsonModelPath)

    

    





    


