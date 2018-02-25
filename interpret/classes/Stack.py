"""
prototyp zasobniku
"""
class Stack:
    """
    inicializuje prazdne pole
    """
    def __init__(self):
        self.items = []
    """
    @:return boolean
    provede kontrolu zda je zasobnik prazdny
    """
    def is_empty(self):
        return self.items == []
    """
    @:argument item
    vlozi polozku na vrchol zasobniku
    """
    def push(self, item):
        self.items.append(item)
    """
    @:return item
    odstrani polozku z vrcholu zasobniku
    """
    def pop(self):
        return self.items.pop()
    """
    @:return value
    vrati hodnotu polozky z vrcholu zasobniku
    """
    def top(self):
        if len(self.items) == 0:
            return None
        else:
            return self.items[len(self.items) - 1]
    """
    @:return int
    vrati pocet polozek na zasobniku
    """
    def size(self):
        return len(self.items)