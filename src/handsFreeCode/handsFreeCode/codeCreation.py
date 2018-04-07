import requests
#from handsFreeCode import setCont

def createFile(name):
    print("made file '" + name + "'")

def saveFile():
    print("save file")

def run():
    saveFile()
    pass

def appendLine(content):
    pass
    #setCont(content)
    #r = requests.post('http://localhost:5000/code', data={"content":content})

def deleteLine(lineNum):
    pass

def changeLine(lineNum, content):
    print(lineNum + " > " + content)
