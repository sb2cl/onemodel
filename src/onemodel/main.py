from onemodel.onemodel import OneModel
from onemodel.model_part import ModelPart
from onemodel.symbol import Symbol

om = OneModel()

mp = Symbol(om,"test")

mp.name = "Omega_A"

print(mp.name)
print(mp.reference)
