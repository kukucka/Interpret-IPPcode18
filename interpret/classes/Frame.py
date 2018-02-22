import copy

class Frame:
    def __init__(self):
        self.dictionaryOfVariables = {}

    def copyFrame(self):
        return copy.deepcopy(self.dictionaryOfVariables)

    def returnFrame(self):
        return self.dictionaryOfVariables

    def setDictionary(self, dictionaryOfVariables):
        self.dictionaryOfVariables = dictionaryOfVariables

    def addVarToDictionary(self, var):
        self.dictionaryOfVariables.update({var: None})

    def updateValueOfVar(self, var, value):
        self.dictionaryOfVariables.update({var: value})

    def isVarDefined(self, varName):
        if varName in self.dictionaryOfVariables:
           return True
        else:
            print("Error varName, var doesnt exist")
            exit(420)

    def findVar(self, varName):
        if varName in self.dictionaryOfVariables.keys():
            try:
                value = self.dictionaryOfVariables.get(varName)
                if value is None:
                    print("Error varName, var has no value")
                    exit(420)
                return value
            except KeyError:
                print("Error variable, is not initialized")
                exit(420)
        else:
            print("Error varialbe " + varName + " doesnt exist")
            exit(420)

    def checkIfVarInicialized(self, varName):
        if varName in self.dictionaryOfVariables.keys():
            try:
                value = self.dictionaryOfVariables.get(varName)
                if value is None:
                    return False
                else:
                    return True
            except KeyError:
                print("Error varName, var doesnt exist")
                exit(420)
        else:
            print("Error varialbe " + str(varName) + " doesnt exist")
            exit(420)

    def wipeFrame(self):
        self.dictionaryOfVariables.clear()
