class FunctionCall:
    def __init__(self, fun_name, *fun_parameters):
        self.__fun_name = fun_name
        self.__fun_parameters = fun_parameters

    def call(self):
        return self.__fun_name(*self.__fun_parameters)

    def __call__(self, *args, **kwargs):
        return self.call()


class Operation:
    def __init__(self, function_undo: FunctionCall, function_redo: FunctionCall):
        self.__function_undo = function_undo
        self.__function_redo = function_redo

    def undo(self):
        return self.__function_undo()

    def redo(self):
        return self.__function_redo()

class CascadedOperation:

    def __init__(self, operations : list):
        self.__operations = operations

    def undo(self):
        for operation in self.__operations:
            operation.undo()

    def redo(self):
        for operation in self.__operations:
            operation.redo()

class UndoError(Exception):
    pass


class UndoService:
    def __init__(self):
        # history of the program's operations
        self.__history = []
        self.__index = 0

    def record_operation(self, operation: Operation):
        self.__history.append(operation)
        self.__index += 1

    def undo(self):
        if self.__index == 0:
            raise UndoError("No more undos")
        self.__index -= 1
        self.__history[self.__index].undo()

    def redo(self):
        if self.__index >= len(self.__history):
            raise UndoError("No more redos")
        self.__history[self.__index].redo()
        self.__index += 1
