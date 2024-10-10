import functools

type void = None

@functools.cache
def catfile(template: str):
    with open(template, "r") as f:
        temp = f.read()
    return temp

def genfile(template: str, filename: str) -> void:
    template = catfile(template)
    with open(filename, "w") as f:
        f.write(template)
    
"""
generate for problems a, b, c,...
each using template
so we need to know how many problems there are
what each there indexes are,
i.e. if problems like c1, c2 exists
"""
def gencontest():
    pass
