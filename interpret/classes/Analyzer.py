import xml.etree.ElementTree as ET
from .Instruction import Instruction
from .Argument import Argument

"""
kontroluje zda nema XML soubor chybny format, dale provadi zakladni lexikalni a 
syntaktickou analyzu vstupniho souboru
"""
class Analyzer:
    """
    @:argument file - vstupni soubor
    konstruktor vytvori dictionaryOfOpcodes(slovnik operacnich kodu), kde jsou na
    pozici klice ulozeny nazvy operacnich kodu, ktere mohou instrukce obsahovat
    a na pozici hodnoty pocet argumentu, ktere maji instrukce s danym operacnim kodem obsahovat
    """
    def __init__(self, file):
        self.file = file
        self.dictionary_of_opcodes = {'MOVE': 2, 'CREATEFRAME': 0, 'PUSHFRAME': 0, 'DEFVAR': 1, 'CALL': 1,
                         'RETURN': 0, 'PUSHS': 1, 'POPS': 1, 'ADD': 3, 'SUB': 3, 'MUL': 3,
                         'IDIV': 3, 'LT': 3, 'GT': 3, 'EQ': 3, 'AND': 3, 'OR': 3, 'NOT': 2,
                         'INT2CHAR': 2, 'STRI2INT': 3, 'READ': 2, 'WRITE': 1, 'CONCAT': 3,
                         'STRLEN': 2, 'GETCHAR': 3, 'SETCHAR': 3, 'TYPE': 2, 'LABEL': 1,
                         'JUMP': 1, 'JUMPIFEQ': 3, 'JUMPIFNEQ': 3, 'DPRINT': 1, 'BREAK': 0,
                                      'POPFRAME': 0}
        self.dictionary_of_commands = {}

    """
    @:return dictionaryOfCommands - slovnik, ve kterem jsou ulozeny jednotlive prikazy
    """
    def analyze_xml_file(self):
        root = self.get_root()
        self.check_root(root)
        self.check_elements(root)
        return self.dictionary_of_commands
    """
    @:return tree.getroot() - korenovy element
    provede analyzu vstupniho souboru a vrati korenovy element XML souboru
    """
    def get_root(self):
        try:
            tree = ET.parse(self.file)
            return tree.getroot()
        except Exception as ex:
            print(type(ex))
            print(ex)
            exit(31)
    """
    @:argument root - korenovy element
    provadi kontrolu zda ma korenovy element pozadovanou znacku a pokud ano zavola
    funkci ktera provede kontrolu atributu korenu
    """
    def check_root(self, root):
        if root.tag == 'program':
            self.check_root_attributes(root)
        else:
            exit(31)
    """
    @:argument root - korenovy element
    provadi kontrolu atributu korenu
    """
    def check_root_attributes(self, root):
        if (len(root.attrib) >= 1) and (len(root.attrib)) <= 3:
            is_language = False
            for key, value in root.attrib.items():
                if key == 'language':
                    is_language = True
                    self.check_language(value)
                elif key == 'name' or key == 'description':
                    continue
                else:
                    print("Error check_root_attributes")
                    exit(31)
            if not is_language:
                print("Error check_root_attributes")
                exit(31)
        else:
            print("Error check_root_attributes")
            exit(31)
    """
    @:argument value - hodnota prirazena atributu language
    provede kontrolu jestli ma atribut language spravnou hodnotu
    """
    def check_language(self, value):
        if (value != "IPPcode18"):
            print("Error check_language")
            exit(31)

    """
    @:argument root - korenovy element
    provede kontrolu zda ma podelement spravnou znacku a pokud ano
    je zavolana funkce, ktera provede vytvoreni instrukce
    """
    def check_elements(self, root):
        for child in root:
            if child.tag == 'instruction':
                self.create_instruction(child)
            else:
                print("Error check_elements")
                exit(31)
    """
    @:argument instruction - podelement korenoveho elementu reprezentujici instrukci
    zavola funkci, ktera provede kontrolu atributu elementu instruction, dale provede kontrolu
    znacek jednotlivych podelementu elemntu instruction a vytvori jejich reprezentaci
    """
    def create_instruction(self, instruction):
        self.check_instruction_attributes(instruction)
        new_instruction = Instruction(instruction.get('opcode'));
        if len(instruction) == self.dictionary_of_opcodes.get(instruction.get('opcode')):
            position_of_arg = 1
            for child in instruction:
                if child.tag == 'arg'+str(position_of_arg):
                    argument = Argument(child.get('type'), child.text)
                    new_instruction.set_argument(argument)
                    position_of_arg += 1
                else:
                    print("Error create_instruction")
                    exit(31)
        else:
            print("Error create_instruction")
            exit(32)
        self.check_arguments_validity(new_instruction)
        self.add_to_dictionary_of_commands(new_instruction, instruction)
    """
    @:argument instruction - objekt Instruction
    provede kontrolu zda jednotlive typy argumentu odpovidaji dane instrukci 
    """
    def check_arguments_validity(self, instruction):
        op_code = instruction.get_opcode()
        list_of_args = instruction.get_list_of_arguments()
        if(op_code == 'CREATEFRAME' or op_code == 'PUSHFRAME' or op_code == 'POPFRAME' or
        op_code == 'RETURN' or op_code == 'BREAK'):
            return
        elif (op_code == 'MOVE' or op_code == 'INT2CHAR' or op_code == 'STRLEN' or op_code == 'TYPE' or
            op_code == 'NOT'):
            if list_of_args[0].get_type() != 'var' or (list_of_args[1].get_type() != 'var' and
                                                       list_of_args[1].get_type() != 'string' and list_of_args[1].get_type() != 'int' and
                                                       list_of_args[1].get_type() != 'bool'):
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'DEFVAR' or op_code == 'POPS':
            if list_of_args[0].get_type() != 'var':
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'LABEL':
            if list_of_args[0].get_type() != 'label':
                print("Error check_arguments_validity")
                exit(32)
        elif (op_code == 'ADD' or op_code == 'SUB' or op_code == 'MUL' or op_code == 'IDIV' or
        op_code == 'LT' or op_code == 'GT' or op_code == 'EQ' or op_code == 'AND' or op_code == 'OR' or
        op_code == 'STRI2INT' or op_code == 'CONCAT' or op_code == 'GETCHAR' or
        op_code == 'SETCHAR'):
            if (list_of_args[0].get_type() != 'var' or (list_of_args[1].get_type() != 'var' and
                                                        list_of_args[1].get_type() != 'string' and list_of_args[1].get_type() != 'int' and
                                                        list_of_args[1].get_type() != 'bool') or (list_of_args[2].get_type() != 'var' and
                                                                                                  list_of_args[2].get_type() != 'string' and list_of_args[2].get_type() != 'int' and
                                                                                                  list_of_args[2].get_type() != 'bool')):
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'READ':
            if list_of_args[0].get_type() != 'var' or list_of_args[1].get_type() != 'type':
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'WRITE' or op_code == 'DPRINT' or op_code == 'PUSHS':
            if(list_of_args[0].get_type() != 'var' and list_of_args[0].get_type() != 'string' and
             list_of_args[0].get_type() != 'int' and list_of_args[0].get_type() != 'bool'):
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'LABEL' or op_code == 'JUMP' or op_code == 'CALL':
            if list_of_args[0].get_type() != 'label':
                print("Error check_arguments_validity")
                exit(32)
        elif op_code == 'JUMPIFEQ' or op_code == 'JUMPIFNEQ':
            if(list_of_args[0].get_type() != 'label' or (list_of_args[1].get_type() != 'var' and
                                                         list_of_args[1].get_type() != 'string' and list_of_args[1].get_type() != 'int' and
                                                         list_of_args[1].get_type() != 'bool') or (list_of_args[2].get_type() != 'var' and
                                                                                                   list_of_args[2].get_type() != 'string' and list_of_args[2].get_type() != 'int' and
                                                                                                   list_of_args[2].get_type() != 'bool')):
                print("Error check_arguments_validity")
                exit(32)
        else:
            print("Error check_arguments_validity")
            exit(32)

    """
    @:argument new_instruction - objekt Instruction
    @:argument instruction - podelementu korenoveho elementu
    prida novy prikaz do slovniku prikazu
    """
    def add_to_dictionary_of_commands(self, new_instruction, instruction):
        self.dictionary_of_commands.update({instruction.get('order'): new_instruction})
    """
    @:argument instruction - podelement korenove elementu
    provede kontrolu jednotlivych atributu elementu instruction 
    """
    def check_instruction_attributes(self, instruction):
        if (len(instruction.attrib) >= 2) and (len(instruction.attrib)) <= 4:
            is_order = False
            is_opcode = False
            for key, value in instruction.attrib.items():
                if key == 'order':
                    is_order = True
                    if instruction.get('order') == str(0):
                        print("Error check_instruction_attributes order == 0")
                        exit(32)
                elif key == 'opcode':
                    is_opcode = True
                    self.check_opcode(value)
                elif key == 'name' or key == 'description':
                    continue
                else:
                    print("Error check_instruction_attributes")
                    exit(31)
            if not is_order and not is_opcode:
                print("Error check_instruction_attributes")
                exit(31)
        else:
            print("Error check_instruction_attributes")
            exit(31)
    """
    @:argument value - hodnota operacniho kodu
    provede kontrolu zda je operacni kod validni 
    """
    def check_opcode(self, value):
        for key in self.dictionary_of_opcodes:
            if key == value:
                return
        print("Error check_opcode")
        exit(32)
