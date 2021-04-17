class TrieNode():
    
    sons = None
    value = None
    terminal = None
    
    def __init__(self,value,terminal = False,sons = []):
        self.value = value
        self.sons = {}
        self.terminal = terminal
        for x in sons:
            self.add_son(x)
    
    def add_son(self,item):
        assert isinstance(item,TrieNode), "item must be a TrieNode"
        self.sons[item.value] = item

    def find_son(self,son_value):
        return self.sons[son_value]
    
    def __iter__(self):
        yield self
        for x in self.sons:
            for y in self.sons[x]:
                yield y
    
    def __str__(self):
        rep = f'{self.value}['
        for x in self.sons:
            rep += f'{self.sons[x]},'
        rep += ']\n'
        return rep

class Trie:
    top = None
    
    def __init__(self):
        self.top = TrieNode('^')
    
    def LCP(self, item):
        current = self.top
        idx = 0
        for x in item:
            try:
                current = current.find_son(x)
                idx += 1
            except KeyError:
                break
        return current,idx
    
    def add(self,item):
        where_to,from_this = self.LCP(item)
        for x in item[from_this:]:
            new = TrieNode(x)
            where_to.add_son(new)
            where_to = new
        where_to.terminal = True
    
    def __str__(self):
        return str(self.top)
    
    def __iter__(self):
        return self.top.__iter__()