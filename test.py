#File Objects
import os
import json
import sys
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

def input():
    namespace = "animecraft"
    modelFolder = "models/item/"
    print("Enter model's json file: ")
    modelFile = input()
    print("Is " + modelFile + " a block or item model? \n0 for item\n1 for block\n")
    block = input()
    typePath = "block" if block==1 else "item"
    if not block:
        print("Is " + modelFile + " handheld or a hat? \n0 for handheld\n1 for hat\n")
        hat = input()
        hat_str = "hats" if hat == 1 else "handheld"
        typepath = os.path.join(typepath, hat_str)
    
    return modelFile, typePath

def parseJSON(filePath):
    with open(filePath, "r") as file:
        modelData = json.loads(file.read()) # DICT

        textures = json.dumps(modelData["textures"]) # TEXTURES STR

        print(textures)
        
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
        return textureKeys, texturePaths

def repath(directory, paths):
    for i in len(paths):
        basename = os.path.basename(paths[i])
        paths[i] = directory + basename


namespace = "animecraft"
init(namespace)
modelFolder = "models/item/"
modelFile = input("Enter model's json file: ")
block = input("Is " + modelFile + " a block or item model? \n0 for item\n1 for block\n")
typePath = "block" if block==1 else "item"
filePath = modelFolder + modelFile
print("Searching for ", filePath)
if os.path.exists(filePath) is False:
    print("The file path is invalid!")
    sys.exit()

textureKeys, texturePaths = parseJSON(filePath)
print("Texture Keys: ", textureKeys)
print("Texture Paths: ", texturePaths) # COPY FILE FROM EACH PATH INTO EITHER textures/block or textures/item

texturesDirectory = os.path.join(namespace, "textures", typePath)
print(texturesDirectory)
print(os.listdir(texturesDirectory))

for i in range(len(texturePaths)):
    print(i)
    texture = texturePaths[i]
    texture = "textures/" + texture
    print(os.path.basename(texture))
    texture+= ".png"
    if(os.path.exists(texture)):
        copy(texture, texturesDirectory)
    else:
        print("ERROR: CANNOT FIND TEXTURE " + texture + " FROM ORIGINAL FILES!")
    texture+=".mcmeta"
    if(os.path.exists(texture)):
        copy(texture, texturesDirectory)
    

print(os.listdir(texturesDirectory))




# with open('text.txt', 'r') as f:
#    f_contents = f.readlines()
#    print(f_contents)



# Step 1: Ask user for name of json file and search for it within ./models
# Step 2: Open json and read textures section
# Step 3: Go to each individual texture and copy it over into new folder
#
#
#
#
#
#
#
#
#
#
#