from coolcmp.utils import cil
from coolcmp.utils import CILFormatter


test_cil = cil.ProgramNode(
    dot_types=[],
    dot_data=[
        cil.DataNode('msg', 'Hello World!\n'),
    ],
    dot_code=[
        cil.FunctionNode(
            name='main',
            params=[],
            local_vars=[
                cil.LocalNode('x'),
            ],
            instructions=[
                cil.LoadNode('x', 'msg'),
                cil.PrintStringNode('x'),
                cil.ReturnNode(0),
            ]
        )
    ]
)

print(CILFormatter().visit(test_cil))
