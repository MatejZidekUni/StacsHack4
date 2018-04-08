def createFile(name):
    print(" ++ made file '" + name + "'")

def saveFile():
    print(" !! save file")

def run():
    saveFile()
    run()

def appendLine(content):
    print(" + " + content)

def changeLine(lineNum, content):
    print(lineNum + " > " + content)
