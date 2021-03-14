import os
import sys
import subprocess

input_file = sys.argv[1].replace('\\', '\\\\')
output_file = input_file[:-2] + 'mips'

print('Stranger Bugs Cool Compiler v0.1')
print('Copyright (c) 2019: Alejandro Klever Clemente, Laura Tamayo Blanco, Miguel Angel Gonzalez Calles')

def run():
    sp = subprocess.run(['python', 'cool', 'compile', input_file, output_file], capture_output=True, timeout=100)        
    print(sp.stdout.decode())
    exit(sp.returncode)

if os.getcwd().endswith('src'):
    run()
else:
    os.chdir('src')
    run()
