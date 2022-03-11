def load_templates() -> str:
    template_names = [
        "malloc.mips",
        "copy.mips",
        "substr.mips",
        "isvoid.mips",
        "less_than.mips",
        "length.mips",
        "concat.mips",
        "remove_eol.mips",
        "less_equal.mips",
        "equal.mips",
        "conforms.mips"
    ]
    code_templates = ["\n# Templates"]

    for tname in template_names:
        with open(f"./coolcmp/codegen/cil2mips/templates/{tname}") as fd:
            code_templates.append("".join(fd.readlines()))

    return "\n".join(code_templates)