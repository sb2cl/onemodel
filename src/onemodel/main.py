from onemodel.onemodel import OneModel
from onemodel.symbol import Symbol

om = OneModel()

mp = Symbol(om,"std::Omega_A")

mp.name = "std::Omega_A"

print(mp.name)
print(mp.reference)
print(mp)
print(mp)
