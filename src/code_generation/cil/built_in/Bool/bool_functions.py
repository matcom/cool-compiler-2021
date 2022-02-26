from code_generation.cil.nodes import *
from constants import BOOL, SELF_LOWERCASE

def build_bool_functions(index=None):
    type_name_params = [CILParamNode(SELF_LOWERCASE, BOOL)]
    type_name_localVars = [CILLocalNode("local_type_name_Bool_result_0")]
    type_name_intructions = [CILLoadNode(type_name_localVars[0].name, 'type_Bool', index),
                             CILReturnNode(type_name_localVars[0].name, index)]
    type_name = CILFunctionNode("function_type_name_Bool", type_name_params,
                             type_name_localVars, type_name_intructions)

    copy_params = [CILParamNode(SELF_LOWERCASE, BOOL)]
    copy_localVars = [CILLocalNode("local_copy_result_Bool_0")]
    copy_intructions = [CILAssignNode(copy_localVars[0].name, copy_params[0].name),
                        CILReturnNode(copy_localVars[0].name, index)]
    copy = CILFunctionNode("function_copy_Bool", copy_params,
                        copy_localVars, copy_intructions)

    abort_params = [CILParamNode(SELF_LOWERCASE, BOOL)]
    abort_localVars = [CILLocalNode('local_abort_Bool_msg_0')]
    abort_intructions = [CILLoadNode(abort_params[0].name, 'bool_abort'),
                         CILOutStringNode(abort_params[0].name, index),
                         CILExitNode(abort_params[0].name, idx=index)]
    abort = CILFunctionNode("function_abort_Bool", abort_params,
                         abort_localVars, abort_intructions)

    dotcode = [abort, type_name, copy]
    methods = [('abort', abort.name), ('type_name', type_name.name), ('copy', copy.name)]

    return (dotcode, methods)
