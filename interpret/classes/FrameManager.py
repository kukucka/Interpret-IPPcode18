import sys

from .Stack import Stack
from .Frame import Frame
"""
slouzi k spravovani vsech ramcu
"""
class FrameManager:
    """
    provede inicializaci vsech ramcu a zasobniku lokalnich ramcu
    """
    def __init__(self):
        self.gf = Frame()
        self.tf = Frame()
        self.lf = Frame()
        self.lf_stack = Stack()
        self.tf_defined = False
        self.lf_defined = False

    """
    @:return tf_defined
    pokud je docasny ramec (tf) definovany vraci True jinak False
    """
    def is_tf_defined(self):
        return self.tf_defined
    """
    @:return lf_defined
    pokud je lokalni ramec (lf) definovany vraci True jinak False
    """
    def is_lf_defined(self):
        return self.lf_defined
    """
    @:argument var - nazev promenne
    prida promenou do slovniku promenych globalniho ramce
    """
    def add_var_to_gf(self, var):
        self.gf.add_var_to_dictionary(var)
    """
    @:argument var - nazev promenne
    prida promenou do slovniku promenych docasneho ramce
    """
    def add_var_to_tf(self, var):
        if self.tf_defined:
            self.tf.add_var_to_dictionary(var)
        else:
            print("ERROR add_var_to_tf")
            exit(55)
    """
    @:argument var - nazev promenne
    prida promenou do slovniku promenych lokalniho ramce
    """
    def add_var_to_lf(self, var):
        if self.lf_defined:
            self.lf.add_var_to_dictionary(var)
        else:
            print("ERROR add_var_to_lf")
            exit(55)

    """
    @:argument var - nazev promenne
    @:argument value - objekt Variable
    aktualizuje hodnotu promenne v globalnim ramci
    """
    def update_var_in_gf(self, var, value):
        self.gf.update_value_of_var(var, value)
    """
    @:argument var - nazev promenne
    @:argument value - objekt Variable
    aktualizuje hodnotu promenne v docasnem ramci
    """
    def update_var_in_tf(self, var, value):
        if self.tf_defined:
            self.tf.update_value_of_var(var, value)
        else:
            print("ERROR update_var_in_tf")
            exit(55)
    """
    @:argument var - nazev promenne
    @:argument value - objekt Variable
    aktualizuje hodnotu promenne v lokalnim ramci
    """
    def update_var_in_lf(self, var, value):
        if self.lf_defined:
            self.lf.update_value_of_var(var, value)
        else:
            print("ERROR update_var_in_lf")
            exit(55)
    """
    @:argument var_name - nazev promenne
    @:return boolean
    provede kontrolu zda promenna lezi v globalnim ramci
    """
    def is_var_in_gf(self, var_name):
        return self.gf.is_var_defined(var_name)
    """
    @:argument var_name - nazev promenne
    @:return boolean
    v pripade ze je docasny ramce definovany provede 
    kontrolu zda promenna lezi v docasnem ramci
    """
    def is_var_in_tf(self, var_name):
        if self.tf_defined:
            return self.tf.is_var_defined(var_name)
        else:
            print("ERROR is_var_in_tf")
            exit(55)
    """
    @:argument var_name - nazev promenne
    @:return boolean
    provede kontrolu zda promenna lezi v lokalnim ramci
    """
    def is_var_in_lf(self, var_name):
        if self.lf_defined:
            return self.lf.is_var_defined(var_name)
        else:
            print("ERROR is_var_in_lf")
            exit(55)
    """
    @:argument var - jmeno promenne
    @:return objekt Variable
    prohleda globalni ramce a vrati hodnotu, ktera ma klic var 
    """
    def get_var_from_gf(self, var):
        return self.gf.find_var(var)
    """
    @:argument var - jmeno promenne
    @:return objekt Variable
    v pripade ze je docasny ramec definovany prohleda ho
    a vrati hodnotu, ktera ma klic var 
    """
    def get_var_from_tf(self, var):
        if self.tf_defined:
            return self.tf.find_var(var)
        else:
            print("ERROR get_var_from_tf")
            exit(55)

        return self.tf.find_var(var)
    """
    @:argument var - jmeno promenne
    @:return objekt Variable
    v pripade ze je lokalni ramec definovany prohleda ho
    a vrati hodnotu, ktera ma klic var 
    """
    def get_var_from_lf(self, var):
        if self.lf_defined:
            return self.lf.find_var(var)
        else:
            print("ERROR get_var_from_lf")
            exit(55)
    """
    ulozi kopii docasneho ramce(tf) na vrchol zasobniku ramcu
    pote ho vymaze cimz docasny ramec zanikne ale vznikne novy
    lokalni ramec
    """
    def push_tf_to_lf_stack(self):
        self.lf_stack.push(self.tf.copy_frame())
        self.lf.set_dictionary(self.lf_stack.top())
        self.tf.wipe_frame()
        self.tf_defined = False
        self.lf_defined = True
    """
    vytvori novy prazdny docasny ramec
    """
    def create_tf(self):
        self.tf.wipe_frame()
        self.tf_defined = True
    """
    odstrani lokalni ramec z vrcholu zasobniku a presune ho do docasneho ramce
    """
    def pop_from_lf_stack(self):
        if(self.lf_stack.is_empty()):
            print("Error Empty stack")
            exit(55)
        self.tf.set_dictionary(self.lf_stack.pop())
        if self.lf_stack.is_empty():
            self.lf_defined = False
        self.tf_defined = True
        self.lf.set_dictionary(self.lf_stack.top())
    """
    @:argument var_name - jmeno promenne
    @:return boolean
    zjisti jestli je promenna v globalnim ramci inicializovana
    """
    def checkIfVarInitInGf(self, varName):
        return self.gf.check_if_var_initialized(varName)
    """
    @:argument var_name - jmeno promenne
    @:return boolean
    zjisti jestli je promenna v lokalnim ramci inicializovana
    """
    def checkIfVarInitInLf(self, varName):
        return self.lf.check_if_var_initialized(varName)
    """
    @:argument var_name - jmeno promenne
    @:return boolean
    zjisti jestli je promenna v docasnem ramci inicializovana
    """
    def checkIfVarInitInTf(self, varName):
        return self.tf.check_if_var_initialized(varName)


    # FOR BREAK
    """
    vypise vsechny promenne obsazene v globalnim ramci na chybovy vystup
    """
    def returnGfFrame(self):
        copyOfGf = self.gf.copy_frame()
        for key, value in copyOfGf.items():
            if self.gf.check_if_var_initialized(key):
                sys.stderr.write("Variable " + str(value.get_name()) + " has type " + str(value.get_type()) + " and value of " + str(value.get_value()) + "\n")
            else:
                sys.stderr.write("Variable "+ str(key) + " is not initialized\n")
    """
    vypise vsechny promenne obsazene v docasnem ramci na chybovy vystup
    """
    def returnTfFrame(self):
        if self.tf_defined == True:
            copyOfTf = self.tf.copy_frame()
            for key, value in copyOfTf.items():
                if self.tf.check_if_var_initialized(key):
                    sys.stderr.write("Variable " + str(value.get_name()) + " has type " + str(
                        value.get_type()) + " and value of " + str(value.get_value()) + "\n")
                else:
                    sys.stderr.write("Variable " + str(key) + " is not initialized\n")
        else:
            sys.stderr.write("Temporary frame not defined.\n")
    """
    vypise vsechny promenne obsazene v lokalnim ramci na chybovy vystup
    """
    def returnLfFrame(self):
        if self.lf_defined == True:
            copyOfLf = self.lf.copy_frame()
            for key, value in copyOfLf.items():
                if self.lf.check_if_var_initialized(key):
                    sys.stderr.write("Variable " + str(value.get_name()) + " has type " + str(
                        value.get_type()) + " and value of " + str(value.get_value()) + "\n")
                else:
                    sys.stderr.write("Variable " + str(key) + " is not initialized\n")
        else:
            sys.stderr.write("Local frame not defined.\n")

    #FOR EXTENSION
    """
    @:return num - pocet promennych v globalnim ramci
    """
    def returnGfNumberOfVar(self):
        list = self.gf.copy_frame()
        num = 0
        for key,value in list.items():
            if self.gf.check_if_var_initialized(key):
                num += 1
        return num
    """
    @:return num - pocet promennych v docasnem ramci
    v pripade ze docasnu ramec neni definovany vrati se 0
    """
    def returnTfNumberOfVar(self):
        if self.tf_defined == True:
            list = self.tf.copy_frame()
            num = 0
            for key,value in list.items():
                if self.tf.check_if_var_initialized(key):
                    num += 1
            return num
        else:
            return 0
    """
    @:return num - pocet promennych v lokalnim ramci
    v pripade ze lokalni ramec neni definovany vrati se 0
    """
    def returnLfNumberOfVar(self):
        if self.lf_defined == True:
            list = self.lf.copy_frame()
            num = 0
            for key,value in list.items():
                if self.lf.check_if_var_initialized(key):
                    num += 1
            return num

        else:
            return 0