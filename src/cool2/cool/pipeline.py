from cool.pipes.pipes import start_pipe, change_escaped_lines, remove_comments_pipe,\
    parse_text_pipe, ast_pipe, type_collector_pipe, build_types_pipe, \
    check_types_pipe, run_program_pipe, reconstruct_pipe, void_as_type_pipe, \
    auto_resolver_pipe, string_escape_pipe
from cool.libs import add_std_pipe
from cool.pipes.pipeline import Pipeline

lexer_syntax_pipeline = Pipeline(start_pipe,
                         change_escaped_lines,
                         remove_comments_pipe, 
                         parse_text_pipe,
                         string_escape_pipe
                        )

semantic_pipeline = Pipeline(add_std_pipe,
                             ast_pipe, 
                             void_as_type_pipe,
                             type_collector_pipe, 
                             build_types_pipe, 
                             check_types_pipe,
                             auto_resolver_pipe,
                             )

execution_pipeline = Pipeline(run_program_pipe)

cool_pipeline = Pipeline(lexer_syntax_pipeline,
                         semantic_pipeline,
                         execution_pipeline)

reconstr_pipeline = Pipeline(lexer_syntax_pipeline,
                             semantic_pipeline,
                             reconstruct_pipe,
                             execution_pipeline)
