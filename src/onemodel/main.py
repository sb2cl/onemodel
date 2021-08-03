from onemodel.onemodel import OneModel
from onemodel.symbol import Symbol

om = OneModel()

mp = Symbol("std.Omega_A")

om.set(mp)

symbol = om.get('std.Omega_A')

print(symbol)
