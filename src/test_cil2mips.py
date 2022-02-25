from coolcmp.utils import cil
from coolcmp.utils import CILFormatter


hello_world = cil.ProgramNode(
    dot_types=[],
    dot_data=[
        cil.DataNode("hello_message", '"Hello\n"'),
        cil.DataNode("world_message", '"World!\n"'),
    ],
    dot_code=[
        cil.FunctionNode(
            name="main",
            params=[],
            local_vars=[
                cil.LocalNode("x"),
                cil.LocalNode("y"),
                cil.LocalNode("z"),
            ],
            instructions=[
                cil.LoadNode("x", "hello_message"),
                cil.PrintStringNode("x"),
                cil.LoadNode("y", "world_message"),
                cil.PrintStringNode("y"),
                cil.LoadNode("z", "hello_message"),
                cil.PrintStringNode("z"),
                cil.ReturnNode(0),
            ],
        )
    ],
)

allocate = cil.ProgramNode(
    dot_types=[cil.TypeNode("Int", ["value"], [], [])],
    dot_data=[
        cil.DataNode("the_value_is", '"The value is\n"'),
    ],
    dot_code=[
        cil.FunctionNode(
            name="main",
            params=[],
            local_vars=[cil.LocalNode("a"), cil.LocalNode("msg")],
            instructions=[
                cil.AllocateNode("Int", "a"),
                cil.LoadNode("msg", "the_value_is"),
                cil.PrintStringNode("msg"),
                cil.PrintIntNode("a"),
                cil.ReturnNode(0),
            ],
        )
    ],
)

test_cil2 = cil.ProgramNode(
    dot_types=[],
    dot_data=[cil.DataNode("msg", '"Hola mundo\n"')],
    dot_code=[
        cil.FunctionNode(
            name="main",
            params=[],
            local_vars=[cil.LocalNode("x"), cil.LocalNode("y"), cil.LocalNode("sum")],
            instructions=[
                cil.LoadNode("x", 1),
                cil.LoadNode("y", 2),
                cil.PrintStringNode("x"),
                cil.ReturnNode(0),
            ],
        )
    ],
)
