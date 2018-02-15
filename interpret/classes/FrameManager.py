from .Stack import Stack
from .Frame import Frame

class FrameManager:
    def __init__(self):
        self.gf = Frame()
        self.tf = Frame()
        self.lf = Frame()
        self.lfStack = Stack()
        self.tfDefined = False
        self.lfDefined = False

    def isTfDefined(self):
        return self.tfDefined

    def isLfDefined(self):
        return self.lfDefined

    def addVarToGf(self, var):
        self.gf.addVarToDictionary(var)

    def addVarToTf(self, var):
        if self.tfDefined:
            self.tf.addVarToDictionary(var)
        else:
            print("ERROR addVarToTf")
            exit(420)

    def addVarToLf(self, var):
        if self.lfDefined:
            self.lf.addVarToDictionary(var)
        else:
            print("ERROR addVarToLf")
            exit(420)

    def getVarFromGf(self, var):
        return self.gf.findVar(var)

    def updateVarInGf(self, var, value):
        self.gf.updateValueOfVar(var, value)

    def updateVarInTf(self, var, value):
        if self.tfDefined:
            self.tf.updateValueOfVar(var, value)
        else:
            print("ERROR updateVarInTf")
            exit(420)

    def updateVarInLf(self, var, value):
        if self.lfDefined:
            self.lf.updateValueOfVar(var, value)
        else:
            print("ERROR updateVarInLf")
            exit(420)

    def isVarInGf(self, varName):
        return self.gf.isVarDefined(varName)

    def isVarInTf(self, varName):
        if self.tfDefined:
            return self.tf.isVarDefined(varName)
        else:
            print("ERROR isVarInTf")
            exit(420)

    def isVarInLf(self, varName):
        if self.lfDefined:
            return self.lf.isVarDefined(varName)
        else:
            print("ERROR isVarInLf")
            exit(420)

    def getVarFromTf(self, var):
        if self.tfDefined:
            return self.tf.findVar(var)
        else:
            print("ERROR getVarFromTf")
            exit(420)

        return self.tf.findVar(var)

    def getVarFromLf(self, var):
        if self.lfDefined:
            return self.lf.findVar(var)
        else:
            print("ERROR getVarFromLf")
            exit(420)

    def pushTfToLfStack(self):
        self.lfStack.push(self.tf.copyFrame())
        self.lf.setDictionary(self.lfStack.top())
        self.tf.wipeFrame()
        self.tfDefined = False
        self.lfDefined = True

    def createTf(self):
        self.tf.wipeFrame()
        self.tfDefined = True

    def popFromLfStack(self):
        if(self.lfStack.isEmpty()):
            print("Error Empty stack")
            exit(55)
        self.tf.setDictionary(self.lfStack.pop())
        if self.lfStack.isEmpty():
            self.lfDefined = False
        self.tfDefined = True
        self.lf.setDictionary(self.lfStack.top())

