


class calc_ec:



  @staticmethod
  def run(): 
    if(not g.inp['ec']['run']):
      return 0
      
    ec_template = pwscf_input()
    ec_template.load("modified_template.in", g.dirs['templates'])
    ec_template.set_dirs()
    ec_template.set_prefix() 
    ec_template.set_calculation("scf")
    
    
    r_alat = g.relaxed['alat']
    r_cp = g.relaxed['cp']
        
    ec_template.set_alat(r_alat)
    ec_template.set_cp(r_cp)
    
    ec_template.save("ec_template.in", g.dirs['templates'])
    
    
    
    
    
    # STRAIN
    s_val = g.inp['ec']['strain']
    s_points = g.inp['ec']['points']    
    s_arr = numpy.linspace(0.0, s_val, s_points)
    
    # MAKE FILES
    f = pwscf_input()
    f.load("ec_template.in", g.dirs['templates'])
    runfile = []
    for dn in range(9):
      for j in range(s_points):
        sigma = s_arr[j]
        d = calc_ec.distortion(sigma, dn + 1)
        cp = numpy.matmul(d, r_cp)
        f.set_cp(cp)
        f.set_prefix() 
        
        nstr = str(j+1)
        while(len(nstr)<3):
          nstr = "0" + nstr
          
        f.save("ec_" + str(dn+1) + "_" + nstr + ".in", g.dirs['ec'])  
        runfile.append(g.dirs['ec'] + "/" + "ec_" + str(dn+1) + "_" + nstr + ".in")
        
        
    
    # Prepare arrays to store data
    g.ec = {'complete': False, }
              
    for dn in range(9):
      key = str(dn)
      g.ec[key] = numpy.zeros((s_points, 4,),)
      for n in range(s_points):
        g.ec[key][n, 0] = float(s_arr[n])
        
  
    # RUN PWSCF
    if(g.inp['settings']['pwscf_run']):
      log, files_out, run_list = pwscf_exec.execute(runfile)
    else:
      files_out = []
      
    try:
      s = 0
      for file in files_out:
        fpo = pwscf_output(file['file'])
        if(fpo.get_job_done() and fpo.get_job_converged()):        
          dn = s // s_points
          key = str(dn)
          n = s % s_points
          g.ec[key][n, 1] = fpo.get_volume_per_atom()
          g.ec[key][n, 2] = fpo.get_energy_per_atom()
          g.ec[key][n, 3] = fpo.get_total_energy()
          s = s + 1  
    except:
      pass
      
    # SAVE DATA
    g.ec['complete'] = True
    save_load.save(g.ec, g.dirs['data'] + '/' + 'ec.dat') 
    
  
  @staticmethod
  def distortion(sigma, dn):
    d = numpy.zeros((3,3),)
    if(dn == 1):
      d[0,0] = 1.0 + sigma
      d[1,1] = 1.0
      d[2,2] = 1.0
    elif(dn == 2):
      d[0,0] = 1.0
      d[1,1] = 1.0 + sigma
      d[2,2] = 1.0
    elif(dn == 3):
      d[0,0] = 1.0
      d[1,1] = 1.0
      d[2,2] = 1.0 + sigma
    elif(dn == 4):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[1,2] = sigma / a
      d[2,1] = sigma / a
    elif(dn == 5):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[0,2] = sigma / a
      d[2,0] = sigma / a
    elif(dn == 6):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = 1.0 / a
      d[1,1] = 1.0 / a
      d[2,2] = 1.0 / a
      d[0,1] = sigma / a
      d[1,0] = sigma / a
    elif(dn == 7):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0 + sigma) / a
      d[1,1] = (1.0 - sigma) / a
      d[2,2] = (1.0) / a
    elif(dn == 8):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0 + sigma) / a
      d[1,1] = (1.0) / a
      d[2,2] = (1.0 - sigma) / a
    elif(dn == 9):
      a = ((1 - sigma**2)**(1/3))
      d[0,0] = (1.0) / a
      d[1,1] = (1.0 + sigma) / a
      d[2,2] = (1.0 - sigma) / a
    return d
    
    
    
    
    
    
    
    