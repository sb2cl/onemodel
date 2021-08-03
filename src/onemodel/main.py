from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter

onemodel = OneModel()

p = Parameter("std.Omega_A")

onemodel.add(p)

symbol = onemodel.get('std.Omega_A')

print(symbol)
