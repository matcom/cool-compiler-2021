
def permutation(n,k):
    """
    returns an iter from all permutations in n places of k elements\n
    Ex: n = 2, k = 2\n
    returns [0,0],[0,1],[1,1],[1,0]
    """
    perm = [None]*n
    if n == 0:
        return []
    for t in inner_permutation(perm,0,k,n):
        yield t
    
def inner_permutation(perm,i,k,n):
    for p in range(k):
        perm[i] = p
        if i < n-1:
            for t in inner_permutation(perm,i+1,k,n):
                yield t
        else:
            yield tuple(perm)
