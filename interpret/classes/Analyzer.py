import xml.etree.ElementTree as ET
from .Instruction import Instruction
from .Argument import Argument

# pouzit dictionary na ukladani jednotlivych instrukci key = order
# TODO kdyz bude order = 0 je to chyba
# TODO prejmenovat na parser
# TODO checknout zda text obsahuje white space?
# TODO za GF@ neni nic prazdno
class XMLAnalyzer:
    def __init__(self, file):
        self.file = file
        self.dictionaryOfOpcodes = {'MOVE': 2, 'CREATEFRAME': 0, 'PUSHFRAME': 0, 'DEFVAR': 1, 'CALL': 1,
                         'RETURN': 0, 'PUSHS': 1, 'POPS': 1, 'ADD': 3, 'SUB': 3, 'MUL': 3,
                         'IDIV': 3, 'LT': 3, 'GT': 3, 'EQ': 3, 'AND': 3, 'OR': 3, 'NOT': 2,
                         'INT2CHAR': 2, 'STRI2INT': 3, 'READ': 2, 'WRITE': 1, 'CONCAT': 3,
                         'STRLEN': 2, 'GETCHAR': 3, 'SETCHAR': 3, 'TYPE': 2, 'LABEL': 1,
                         'JUMP': 1, 'JUMPIFEQ': 3, 'JUMPIFNEQ': 3, 'DPRINT': 1, 'BREAK': 0,
                         'POPFRAME': 0}
        self.dictionaryOfCommands = {}


    def analyzeXmlFile(self):
        root = self.getRoot()
        self.checkRoot(root)
        self.checkElements(root)
        return self.dictionaryOfCommands

    def getRoot(self):
        tree = ET.parse(self.file)
        return tree.getroot()

    def checkRoot(self, root):
        if root.tag == 'program':
            print("program equals")
            self.checkRootAtributes(root)
        else:
            exit(420)

    def checkRootAtributes(self, root):
        if (len(root.attrib) >= 1) and (len(root.attrib)) <= 3:
            isLanguage = False
            for key, value in root.attrib.items():
                if key == 'language':
                    isLanguage = True
                    self.checkLanguage(value)
                elif key == 'name' or key == 'description':
                    continue
                else:
                    print("Error checkRootAtributes")
                    exit(420)
            if not isLanguage:
                print("Error checkRootAtributes")
                exit(420)
        else:
            print("Error checkRootAtributes")
            exit(420)

    def checkLanguage(self, value):
        if (value != "IPPcode18"):
            print("Error checkLanguage")
            exit(420)


    def checkElements(self, root):
        for child in root:
            if child.tag == 'instruction':
                self.createInstruction(child)
                # self.checkArguments(child)
            else:
                print("Error checkElements")
                exit(420)

    def createInstruction(self, instruction):
        self.checkInstructionAtributes(instruction)
        newInstruction = Instruction(instruction.get('opcode'));
        if len(instruction) == self.dictionaryOfOpcodes.get(instruction.get('opcode')):
            positionOfArg = 1
            for child in instruction:
                if child.tag == 'arg'+str(positionOfArg):
                    argument = Argument(child.get('type'), child.text)
                    # print(argument.getType() + " " + argument.getValue())
                    newInstruction.setArgument(argument)
                    positionOfArg += 1
                else:
                    print("Error createInstruction")
                    exit(420)
        else:
            print("Error createInstruction")
            exit(420)
        # self.checkArguments(newInstruction)
        self.checkArgumentsValidy(newInstruction)
        self.addToDictionaryOfCommands(newInstruction, instruction)
        # newInstruction.setArgument()

    def checkArgumentsValidy(self, instruction):
        opCode = instruction.getOpcode()
        numOfArgs = instruction.getNumberOfArguments()
        listOfArgs = instruction.getListOfArguments()
        print(opCode + " " + str(numOfArgs))
        if(opCode == 'CREATEFRAME' or opCode == 'PUSHFRAME' or opCode == 'POPFRAME' or
        opCode == 'RETURN' or opCode == 'BREAK'):
            return
        elif (opCode == 'MOVE' or opCode == 'INT2CHAR' or opCode == 'STRLEN' or opCode == 'TYPE' or
            opCode == 'NOT'):
            if listOfArgs[0].getType() != 'var' or (listOfArgs[1].getType() != 'var' and
            listOfArgs[1].getType() != 'string' and listOfArgs[1].getType() != 'int' and
            listOfArgs[1].getType() != 'bool'):
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'DEFVAR' or opCode == 'POPS':
            if listOfArgs[0].getType() != 'var':
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'LABEL':
            if listOfArgs[0].getType() != 'label':
                print("Error checkArgumentsValidy")
                exit(420)
        elif (opCode == 'ADD' or opCode == 'SUB' or opCode == 'MUL' or opCode == 'IDIV' or
        opCode == 'LT' or opCode == 'GT' or opCode == 'EQ' or opCode == 'AND' or opCode == 'OR' or
        opCode == 'STRI2INT' or opCode == 'CONCAT' or opCode == 'GETCHAR' or
        opCode == 'SETCHAR'):
            if (listOfArgs[0].getType() != 'var' or (listOfArgs[1].getType() != 'var' and
            listOfArgs[1].getType() != 'string' and listOfArgs[1].getType() != 'int' and
            listOfArgs[1].getType() != 'bool') or (listOfArgs[2].getType() != 'var' and
            listOfArgs[2].getType() != 'string' and listOfArgs[2].getType() != 'int' and
            listOfArgs[2].getType() != 'bool')):
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'READ':
            if (listOfArgs[0].getType() != 'var' or (listOfArgs[1].getType() != 'string' and
            listOfArgs[1].getType() != 'int' and listOfArgs[1].getType() != 'bool')):
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'WRITE' or opCode == 'DPRINT' or opCode == 'PUSHS':
            if(listOfArgs[0].getType() != 'var' and listOfArgs[0].getType() != 'string' and
             listOfArgs[0].getType() != 'int' and listOfArgs[0].getType() != 'bool'):
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'LABEL' or opCode == 'JUMP':
            if listOfArgs[0].getType() != 'label':
                print("Error checkArgumentsValidy")
                exit(420)
        elif opCode == 'JUMPIFEQ' or opCode == 'JUMPIFNEQ':
            if(listOfArgs[0].getType() != 'label' or (listOfArgs[1].getType() != 'var' and
            listOfArgs[1].getType() != 'string' and listOfArgs[1].getType() != 'int' and
            listOfArgs[1].getType() != 'bool') or (listOfArgs[2].getType() != 'var' and
            listOfArgs[2].getType() != 'string' and listOfArgs[2].getType() != 'int' and
            listOfArgs[2].getType() != 'bool')):
                print("Error checkArgumentsValidy")
                exit(420)
        else:
            print("Error checkArgumentsValidy")
            exit(420)

    def addToDictionaryOfCommands(self, newInstruction, instruction):
        self.dictionaryOfCommands.update({instruction.get('order'): newInstruction})
        # print(self.dictionaryOfCommands)

    def checkInstructionAtributes(self, instruction):
        if (len(instruction.attrib) >= 2) and (len(instruction.attrib)) <= 4:
            isOrder = False
            isOpcode = False
            for key, value in instruction.attrib.items():
                if key == 'order':
                    isOrder = True
                    if instruction.get('order') == str(0):
                        print("Error checkInstructionAtributes order == 0")
                        exit(420)
                elif key == 'opcode':
                    isOpcode = True
                    self.checkOpcode(value)
                elif key == 'name' or key == 'description':
                    continue
                else:
                    print("Error checkInstructionAtributes")
                    exit(420)
            if not isOrder and not isOpcode:
                print("Error checkInstructionAtributes")
                exit(420)
        else:
            print("Error checkInstructionAtributes")
            exit(420)

    def checkOpcode(self, value):
        for key in self.dictionaryOfOpcodes:
            if key == value:
                return
        print("Error checkOpcode")
        exit(420)

    #
    #
    # def checkAttributesOfInstruction(self, attributes):
    #
    # def checkArgumentsOfElement(self, element):
    #
    # def checkAttributesOfArgument(self, argument):
    #
    # def checkTextOfArgument(self, argument):
    #

