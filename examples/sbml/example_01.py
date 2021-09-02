import tellurium as te

model_name = 'example_01'

r = te.loada(f"""
model {model_name}
    J1: S1 -> S2; k1*S1;
    J2: S2 -> S3; k2*S2 - k3*S3
    J3: S3 -> S4; k4*S3;
    k1 = 0.1; k2 = 0.5; k3 = 0.5; k4 = 0.5;
    S1 = 100;
end
""")

m = r.simulate (0, 50, 300, ['time', 'S1', 'S2', 'S3', 'S4'])

r.plot(
    title='My plot', 
    xtitle='Time', 
    ytitle='Concentration', 
    dpi=150,
    savefig=f'./{model_name}.png'
)

r.exportToSBML(f'./{model_name}.xml', current=False)
