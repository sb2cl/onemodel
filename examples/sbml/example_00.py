import tellurium as te

model_name = 'example_00'

r = te.loada(f"""
model {model_name}
    S1 -> S2; k1*S1;
    k1 = 0.1;
    S1 = 10;
end
""")

m = r.simulate (0, 50, 300, ['time', 'S1', 'S2'])

r.plot(
    title='My plot', 
    xtitle='Time', 
    ytitle='Concentration', 
    dpi=150,
    savefig='./example_00.png'
)

r.exportToSBML('./example_00.xml', current=False)
