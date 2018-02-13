from .Stack import Stack
from .Variable import Variable
from .FrameManager import FrameManager

class Execute:
    def __init__(self, dictionaryOfCommands):
        self.dicOfCom = dictionaryOfCommands
        self.curInst = 1
        self.frames = FrameManager
        self.stack = Stack

    def start(self):
        while self.curInst < len(self.dicOfCom):
            instruction = self.dicOfCom.get(self.curInst)
            opcode = instruction.getOpcode()
            if opcode == 'MOVE':
                self.executeMove(instruction)
            elif opcode == 'CREATEFRAME':
                self.executeCreateframe(instruction)
            elif opcode == 'PUSHFRAME':
                self.executePushframe(instruction)
            elif opcode == 'DEFVAR':
                self.executeDefvar(instruction)
            elif opcode == 'CALL':
                self.executeCall(instruction)
            elif opcode == '':
                self.executeIdiv




    def executePushframe(self, instruction):
        self.executePushframe(instruction)

    def executeCreateframe(self, instruction):
        self.executeCreateframe(instruction)

    def executeMove(self, instruction):
        self.executeMove(instruction)



