


class process_results:


  @staticmethod
  def run(): 
    if(g.eos['complete']):
      process_results.eos_results()
    if(g.ec['complete']):
      process_results.ec_results()
  
    if(g.ec['complete']):
      process_results.material_properties()
  
  @staticmethod
  def eos_results():
  
    ######################
    # EOS RESULTS
    ######################
  
      g.eos_results = {'complete': False}
      g.eos_results['data'] = g.eos['data']
    
      V = g.eos['data'][:,1]
      E = g.eos['data'][:,2]
      p = eos_fit.run(V, E)
    
      g.eos_results['V0'] = p[0]
      g.eos_results['E0'] = p[1]
      g.eos_results['B0'] = p[2]
      g.eos_results['B0P'] = p[3]
      g.eos_results['B0_gpa'] = p[2] * 14710.5
  
      V = numpy.linspace(g.eos['data'][0,1], g.eos['data'][-1,1], 101)
      E = eos_fit.bm_calc(V, p)
      g.eos_results['data_fit'] = numpy.zeros((101, 2,),)
      g.eos_results['data_fit'][:,0] = V
      g.eos_results['data_fit'][:,1] = E
    
      # SAVE DATA
      g.eos_results['complete'] = True
      save_load.save(g.eos_results, g.dirs['data'] + '/' + 'eos_results.dat')  
    
    
  
  
  @staticmethod
  def ec_results():
    ######################
    # EC RESULTS
    ######################
    
    # SAVE DATA POINTS
    g.ec_results = {'complete': False}
    for n in range(9):
      g.ec_results['data_' + str(n)] = g.ec[str(n)]
    
    # FIT POLY
    g.ec_results['fit'] = numpy.zeros((9, 3,),)
    for n in range(9):
      key = 'data_' + str(n)
      s = g.ec_results[key][:,0]
      E = g.ec_results[key][:,2]
      g.ec_results['fit'][n,:] = numpy.polyfit(s, E, 2)
      
    # FIT POINTS
    for n in range(9):
      key = 'data_' + str(n)
      s = numpy.linspace(g.ec_results[key][0,0], g.ec_results[key][-1,0], 101)
      E = process_results.p_calc(g.ec_results['fit'][n,:], s)
      g.ec_results['data_fit_' + str(n)] = numpy.zeros((101, 2,),)
      g.ec_results['data_fit_' + str(n)][:,0] = s[:]
      g.ec_results['data_fit_' + str(n)][:,1] = E[:]
    
    
    # CALC ELASTIC CONSTANTS
    pf = numpy.zeros((9,),)
    for n in range(9):
      pf[n] = g.ec_results['fit'][n,0]
    
    v = g.relaxed['volume']
    
    c11 = (2 / v) * pf[0]
    c22 = (2 / v) * pf[1]
    c33 = (2 / v) * pf[2]
    c44 = (1 / (2 * v)) * pf[3]
    c55 = (1 / (2 * v)) * pf[4]
    c66 = (1 / (2 * v)) * pf[5]
    c12 = (c11 + c22) / 2 - pf[6] / v
    c13 = (c11 + c33) / 2 - pf[7] / v    
    c23 = (c22 + c33) / 2 - pf[8] / v
    
    
    g.ec_results['stiffness'] = numpy.zeros((6,6,),)
    g.ec_results['stiffness_gpa'] = numpy.zeros((6,6,),)
    g.ec_results['compliance'] = numpy.zeros((6,6,),)
    
    
    g.ec_results['stiffness'][0,0] = c11
    g.ec_results['stiffness'][1,1] = c22
    g.ec_results['stiffness'][2,2] = c33
    g.ec_results['stiffness'][3,3] = c44
    g.ec_results['stiffness'][4,4] = c55
    g.ec_results['stiffness'][5,5] = c66
    
    g.ec_results['stiffness'][0,1] = c12
    g.ec_results['stiffness'][1,0] = c12
    g.ec_results['stiffness'][0,2] = c13
    g.ec_results['stiffness'][2,0] = c13
    g.ec_results['stiffness'][1,2] = c23
    g.ec_results['stiffness'][2,1] = c23
    
    # GPA Stiffness Matrix
    for i in range(6):
      for j in range(6):
        g.ec_results['stiffness_gpa'][i,j] = units.convert('RY/BOHR3', 'GPA', g.ec_results['stiffness'][i,j])
   
    # Compliance Matrix
    g.ec_results['compliance'][:,:] = numpy.linalg.inv(g.ec_results['stiffness_gpa'][:,:])
    
    # SAVE DATA
    g.ec_results['complete'] = True
    save_load.save(g.ec_results, g.dirs['data'] + '/' + 'ec_results.dat')  
    
    
  
  
  @staticmethod
  def material_properties():
  
    ############################################
    # CALCULATE MATERIAL PROPERTIES
    ############################################
    
    # Constants
    h = 6.62607004e-34
    k = 1.38064852e-23
    pi = 3.1415926535898
    na = 6.02214076e23
        
    c = g.ec_results['stiffness_gpa']
    s = g.ec_results['compliance']
    rho = g.relaxed['density']
    
    g.material_properties = {}
  
    g.material_properties['E_vec'] = numpy.zeros((3,),)
    g.material_properties['E_vec'][0] = 1.0 / s[0,0]
    g.material_properties['E_vec'][1] = 1.0 / s[1,1]
    g.material_properties['E_vec'][2] = 1.0 / s[2,2]
    
    g.material_properties['G_vec'] = numpy.zeros((3,),)
    g.material_properties['G_vec'][0] = 1.0 / (2.0 * s[3,3])
    g.material_properties['G_vec'][1] = 1.0 / (2.0 * s[4,4])
    g.material_properties['G_vec'][2] = 1.0 / (2.0 * s[5,5])
    
    g.material_properties['v_vec'] = numpy.zeros((3,3,),)
    g.material_properties['v_vec'][0,0] = 1.0
    g.material_properties['v_vec'][1,0] = -(s[0,1] * g.material_properties['E_vec'][1])
    g.material_properties['v_vec'][2,0] = -(s[0,2] * g.material_properties['E_vec'][2])
    g.material_properties['v_vec'][0,1] = -(s[1,0] * g.material_properties['E_vec'][0])
    g.material_properties['v_vec'][1,1] = 1.0
    g.material_properties['v_vec'][1,2] = -(s[1,2] * g.material_properties['E_vec'][2])
    g.material_properties['v_vec'][2,0] = -(s[2,0] * g.material_properties['E_vec'][0])
    g.material_properties['v_vec'][2,1] = -(s[2,1] * g.material_properties['E_vec'][1])
    g.material_properties['v_vec'][2,2] = 1.0
    
    g.material_properties['GR'] = 15 / (4*(s[0,0]+s[1,1]+s[2,2]) - 4*(s[0,1]+s[0,2]+s[1,2]) + 3*(s[3,3]+s[4,4]+s[5,5]))
    g.material_properties['GV'] = (1/15)*(c[0,0]+c[1,1]+c[2,2]-c[0,1]-c[0,2]-c[1,2])+(1/5)*(c[3,3]+c[4,4]+c[5,5])
    g.material_properties['G'] = (1/2) * (g.material_properties['GV'] + g.material_properties['GR'])
    G = g.material_properties['G']
    
    g.material_properties['BR'] = 1 / ((s[0,0] + s[1,1] + s[2,2])+ 2*(s[0,1] + s[0,2] + s[1,2]))
    g.material_properties['BV'] = (1/9)*(c[0,0]+c[1,1]+c[2,2])+(2/9)*(c[0,1]+c[0,2]+c[1,2])
    g.material_properties['B'] = (1/2) * (g.material_properties['BV'] + g.material_properties['BR'])
    B = g.material_properties['B']
    
    g.material_properties['vl'] = numpy.sqrt((B + (4/3) * G)/rho) 
    g.material_properties['vt'] = numpy.sqrt(G/rho)
    g.material_properties['vm'] = ((1/3)*(2/(g.material_properties['vt']**3) + 1/(g.material_properties['vl']**3)))**(-(1/3))
    
    g.material_properties['E'] = (9 * B * G) / (3*B + G)
    g.material_properties['v'] = (3 * B - 2 * G) / (2 * (3 * B + G))
    
    
    
    h = 6.62607004e-34
    k = 1.38064852e-23
    pi = 3.1415926535898
    na = 6.02214076e23
    n = g.data['atoms_in_crystal']
    M = g.relaxed['mass_per_crystal']
    vm = g.material_properties['vm']
    
    g.material_properties['debye'] = ((h/k) * (((3 * n)/(4*pi))*((na * rho) / M))**(1/3)) * vm
    
    cavg = (c[0,0] + c[1,1] + c[2,2]) / 3
    g.material_properties['melting_point'] = 598 + 6.66 * cavg - 0.003 * cavg**2 
    
    
    # SAVE DATA
    save_load.save(g.material_properties, g.dirs['data'] + '/' + 'material_properties.dat')  
    
    
    
    
    ############################################
    # SAVE TO LOG
    ############################################
    
 
    g.log_fh.write("\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("EOS Parameters\n")
    g.log_fh.write("############################\n")
    g.log_fh.write("V0 " + str(p[0]) + " Bohr^3\n")
    g.log_fh.write("E0 " + str(p[1]) + " Ry\n")
    g.log_fh.write("B0 " + str(p[2]) + " Ry/Bohr^3\n")
    g.log_fh.write("B0P " + str(p[3]) + "\n")
    g.log_fh.write("B0 " + str(p[2] * 14710.5) + " GPa\n")
    g.log_fh.write("\n")
    
    

    
  @staticmethod
  def p_calc(p, x):
    return p[0] * x**2 + p[1] * x + p[2]
    
    
    """
    fh.write("Atoms in crystal:             " + str(g.data['atoms_in_crystal']) + "\n")
    fh.write("Atoms in crystal (exp.):      " + str(globals.d['atoms_in_crystal_expanded']) + "\n")
    fh.write("AMU per crystal:              " + str(globals.d['mass_per_crystal']) +"\n")
    fh.write("\n")
    fh.write("Ecutwfc:                      " + str(globals.d['calc_ecutwfc']) +"\n")
    fh.write("Ecutrho:                      " + str(globals.d['calc_ecutrho']) +"\n")
    fh.write("Degauss:                      " + str(globals.d['calc_degauss']) +"\n")
    fh.write("Kpoints:                      " + str(globals.d['calc_kpoints']) +"\n")
    fh.write("\n")

    
    
    
    fh.write("EOS Points:                   " + str(globals.d['eos_points']) +"\n")
    fh.write("Total Strain:                 " + str(globals.d['eos_strain']) +"\n")
    fh.write("\n") 
    fh.write("V0 (Bohr^3):                  " + str(globals.d['eos_v0']) +"\n")
    fh.write("E0:                           " + str(globals.d['eos_e0']) +"\n")
    fh.write("B0 (RY/BOHR3):                " + str(globals.d['eos_b0']) +"\n")
    fh.write("B0 (GPA):                     " + str(globals.d['eos_b0_gpa']) +"\n")
    fh.write("B0P:                          " + str(globals.d['eos_b0p']) +"\n")    
    fh.write("\n")
    fh.write("EC Points:                    " + str(globals.d['ec_points']) +"\n")
    fh.write("Total Strain:                 " + str(globals.d['ec_strain']) +"\n")
    fh.write("\n")
    fh.write("\n")
    fh.write("Relaxed alat (Bohr):          " + str(globals.d['relaxed_alat'] / globals.d['size']) +"\n")
    fh.write("Relaxed alat (Bohr) (exp):    " + str(globals.d['relaxed_alat']) +"\n")
    fh.write("Relaxed alat (Ang):           " + str((globals.d['relaxed_alat'] / globals.d['size'])*0.529) +"\n")
    fh.write("Relaxed alat (Ang) (exp):     " + str(globals.d['relaxed_alat']*0.529) +"\n")
    fh.write("Relaxed cp:                   " + std.float_padded(globals.d['relaxed_cp'][0,0]) +" " + std.float_padded(globals.d['relaxed_cp'][0,1]) +" " + std.float_padded(globals.d['relaxed_cp'][0,2]) +"\n")
    fh.write("                              " + std.float_padded(globals.d['relaxed_cp'][1,0]) +" " + std.float_padded(globals.d['relaxed_cp'][1,1]) +" " + std.float_padded(globals.d['relaxed_cp'][1,2]) +"\n")
    fh.write("                              " + std.float_padded(globals.d['relaxed_cp'][2,0]) +" " + std.float_padded(globals.d['relaxed_cp'][2,1]) +" " + std.float_padded(globals.d['relaxed_cp'][2,2]) +"\n")
    fh.write("Relaxed volume (Bohr^3):      " + str(globals.d['relaxed_volume']) +"\n")
    fh.write("Relaxed density (kgm^-3):     " + str(globals.d['relaxed_density']) +"\n")
    fh.write("\n")
    
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (RY/BOHR3):         " + std.float_padded(globals.d['stiffness'][i,0], 10) + " " + std.float_padded(globals.d['stiffness'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['stiffness'][i,2], 10) + " " + std.float_padded(globals.d['stiffness'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['stiffness'][i,4], 10) + " " + std.float_padded(globals.d['stiffness'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + std.float_padded(globals.d['stiffness'][i,0], 10) + " " + std.float_padded(globals.d['stiffness'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['stiffness'][i,2], 10) + " " + std.float_padded(globals.d['stiffness'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['stiffness'][i,4], 10) + " " + std.float_padded(globals.d['stiffness'][i,5], 10) + "\n" )    
    
    fh.write("\n")    
    for i in range(6):
      if(i == 0):        
        fh.write("Stiffness (GPA):              " + std.float_padded(globals.d['stiffness_gpa'][i,0], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['stiffness_gpa'][i,2], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['stiffness_gpa'][i,4], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + std.float_padded(globals.d['stiffness_gpa'][i,0], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['stiffness_gpa'][i,2], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['stiffness_gpa'][i,4], 10) + " " + std.float_padded(globals.d['stiffness_gpa'][i,5], 10) + "\n" )

    fh.write("\n")
    for i in range(6):
      if(i == 0):        
        fh.write("Compliance (1/GPA):           " + std.float_padded(globals.d['compliance_gpa'][i,0], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['compliance_gpa'][i,2], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['compliance_gpa'][i,4], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,5], 10) + "\n" )
      else:
        fh.write("                              " + std.float_padded(globals.d['compliance_gpa'][i,0], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,1], 10) + " " + 
                                                std.float_padded(globals.d['compliance_gpa'][i,2], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,3], 10) + " "  + 
                                                std.float_padded(globals.d['compliance_gpa'][i,4], 10) + " " + std.float_padded(globals.d['compliance_gpa'][i,5], 10) + "\n" )                                            
    fh.write("\n")
    
    
    fh.write("Bulk Modulus B (GPA):         " + str(globals.d['B']) + "\n")
    fh.write("BR (GPA):                     " + str(globals.d['BR']) + "\n")
    fh.write("BV (GPA):                     " + str(globals.d['BV']) + "\n")
    fh.write("\n")
    
    fh.write("Shear Modulus G (GPA):        " + str(globals.d['G']) + "\n")
    fh.write("GR:                           " + str(globals.d['GR']) + "\n")
    fh.write("GV:                           " + str(globals.d['GV']) + "\n")
    fh.write("\n")
    
    fh.write("Young's Modulus E (GPA):      " + str(globals.d['E']) + "\n")
    fh.write("\n")
    fh.write("Poisson's Ratio v:            " + str(globals.d['v']) + "\n")
    fh.write("\n")
    fh.write("\n")
    
    
    fh.write("L Elastic Wave V:             " + str(globals.d['vl']) + "\n")
    fh.write("T Elastic Wave V:             " + str(globals.d['vt']) + "\n")
    fh.write("M Elastic Wave V:             " + str(globals.d['vm']) + "\n")
    fh.write("\n")
    fh.write("Debye Temperature:            " + str(globals.d['debye']) + "\n")
    fh.write("\n")
    fh.write("Melting Point:                " + str(round(globals.d['melting_point'],0)) + "K \n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")
    fh.write("\n")
    """
  
    
    
    
    
