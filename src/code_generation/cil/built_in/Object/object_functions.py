from code_generation.cil.nodes import *
from constants import OBJECT, SELF_LOWERCASE

def build_object_functions(index=None):
    abort_params = [CILParamNode(SELF_LOWERCASE, OBJECT)]
    abort_localVars = [CILLocalNode("local_abort_Object_self_0")]
    abort_intructions = [CILAssignNode(abort_localVars[0].name, abort_params[0].name, index),
                         CILExitNode(abort_params[0].name, idx=index)]
    abort = CILFunctionNode("function_abort_Object", abort_params,
                         abort_localVars, abort_intructions)

    type_name_params = [CILParamNode(SELF_LOWERCASE, OBJECT)]
    type_name_localVars = [CILLocalNode("local_type_name_Object_result_0")]
    type_name_intructions = [CILTypeOfNode(type_name_params[0].name, type_name_localVars[0].name, index),
                             CILReturnNode(type_name_localVars[0].name, index)]
    type_name = CILFunctionNode("function_type_name_Object", type_name_params,
                             type_name_localVars, type_name_intructions)

    copy_params = [CILParamNode(SELF_LOWERCASE, OBJECT)]
    copy_localVars = [CILLocalNode("local_copy_Object_result_0")]
    copy_intructions = [CILCopyNode(copy_localVars[0].name, copy_params[0].name, index),
                        CILReturnNode(copy_localVars[0].name, index)]
    copy = CILFunctionNode("function_copy_Object", copy_params,
                        copy_localVars, copy_intructions)

    dotcode = [abort, type_name, copy]
    methods = [('abort', abort.name), ('type_name', type_name.name), ('copy', copy.name)]

    return (dotcode, methods)
