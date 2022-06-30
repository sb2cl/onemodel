def get_ast_names(ast):
    """Returns the user defined names in a MathML ast."""
    names = []

    if ast.isName():
        names.append(ast.getName())

    for i in range(ast.getNumChildren()):
        child = ast.getChild(i)
        child_names = get_ast_names(child)

        for item in child_names:
            names.append(item)

    return names
