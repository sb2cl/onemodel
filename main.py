from OneModel import OneModel
from ModelPart import ModelPart
from Symbol import Symbol

om = OneModel()

mp = Symbol(om,"test")

mp.name = "Omega_A"
mp.nameTex = "Omega_A"
mp.units = 1

print(mp.name)
print(mp.nameTex)
print(mp.units)
