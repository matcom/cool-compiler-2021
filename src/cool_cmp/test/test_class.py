import sys
import pytest
import os
base_dir = os.path.dirname(__file__)
sys.path.append(os.path.join(base_dir, ".."))
from cool_cmp.pipes.pipelines import cool_pipeline, generate_cool_pipeline
from error.errors import CoolError
from .tests import tests, tests_run

class TestPrograms:
    
    @pytest.mark.parametrize("name,progr,exp_result,exp_errors",[x for x in tests if "in_out" not in x[0]])        
    def test_general(self, name, progr, exp_result, exp_errors):
        result = cool_pipeline(progr)
        ast, errors, parse, tokens, context, scope, operator, out = [result.get(x,None) for x in ["ast", "errors", "text_parse", "text_tokens", "context", "scope", "operator", "value"]] 
        if hasattr(out, "value"):
            assert out.value == exp_result
        assert errors == exp_errors
    
    @pytest.mark.parametrize("name,program", [(x[0],x[1]) for x in tests if "in_out" not in x[0]])
    def test_reconstruction(self, name, program):
        result = generate_cool_pipeline(program)
        ast, errors, context, scope, operator, out, reconstr_text = [result.get(x,None) for x in ["ast", "errors", "context", "scope", "operator", "value", "reconstructed_text"]]
        with open(os.path.join(base_dir, "test_reconstruction", name + ".cl"), "w") as f:
            f.write(reconstr_text)
        result = generate_cool_pipeline(reconstr_text)
        ast2, errors2, context2, scope2, operator2, out2, reconstr_text2 = [result.get(x,None) for x in ["ast", "errors", "context", "scope", "operator", "value", "reconstructed_text"]]
        assert len(errors) == len(errors2)
        assert reconstr_text == reconstr_text2
        if hasattr(out, "value"):
            assert out.value == out2.value
        
    @pytest.mark.parametrize("progr",tests_run)        
    def test_run(self, progr):
        result = cool_pipeline(progr)
        errors, out = [result.get(x,None) for x in ["errors", "value"]] 
        assert len(errors) == 0
        
    
    def test_input(self, monkeypatch):
        with monkeypatch.context() as m:
            import builtins # Mocking input
            def input():
                return "20"
            monkeypatch.setattr(builtins, "input", input)
            name, progr, exp_result, exp_errors = [x for x in tests if "in_out" in x[0]][0]

            result = cool_pipeline(progr)
            ast, errors, parse, tokens, context, scope, operator, out = [result[x] for x in ["ast", "errors", "text_parse", "text_tokens", "context", "scope", "operator", "value"]] 

            if hasattr(out, "value"):
                assert out.value == "20"
            assert errors == exp_errors
    
