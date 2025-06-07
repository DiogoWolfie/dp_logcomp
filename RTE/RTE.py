class ReturnException(Exception):
    def __init__(self, type_, value):
        super().__init__()
        self.type = type_   # tipo primeiro
        self.value = value  # valor depois