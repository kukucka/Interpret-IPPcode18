class Frame:
    def __init__(self):
        self.dictionaryOfVariables = {}

    def copyFrame(self):
        return self.dictionaryOfVariables

    def setFrame(self, dictionaryOfVariables):
        self.dictionaryOfVariables = dictionaryOfVariables

    def addVarToDictionary(self, var):
        self.dictionaryOfVariables.update({var: None})

    def updateValueOfVar(self, var, value):
        self.dictionaryOfVariables.update({var: value})

    def findVar(self, varName):
        try:
            value = self.dictionaryOfVariables.get(varName)
            if value is None:
                print("Error varName, var has no value")
                exit(420)
            return value
        except KeyError:
            print("Error varName, var doesnt exist")
            exit(420)


    def wipeFrame(self):
        self.dictionaryOfVariables = {}
