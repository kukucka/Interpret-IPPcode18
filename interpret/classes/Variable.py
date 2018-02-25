"""
reprezentuje jednotlive promenne, obsahuje jmeno, hodnotu a typ
"""
class Variable:
    """
    @:argument name - jmeno promenne
    @:argument value - hodnota promenne
    @:argument type - typ promenne
    """
    def __init__(self, name, value, type):
        self.name = name
        self.value = value
        self.type = type
    """
    @:return type - typ promenne
    vrati typ promenne
    """
    def get_type(self):
        return self.type
    """
    @:return value - hodnota promenne
    vrati hodnotu promenne
    """
    def get_value(self):
        return self.value
    """
    @:return name - jmeno promenne
    vrati jmeno promenne
    """
    def get_name(self):
        return self.name
    """
    @:argument value - hodnota promenne
    nastavi hodnotu promenne
    """
    def set_value(self, value):
        self.value = value
    """
    @:argument type - typ promenne
    nastavi typ promenne
    """
    def set_type(self, type):
        self.type = type


