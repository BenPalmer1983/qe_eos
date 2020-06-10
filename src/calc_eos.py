


class calc_eos:



  @staticmethod
  def run(): 
    if(not g.inp['eos']['run']):
      return 0
    eos_template = pwscf_input()
    eos_template.load("modified_template.in", g.dirs['templates'])
    eos_template.set_dirs()
    eos_template.set_prefix() 
    eos_template.set_calculation("scf")
    
    
    r_alat = g.relaxed['alat']
    r_cp = g.relaxed['cp']
    
    eos_template.set_alat(r_alat)
    eos_template.set_cp(r_cp)
    
    eos_template.save("eos_template.in", g.dirs['templates'])
    
    
    # STRAIN
    s_val = g.inp['eos']['strain']
    s_points = g.inp['eos']['points']    
    s_arr = numpy.linspace(-s_val, s_val, s_points)

    #
    runfile = []
    f = pwscf_input()
    f.load("eos_template.in", g.dirs['templates'])
    for n in range(s_points):
      cp = (1.0 + s_arr[n]) * r_cp
      f.set_cp(cp)
      f.set_prefix() 
      nstr = str(n+1)
      while(len(nstr)<3):
        nstr = "0" + nstr
      
      f.save("eos_" + nstr + ".in", g.dirs['eos'])  
      runfile.append(g.dirs['eos'] + "/eos_" + nstr + ".in")
      
    # Prepare array to store data
    g.eos = {
             'complete': False,  
             'data': numpy.zeros((s_points, 3,),),
            }
    for n in range(s_points):
      g.eos['data'][n, 0] = float(s_arr[n])
      
      
    # RUN PWSCF
    if(g.inp['settings']['pwscf_run']):
      log, files_out, run_list = pwscf_exec.execute(runfile)
    else: 
      files_out = []
      
    try:
      for n in range(len(files_out)):
        fpo = pwscf_output(files_out[n]['file'])
        g.eos['data'][n, 1] = fpo.get_volume_per_atom()
        g.eos['data'][n, 2] = fpo.get_energy_per_atom()
    except:
      pass
      
    # SAVE DATA
    g.eos['complete'] = True  
    save_load.save(g.eos, g.dirs['data'] + '/' + 'eos.dat')  
    
    
    
