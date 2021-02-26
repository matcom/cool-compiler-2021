import os
from parsing import parser
from semantics import type_collector, type_builder, autotype_collector

def format_errors(errors, s = ""):
    count = 1
    for error in errors:
        s += str(count) + ". " + error + "\n"
        count += 1
    return s

def run_pipeline(program):
    ast = parser.parse(program)
    
    collector = type_collector.TypeCollector()
    collector.visit(ast)
    context = collector.context
    print('Context\n', context)

    builder = type_builder.TypeBuilder(context)
    builder.visit(ast)
    print('Context\n', context)

    auto_collector = autotype_collector.AutotypeCollector(context)
    scope = auto_collector.visit(ast)

    s = "Type Collector Errors:\n"
    s = format_errors(collector.errors, s)
    s += "Type Builder Errors:\n"
    s = format_errors(builder.errors, s)
    s += "Inference Gatherer Errors:\n"
    s = format_errors(auto_collector.errors, s)
    s += "Scope:\n" +  scope.get_all_names()
    print(s)

try:
    folder_path = r'./zTests/Misc'
    filenames = os.listdir(folder_path)
    filenames.sort()
except FileNotFoundError:
    print("Error Importing Files")
count = 4

filenames = [r'/home/rodro/Aarka/Complementos de Compilacion/cool-compiler-2022/src/zTests/Misc/06FooBarRaz.cl']
filenames = [r'/home/rodro/Aarka/Complementos de Compilacion/cool-compiler-2022/src/zTests/Misc/07MultipleClass.cl']

for filename in filenames:
    if count == 0:
        print("Reach Count Limit")
        break

    path = os.path.join(folder_path, filename)
    file = open(path, "r")
    program = file.read()
    file.close()

    print(f"Running {filename}")
    run_pipeline(program)
    count -= 1
    print("-------------------------------------------------------------------------\n")

print("EndOfFiles")

