


class calc_relax:



  @staticmethod
  def run():  
   
    # CREATE
    relax_file = pwscf_input()
    relax_file.load("modified_template.in", g.dirs['templates'])
    relax_file.set_dirs()
    relax_file.set_prefix() 
    relax_file.set_calculation("vc-relax")
    relax_file.save("relax.in", g.dirs['relax'])    


    # RUN PWSCF
    runfile = []
    runfile.append(g.dirs['relax'] + '/relax.in')
    
    if(g.inp['settings']['pwscf_run']):
      log, files_out, run_list = pwscf_exec.execute(runfile)
    else:
      files_out = []

    if(files_out[0]['status'] == 'complete'):     
      relaxed_file = pwscf_output(files_out[0]['file'])      
      g.relaxed['alat'] = relaxed_file.get_vc_relax_alat()
      g.relaxed['cp'] = relaxed_file.get_vc_relax_cp()
      g.relaxed['volume'] = relaxed_file.get_vc_relax_volume()
      g.relaxed['density'] = relaxed_file.get_vc_relax_density()
      g.relaxed['mass_per_crystal'] = relaxed_file.get_mass_per_crystal()
      
      save_load.save(g.relaxed, g.dirs['data'] + '/' + 'relax.dat')
    
    else:
      save_load.save({'ERROR': True,}, g.dirs['data'] + '/' + 'relax.dat')

      








#d = save_load.load(g.dirs['data'] + '/' + 'relax.dat')

