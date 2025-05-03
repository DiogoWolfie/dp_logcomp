from abc import ABC, abstractmethod

class Node(ABC):
    id = 0
    def generate_id() -> int:
        Node.id += 1
        return Node.id
    
    def __init__(self, value, children):
        self.value = value
        self.children = children
        self.id = Node.generate_id()

    @abstractmethod
    def Evaluate(self, SymbolTable):
        pass
        
    @abstractmethod
    def Generate(self, SymbolTable) -> None:
        pass
    pass
   