from code_generation.cil.nodes import *
from constants import INT, SELF_LOWERCASE

def build_int_functions(index=None):
    type_name_params = [CILParamNode(SELF_LOWERCASE, INT)]
    type_name_localVars = [CILLocalNode("local_type_name_Int_result_0")]
    type_name_intructions = [CILLoadNode(type_name_localVars[0].name, 'type_Int', index),
                             CILReturnNode(type_name_localVars[0].name, index)]
    type_name = CILFunctionNode("function_type_name_Int", type_name_params,
                             type_name_localVars, type_name_intructions)

    copy_params = [CILParamNode(SELF_LOWERCASE, INT)]
    copy_localVars = [CILLocalNode("local_copy_Int_result_0")]
    copy_intructions = [CILAssignNode(copy_localVars[0].name, copy_params[0].name),
                        CILReturnNode(copy_localVars[0].name, index)]
    copy = CILFunctionNode("function_copy_Int", copy_params,
                        copy_localVars, copy_intructions)

    abort_params = [CILParamNode(SELF_LOWERCASE, INT)]
    abort_localVars = [CILLocalNode('local_abort_Int_msg_0')]
    abort_intructions = [CILLoadNode(abort_params[0].name, 'int_abort'),
                         CILOutStringNode(abort_params[0].name, index),
                         CILExitNode(abort_params[0].name, idx=index)]
    abort = CILFunctionNode("function_abort_Int", abort_params,
                         abort_localVars, abort_intructions)

    dotcode = [abort, type_name, copy]
    methods = [('abort', abort.name), ('type_name',
                                       type_name.name), ('copy', copy.name)]

    return (dotcode, methods)
