from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter
from onemodel.variable import Variable
from onemodel.equation import Equation, EquationType
from onemodel.export.matlab.matlab import Matlab
from onemodel.math_expr import MathToken, MathTokenType, MathLexer

onemodel = OneModel("antithetic")

# Variable definiton.

v = Variable("x1")
v.value = '0'
v.units = 'molec'
v.comment = 'Sigma unit'
onemodel.add(v)

v = Variable("x2")
v.value = '0'
v.units = 'molec'
v.comment = 'Anti-sigma unit'
onemodel.add(v)

v = Variable("x3")
v.value = '0'
v.units = 'molec'
v.comment = 'Protein of interest'
onemodel.add(v)

v = Variable("ref")
v.value = '0'
v.units = 'molec'
v.comment = 'Reference of the antithetic controller'
onemodel.add(v)


# Parameter definiton.

p = Parameter('k1')
p.value = '1.0'
p.units = 'molec/t'
p.comment = 'Sigma production'
onemodel.add(p)

p = Parameter('k2')
p.value = '1.0'
p.units = '1/t'
p.comment = 'Anti-sigma production'
onemodel.add(p)

p = Parameter('k3')
p.value = '1.0'
p.units = '1/t'
p.comment = 'Protein production'
onemodel.add(p)

p = Parameter('d1')
p.value = '1.0'
p.units = '1/t'
p.comment = 'Sigma degradation'
onemodel.add(p)

p = Parameter('d2')
p.value = '1.0'
p.units = '1/t'
p.comment = 'Anti-sigma degradation'
onemodel.add(p)

p = Parameter('d3')
p.value = '1.0'
p.units = '1/t'
p.comment = 'Protein degradation'
onemodel.add(p)

p = Parameter('gamma12')
p.value = '1.0'
p.units = '1/molec/t'
p.comment = 'Sigma and anti-sigma secuestration rate'
onemodel.add(p)

# Equation definition.

e = Equation('eq_1')
e.equation_type = EquationType.ODE
e.variable_name = 'x1'
e.value = 'k1 - gamma12*x1*x2 - d1*x1'
e.comment = 'Dynamic of sigma'
onemodel.add(e)

e = Equation('eq_2')
e.equation_type = EquationType.ODE
e.variable_name = 'x2'
e.value = 'k2*x3 - gamma12*x1*x2 - d2*x2'
e.comment = 'Dynamic of anti-sigma'
onemodel.add(e)

e = Equation('eq_3')
e.equation_type = EquationType.ODE
e.variable_name = 'x3'
e.value = 'k3*x1 - d3*x3'
e.comment = 'Dynamic of protein'
onemodel.add(e)

e = Equation('eq_4')
e.equation_type = EquationType.SUBSTITUTION
e.variable_name = 'ref'
e.value = 'k1/k2'
e.comment = 'Reference of the antithetic controller'
onemodel.add(e)

matlab = Matlab(onemodel)
matlab.generate_param()
matlab.generate_ode()
matlab.generate_driver()
matlab.generate_states()

matlab.sympy2matlab('k1/k2')

mp = MathLexer('+ 1.0 - 200 ^.01 */1.')
print(mp.generate_tokens())
