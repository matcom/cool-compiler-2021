from soupsieve import select


class MIPS_Node:
    pass


class ProgramNode(MIPS_Node):
    def __init__(self, data, code):
        self.data = data
        self.text = code

class MIPSDataNode(MIPS_Node):
        pass
    
class MIPSInstructionNode(MIPS_Node):
        pass
    
class DataTransferNode(MIPSInstructionNode):
    pass

class ProcedureNode(MIPSInstructionNode):
    def __init__(self, label):
        self.label = label
        self.instructions = []



class DataTransferWithOffset(DataTransferNode):
    def __init__(self,source,offset,dest):
        self.source = source
        self.offset = offset
        self.destination = dest
        
class LoadWordNode(DataTransferWithOffset):
    def __str__(self):
        return f'lw {self.source}, {str(self.offset)}({self.destination})'
        
class StoreWordNode(DataTransferWithOffset):
    def __str__(self):
        return f'sw {self.source}, {str(self.offset)}({self.destination})'
    
class LoadNode(DataTransferNode):
    def __init__(self,dest,value):
        self.destination = dest
        self.value

class LoadInmediate(LoadNode):
    def __str__(self):
        return f'li {self.destination}, {self.value}'

class LoadAddress(LoadNode):
    def __str__(self):
        return f'la {self.destination}, {self.value}'

class MoveNode(DataTransferNode):
    def __init__(self, destination, source):
        self.destination = destination
        self.source = source

    def __str__(self):
        return f"move {self.destination} {self.source}"



        


class DataTypeNode(MIPSDataNode):
    def __init__(self, name, datatype,vt_values):
        self.name = name
        self.datatype = datatype
        self.vt_values = vt_values

    def __str__(self):
        values = ""
        for value in self.vt_values:
            values += f", {value}"
        return f"{self.name} : {self.datatype}{values}"
    
class CommentNode(MIPS_Node):
    def __init__(self,text):
        self.text = text
    
    def __str__(self):
        return f"#{self.text}"