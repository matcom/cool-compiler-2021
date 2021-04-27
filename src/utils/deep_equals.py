import json

_all_ = ['deep_equals']

def generate_json_string(a):
    json_dump = json.dumps(a)
    return str(json_dump)


def deep_equals(a, b) -> bool:
    return generate_json_string(a) == generate_json_string(b)
    
# TODO: Implementar deep_equals para hacer varias pasadas 
# del BackInferncer si no hay cambios en el ast que se devuelve