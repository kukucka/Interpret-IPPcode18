class Variable:
    def __init__(self, name, value, type):
        # self.reach = reach #tim myslim jestli je to GF,LF,TF
        self.name = name
        self.value = value
        self.type = type

    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    # def getReach(self):
    #     return self.reach

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def setType(self, type):
        self.type = type


