import re

def algebraic2tellurium(model):
    """ Replaces the algebraic rules of our extended tellurium with a dummy
    syntax of original tellurium
    """
    # Regex expression to look for algebraic rules.
    exp = "((?!\d)\w+) \s*==\s*([^\\\r\n\f'#]*)"
    p = re.compile(exp)

    while True:
        # Search first ocurrence of a algebraic rule.
        m = p.search(model)

        if m == None: break

        # Create the dummy syntax for original tellurium.
        g = m.groups()
        string = f'{g[0]}_algebraic_rule__ := {g[0]} - ({g[1]})'

        # Replace algebraic rule with the dummy syntax.
        model = p.sub(string, model, count=1)

    return model

if __name__ == '__main__':
    model_test = """
    k1_on = 100000
    k1_off = 100000
    k2 = 1
    
    P = 0
    S = 10
    E_tot = 1
    
    K_m := (k1_off + k2) / k1_on
    
    ES == E*S/K_m
    E == E_tot - ES
    
    P' = k2 * ES
    """

    print(model_test)
    print('### CONVERTED INTO TELLURIUM ###')
    print(algebraic2tellurium(model_test))
