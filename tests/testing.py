
import pathlib
import os

print(os.getcwd() + 'tests\\lexer')
cwd = os.getcwd()
print(pathlib.Path(__file__))
print(pathlib.Path(__file__).parent/"lexer")
tests_dir = str(pathlib.Path(__file__).parent / 'lexer')