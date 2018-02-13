from .Stack import Stack
from .Frame import Frame

class FrameManager:
    def __init__(self):
        self.gf = Frame
        self.lfStack = Stack
        self.tf = Frame
        self.stack = Stack
        self.tfDefined = False
        self.lf = Frame

    def addVarToGf(self, var):
        self.gf.addVarToDictionary(var)

    def addVarToTf(self, var):
        self.tf.addVarToDictionary(var)

    def getVarFromGf(self, var):
        return self.gf.findVar(var)

    def getVarFromTf(self, var):
        return self.tf.findVar(var)

    def getVarFromLf(self, var):
        return self.lf.findVar(var)

    def pushTftoLfStack(self, var):
        self.lfStack.push(self.tf.copyFrame())
        self.lf = self.tf
        self.tf.wipeFrame()

    def popFromLfStack(self, var):
        if(self.lfStack.isEmpty()):
            print("Error Empty stack")
            exit(420)
        self.tf = self.lfStack.pop()