from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter
from onemodel.variable import Variable

onemodel = OneModel()

# Variable definiton.

v = Variable("x1")
v.value = 0
v.units = 'molec'
v.comment = 'Sigma unit'
onemodel.add(v)

v = Variable("x2")
v.value = 0
v.units = 'molec'
v.comment = 'Anti-sigma unit'
onemodel.add(v)

v = Variable("x3")
v.value = 0
v.units = 'molec'
v.comment = 'Protein of interest'
onemodel.add(v)

# Parameter definiton.

p = Parameter("k1")
p.value = 1.0
p.units = 'molec/t'
p.comment = 'Sigma production'
onemodel.add(p)

p = Parameter("k2")
p.value = 1.0
p.units = '1/t'
p.comment = 'Anti-sigma production'
onemodel.add(p)

p = Parameter("k3")
p.value = 1.0
p.units = '1/t'
p.comment = 'Protein production'
onemodel.add(p)

p = Parameter("d1")
p.value = 1.0
p.units = '1/t'
p.comment = 'Sigma degradation'
onemodel.add(p)

p = Parameter("d2")
p.value = 1.0
p.units = '1/t'
p.comment = 'Anti-sigma degradation'
onemodel.add(p)

p = Parameter("d3")
p.value = 1.0
p.units = '1/t'
p.comment = 'Protein degradation'
onemodel.add(p)

p = Parameter("gamma12")
p.value = 1.0
p.units = '1/molec/t'
p.comment = 'Sigma and anti-sigma secuestration rate'
onemodel.add(p)

print(onemodel.variables)
