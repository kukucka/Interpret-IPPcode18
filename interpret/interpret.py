import xml.etree.ElementTree as ET

print("Heelllo")
tree = ET.parse('C:\Interpret-IPPcode18\interpret\output.xml')
root = tree.getroot()
for child in root:
     print(child.tag, child.attrib)
for arg1 in root.iter('instruction'):
     print(arg1.attrib)

lol = root.findall("./instruction/arg1")
for ws in lol:
    print(ws)