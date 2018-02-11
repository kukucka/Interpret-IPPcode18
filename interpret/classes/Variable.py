class Variable:
    def __init__(self, type, reach, name):
        self.type = type
        self.reach = reach #tim myslim jestli je to GF,LF,TF
        self.name = name

    def getType(self):
        return self.type

    def getReacg(self):
        return self.reach

    def getName(self):
        return self.name



