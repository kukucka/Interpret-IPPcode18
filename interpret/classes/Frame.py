class Frame:
    def __init__(self):
        dictionaryOfVariables = {}

    def copyFrame(self):
        return self.dictionaryOfVariables

    def setFrame(self, dictionaryOfVariables):
        self.dictionaryOfVariables = dictionaryOfVariables

    def addVarToDictionary(self, var):
        self.dictionaryOfVariables.update({var: None})

    def udpateValueOfVar(self, var, value):
        self.dictionaryOfVariables.update({var: value})

    def varName(self, varName):
        try:
            value = self.dictionaryOfVariables.get(varName)
            if value is None:
                print("Error varName, var has no value")
                exit(420)
            return value
        except KeyError:
            print("Error varName, var doesnt exist")
            exit(420)


