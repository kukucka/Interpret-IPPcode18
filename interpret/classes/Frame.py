import copy
"""
reprezentuje ramec neboli prostor, do ktereho jsou ukladany promenne
"""
class Frame:
    """
    definuje slovnik promenych
    """
    def __init__(self):
        self.dictionary_of_variables = {}
    """
    @:return dictionary_of_variables - slovnik promenych
    vraci hlubokou kopii slovniku promennych
    """
    def copy_frame(self):
        return copy.deepcopy(self.dictionary_of_variables)
    """
    @:argument dictionary_of_variables - slovnik promennych
    nastavi slovnik promennych na zadany slovnik promennych
    """
    def set_dictionary(self, dictionary_of_variables):
        self.dictionary_of_variables = dictionary_of_variables
    """
    @:argument var - nova promenna
    vlozi promennou var do slovniku promennych jako klic, ale neinicializuje ji
    """
    def add_var_to_dictionary(self, var):
        self.dictionary_of_variables.update({var: None})
    """
    @:argument var - promenna 
    @:argument value - hodnota, ktera ma byt ulozena do promenne
    ulozi do slovniku promennych hodnotu promenne, var slouzi jako klic
    """
    def update_value_of_var(self, var, value):
        self.dictionary_of_variables.update({var: value})
    """
    @:argument var_name - jmeno promenne
    zkontroluje zda je dana promenna ulozena v slovniku promennych
    """
    def is_var_defined(self, var_name):
        if var_name in self.dictionary_of_variables:
           return True
        else:
            print("Error varName, var doesnt exist")
            exit(54)
    """
    @:argument var_name - jmeno hledane promenne
    @:return value - hodnota hledane promenne
    prohleda slovnik promennych a v pripade nalezu pozadovane promenne
    vrati jeji hodnotu
    """
    def find_var(self, var_name):
        if var_name in self.dictionary_of_variables.keys():
            try:
                value = self.dictionary_of_variables.get(var_name)
                if value is None:
                    print("Error varName, var has no value")
                    exit(56)
                return value
            except KeyError:
                print("Error variable, is not initialized")
                exit(56)
        else:
            print("Error varialbe " + var_name + " doesnt exist")
            exit(54)
    """
    @:argument var_name - jmeno promenne
    provede kontrolu zda je dana promenna inicializovana
    """
    def check_if_var_initialized(self, var_name):
        if var_name in self.dictionary_of_variables.keys():
            try:
                value = self.dictionary_of_variables.get(var_name)
                if value is None:
                    return False
                else:
                    return True
            except KeyError:
                print("Error varName, var doesnt exist")
                exit(54)
        else:
            print("Error varialbe " + str(var_name) + " doesnt exist")
            exit(54)
    """
    vymaze obsah slovniku promennych
    """
    def wipe_frame(self):
        self.dictionary_of_variables.clear()
