class Variable:
    def __init__(self, name):
        # self.reach = reach #tim myslim jestli je to GF,LF,TF
        self.name = name
        self.value = None
        self.type = None

    def getType(self):
        return self.type

    # def getReach(self):
    #     return self.reach

    def getName(self):
        return self.name

    def setValue(self, value):
        self.value = value

    def setType(self, type):
        self.type = type


