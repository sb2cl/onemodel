
#def test_ex02_two_gene_expression():
#
#    m = OneModel()
#
#    # Gene A
#    m['mRNA_A'] = Species(start=0)
#    m['protein_A'] = Species(start=0)
#
#    m['k_m_A'] = Parameter(value=1)    
#    m['d_m_A'] = Parameter(value=1)    
#    m['k_p_A'] = Parameter(value=1)    
#    m['d_p_A'] = Parameter(value=1)    
#
#    m['J1_A'] = Reaction(
#        None, 
#        'mRNA_A', 
#        'k_m_A'
#    )
#
#    m['J2_A'] = Reaction(
#        'mRNA_A', 
#        None, 
#        'd_m_A*mRNA_A']
#    )
#
#    m['J3_A'] = Reaction(
#        'mRNA_A', 
#        ['mRNA_A', 'protein_A'],
#        'k_p_A*mRNA_A'
#    )
#
#    m['J4_A'] = Reaction(
#        'protein_A', 
#        None, 
#        'd_p_A*protein_A'
#    )
#
#    # Gene B
#    m['mRNA_B'] = Species(start=0)
#    m['protein_B'] = Species(start=0)
#
#    m['k_m_B'] = Parameter(value=1)    
#    m['d_m_B'] = Parameter(value=1)    
#    m['k_p_B'] = Parameter(value=1)    
#    m['d_p_B'] = Parameter(value=1)    
#
#    m['J1_B'] = Reaction(
#        None, 
#        'mRNA_B', 
#        'k_m_B'
#    )
#
#    m['J2_B'] = Reaction(
#        'mRNA_B', 
#        None, 
#        'd_m_B*mRNA_B'
#    )
#
#    m['J3_B'] = Reaction(
#        'mRNA_B', 
#        ['mRNA_B', 'protein_B'],
#        'k_p_B*mRNA_B'
#    )
#
#    m['J4_B'] = Reaction(
#        'protein_B', 
#        None, 
#        'd_p_B*protein_B'
#    )
#
#def ProteinConstitutive(c):
#    c['mRNA'] = Species(start=0)
#    c['protein'] = Species(start=0)
#    
#    c['k_m'] = Parameter(value=1)    
#    c['d_m'] = Parameter(value=1)    
#    c['k_p'] = Parameter(value=1)    
#    c['d_p'] = Parameter(value=1)    
#    
#    c['J1'] = Reaction(
#        None, 
#        'mRNA', 
#        'k_m'
#    )
#    
#    c['J2'] = Reaction(
#        'mRNA', 
#        None, 
#        'd_m*mRNA'
#    )
#    
#    c['J3'] = Reaction(
#        'mRNA', 
#        ['mRNA', 'protein'],
#        'k_p*mRNA'
#    )
#    
#    c['J4'] = Reaction(
#        'protein', 
#        None, 
#        'd_p*protein'
#    )
#
#def test_ex03_protein_constitutive():
#
#    m = OneModel()
#    
#    ## Definition of Protein Constitutive class.
#    m['ProteinConstitutive'] = Class()
#
#    ProteinConstitutive(m['ProteinConstitutive'])
#
#    ## Create instance.
#    m['A'] = m['ProteinConstitutive'].__init__()
#
#
#def ProteinInduced(c):
#    ProteinConstitutive(c)
#
#    c['TF'] = Input()
#    c['k_m'] = Species(start = 0)
#    c['h'] = Parameter(value = 1)
#    c['k_m_max'] = Parameter(value = 1)
#    c['R1'] = Rule('k_m', 'k_m_max*TF/(TF+h)')
#
#def test_ex05_protein_induced():
#
#    m = OneModel()
#
#    m['ProteinConstitutive'] = ProteinConstitutive()
#    m['ProteinInduced'] = ProteinInduced()
#
#    m['A'] = m['ProteinConstitutive'].__init__()
#    m['B'] = m['ProteinInduced'].__init__()
#    m['R1'] = Rule('B.TF', 'A.protein']
#
