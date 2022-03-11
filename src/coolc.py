import os
import sys
import subprocess

input_file = sys.argv[1].replace('\\', '\\\\')
output_file = input_file[:-2] + 'mips'

print('AnotherCoolTeamCompiler')
print('Copyright (c) 2021: Yasmin Cisneros Cimadevila & Jessy Gigato Izquierdo')

def run():
    sp = subprocess.run(['python3.9', 'utils/pipeline.py', 'final-execution', input_file, output_file], capture_output=True, timeout=100) 
    dcode = sp.stdout.decode()
    print(dcode)
    exit(sp.returncode)

if os.getcwd().endswith('src'):
    run()
else:
    os.chdir('src')
    run()
