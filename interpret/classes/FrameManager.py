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
        self.tf.addVarToDictionary(var)

    def addVarToLf(self, var):
        self.lf.addVarToDictionary(var)

    def getVarFromGf(self, var):
        return self.gf.findVar(var)

    def updateVarInGf(self, var, value):
        self.gf.updateValueOfVar(var, value)

    def updateVarInTf(self, var, value):
        self.tf.updateValueOfVar(var, value)

    def updateVarInLf(self, var, value):
        self.lf.updateValueOfVar(var, value)

    def isVarInGf(self, varName):
        return self.gf.isVarDefined(varName)

    def isVarInTf(self, varName):
        return self.tf.isVarDefined(varName)

    def isVarInLf(self, varName):
        return self.lf.isVarDefined(varName)

    def getVarFromTf(self, var):
        return self.tf.findVar(var)

    def getVarFromLf(self, var):
        return self.lf.findVar(var)

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

