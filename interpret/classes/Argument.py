class Argument:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.checkIfValueIsNone()


    def getType(self):
        return self.type

    def getValue(self):
        return self.value

    def checkIfValueIsNone(self):
        if self.type == 'string':
            if self.value == None:
                self.value = ''
