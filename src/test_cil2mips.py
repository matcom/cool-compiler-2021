from coolcmp.utils import cil
from coolcmp.utils import CILFormatter


hello_world = cil.ProgramNode(
    dot_types=[
        cil.TypeNode(
            name="String",
            attrs=[
                "String_value",
            ],
            methods=[
                "String_length",
                "String_concat",
                "String_substr",
            ],
        ),
    ],
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

print_int = cil.ProgramNode(
    dot_types=[],
    dot_data=[cil.DataNode("the_sum_is", '"The sum is\n"')],
    dot_code=[
        cil.FunctionNode(
            name="main",
            params=[],
            local_vars=[
                cil.LocalNode("msg"),
                cil.LocalNode("x"),
                cil.LocalNode("y"),
                cil.LocalNode("sum"),
            ],
            instructions=[
                cil.LoadNode("msg", "the_sum_is"),
                cil.AssignNode("x", 10 + 12 + 10),
                cil.AssignNode("y", "x"),
                cil.PlusNode("sum", "x", "y"),
                cil.PrintStringNode("msg"),
                cil.PrintIntNode("sum"),
                cil.ReturnNode(0),
            ],
        )
    ],
)
