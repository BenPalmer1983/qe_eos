
class load_template:
  
  @staticmethod
  def run():
  
  
    # SAVE INPUT TEMPLATE
    template = pwscf_input()
    template.load(g.inp['pwscf_template']['file'])
    template.set_dirs()
    template.save("input_template.in", g.dirs['templates'])    
  
  
    # CREATE MODIFIED TEMPLATE FILE
    pw_in = pwscf_input()
    pw_in.load("input_template.in", g.dirs['templates'])   
     
    # Settings
    pw_in.set_ecutwfc(g.inp['settings']['ecutwfc'])
    pw_in.set_ecutrho(g.inp['settings']['ecutrho'])
    pw_in.set_k_points(g.inp['settings']['kpointstype'], g.inp['settings']['kpoints'])
    pw_in.set_degauss(g.inp['settings']['degauss'])
    
  
    if(g.inp['config']['structure'] is not None):
      alat = units.convert(g.inp['config']['alat_units'], 'bohr', g.inp['config']['alat'])
      pw_in.set_alat(alat)
      s = {
          'type': g.inp['config']['structure'],
          'labels': None,
          'size_x': g.inp['config']['size'],
          'size_y': g.inp['config']['size'],
          'size_z': g.inp['config']['size'],
          }       
      pw_in.set_config(s)
      
      g.data['size'] = g.inp['config']['size']
      
    # Atom count
    g.data['atoms_in_crystal_expanded'] = pw_in.get_nat()
    g.data['atoms_in_crystal'] = int(g.data['atoms_in_crystal_expanded'] / g.data['size']**3)
    g.data['alat_in_bohr'] = pw_in.get_alat()
    
    # SAVE
    pw_in.save("modified_template.in", g.dirs['templates'])
    
    
    
    
   