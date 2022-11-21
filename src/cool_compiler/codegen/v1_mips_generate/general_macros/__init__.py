_list = ['int', 'bool', 'str']

def sys_macro_load():
    result = ''

    for _type in _list:
        with open(f'cool_compiler/codegen/v1_mips_generate/general_macros//{_type}.mips') as mips:
            text = mips.read()
            mips.close()
            result += text[text.index('#region'): text.index('#endregion')]

    return result
        

