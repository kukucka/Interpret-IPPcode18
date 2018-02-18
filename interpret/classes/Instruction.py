class Instruction:
    def __init__(self, opcode):
        self.opcode = opcode
        self.listOfArgument = []

    def getOpcode(self):
        return self.opcode

    def getListOfArguments(self):
        return self.listOfArgument

    def setArgument(self, argument):
        self.listOfArgument.append(argument)

    def getNumberOfArguments(self):
        return len(self.listOfArgument)
