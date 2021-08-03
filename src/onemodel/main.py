from onemodel.onemodel import OneModel
from onemodel.symbol import Symbol

onemodel = OneModel()

symbol = Symbol("std.Omega_A")

onemodel.add(symbol)

symbol = onemodel.get('std.Omega_A')

print(symbol)
