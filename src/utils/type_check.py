def type_check(func):
    def wrapper(*args, **kargs):
        args_type = func.__annotations__
        for arg_type in args_type:
            if arg_type in kargs.keys() and not isinstance(kargs[arg_type], args_type[arg_type]):
                raise Exception('ERROR!')

        i = 0
        vars_name = func.__code__.co_varnames
        for var_name in vars_name:
            if i < len(vars_name) and var_name in args_type.keys() and not isinstance(args[i], args_type[var_name]):
                raise Exception(f'Unexpected arguments type in {func.__name__}')
            i += 1

        result = func(*args, **kargs)
        if 'return' in args_type.keys() and args_type['return'] != None and not isinstance(result, args_type['return']):
            raise Exception(f'Unexpected "return" type in {func.__name__}')
        return result
    return wrapper

@type_check
def f1(x : int, y : str) -> str:
    return y * x

@type_check
def f2(name : str) -> None:
    print(f'hello {name}')

# print(f1(3, '8'))
# f2('ariel')