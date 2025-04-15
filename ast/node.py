from abc import ABC, abstractmethod

class Node(ABC):
    def __init__(self, value, children):
        self.value = value
        self.children = children

    @abstractmethod
    def Evaluate(self, SymbolTable):
        pass
        
    pass