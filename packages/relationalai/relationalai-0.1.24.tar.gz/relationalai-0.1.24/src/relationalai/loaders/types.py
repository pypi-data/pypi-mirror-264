from relationalai.metamodel import Type

Schema = dict[str, Type]

LoadType = str

class UnsupportedTypeError(Exception):
    def __init__(self, message: str, type: str|None = None):
        super().__init__(message)
        self.type = type
