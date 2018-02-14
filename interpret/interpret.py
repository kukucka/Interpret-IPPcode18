import xml.etree.ElementTree as ET

# TODO poruseni formatu textu, udelat to pres catch?
# TODO je validni kdyz mam napirklad
# TODO replace zase nejaky special znaky z XML
# TODO chytit pripadne error z TE.parse
# TODO zkontrolovat jestli jsou spravne \xxx v interpretu i parseru
from classes.Analyzer import XMLAnalyzer
from classes.Execute import Execute
# print("Heelllo")
# tree = ET.parse('C:\Interpret-IPPcode18\interpret\')
# root = tree.getroot()
file = 'output.xml'
cl = XMLAnalyzer(file)
dicOfVar = cl.analyzeXmlFile()
s = Execute(dicOfVar)
s.start()
#
# tree = ET.parse('output.xml')
# root = tree.getroot()
# for child in root.child:
#     root2 = child
    # print(len(child.attrib))
    # for key,value in child.attrib.items():
    #     print(key + " : " + value)
    # print(child.get('order'))
    # for child in root2:
    #     print(child.attrib)

# root - koren programu tady je to program
# child - tim nactu jednotlive instrukce, kdyzna tu nactenou pouziju znova child dostanu argumenty
# .attrib ukaze atributy daneho elementu
# child.attrib zobrazi jednotlive attributy instrukci
# root.attrib zobrazi elementy korenu
# .tag vypise nazev elementu
# find pro vyhledani
# child.text vypise mi ten text
# .get pres to dostanu hodnotu ulozenou v attributu
# Dictionary je vygenerovanu tim child.attrib,
# na prochazeni slovniku funkce nize
#     for key, value in child.attrib.items():
#         print(key + " : " + value)

#
# with open('output.xml', 'rt') as f:
#     tree = ET.parse(f)
#
# for node in tree.iter():
#     print(node.tag, node.attrib)
#
# # print("Ahoj0")
# # for child in root:
# #      print(child.tag, child.attrib)
# # for arg1 in root.iter('instruction'):
# #      print(arg1.attrib)
# # prin("Ahoj1")
# # lol = root.findall("./instruction/arg1")
# # for ws in lol:
# #     print(ws)
# for elem in tree:
#     print(elem.tag)
#     if elem.text is not None and elem.text.strip():
#         print('  text: "%s"' % elem.text)
#     if elem.tail is not None and elem.tail.strip():
#         print('  tail: "%s"' % elem.tail)
#     for name, value in sorted(elem.attrib.items()):
#         print('  %-4s = "%s"' % (name, value))
#     print