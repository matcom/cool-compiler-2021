class DNode:
    def setType(self, typex):
        pass
    
class PrimeNode(DNode):
    def __init__(self, typex):
        self.type = typex
        
    def setType(self, new_type):
        self.type = new_type
        
class AttrNode(DNode):
    def __init__(self, typex, attr):
        self.type = typex
        self.attribute = attr
        
    def setType(self, new_type):
        self.type = new_type
        self.attribute.type = new_type
        
class ParamNode(DNode):
    def __init__(self, typex, method, i):
        self.type = typex
        self.index = i
        self.method = method
        
    def setType(self, typex):
        self.type = typex
        self.method.param_types[self.index] = typex
        
class RTypeNode(DNode):
    def __init__(self, typex, method):
        self.type = typex
        self.method = method
    
    def setType(self, typex):
        self.type = typex
        self.method.return_type = typex
        
class VarNode(DNode):   #do not confundir con VariableNode de semantic.py
    def __init__(self, typex, varInfo):
        self.type = typex
        self.varInfo = varInfo
        
    def setType(self, typex):
        self.type = typex
        self.varInfo.type = typex
        
class DGraph:
    def __init__(self):
        self.dependencies = {}
        
    def CreateNode(self, node):
        if node not in self.dependencies:
            self.dependencies[node] = []

    def AddEdge(self,fromNode, toNode):
        try:
            self.dependencies[fromNode].append(toNode)
        except:
            self.dependencies[fromNode] = [toNode]
        
        self.CreateNode(toNode)
        
    def Build(self, objectType):
        # pending = [v for v in self.dependencies.keys() if isinstance(v,PrimeNode)]
        pending = [ ]
        for v in self.dependencies.keys():
            if isinstance(v, PrimeNode):
                pending.append(v)
        
        visited = set()
        
        while pending:
            n = pending[0]
            pending = pending[1:len(pending)]
            
            if n in visited:
                continue
            
            self.UpdateNode(n,visited)
            
        for m in self.dependencies:
            if m not in visited:
                m.setType(objectType)   #object pacasa'e domingo 
        
    def UpdateNode(self, node, visited):
        # pending = [node] + self.dependencies[node]
        pending = [ node ]
        pending.extend(self.dependencies[node])
        
        t = node.type
        while pending:
            n = pending[0]
            pending = pending[1:len(pending)]

            if n in visited:
                continue
            
            n.setType(t)
            visited.add(n)
            pending.extend(self.dependencies[n])