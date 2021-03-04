"""
Cool pipes package
"""

from typing import List
from cool_cmp.shared.pipeline.pipes import *

class IPipeable:

    @property
    def name(self)->str:
        raise NotImplementedError()

    def __call__(self, arg):
        raise NotImplementedError()

class PipeResult:
    """
    Class that should return all Cool pipelines  
    Defines a last property that returns the last object setted as an atribute
    """

    def __init__(self):
        self.last = None

    def __setattr__(self, name:str, value):
        if name != "last":
            self.last = value
        super().__setattr__(name, value)

    def __str__(self):
        result = "PipeResult:\n"
        for attr in self.__dict__.keys():
            result += f"    {attr}\n"
        return result

class InterfacePipeline(Pipeline):

    def __init__(self, pipeline:'InterfacePipeline', *interfaces:List[IPipeable]):

        def make_pipe(result:PipeResult, interface:IPipeable):
            returned = interface(result.last)
            result.__setattr__(interface.name, returned)
            return result

        pipes = []
        for interface in interfaces:
            pipes.append(Pipe(lambda x, y=interface: make_pipe(x,y)))
        if pipeline:
            super().__init__(pipeline, *pipes)
        else:
            super().__init__(*pipes)