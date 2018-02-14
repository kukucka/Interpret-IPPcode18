import re

from .Stack import Stack
from .Variable import Variable
from .FrameManager import FrameManager

class Execute:
    def __init__(self, dictionaryOfCommands):
        self.dicOfCom = dictionaryOfCommands
        self.curInst = 1
        self.frames = FrameManager()
        self.stack = Stack()

    def start(self):
        while self.curInst < len(self.dicOfCom):
            instruction = self.dicOfCom.get(str(self.curInst))
            opcode = instruction.getOpcode()
            if opcode == 'MOVE':
                print("works")
                self.executeMove(instruction)
            elif opcode == 'CREATEFRAME':
                self.executeCreateframe(instruction)
            elif opcode == 'PUSHFRAME':
                self.executePushframe(instruction)
            elif opcode == 'DEFVAR':
                self.executeDefvar(instruction.getListOfArguments())
            elif opcode == 'CALL':
                self.executeCall(instruction)
            elif opcode == 'RETURN':
                self.executeReturn(instruction)
            elif opcode == 'PUSHS':
                self.executePushs(instruction)
            elif opcode == 'POPS':
                self.executePops(instruction)
            elif opcode == 'ADD':
                self.executeAdd(instruction)
            elif opcode == 'SUB':
                self.executeSub(instruction)
            elif opcode == 'MUL':
                self.executeMul(instruction)
            elif opcode == 'IDIV':
                self.executeIdiv(instruction)
            elif opcode == 'LT':
                self.executeLt(instruction)
            elif opcode == 'GT':
                self.executeGt(instruction)
            elif opcode == 'EQ':
                self.executeEq(instruction)
            elif opcode == 'AND':
                self.executeAnd(instruction)
            elif opcode == 'OR':
                self.executeOr(instruction)
            elif opcode == 'NOT':
                self.executeNot(instruction)
            elif opcode == 'INT2CHAR':
                self.executeInt2Char(instruction)
            elif opcode == 'STRI2INT':
                self.executeStri2Int(instruction)
            elif opcode == 'READ':
                self.executeRead(instruction)
            elif opcode == 'WRITE':
                self.executeWrite(instruction)
            elif opcode == 'CONCAT':
                self.executeConcat(instruction)
            elif opcode == 'STRLEN':
                self.executeStrlen(instruction)
            elif opcode == 'GETCHAR':
                self.executeGetchar(instruction)
            elif opcode == 'SETCHAR':
                self.executeSetchar(instruction)
            elif opcode == 'TYPE':
                self.executeType(instruction)
            elif opcode == 'LABEL':
                self.executeLabel(instruction)
            elif opcode == 'JUMP':
                self.executeJump(instruction)
            elif opcode == 'JUMPIFEQ':
                self.executeJumpIfEq(instruction)
            elif opcode == 'JUMPIFNEQ':
                self.executeJumpIfNeq(instruction)
            elif opcode == 'DPRINT':
                self.executeDprint(instruction)
            elif opcode == 'BREAK':
                self.executeBreak(instruction)
            else:
                print("Error execute start")
                exit(420)
            self.curInst += 1

    # def executeMove(self, instruction):
        # self.executeMove(instruction)
    #TODO muzu definovat promenu LF@something????
    def executeDefvar(self, arguments):
        # if instruction.getListOfArguments()
        # if preg_match('/^bool@/', $argument) || preg_match('/^int@/', $argument) ||
        # preg_match('/^string@/', $argument
        print(arguments[0].getType())
        if len(arguments[0].getValue().split()) != 1:
            print("Cant define multiple variables in one command")
            exit(420)
        if re.match(r'^GF@', arguments[0].getValue().strip()):
            value = arguments[0].getValue().split('@', 1)
            if re.match(r'^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$', value[1]):
                var = Variable(value[1])
                self.frames.addVarToGf(var)
            else:
                print("ERROR executeDefvar ")
                exit(420)
        elif re.match(r'^TF@', arguments[0].getValue().strip()):
            value = arguments[0].getValue().split('@', 1)
            if re.match(r'^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$', value[1]):
                var = Variable(value[1])
                self.frames.addVarToTf(var)
            else:
               print("ERROR executeDefvar ")
               exit(420)



    # def executePushframe(self, instruction):
    #     self.executePushframe(instruction)
    #
    # def executeCreateframe(self, instruction):
    #     self.executeCreateframe(instruction)
    #
    # def executeMove(self, instruction):
    #     self.executeMove(instruction)
    #
    #

