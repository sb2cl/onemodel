from libsbml import *

def check(value, message):
    """If 'value' is None, prints an error message constructed using
    'message' and then exits with status code 1.  If 'value' is an integer,
    it assumes it is a libSBML return status code.  If the code value is
    LIBSBML_OPERATION_SUCCESS, returns without further action; if it is not,
    prints an error message constructed using 'message' along with text from
    libSBML explaining the meaning of the code, and exits with status code 1.
    """
    if value == None:
        raise SystemExit(
            'LibSBML returned a null value trying to ' + message + '.'
        )
    elif type(value) is int:
        if value == LIBSBML_OPERATION_SUCCESS:
            return
        else:
            err_msg = 'Error encountered trying to ' + message + '.' \
                 + 'LibSBML returned error code ' + str(value) + ': "' \
                 + OperationReturnValue_toString(value).strip() + '"'
        raise SystemExit(err_msg)
    else:
        return

def getAstNames(ast):
    """ Returns the user defined names in a MathML ast.
    """
    names = []

    if ast.isName():
        names.append(ast.getName())

    for i in range(ast.getNumChildren()):
        child = ast.getChild(i)
        child_names = getAstNames(child)

        for item in child_names:
            names.append(item)

    return names
