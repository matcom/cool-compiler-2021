from cool.pipes.pipes import cil_ast_to_text_pipe, cool_to_cil_pipe, start_pipe, change_escaped_lines, remove_comments_pipe,\
    parse_text_pipe, ast_pipe, type_collector_pipe, build_types_pipe, \
    check_types_pipe, run_program_pipe, reconstruct_pipe, void_as_type_pipe, \
    auto_resolver_pipe, string_escape_pipe, tokenize_text_pipe, ply_lexer_pipe, remove_comment_tokens_pipe
from cool.libs import add_std_pipe
from cool.pipes.pipeline import Pipeline, Pipe

lexer_pipeline = Pipeline(start_pipe,
                            ply_lexer_pipe
                        #   change_escaped_lines,
                        #   remove_comments_pipe,
                        #   tokenize_text_pipe,
                        #   string_escape_pipe,
                          )

# lexer_pipeline = Pipeline(start_pipe, # Temporary lexer for testing semantics 
#                           change_escaped_lines,
#                           tokenize_text_pipe,
#                           remove_comment_tokens_pipe,
#                           string_escape_pipe,
#                           )

# lexer_pipeline = Pipeline(start_pipe,
#                           change_escaped_lines,
#                           remove_comments_pipe,
#                           tokenize_text_pipe,
#                           string_escape_pipe,
#                           )

syntax_pipeline = Pipeline(parse_text_pipe,
                          )

pre_semantic_pipeline = Pipeline(ast_pipe, 
                                void_as_type_pipe,
                                type_collector_pipe, 
                                build_types_pipe, 
                                check_types_pipe,
                                auto_resolver_pipe,
                                )


def get_std():
    import os
    std_dir = os.path.join(os.path.dirname(__file__),"lib","std.cool")
    with open(std_dir, "r") as f:
        std = f.read()
    return std

def get_std_context():
    std_pipeline = Pipeline(lexer_pipeline,
                            syntax_pipeline,
                            pre_semantic_pipeline)

    std_result = std_pipeline(get_std())
    return std_result['context']

def add_std_pipe(result:dict):
    std_context = get_std_context()
    result['context'] = std_context
    return result

add_std_pipe = Pipe(add_std_pipe)


semantic_pipeline = Pipeline(add_std_pipe,
                             pre_semantic_pipeline,
                             )

execution_pipe = Pipe(run_program_pipe)

base_cool_pipeline = Pipeline(lexer_pipeline,
                              syntax_pipeline,
                              semantic_pipeline,)

cool_pipeline = Pipeline(base_cool_pipeline,
                         cool_to_cil_pipe,
                         cil_ast_to_text_pipe)

interprete_cool_pipeline = Pipeline(base_cool_pipeline,
                                    execution_pipe)

reconstr_pipeline = Pipeline(base_cool_pipeline,
                             reconstruct_pipe,
                             cool_to_cil_pipe,
                             cil_ast_to_text_pipe,
                             execution_pipe)

