import xml.etree.ElementTree as ET
# pouzit dictionary na ukladani jednotlivych instrukci key = order
# TODO kdyz bude order = 0 je to chyba
class XMLAnalyzer:
    def __init__(self, file):
        self.file = file
        self.listOfOpcodes = {'MOVE': 2, 'CREATEFRAME': 0, 'PUSHFRAME': 0, 'DEFVAR': 1, 'CALL': 1
                         'RETURN': 0, 'PUSHS': 1, 'POPS': 1, 'ADD': 3, 'SUB': 3, 'MUL': 3,
                         'IDIV': 3, 'LT': 3, 'GT': 3, 'EQ': 3, 'AND': 3, 'OR': 3, 'NOT': 3,
                         'INT2CHAR': 2, 'STRI2INT': 3, 'READ': 2, 'WRITE': 1, 'CONCAT': 3,
                         'STRLEN': 2, 'GETCHAR': 3, 'SETCHAR': 3, 'TYPE': 2, 'LABEL': 1,
                         'JUMP': 1, 'JUMPIFEQ': 3, 'JUMPIFNEQ': 3, 'DPRINT': 1, 'BREAK': 0}

    def analyzeXmlFile(self):
        root = self.getRoot()
        self.checkRoot(root)
        self.checkElements(root)

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
                self.checkInstruction(child)
                # self.checkArguments(child)
            else:
                print("Error checkElements")
                exit(420)

    def checkInstruction(self, instruction):
        self.checkInstructionAtributes(instruction)


    def checkInstructionAtributes(self, instruction):
        if (len(instruction.attrib) >= 2) and (len(instruction.attrib)) <= 4:
            isOrder = False
            isOpcode = False
            for key, value in instruction.attrib.items():
                if key == 'order':
                    isOrder = True
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
        print(value)

    #
    # def areArgumentsValid(self):
    #
    # def checkAttributesOfInstruction(self, attributes):
    #
    # def checkArgumentsOfElement(self, element):
    #
    # def checkAttributesOfArgument(self, argument):
    #
    # def checkTextOfArgument(self, argument):
    #

