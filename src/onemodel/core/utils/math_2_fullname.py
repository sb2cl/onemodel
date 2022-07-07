from io import BytesIO
from tokenize import ENCODING, NAME, OP, tokenize

def math_2_fullname(math_expr, scope):
    """Changes local user defined names into fullnames.

    Arguments:
        math_expr: str
            Math formula obtained with libSBML.formulaToL3String()
    """
    result = ""

    g = tokenize(BytesIO(math_expr.encode("utf-8")).readline)

    last_tokval = None

    for toknum, tokval, _, _, _ in g:
        if toknum == ENCODING:
            continue

        if str(last_tokval) == "." and toknum == NAME:
            result = result[0:-1]
            result += "__"

        if toknum == NAME:
            try:
                fullname = scope.get_fullname(str(tokval))
                result += fullname
            except:
                result += str(tokval)

        else:
            result += str(tokval)

        last_tokval = tokval

    return str(result)
