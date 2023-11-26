from cmp.automata import State
class Parser():
    
    def __call__(self,tokens,errors):
        raise NotImplementedError()
    
    def find_conflit(self):
        '''
        return a list of conflicts
        '''
        raise NotImplementedError()
    
    def evaluate(self,tokens,errors,return_ast=False):
        raise NotImplementedError()
    
    def get_derivation_tree(self,parse_list, left_to_right=True):
        if not left_to_right: parse_list.reverse()

        node = State(parse_list[0].Left)
        self.build_tree(node,[0],parse_list,left_to_right)
        return node.graph('TD')
    
    def build_tree(self,current_node, index, parse_list, left_to_right):

        new_nodes = []
        if parse_list[index[0]].Right:
            for x in parse_list[index[0]].Right:
                new_nodes.append(State(x))
        else:
            new_nodes.append(State(parse_list[index[0]].Right))

        if not left_to_right: new_nodes.reverse()

        for x in new_nodes:
            current_node.add_transition('',x)
            if x.state.IsNonTerminal:
                index[0] += 1
                self.build_tree(x,index,parse_list,left_to_right)

        if not left_to_right:
            try:
                current_node.transitions[''].reverse()
            except:
                pass
