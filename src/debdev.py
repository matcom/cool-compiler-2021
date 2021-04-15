import os

from debbuging import type_logger
from parsing import parser
from semantics import type_collector, type_builder, soft_inferencer


def format_errors(errors, s=""):
    count = 1
    errors.sort(key=lambda x: x[0])
    for error in errors:
        num = str(count) if count > 9 else "0" + str(count)
        s += num + ". " + error[1] + "\n"
        count += 1
    return s


def run_pipeline(program):
    ast = parser.parse(program)

    collector = type_collector.TypeCollector()
    collector.visit(ast)
    context = collector.context
    errors = collector.errors
    # print('Context\n', context)

    builder = type_builder.TypeBuilder(context, errors)
    builder.visit(ast)
    # print('Context\n', context)

    soft = soft_inferencer.SoftInferencer(context)
    soft_ast = soft.visit(ast)

    # auto_inferencer = autotype_inferencer.AutotypeInferencer(context, errors)
    # auto_inferencer.visit(ast, scope)

    logger = type_logger.TypeLogger(context)
    log = logger.visit(soft_ast, soft_ast.scope)
    print(log)
    s = "Semantic Errors:\n"
    s = format_errors(errors, s)
    print(s)


try:
    misc = r"./tests/Misc"
    auto = r"./tests/Auto"
    folder_path = auto
    filenames = os.listdir(folder_path)
    filenames.sort()
except FileNotFoundError:
    print("Error Importing Files")
count = 100

filenames = [
    r"/home/rodro/Aarka/Complementos de Compilacion/cool-cows/src/debbuging/tests/Auto/"
    r"01Assign.cl"
]

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
    if len(filenames) > 1:
        # input()
        pass

print("EndOfFiles")


# todo: Manejar los self types dentro de los type bags correctamente (acualizar metodo swap swlf types)