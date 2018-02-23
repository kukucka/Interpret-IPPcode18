import re

import sys

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
    #     Extension
        self.executed_inst = 0
        self.max_var = 0
    # TODO co vytysknout kdyz je prommena nedefinovana
    def get_max_var(self):
        return self.max_var

    def get_executed_inst(self):
        return self.executed_inst

    def iterate_exec_inst(self):
        self.executed_inst += 1

    def check_amount_var(self):
        new_max_var = self.frames.returnGfNumberOfVar() + self.frames.returnTfNumberOfVar() + self.frames.returnLfNumberOfVar()
        if new_max_var > self.max_var:
            self.max_var = new_max_var

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
                self.executeInt2Char(instruction.getListOfArguments())
            elif opcode == 'STRI2INT':
                self.executeStri2Int(instruction.getListOfArguments())
            elif opcode == 'READ':
                self.executeRead(instruction.getListOfArguments())
            elif opcode == 'WRITE':
                self.executeWrite(instruction.getListOfArguments())
            elif opcode == 'CONCAT':
                self.executeConcat(instruction.getListOfArguments())
            elif opcode == 'STRLEN':
                self.executeStrlen(instruction.getListOfArguments())
            elif opcode == 'GETCHAR':
                self.executeGetchar(instruction.getListOfArguments())
            elif opcode == 'SETCHAR':
                self.executeSetchar(instruction.getListOfArguments())
            elif opcode == 'TYPE':
                self.executeType(instruction.getListOfArguments())
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
                self.executeDprint(instruction.getListOfArguments())
            elif opcode == 'BREAK':
                self.executeBreak()
            else:
                print("Error execute start")
                exit(52)
            self.curInst += 1
            self.iterate_exec_inst()
            self.check_amount_var()

    def executeDprint(self, argument):
        type = argument[0].getType()
        value = "Unidentified value"
        if type == 'var':
            type = self.returnType(argument[0].getValue())
        if type == 'int':
            value = self.returnIntValue(argument[0])
        elif type == 'string':
            value = self.checkAndReturnString(argument[0])
        elif type == 'bool':
            value = str(self.checkAndReturnBoolValue(argument[0])).lower()
        sys.stderr.write(value+"\n")

    # TODO pridat pocet vykonanych instrukci
    def executeBreak(self):
        sys.stderr.write("Positon in code: " + str(self.curInst) + "\n")
        sys.stderr.write("Global frame contains:\n")
        self.frames.returnGfFrame()
        sys.stderr.write("Temporary frame contains:\n")
        self.frames.returnTfFrame()
        sys.stderr.write("Local frame contains:\n")
        self.frames.returnLfFrame()



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
                exit(52)

    def getLabelPosition(self, labelName):
        if labelName in self.labels.keys():
            return self.labels.get(labelName)
        else:
            print("Label doesnt exist")
            exit(52)

    def setCurInst(self, position):
        self.curInst = int(position)


    def executeInt2Char(self,arguments):
        number = self.returnIntValue(arguments[1])
        try:
            self.assignValueToVar(arguments[0].getValue(), chr(number), 'string' )
        except ValueError:
            print(arguments[1].getValue() + " cant be converted to unicode ")
            exit(58)

    def executeStri2Int(self, arguments):
        number = self.returnIntValue(arguments[2])
        string = self.checkAndReturnString(arguments[1])
        if number >= len(string):
            print("sri2Int unsucesfull")
            exit(58)
        else:
            self.assignValueToVar(arguments[0].getValue(), ord(string[number]), 'int')

    def executeGetchar(self, arguments):
        number = self.returnIntValue(arguments[2])
        string = self.checkAndReturnString(arguments[1])
        if number >= len(string):
            print("getchar unsucesfull")
            exit(58)
        else:
            self.assignValueToVar(arguments[0].getValue(), string[number], 'string')
    def executeSetchar(self, arguments):
        stringToChange = self.checkAndReturnString(arguments[0])
        string = self.checkAndReturnString(arguments[2])
        number = self.returnIntValue(arguments[1])
        if number >= len(stringToChange):
            print("setchar unsucesfull")
            exit(58)
        else:
            shredString = list(stringToChange)
            shredString[number] = string[0]
            stringToChange = "".join(shredString)
            self.assignValueToVar(arguments[0].getValue(), stringToChange, 'string')


    def executeJump(self, instruction):
        self.setCurInst(self.getLabelPosition(self.getLabelName(instruction)))

    def executeReturn(self):
        if self.callStack.isEmpty():
            print("Cant return anything from empty callStack")
            exit(56)
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

    def executeStrlen(self, arguments):
        arg1 = self.checkAndReturnString(arguments[1])
        number = len(arg1)
        self.assignValueToVar(arguments[0].getValue(), number, 'int')

    def executeType(self, arguments):
        if arguments[1].getType() == 'var':
            if self.checkIfVarInicialized(arguments[1].getValue()):
                type = self.returnType(arguments[1].getValue())
                value = self.returnValue(arguments[1].getValue())
                self.checkIfValueEqualsType(value, type)
                self.assignValueToVar(arguments[0].getValue(), type, 'string')
            else:
                self.assignValueToVar(arguments[0].getValue(), '', 'string')
        elif arguments[1].getType() == 'int':
            if self.isInt(arguments[1].getValue()):
                self.assignValueToVar(arguments[0].getValue(), 'int', 'string')
        elif arguments[1].getType() == 'string':
            if self.isStr(arguments[1].getValue()):
                self.assignValueToVar(arguments[0].getValue(), 'string', 'string')
        elif arguments[1].getType() == 'bool':
            if self.isBool(arguments[1].getValue()):
                self.assignValueToVar(arguments[0].getValue(), 'bool', 'string')

    def checkIfVarInicialized(self, varName):
        name = varName.split('@', 1)
        if re.match(r'^GF@', varName.strip()):
            return self.frames.checkIfVarInitInGf(name[1])
        elif re.match(r'^LF@', varName.strip()):
            return self.frames.checkIfVarInitInLf(name[1])
        elif re.match(r'^TF@', varName.strip()):
            return self.frames.checkIfVarInitInTf(name[1])

    def checkAndReturnString(self, argument):
        if argument.getType() == 'string':
            self.isStr(argument.getValue())
            modifiedString = self.transferString(argument.getValue())
            return modifiedString
        elif argument.getType() == 'var':
            if self.returnType(argument.getValue()) == 'string':
                str = self.returnValue(argument.getValue())
                self.isStr(str)
                modifiedString = self.transferString(str)
                return modifiedString
            else:
                print(argument.getValue() + " is not a strings")
                exit(53)
        else:
            print(argument.getValue() + " is not a type of strings")
            exit(53)

    def transferString(self, str):
        toConvert = []
        strToMod = list(str)
        found = False
        i = 0
        for letter in str:
            if found:
                if re.match(r'[0-9]', strToMod[i]):
                    toConvert.append(letter)
                    if(len(toConvert) == 3):
                        code = ''.join(toConvert)
                        code = int(code)
                        strToMod[i] = ''
                        strToMod[i-1] = ''
                        strToMod[i-2] = ''
                        strToMod[i-3] = chr(code)
                        found = False
                        toConvert = []
                else:
                    print("ERROR")
                    exit(32)
            if letter == '\\':
                found = True
            i += 1
        if found:
            print("ERROR")
            exit(32)
        strToMod = ''.join(strToMod)
        # strMod = re.sub(r'[\\][0-9][0-9][0-9]', r'[0-9][0-9][0-9]', str)
        # print(strMod)
        # print(str)
        return strToMod


    def checkVarValidity(self, name):
        if re.match(r'^([a-zA-Z_-]|[*]|[$]|[%]|[&])([a-zA-Z0-9_-]|[*]|[$]|[%]|[&])*$', name):
            return True
        else:
            print("ERROR in checkVarValidity during executeDefvar ")
            exit(32)
    # TODO nejaka divna vec zbyla v lf kdyz z nej popnu
    def executeDefvar(self, arguments):
        # if instruction.getListOfArguments()
        # if preg_match('/^bool@/', $argument) || preg_match('/^int@/', $argument) ||
        # preg_match('/^string@/', $argument
        if len(arguments[0].getValue().split()) != 1:
            print("Cant define multiple variables in one command")
            exit(32)
        varName = arguments[0].getValue().strip()
        value = arguments[0].getValue().split('@', 1)
        if re.match(r'^GF@', varName):
            if self.checkVarValidity(value[1]):
                self.frames.addVarToGf(value[1])
        elif re.match(r'^TF@', varName):
            if self.frames.isTfDefined():
                if self.checkVarValidity(value[1]):
                    self.frames.addVarToTf(value[1])
            else:
                print("ERROR temporary frame not defined")
                exit(55)
        elif re.match(r'^LF@', varName):
            if self.frames.isLfDefined():
                if self.checkVarValidity(value[1]):
                    self.frames.addVarToLf(value[1])
            else:
                print("ERROR local frame not defined")
                exit(55)

    def executeCreateframe(self):
        self.frames.createTf()

    def executePushframe(self):
        self.frames.pushTfToLfStack()

    def executePopframe(self):
        self.frames.popFromLfStack()


    def defineVar(self, argument, name):
        if argument.getType() == "var":
            variable = Variable(name, self.returnValue(argument.getValue()), self.returnType(argument.getValue()))
        else:
            if argument.getType() == 'int':
                number = self.isInt(argument.getValue())
                variable = Variable(name, number, argument.getType())
            elif argument.getType() == 'string':
                val = argument.getValue().strip()
                self.isStr(val)
                strMod = self.checkAndReturnString(argument)
                variable = Variable(name, strMod, argument.getType())
            elif argument.getType() == 'bool':
                self.isBool(argument.getValue())
                variable = Variable(name, argument.getValue(), argument.getType())
        return variable

    def executeMove(self, instruction):
        argument = instruction.getListOfArguments()
        name = argument[0].getValue().split('@', 1)
        if re.match(r'^GF@', argument[0].getValue().strip()):
            if self.frames.isVarInGf(name[1]):
                variable = self.defineVar(argument[1], name[1])
                self.frames.updateVarInGf(name[1], variable)
        elif re.match(r'^LF@', argument[0].getValue().strip()):
            if self.frames.isVarInLf(name[1]):
                variable = self.defineVar(argument[1], name[1])
                self.frames.updateVarInLf(name[1], variable)
        elif re.match(r'^TF@', argument[0].getValue().strip()):
            if self.frames.isVarInTf(name[1]):
                variable = self.defineVar(argument[1], name[1])
                self.frames.updateVarInTf(name[1], variable)
        else:
            print("ERROR executeMove")
            exit(52)

    def executeWrite(self, argument):
        if argument[0].getType() == 'var':
            print(self.returnValue(argument[0].getValue()),end='') #mozna pridat ,end=''
        else:
            self.checkIfValueEqualsType(argument[0].getValue(), argument[0].getType())
            if argument[0].getType() == 'string':
                strMod = self.checkAndReturnString(argument[0])
                print(strMod, end='') #mozna pridat ,end=''
            else:
                print(argument[0].getValue(),end='') #mozna pridat ,end=''
    # TODO checknout ze int je opravdu int   <arg2 type="int">LF@loll</arg2> checkIfValueEqualsType udelam funcki ktera odkaze
    # na tuhle a checkne to a vrati bool zatim je to rozbite


    def executeRead(self, argument):
        value = argument[1].getValue().strip()
        if value == 'bool':
            entered = self.getInput()
            if self.checkReadBool(entered):
                self.assignValueToVar(argument[0].getValue(), 'true', 'bool')
            else:
                self.assignValueToVar(argument[0].getValue(), 'false', 'bool')
        elif value == 'int':
            entered = self.getInput()
            if self.checkReadInt(entered):
                self.assignValueToVar(argument[0].getValue(), int(entered), 'int')
            else:
                self.assignValueToVar(argument[0].getValue(), 0, 'int')
        elif value == 'string':
            entered = self.getInput()
            if self.checkReadString(entered):
                self.assignValueToVar(argument[0].getValue(), entered, 'string')
            else:
                self.assignValueToVar(argument[0].getValue(), '', 'string')
        else:
            print("Wrong argument for READ")
            exit(52)

    def getInput(self):
        sys.stdin.flush()
        try:
            entered = input()
            return entered
        except:
            exit(99) #//predelat

    def checkReadBool(self, value):
        if re.match(r'^(T|t)(R|r)(U|u)(E|e)$', value):
            return True
        else:
            return False

    def checkReadInt(self, value):
        if value != None:
            try:
                if int(value):
                    return True
            except ValueError:
                return False
        else:
            return False

    def checkReadString(self, value):
        if value != None:
            if len(value.split()) != 1:
                return False
            else:
                return True
        else:
            return False
    def returnIntValue(self, argument):
        if argument.getType() == 'var':
            if self.returnType(argument.getValue()) == 'int':
                return self.returnValue(argument.getValue())
            else:
                print("NOT and int")
                exit(53)
        elif argument.getType() == 'int':
            number = self.isInt(argument.getValue())
            return number
        else:
            print("NOT an int")
            exit(53)

    def executeArithmeticOperations(self, arguments, typeOfOperation):
        values = []
        values.append(self.returnIntValue(arguments[1]))
        values.append(self.returnIntValue(arguments[2]))
        if typeOfOperation == AR.ADD:
            value = values[0] + values[1]
            self.assignValueToVar(arguments[0].getValue(), value, 'int')
        elif typeOfOperation == AR.SUB:
            value = values[0] - values[1]
            self.assignValueToVar(arguments[0].getValue(), value, 'int')
        elif typeOfOperation == AR.MUL:
            value = values[0] * values[1]
            self.assignValueToVar(arguments[0].getValue(), value, 'int')
        elif typeOfOperation == AR.IDIV:
            if values[1] == 0:
                exit(57)
            value = int(values[0] / values[1])
            self.assignValueToVar(arguments[0].getValue(), value, 'int')
        else:
            print("ERROR executeArithmeticOperations not ints")
            exit(52)


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
            exit(52)

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
                    exit(53)
            else:
                print("ERROR not a bool")
                exit(53)
        else:
            if argument.getType() == 'bool':
                if self.isBool(argument.getValue()):
                    return self.getBoolValues(argument)
                else:
                    print("ERROR not a bool")
                    exit(53)
            else:
                print("ERROR not a bool")
                exit(53)

    def getBoolValues(self,argument):
        if argument.getType() == 'var':
            if self.returnValue(argument.getValue()) == 'true':
                return True
            else:
                return False
        else:
            if argument.getValue() == 'true':
                return True
            else:
                return False


    def compareTypesOfArguments(self, arguments):
        argValue = []
        if arguments[1].getType() == 'var':
            arg1 = self.returnType(arguments[1].getValue())
            if arg1 == 'bool' or arg1 == 'string':
                argValue.append(str(self.returnValue(arguments[1].getValue())))
            else:
                argValue.append(self.returnValue(arguments[1].getValue()))
        else:
            arg1 = arguments[1].getType()
            if arg1 == 'string':
                self.isStr(arguments[1].getValue())
                strMod = self.checkAndReturnString(arguments[1])
                argValue.append(strMod)
            elif arg1 == 'int':
                number = self.isInt(arguments[1].getValue())
                argValue.append(number)
            elif arg1 == 'bool':
                self.isBool(arguments[1].getValue())
                argValue.append(str(arguments[1].getValue()))
        if arguments[2].getType() == 'var':
            arg2 = self.returnType(arguments[2].getValue())
            if arg2 == 'bool' or arg2 == 'string':
                argValue.append(str(self.returnValue(arguments[2].getValue())))
            else:
                argValue.append(self.returnValue(arguments[2].getValue()))
        else:
            arg2 = arguments[2].getType()
            if arg1 == 'string':
                self.isStr(arguments[2].getValue())
                strMod = self.checkAndReturnString(arguments[2])
                argValue.append(strMod)
            elif arg1 == 'int':
                number = self.isInt(arguments[2].getValue())
                argValue.append(number)
            elif arg1 == 'bool':
                self.isBool(arguments[2].getValue())
                argValue.append(str(arguments[2].getValue()))
        if arg1 != arg2:
            print("ERROR compareTypesOfArguments types are not equal")
            exit(53)
        return argValue


    def isInt(self, value):
        result = self.checkIfValueEqualsType(value, 'int')
        try:
            result = int(result)
            return result
        except ValueError:
            exit(53)

    def isStr(self, value):
        result = self.checkIfValueEqualsType(value, 'string')
        try:
            result = str(result)
            return True
        except ValueError:
            exit(53)

    def isBool(self, value):
        result = self.checkIfValueEqualsType(value, 'bool')
        try:
            result = str(result)
            return True
        except ValueError:
            exit(53)


    # TODO mozna pouzit pro konkatenaci pridat parametr type
    def assignValueToVar(self, variable, value, type):
        name = variable.split('@', 1)
        if re.match(r'^GF@', variable.strip()):
            if self.frames.isVarInGf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInGf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
                exit(54)
        elif re.match(r'^TF@', variable.strip()):
            if self.frames.isVarInTf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInTf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
                exit(54)
        elif re.match(r'^LF@', variable.strip()):
            if self.frames.isVarInLf(name[1]):
                var = Variable(name[1], value, type)
                self.frames.updateVarInLf(name[1], var)
            else:
                print("ERROR cant assign to undefinded variable")
                exit(54)


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
        type = self.returnType(argument)
        if re.match(r'^GF@', argument.strip()):
            var = self.frames.getVarFromGf(name[1])
            if type == 'int':
                return var.getValue()
            else:
                return var.getValue()
        elif re.match(r'^LF@', argument.strip()):
            var = self.frames.getVarFromLf(name[1])
            if type == 'int':
                return var.getValue()
            else:
                return var.getValue()
        elif re.match(r'^TF@', argument.strip()):
            var = self.frames.getVarFromTf(name[1])
            if type == 'int':
                return var.getValue()
            else:
                return var.getValue()


    def checkIfValueEqualsType(self, value, type):
        if type == 'int':
            if value != None:
                try:
                    return int(value)
                except ValueError:
                    print("Value is not int")
                    exit(53)
            else:
                print("ERROR checkifValueEqualsType")
                exit(53)
        elif type == 'string':
            if (len(value.split()) != 1) and (value != ''):
                print("Not a string")
                exit(53)
            #         TODO tady bude check jestli je string valid
            else:
                return value
        elif type == 'bool':
            if value != None:
                if re.match(r'^true$', value.strip()):
                    return 'true'
                elif re.match(r'^false$', value.strip()):
                    return 'false'
                else:
                    print("Not bool checkifValueEqualsType")
                    exit(53)
            else:
                print("ERROR checkifValueEqualsType")
                exit(53)
        else:
            print("ERROR checkifValueEqualsType")
            exit(53)
