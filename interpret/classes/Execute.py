import re

from .Stack import Stack
from .Variable import Variable
from .FrameManager import FrameManager
from .Operations import ArithmeticOperations as AR
from .Operations import CompareOperations as CO
from .Operations import LogicOperations as LO

class Execute:
    def __init__(self, dictionaryOfCommands):
        self.dicOfCom = dictionaryOfCommands
        self.curInst = 1
        self.frames = FrameManager()
        self.stack = Stack()
        self.callStack = Stack()
        self.labels = {}
    # TODO co vytysknout kdyz je prommena nedefinovana
    def start(self):
        self.getLabels()
        while self.curInst <= len(self.dicOfCom):
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
                self.executeReturn()
            elif opcode == 'PUSHS':
                self.executePushs(instruction.getListOfArguments())
            elif opcode == 'POPS':
                self.executePops(instruction.getListOfArguments())
            elif opcode == 'ADD':
                self.executeArithmeticOperations(instruction.getListOfArguments(), AR.ADD)
            elif opcode == 'SUB':
                self.executeArithmeticOperations(instruction.getListOfArguments(), AR.SUB)
            elif opcode == 'MUL':
                self.executeArithmeticOperations(instruction.getListOfArguments(), AR.MUL)
            elif opcode == 'IDIV':
                self.executeArithmeticOperations(instruction.getListOfArguments(), AR.IDIV)
            elif opcode == 'LT':
                self.executeCompareOperations(instruction.getListOfArguments(), CO.LT)
            elif opcode == 'GT':
                self.executeCompareOperations(instruction.getListOfArguments(), CO.GT)
            elif opcode == 'EQ':
                self.executeCompareOperations(instruction.getListOfArguments(), CO.EQ)
            elif opcode == 'AND':
                self.executeLogicOperations(instruction.getListOfArguments(), LO.AND)
            elif opcode == 'OR':
                self.executeLogicOperations(instruction.getListOfArguments(), LO.OR)
            elif opcode == 'NOT':
                self.executeLogicOperations(instruction.getListOfArguments(), LO.NOT)
            elif opcode == 'INT2CHAR':
                self.executeInt2Char(instruction)
            elif opcode == 'STRI2INT':
                self.executeStri2Int(instruction)
            elif opcode == 'READ':
                self.executeRead(instruction)
            elif opcode == 'WRITE':
                self.executeWrite(instruction.getListOfArguments())
            elif opcode == 'CONCAT':
                self.executeConcat(instruction.getListOfArguments())
            elif opcode == 'STRLEN':
                self.executeStrlen(instruction)
            elif opcode == 'GETCHAR':
                self.executeGetchar(instruction)
            elif opcode == 'SETCHAR':
                self.executeSetchar(instruction)
            elif opcode == 'TYPE':
                self.executeType(instruction)
            elif opcode == 'LABEL':
                self.curInst += 1
                continue
            elif opcode == 'JUMP':
                self.executeJump(instruction)
            elif opcode == 'JUMPIFEQ':
                self.executeJumpIfEq(instruction)
            elif opcode == 'JUMPIFNEQ':
                self.executeJumpIfNeq(instruction)
            elif opcode == 'DPRINT':
                self.executeDprint(instruction)
            elif opcode == 'BREAK':
                self.curInst += 1
                continue
            else:
                print("Error execute start")
                exit(420)
            self.curInst += 1

    def getLabels(self):
        for instNum in self.dicOfCom:
            inst = self.dicOfCom.get(str(instNum))
            if inst.getOpcode() == 'LABEL':
                labelName = self.getLabelName(inst)
                if labelName in self.labels:
                    print("Error getLabels, label already exists")
                    exit(52)
                else:
                    self.labels.update({labelName: instNum})

    def getLabelName(self, inst):
            arg = inst.getListOfArguments()
            labelName = arg[0].getValue()
            if labelName != None:
                return labelName
            else:
                print("Error isLabel, this is not a label")
                exit(420)

    def getLabelPosition(self, labelName):
        if labelName in self.labels.keys():
            return self.labels.get(labelName)
        else:
            print("Label doesnt exist")
            exit(420)

    def setCurInst(self, position):
        self.curInst = int(position)

    def executeJump(self, instruction):
        self.setCurInst(self.getLabelPosition(self.getLabelName(instruction)))

    def executeReturn(self):
        if self.callStack.isEmpty():
            print("Cant return anything from empty callStack")
            exit(420)
        else:
            self.setCurInst(self.callStack.pop())

    def executeJumpIfEq(self, instruction):
        valuesToCompare = self.compareTypesOfArguments(instruction.getListOfArguments())
        if valuesToCompare[0] == valuesToCompare[1]:
            self.executeJump(instruction)

    def executeJumpIfNeq(self, instruction):
        valuesToCompare = self.compareTypesOfArguments(instruction.getListOfArguments())
        if valuesToCompare[0] != valuesToCompare[1]:
            self.executeJump(instruction)



    def executeCall(self, instruction):
        self.callStack.push(self.curInst)
        self.setCurInst(self.getLabelPosition(self.getLabelName(instruction)))

    def executeConcat(self, arguments):
        arg1 = self.checkAndReturnString(arguments[1])
        arg2 = self.checkAndReturnString(arguments[2])
        concatArg = arg1 + arg2
        self.assignValueToVar(arguments[0].getValue(), concatArg, 'string')

    def checkAndReturnString(self, argument):
        if argument.getType() == 'string':
            self.isStr(argument.getValue())
            return argument.getValue()
        elif argument.getType() == 'var':
            if self.returnType(argument.getValue()) == 'string':
                str = self.returnValue(argument.getValue())
                self.isStr(str)
                return str
            else:
                print(argument.getValue() + " is not a strings")
                exit(420)
        else:
            print(argument.getValue() + " is not a type of strings")
            exit(420)

    # TODO nejaka divna vec zbyla v lf kdyz z nej popnu
    def executeDefvar(self, arguments):
        # if instruction.getListOfArguments()
        # if preg_match('/^bool@/', $argument) || preg_match('/^int@/', $argument) ||
        # preg_match('/^string@/', $argument
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

    def executeWrite(self, argument):
        if argument[0].getType() == 'var':
            print(self.returnValue(argument[0].getValue())) #mozna pridat ,end=''
        else:
            self.checkIfValueEqualsType(argument[0].getValue(), argument[0].getType())
            print(argument[0].getValue()) #mozna pridat ,end=''
    # TODO checknout ze int je opravdu int   <arg2 type="int">LF@loll</arg2> checkIfValueEqualsType udelam funcki ktera odkaze
    # na tuhle a checkne to a vrati bool zatim je to rozbite
    def executeArithmeticOperations(self, arguments, typeOfOperation):
        if arguments[1].getType() == 'var' and arguments[2].getType() == 'int':
            if self.returnType(arguments[1].getValue()) == 'int' and self.isInt(arguments[2].getValue(), arguments[2].getType()):
                if typeOfOperation == AR.ADD:
                    value = int(self.returnValue(arguments[1].getValue())) + int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.SUB:
                    value = int(self.returnValue(arguments[1].getValue())) - int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.MUL:
                    value = int(self.returnValue(arguments[1].getValue())) * int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.IDIV:
                    argValue = int(arguments[2].getValue())
                    if argValue == 0:
                        print("ERROR cant devide with zero")
                        exit(57)
                    value = int(int(self.returnValue(arguments[1].getValue())) / argValue)
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                # print(self.returnValue(arguments[0].getValue()))
            else:
                print("ERROR cant use string/bool in arithmetic operation")
                exit(420)
        elif arguments[1].getType() == 'int' and arguments[2].getType() == 'var':
            if self.isInt(arguments[1].getValue(), arguments[1].getType()) and self.returnType(arguments[2].getValue()) == 'int':
                if typeOfOperation == AR.ADD:
                    value = int(arguments[1].getValue()) + int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.SUB:
                    value = int(arguments[1].getValue()) - int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.MUL:
                    value = int(arguments[1].getValue()) * int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.IDIV:
                    argValue = int(self.returnValue(arguments[2].getValue()))
                    if argValue == 0:
                        print("ERROR cant devide with zero")
                        exit(57)
                    value = int(int(arguments[1].getValue()) / argValue)
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                # print(self.returnValue(arguments[0].getValue()))
            else:
                print("ERROR cant use string/bool in arithmetic operation")
                exit(420)
        elif arguments[1].getType() == 'var' and arguments[2].getType() == 'var':
            if (self.returnType(arguments[1].getValue()) == 'int' and
            self.returnType(arguments[2].getValue()) == 'int'):
                if typeOfOperation == AR.ADD:
                    value = int(self.returnValue(arguments[1].getValue())) + int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.SUB:
                    value = int(self.returnValue(arguments[1].getValue())) - int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.MUL:
                    value = int(self.returnValue(arguments[1].getValue())) * int(self.returnValue(arguments[2].getValue()))
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.IDIV:
                    argValue = int(self.returnValue(arguments[2].getValue()))
                    if argValue == 0:
                        print("ERROR cant devide with zero")
                        exit(57)
                    value = int(int(self.returnValue(arguments[1].getValue())) / argValue)
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                # print(self.returnValue(arguments[0].getValue()))
            else:
                print("ERROR executeArithmeticOperations not ints")
                exit(420)
        elif arguments[1].getType() == 'int' and arguments[2].getType() == 'int':
            if self.isInt(arguments[1].getValue(), arguments[1].getType())  and self.isInt(arguments[2].getValue(), arguments[2].getType()):
                if typeOfOperation == AR.ADD:
                    value = int(arguments[1].getValue()) + int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.SUB:
                    value = int(arguments[1].getValue()) - int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.MUL:
                    value = int(arguments[1].getValue()) * int(arguments[2].getValue())
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                elif typeOfOperation == AR.IDIV:
                    argValue = int(arguments[2].getValue())
                    if argValue == 0:
                        print("ERROR cant devide with zero")
                        exit(57)
                    value = int(int(arguments[1].getValue()) / argValue)
                    self.assignValueToVar(arguments[0].getValue(), value, 'int')
                # print(self.returnValue(arguments[0].getValue()))
            else:
                print("ERROR executeArithmeticOperations not ints")
                exit(420)
        else:
            print("ERROR executeArithmeticOperations not ints")
            exit(420)


    def executeCompareOperations(self, arguments, typeOfOperator):
        valuesToCompare = self.compareTypesOfArguments(arguments)
        if typeOfOperator == CO.GT:
            if valuesToCompare[0] > valuesToCompare[1]:
                self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
            else:
                self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')
        elif typeOfOperator == CO.LT:
            if valuesToCompare[0] < valuesToCompare[1]:
                self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
            else:
                self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')
        elif typeOfOperator == CO.EQ:
            if valuesToCompare[0] == valuesToCompare[1]:
                self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
            else:
                self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')
        else:
            print("Error inexecute CompareOperations")
            exit(430)

    def executeLogicOperations(self, arguments, typeOfOperator):
        args = []
        if typeOfOperator == LO.AND or typeOfOperator == LO.OR:
            args.append(self.checkAndReturnBoolValue(arguments[1]))
            args.append(self.checkAndReturnBoolValue(arguments[2]))
            if typeOfOperator == LO.AND:
                if args[0] and args[1]:
                    self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
                else:
                    self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')
            elif typeOfOperator == LO.OR:
                if args[0] or args[1]:
                    self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
                else:
                    self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')
        elif typeOfOperator == LO.NOT:
            args.append(self.checkAndReturnBoolValue(arguments[1]))
            if not args[0]:
                self.assignValueToVar(arguments[0].getValue(), 'true', 'bool')
            else:
                self.assignValueToVar(arguments[0].getValue(), 'false', 'bool')

    def executePushs(self, argument):
        args = []
        if argument[0].getType() == 'var':
            args.append(self.returnValue(argument[0].getValue()))
            args.append(self.returnType(argument[0].getValue()))
        else:
            if self.checkIfValueEqualsType(argument[0].getValue(), argument[0].getType()):
                args.append(argument[0].getValue())
                args.append(argument[0].getType())
        self.stack.push(args)

    def executePops(self, argument):
        if self.stack.isEmpty():
            print("Nelze popnout z prazdneho zasobniku")
            exit(56)
        else:
            popVal = self.stack.pop()
            self.assignValueToVar(argument[0].getValue(), popVal[0], popVal[1])



    def checkAndReturnBoolValue(self, argument):
        if argument.getType() == 'var':
            if self.returnType(argument.getValue()) == 'bool':
                arg1 = self.returnValue(argument.getValue())
                if self.isBool(arg1):
                    return self.getBoolValues(argument)
                else:
                    print("ERROR not a bool")
                    exit(420)
            else:
                print("ERROR not a bool")
                exit(420)
        else:
            if argument.getType() == 'bool':
                if self.isBool(argument.getValue()):
                    return self.getBoolValues(argument)
                else:
                    print("ERROR not a bool")
                    exit(420)
            else:
                print("ERROR not a bool")
                exit(420)



    def getBoolValues(self,argument):
        if argument.getValue() == 'true':
            return True
        else:
            return False


    def compareTypesOfArguments(self, arguments):
        argValue = []
        if arguments[1].getType() == 'var':
            arg1 = self.returnType(arguments[1].getValue())
            argValue.append(str(self.returnValue(arguments[1].getValue())))
        else:
            arg1 = arguments[1].getType()
            if arg1 == 'string':
                self.isStr(arguments[1].getValue())
            elif arg1 == 'int':
                self.isInt(arguments[1].getValue())
            elif arg1 == 'bool':
                self.isBool(arguments[1].getValue())
            argValue.append(str(arguments[1].getValue()))
        if arguments[2].getType() == 'var':
            arg2 = self.returnType(arguments[2].getValue())
            argValue.append(str(self.returnValue(arguments[2].getValue())))
        else:
            arg2 = arguments[2].getType()
            if arg1 == 'string':
                self.isStr(arguments[2].getValue())
            elif arg1 == 'int':
                self.isInt(arguments[2].getValue())
            elif arg1 == 'bool':
                self.isBool(arguments[2].getValue())
            argValue.append(str(arguments[2].getValue()))
        if arg1 != arg2:
            print("ERROR compareTypesOfArguments types are not equal")
            exit(420)

        return argValue


    def isInt(self, value):
        result = self.checkIfValueEqualsType(value, 'int')
        try:
            result = int(result)
            return True
        except ValueError:
            exit(430)

    def isStr(self, value):
        result = self.checkIfValueEqualsType(value, 'string')
        try:
            result = str(result)
            return True
        except ValueError:
            exit(430)

    def isBool(self, value):
        result = self.checkIfValueEqualsType(value, 'bool')
        try:
            result = str(result)
            return True
        except ValueError:
            exit(430)


    # TODO mozna pouzit pro konkatenaci pridat parametr type
    def assignValueToVar(self, variable, value, type):
        name = variable.split('@', 1)
        if re.match(r'^GF@', variable.strip()):
            if self.frames.isVarInGf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInGf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
                exit(420)
        elif re.match(r'^TF@', variable.strip()):
            if self.frames.isVarInTf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInTf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
                exit(420)
        elif re.match(r'^LF@', variable.strip()):
            if self.frames.isVarInLf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInLf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
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
        elif re.match(r'^TF@', argument.strip()):
            var = self.frames.getVarFromTf(name[1])
            return var.getValue()


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
            return value
        elif type == 'bool':
            if value != None:
                if re.match(r'^true$', value):
                    return 'true'
                elif re.match(r'^false', value):
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

