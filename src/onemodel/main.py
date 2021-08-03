from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter

onemodel = OneModel()

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

print(onemodel.parameters)
print(onemodel.parameters_name)
