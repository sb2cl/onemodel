from onemodel.onemodel import OneModel
from onemodel.parameter import Parameter

onemodel = OneModel()

p = Parameter("p1")
onemodel.add(p)
p = Parameter("p2")
onemodel.add(p)
p = Parameter("p3")
onemodel.add(p)

print(onemodel.parameters)
