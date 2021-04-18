"""
Shared code between packages
"""

from cool_cmp.shared.pipeline import IPipeable, Pipe, Pipeline
from cool_cmp.shared.errors import ErrorTracker, IErrorTraceable, CoolError
from typing import List, Dict

class ICoolService(IErrorTraceable, IPipeable):
    """
    Interface that should implement all parts of the cool pipeline
    """
    
    def __call__(self, arg:object, context:Dict[str,object]):
        raise NotImplementedError()
    
    def add_extra_info(self, key:str, value:object):
        """
        Add extra information that will be pass to all following CoolServices
        """
        if not hasattr(self, "_extra"):
            self._extra = {}
        self._extra[key] = value
    
    def get_extra_info(self) -> Dict[str,object]:
        """
        Get current extra information
        """
        if not hasattr(self, "_extra"):
            self._extra = {}
        return self._extra
        

class SymbolTable(IErrorTraceable):
    """
    Class that should return all Cool pipelines  
    It holds all the shared information between stages
    Defines a last property that returns the last object setted as an atribute
    """

    def __init__(self):
        self.last = None
        self.context = {}
        self.__errors = ErrorTracker()

    def __setattr__(self, name:str, value):
        if name != "last":
            self.last = value
        super().__setattr__(name, value)

    def add_error(self, error:CoolError):
        self.__errors.add_error(error)

    def get_errors(self)->List[CoolError]:
        return self.__errors.get_errors()

    def __str__(self):
        result = "SymbolTable:\n"
        for attr in self.__dict__.keys():
            result += f"    {attr}\n"
        return result


class InterfacePipeline(Pipeline):

    def __init__(self, pipeline:'InterfacePipeline', *interfaces:List[ICoolService]):

        def make_pipe(result:SymbolTable, interface:ICoolService):
            returned = interface(result.last, result.context.copy())
            for error in interface.get_errors():
                result.add_error(error)
            result.__setattr__(interface.name, returned)
            result.context.update(interface.get_extra_info())
            return result

        pipes = []
        for interface in interfaces:
            pipes.append(Pipe(lambda x, y=interface: make_pipe(x,y)))
        if pipeline:
            super().__init__(pipeline, *pipes)
        else:
            super().__init__(*pipes)