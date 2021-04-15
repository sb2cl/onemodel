from OneModel import OneModel
from ModelPart import ModelPart

om = OneModel()

mp = ModelPart(om)

mp.name
print(mp.name)

mp.name = "Omega_A"

print(mp.name)
