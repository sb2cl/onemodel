from OneModel import OneModel
from ModelPart import ModelPart
from Symbol import Symbol

om = OneModel()

mp = Symbol(om,"test")

mp.name = "Omega_A"
mp.comment = "This is a comment"

print(mp.name)
print(mp.comment)
