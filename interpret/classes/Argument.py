"""
reprezentuje jednotlive argumenty, obsahuje typ a hodnotu argumentu
"""
class Argument:
    """
    @:argument type - typ argumentu
    @:argument value - hodnota argumentu
    """
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.check_if_value_is_none()

    """
    @:return type - typ argumentu
    vrati typ argumentu
    """
    def get_type(self):
        return self.type
    """
    @:return value - hodnora argumentu
    vrati hodnotu argumentu
    """
    def get_value(self):
        return self.value

    """
    pro pripad ze je zadan prazdny retezec je jeho originalni hodnota None 
    nahrazena ''
    """
    def check_if_value_is_none(self):
        if self.type == 'string':
            if self.value == None:
                self.value = ''
