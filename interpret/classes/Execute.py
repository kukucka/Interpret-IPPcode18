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
    # TODO co vytysknout kdyz je prommena nedefinovana
    def start(self):
        while self.curInst < len(self.dicOfCom):
            instruction = self.dicOfCom.get(str(self.curInst))
            opcode = instruction.getOpcode()
            if opcode == 'MOVE':
                self.executeMove(instruction)
            elif opcode == 'CREATEFRAME':
                self.executeCreateframe()
            elif opcode == 'PUSHFRAME':
                self.executePushframe()
            elif opcode == 'POPFRAME':
                self.executePopframe()
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
                self.executeWrite(instruction.getListOfArguments())
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
    # TODO nejaka divna vec zbyla v lf kdyz z nej popnu
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
                self.frames.addVarToGf(value[1])
            else:
                print("ERROR executeDefvar ")
                exit(420)
        elif re.match(r'^TF@', arguments[0].getValue().strip()):
            if self.frames.isTfDefined():
                value = arguments[0].getValue().split('@', 1)
                if re.match(r'^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$', value[1]):
                    self.frames.addVarToTf(value[1])
                else:
                   print("ERROR executeDefvar ")
                   exit(420)
            else:
                print("ERROR temporary frame not defined")
                exit(55)
        elif re.match(r'^LF@', arguments[0].getValue().strip()):
            if self.frames.isLfDefined():
                value = arguments[0].getValue().split('@', 1)
                if re.match(r'^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$', value[1]):
                    self.frames.addVarToLf(value[1])
                else:
                   print("ERROR executeDefvar ")
                   exit(420)
            else:
                print("ERROR temporary frame not defined")
                exit(55)

    def executeCreateframe(self):
        self.frames.createTf()

    def executePushframe(self):
        self.frames.pushTfToLfStack()

    def executePopframe(self):
        self.frames.popFromLfStack()

    def executeMove(self, instruction):
        argument = instruction.getListOfArguments()
        name = argument[0].getValue().split('@', 1)
        if re.match(r'^GF@', argument[0].getValue().strip()):
            if self.frames.isVarInGf(name[1]):
                if argument[1].getType() == "var":
                    variable = Variable(name[1], self.returnValue(argument[1].getValue()), self.returnType(argument[1].getValue()))
                else:
                    variable = Variable(name[1], argument[1].getValue(), argument[1].getType())

                self.frames.updateVarInGf(name[1], variable)
        elif re.match(r'^LF@', argument[0].getValue().strip()):
            if self.frames.isVarInLf(name[1]):
                if argument[1].getType() == "var":
                    variable = Variable(name[1], self.returnValue(argument[1].getValue()), self.returnType(argument[1].getValue()))
                else:
                    variable = Variable(name[1], argument[1].getValue(), argument[1].getType())

                self.frames.updateVarInLf(name[1], variable)
        elif re.match(r'^TF@', argument[0].getValue().strip()):
            if self.frames.isVarInTf(name[1]):
                if argument[1].getType() == "var":
                    variable = Variable(name[1], self.returnValue(argument[1].getValue()), self.returnType(argument[1].getValue()))
                else:
                    variable = Variable(name[1], argument[1].getValue(), argument[1].getType())

                self.frames.updateVarInTf(name[1], variable)
        else:
            print("ERROR executeMove")
            exit(420)

    def returnType(self, argument):
        name = argument.split('@', 1)
        if re.match(r'^GF@', argument.strip()):
            var = self.frames.getVarFromGf(name[1])
            return var.getType()
        elif re.match(r'^LF@', argument.strip()):
            var = self.frames.getVarFromLf(name[1])
            return var.getType()
        elif re.match(r'^TF@', argument.strip()):
            var = self.frames.getVarFromTf(name[1])
            return var.getType()


    def returnValue(self, argument):
        name = argument.split('@', 1)
        if re.match(r'^GF@', argument.strip()):
            var = self.frames.getVarFromGf(name[1])
            return var.getValue()
        elif re.match(r'^LF@', argument.strip()):
            var = self.frames.getVarFromLf(name[1])
            return var.getValue()
        if re.match(r'^TF@', argument.strip()):
            var = self.frames.getVarFromTf(name[1])
            return var.getValue()

    def executeWrite(self, argument):
        if argument[0].getType() == 'var':
            print(self.returnValue(argument[0].getValue()))
        else:
            self.checkIfValueEqualsType(argument[0].getValue(), argument[0].getType())
            print(argument[0].getValue())

    def checkIfValueEqualsType(self, value, type):
        if type == 'int':
            if value != None:
                try:
                    return int(value)
                except ValueError:
                    print("Value is not int")
                    exit(200)
            else:
                print("ERROR checkifValueEqualsType")
                exit(430)
        elif type == 'string':
    #         TODO tady bude check jestli je string valid
    #          TODO co vytisknout v pripade prazdneho stringu None?
            return value
        #   TODO checknout jestli muze byt napriklad TruE FaALsE
        elif type == 'bool':
            if value != None:
                if re.match(r'^true$', value.lower()):
                    return 'true'
                elif re.match(r'^false', value.lower()):
                    return 'false'
                else:
                    print("Not bool checkifValueEqualsType")
                    exit(430)
            else:
                print("ERROR checkifValueEqualsType")
                exit(430)
        else:
            print("ERROR checkifValueEqualsType")
            exit(430)
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

