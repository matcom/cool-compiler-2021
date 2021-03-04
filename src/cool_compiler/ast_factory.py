from enum import Enum

class KeyNameNode(Enum):
    kclass = "class" 

# interface to create ast nodes
# and decouple the grammar of these nodes 
class AstFactory:
    def __init__(self, dict_knn_ast_node : dict = {}):
        self.__dict = dict_knn_ast_node

    def __call__(self, key_name_node : str ) : 
        return self.Builder(key_name_node, self.__dict)
    
    class Builder:
        def __init__(self, knn, dicc):
            self.knn = knn
            self.dicc = dicc

        # synteticed is a list with tokens and nodes 
        def build(self, synteticed_list : list):
            return self.dicc[self.knn](synteticed_list)

   
