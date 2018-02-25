"""
reprezentuje jednotlive instrukce, obsahuje operacni kod a list argumentu
"""
class Instruction:
    """
    @:argument opcode - operacni kod
    """
    def __init__(self, opcode):
        self.opcode = opcode
        self.list_of_arguments = []
    """
    @:return opcode - operacni kod
    vrati operacni kod instrukce
    """
    def get_opcode(self):
        return self.opcode
    """
    @:return list_of_arguments - list argumentu
    vrati list obsahujici jednotlive argumenty
    """
    def get_list_of_arguments(self):
        return self.list_of_arguments
    """
    @:argument argument - objekt Argument
    prida argument do listu argumentu
    """
    def set_argument(self, argument):
        self.list_of_arguments.append(argument)
    """
    @:return int
    vrati pocet argumentu ulozenych v listu argumentu
    """
    def get_number_of_arguments(self):
        return len(self.list_of_arguments)
