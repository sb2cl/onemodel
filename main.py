from OneModel import OneModel
from ModelPart import ModelPart
from Symbol import Symbol

om = OneModel()

mp = Symbol(om,"test")

print(mp.name)
print(mp.namebase)
print(mp.namespace)

mp.name = "Omega_A"

print(mp.name)
print(mp.namebase)
print(mp.namespace)
print(mp.nameTex)
