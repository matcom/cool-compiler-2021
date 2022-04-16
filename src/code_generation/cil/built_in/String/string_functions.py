from code_generation.cil.nodes import *
from utils.constants import INT, STRING, SELF_LOWERCASE


def build_string_functions(index=None):
    length_params = [CILParamNode(SELF_LOWERCASE, STRING)]
    length_localVars = [CILLocalNode("local_length_String_result_0")]
    length_intructions = [CILLengthNode(length_localVars[0].name, length_params[0].name, index),
                          CILReturnNode(length_localVars[0].name, index)]
    length = CILFunctionNode("function_length_String",
                             length_params, length_localVars, length_intructions)

    concat_params = [CILParamNode(
        SELF_LOWERCASE, STRING), CILParamNode("word", STRING)]
    concat_localVars = [CILLocalNode("local_concat_String_result_0")]
    concat_intructions = [CILConcatNode(concat_localVars[0].name, concat_params[0].name, concat_params[1].name, index),
                          CILReturnNode(concat_localVars[0].name, index)]
    concat = CILFunctionNode("function_concat_String",
                             concat_params, concat_localVars, concat_intructions)

    substr_params = [CILParamNode(SELF_LOWERCASE, STRING), CILParamNode(
        "begin", INT), CILParamNode("end", INT)]
    substr_localVars = [CILLocalNode("local_substr_String_result_0")]
    substr_intructions = [CILSubstringNode(substr_localVars[0].name, substr_params[0].name, substr_params[1].name, substr_params[2].name, index),
                          CILReturnNode(substr_localVars[0].name, index)]
    substr = CILFunctionNode("function_substr_String",
                             substr_params, substr_localVars, substr_intructions)

    type_name_params = [CILParamNode(SELF_LOWERCASE, STRING)]
    type_name_localVars = [CILLocalNode("local_type_name_String_result_0")]
    type_name_intructions = [CILLoadNode(type_name_localVars[0].name, 'type_String', index),
                             CILReturnNode(type_name_localVars[0].name, index)]
    type_name = CILFunctionNode("function_type_name_String",
                                type_name_params, type_name_localVars, type_name_intructions)

    copy_params = [CILParamNode(SELF_LOWERCASE, STRING)]
    copy_localVars = [CILLocalNode("local_copy_String_result_0")]
    copy_intructions = [CILConcatNode(copy_localVars[0].name, copy_params[0].name, None, index),
                        CILReturnNode(copy_localVars[0].name, index)]
    copy = CILFunctionNode("function_copy_String", copy_params,
                           copy_localVars, copy_intructions)

    abort_params = [CILParamNode(SELF_LOWERCASE, STRING)]
    abort_localVars = [CILLocalNode('local_abort_String_msg_0')]
    abort_intructions = [CILLoadNode(abort_params[0].name, 'string_abort'),
                         CILOutStringNode(abort_params[0].name, index),
                         CILExitNode(abort_params[0].name, idx=index)]
    abort = CILFunctionNode("function_abort_String", abort_params,
                            abort_localVars, abort_intructions)

    dotcode = [length, concat, substr, abort, type_name, copy]
    methods = [('length', length.name), ('concat', concat.name), ('substr', substr.name),
               ('abort', abort.name), ('type_name', type_name.name), ('copy', copy.name)]

    return (dotcode, methods)
