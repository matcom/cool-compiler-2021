import os
from cool.pipes.pipes import start_pipe, change_escaped_lines, remove_comments_pipe, parse_text_pipe, ast_pipe, type_collector_pipe, build_types_pipe, check_types_pipe
from cool.pipes.pipeline import Pipeline, Pipe

def get_std():
    std_dir = os.path.join(os.path.dirname(__file__),"lib","std.cool")
    with open(std_dir, "r") as f:
        std = f.read()
    return std

def get_std_context():
    std_pipeline = Pipeline(start_pipe,
                            change_escaped_lines,
                            remove_comments_pipe, 
                            parse_text_pipe,
                            ast_pipe, 
                            type_collector_pipe, 
                            build_types_pipe,
                            check_types_pipe)

    std_result = std_pipeline(get_std())
    return std_result['context']

def add_std_pipe(result:dict):
    std_context = get_std_context()
    result['context'] = std_context
    return result

add_std_pipe = Pipe(add_std_pipe)
