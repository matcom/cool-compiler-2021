import json
import os

base_dir = os.path.dirname(__file__)
test_dir = os.path.join(base_dir, "test_data")

def dump_meta_test(name, code, result, errors):
    meta = json.dumps({"name":name, "result":result, "errors":errors})
    dump_dir = os.path.join(test_dir, name+".meta_test")
    with open(dump_dir, "w") as f:
        json.dump(meta,f)
        f.write("\n")
        f.write(code)

def load_meta_test(path):
    with open(path, "r") as f:
        meta = f.readline()
        meta = json.loads(meta)
        meta = json.loads(meta)
        name, result, errors = [meta[x] for x in ["name", "result", "errors"]]
        code = f.read()
    return name, code, result, errors

tests = []

for meta_file in os.listdir(test_dir):
    tests.append(load_meta_test(os.path.join(test_dir, meta_file)))
    
run_dir = os.path.join(base_dir, "test_run")

tests_run = []
for program in os.listdir(run_dir):
    with open(os.path.join(run_dir, program)) as f:
        program = f.read()
        tests_run.append(program)