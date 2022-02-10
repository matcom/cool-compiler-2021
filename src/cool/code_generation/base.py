from typing import Any, List, Optional

import cool.code_generation.cil as cil
from cool.semantics.utils.scope import Context, Method, Type


class BaseCOOLToCILVisitor:
    def __init__(self, context: Context):
        self.dottypes: List[cil.TypeNode] = []
        self.dotdata: List[cil.DataNode] = []
        self.dotcode: List[cil.FunctionNode] = []

        self.current_type: Optional[Type] = None
        self.current_method: Optional[Method] = None
        self.current_function: Optional[cil.FunctionNode] = None

        self.context: Context = context

        self.locals_dict = {}
        self.param_set = set()
        self.attr_set = set()

    @property
    def params(self) -> List[cil.ParamNode]:
        return self.current_function.params

    @property
    def localvars(self) -> List[cil.LocalNode]:
        return self.current_function.local_vars

    @property
    def instructions(self) -> List[cil.InstructionNode]:
        return self.current_function.instructions

    def register_local(self, var_name: str, comment: str = "") -> str:
        local_name = (
            f"local_{self.current_function.name[9:]}_{var_name}_{len(self.localvars)}"
        )
        local_name = var_name
        local_node = cil.LocalNode(local_name).set_comment(comment)
        self.localvars.append(local_node)
        return local_name

    def define_internal_local(self, comment: str = "") -> str:
        return self.register_local(f"internal_{len(self.localvars)}", comment)

    def register_instruction(
        self, instruction: cil.InstructionNode
    ) -> cil.InstructionNode:
        self.instructions.append(instruction)
        return instruction

    def to_function_name(self, method_name: str, type_name: str) -> str:
        return f"function_{method_name}_at_{type_name}"

    def register_function(self, function_name: str) -> cil.FunctionNode:
        function_node = cil.FunctionNode(function_name, [], [], [])
        self.dotcode.append(function_node)
        return function_node

    def register_type(self, name: str) -> cil.TypeNode:
        type_node = cil.TypeNode(name)
        self.dottypes.append(type_node)
        return type_node

    def register_data(self, value: Any) -> cil.DataNode:
        data_name = f"data_{len(self.dotdata)}"
        data_node = cil.DataNode(data_name, value)
        self.dotdata.append(data_node)
        return data_node
