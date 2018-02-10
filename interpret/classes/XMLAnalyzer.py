import xml.etree.ElementTree as ET

class XMLAnalyzer:
    def __init__(self, file):
        self.file = file

    def analyzeXmlFile(self):
        root = self.getRoot()
        self.checkRoot(root)

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
            print("good")
            isLanguage = False
            isName = False
            isDescription = False
            for key, value in root.attrib.items():
                if key == 'language' and not isLanguage:
                    isLanguage = True
                    if(value != "IPPcode18"):
                        exit(420)
                elif key == 'name' and not isName:
                    isName = True
                elif key == 'description' and not isDescription:
                    isDescription = True
                else:
                    print("Error checkRootAtributes")
                    exit(420)
            if not isLanguage:
                print("Error checkRootAtributes")
                exit(420)
        else:
            print("Error checkRootAtributes")
            exit(420)

    # def checkLanguage(self):

    # def checkElements(self, elements):

    #
    # def checkAttributesOfInstruction(self, attributes):
    #
    # def checkArgumentsOfElement(self, element):
    #
    # def checkAttributesOfArgument(self, argument):
    #
    # def checkTextOfArgument(self, argument):
    #

