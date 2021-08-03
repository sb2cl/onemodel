from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter

onemodel = OneModel()

p = Parameter("std.Omega_A")
p.value = 5        

onemodel.add(p)

symbol = onemodel.get('std.Omega_A')

print(symbol)

print(onemodel.parameters)
