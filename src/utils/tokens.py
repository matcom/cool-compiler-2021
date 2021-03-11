reservedKeywords = {
    'class': 'CLASS',
    'inherits': 'INHERITS',
    'if': 'IF',
    'then': 'THEN',
    'else': 'ELSE',
    'fi': 'FI',
    'while': 'WHILE',
    'loop': 'LOOP',
    'pool': 'POOL',
    'let': 'LET',
    'in': 'IN',
    'case': 'CASE',
    'of': 'OF',
    'esac': 'ESAC',
    'new': 'NEW',
    'isvoid': 'ISVOID',
}

literals = ['+', '-', '*', '/', ':', ';', '(', ')', '{', '}', '@', '.', ',']
ignored = [' ', '\f', '\r', '\t', '\v']

tokens = [    
    'TYPE', 'ID', 'INTEGER', 'STRING', 'BOOL', 'ACTION', 'ASSIGN', 'LESS', 'LESSEQUAL', 'EQUAL', 'INT_COMPLEMENT', 'NOT',
] + list(reservedKeywords.values())

