def load_templates() -> str:
    code_templates = ["\n# Templates"]

    with open("./coolcmp/codegen/cil2mips/templates/malloc.mips") as fd:
        code_templates.append("".join(fd.readlines()))

    return "\n".join(code_templates)
