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
        return False, "", "", ""
    
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
    return True, modelPath, pasteJSONLoc, pasteTextureLoc
    
def copyTextures(texturePaths, textureDir, textureKeys, modelData, textureDir_short, jsonFileName):
    for i in range(len(texturePaths)):
        temp = texturePaths[i]
        itemName = os.path.basename(temp)
        temp = "textures/" + temp + ".png"

        if(os.path.exists(temp)):
            copy(temp, textureDir)
            print("Sucessfully copied " + temp)
        else:
            print("ERROR: CANNOT FIND TEXTURE " + temp + " FROM ORIGINAL FILES!")

        temp += ".mcmeta"

        if(os.path.exists(temp)):
            copy(temp, textureDir)
            print("Successfully copied " + temp)

        modelData["textures"][textureKeys[i]] = os.path.join(textureDir_short, itemName).replace("\\", "/")
    
    jsonFilePath = textureDir.replace("textures", "models")
    jsonFilePath = os.path.join(jsonFilePath, jsonFileName)
    with open(jsonFilePath, "w") as write_file:
        json.dump(modelData, write_file)
        print("Successfully saved " + jsonFilePath)
    


namespace = "animecraft"
init(namespace)

running = True
print("Welcome to ItemsAdder Resource Pack Importer v2")


while running:
    valid, modelPath, pasteJSONLoc, pasteTextureLoc = grabInput(namespace)
    if not valid: 
        print("Input invalid!")
        continue

    #print(modelPath)
    #print(pasteJSONLoc)
    #print(pasteTextureLoc)

    textureKeys, texturePaths, modelData = parseJSON(modelPath)

    textureDir = os.path.join(namespace, "textures", pasteTextureLoc)
    copyTextures(texturePaths, textureDir, textureKeys, modelData, pasteTextureLoc, os.path.basename(modelPath))




    


