from typing import Callable

class Pipe:
    def __init__(self, pipe_func:Callable[[object],object], pipe_check:Callable[[object],bool]=None):
        """
        pipe_func: callable that recieve an argument and return a value  
        pipe_check: callable that recieve an argument and return if the pipe can be executed
        """
        self.func = pipe_func
        if pipe_check:
            self.check = pipe_check
        else:
            self.check = lambda x: True

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def can_execute(self, dictionary):
        return self.check(dictionary)

class Pipeline(Pipe):
    
    def __init__(self, *pipes):
        super().__init__(self.__call__)
        self.pipes = [pipe for pipe in pipes]
    
    def __call__(self, *args, **kwargs):
        start_pipe = self.pipes[0]
        
        result = start_pipe(*args, **kwargs)
        
        for pipe in self.pipes[1:]:
            if pipe.can_execute(result):
                result = pipe(result)
            else:
                break
        
        return result

