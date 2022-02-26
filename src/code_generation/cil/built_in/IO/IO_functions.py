from code_generation.cil.nodes import *
from constants import INT, IO, STRING, SELF_LOWERCASE

def build_io_functions(index=None):
    out_string_params = [CILParamNode(SELF_LOWERCASE, IO), CILParamNode("word", STRING)]
    out_string_localVariables = [CILLocalNode("local_out_string_String_self_0")]
    out_string_intructions = [CILAssignNode(out_string_localVariables[0].name, out_string_params[0].name, index),
                              CILOutStringNode(out_string_params[1].name, index),
                              CILReturnNode(out_string_localVariables[0].name, index)]
    out_string = CILFunctionNode("function_out_string_IO", out_string_params,
                              out_string_localVariables, out_string_intructions)

    out_int_params = [CILParamNode(SELF_LOWERCASE, IO), CILParamNode("number", INT)]
    out_int_localVariables = [CILLocalNode("local_out_int_IO_self_0")]
    out_int_intructions = [CILAssignNode(out_int_localVariables[0].name, out_int_params[0].name, index),
                           CILOutIntNode(out_int_params[1].name, index),
                           CILReturnNode(out_int_localVariables[0].name, index)]
    out_int = CILFunctionNode("function_out_int_IO", out_int_params,
                           out_int_localVariables, out_int_intructions)

    in_int_params = [CILParamNode(SELF_LOWERCASE, IO)]
    in_int_localVariables = [CILLocalNode("local_in_int_IO_result_0")]
    in_int_intructions = [CILReadIntNode(in_int_localVariables[0].name, index),
                          CILReturnNode(in_int_localVariables[0].name, index)]
    in_int = CILFunctionNode("function_in_int_IO", in_int_params,
                          in_int_localVariables, in_int_intructions)

    in_string_params = [CILParamNode(SELF_LOWERCASE, IO)]
    in_string_localVariables = [CILLocalNode("local_in_string_IO_result_0")]
    in_string_intructions = [CILReadStringNode(in_string_localVariables[0].name, index),
                             CILReturnNode(in_string_localVariables[0].name, index)]
    in_string = CILFunctionNode("function_in_string_IO", in_string_params,
                             in_string_localVariables, in_string_intructions)

    dotcode = [out_string, out_int, in_int, in_string]
    methods = [('out_string', out_string.name), ('out_int', out_int.name),
               ('in_int', in_int.name), ('in_string', in_string.name)]

    return (dotcode, methods)
