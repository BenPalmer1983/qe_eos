class atom_config:

  @staticmethod
  def make(settings_in={}):
  
    # Default Settings
    s = {
        'alat_in': None,
        'alat_out': None,
        'type': 'sc',
        'labels': ['Atom'],
        'size_x': 1,
        'size_y': 1,
        'size_z': 1,
        'vac': 0,
        'tetra': [],
        'octa': [],
        'atoms': [],
        'alat_change': 0.0,
        'cell_count': 0,
        'atom_count_no_defects': 0,
        'atom_count': 0,
        'log': [],
        }
               
    # Load Settings
    for k in s.keys():
      if(k in settings_in.keys()):
        s[k] = settings_in[k]

    # Atom list
    atoms = []
    
    # Size
    cell_count = s['size_x'] * s['size_y'] * s['size_z']
    

    # Base Cell
    b = atom_config.base(s['type'])
    
    # Unedited size
    a_count = len(b) * cell_count
    
    tetra_l = atom_config.r_list(s['tetra'], cell_count)
    octa_l = atom_config.r_list(s['octa'], cell_count)
    vac = []
    for v in range(s['vac']):
      vac.append('')
    vac = atom_config.r_list(vac, a_count)
        
    l = 0
    c = 0
    a = 0
    for x in range(s['size_x']):
      for y in range(s['size_y']):
        for z in range(s['size_z']):
          for n in range(len(b)):
            label = s['labels'][l % len(s['labels'])]
            xc = (x + b[n][0]) / s['size_x']
            yc = (y + b[n][1]) / s['size_y']
            zc = (z + b[n][2]) / s['size_z']            
            if(vac[a] == None):
              atoms.append([label, xc, yc, zc])
            else:
              s['log'].append('Vacancy: ' + str(label) + ' ' + str(xc) + ' ' + str(yc) + ' ' + str(zc) + ' ' )
            a = a + 1
            l = l + 1
          if(tetra_l[c] != None):
            t = atom_config.fcc_tetra()
            atoms.append([tetra_l[c], t[0][0], t[0][1], t[0][2]])
            s['log'].append('Tetra: ' + str(tetra_l[c]) + ' ' + str(t[0][0]) + ' ' + str(t[0][1]) + ' ' + str(t[0][2]) + ' ' )
          if(octa_l[c] != None):
            rn = random.randint(0,1)
            if(rn == 0):
              o = atom_config.fcc_octa_1()
            else:
              o = atom_config.fcc_octa_2()              
            atoms.append([octa_l[c], o[0][0], o[0][1], o[0][2]])
            s['log'].append('Octa: ' + str(octa_l[c]) + ' ' + str(o[0][0]) + ' ' + str(o[0][1]) + ' ' + str(o[0][2]) + ' ' )
          c = c + 1
            
    alat_change = (len(atoms)/a_count)**(1/3)  
    
    if(s['alat_in'] != None):
      try:
        s['alat_out'] = s['alat_in'] * s['size_x'] * alat_change
      except:
        pass
    
    # Store output
    s['atoms'] = atoms
    s['alat_change'] = alat_change
    s['cell_count'] = cell_count
    s['atom_count_no_defects'] = a_count
    s['atom_count'] = len(atoms)
 
    # RETURN
    return s
    

  @staticmethod
  def base(type = 'sc'):
    type = type.lower()
    if(type == 'bcc'):
      return atom_config.bcc()
    elif(type == 'fcc'):
      return atom_config.fcc()
    elif(type == 'zb'):
      return atom_config.zb()
    return atom_config.sc()
    

  @staticmethod
  def sc():
    return [
           [0.0,0.0,0.0]
           ]


  @staticmethod
  def bcc():
    return [
           [0.0,0.0,0.0],
           [0.5,0.5,0.5]
           ]
           
  @staticmethod
  def fcc():
    return [
           [0.0,0.0,0.0],
           [0.5,0.5,0.0],
           [0.5,0.0,0.5],
           [0.0,0.5,0.5]
           ]                
           
  @staticmethod
  def zb():
    return [
           [0.0,0.0,0.0],
           [0.5,0.5,0.0],
           [0.5,0.0,0.5],
           [0.0,0.5,0.5],
           [0.25,0.25,0.25],
           [0.75,0.75,0.25],
           [0.25,0.75,0.75],
           [0.75,0.25,0.75]
           ]   
           
           
  @staticmethod
  def fcc_tetra():
    return [
           [0.25,0.25,0.25]
           ]     
           
  @staticmethod
  def fcc_octa_1():
    return [
           [0.5,0.5,0.5]
           ]    
           
  @staticmethod
  def fcc_octa_2():
    return [
           [1.0,0.5,0.0]
           ]         
           
  @staticmethod        
  def r_list(inp, out_size):
    out = []
    for i in range(out_size):
      out.append(None)
    
    if(len(inp) == 0):
      return out
      
    for i in range(min(len(inp), out_size)):
      out[i] = inp[i]
    # Shuffle
    for i in range(5 * len(out)):
      a = random.randint(0,len(out)-1)
      b = random.randint(0,len(out)-1)
      while(a == b):
        b = random.randint(0,len(out)-1)
      temp = out[a]
      out[a] = out[b]
      out[b] = temp
    
    return out 
           
           
           
"""

  @staticmethod
  def sc(label, size=1):
    c_atoms = 4
    n_atoms = c_atoms * size**3
    if(not isinstance(label, (list,))):
      label = [label]
    atoms = ['crystal']
    for x in range(size):
      for y in range(size):
        for z in range(size):
          coords = [[str((x+0.0)/size), str((y+0.0)/size), str((z+0.0)/size)]]
          for i in range(len(coords)):
            atoms.append([label[i % len(label)],coords[i][0],coords[i][1],coords[i][2]])
    return atoms, c_atoms, n_atoms   

  @staticmethod
  def bcc(label, size=1):
    c_atoms = 4
    n_atoms = c_atoms * size**3
    if(not isinstance(label, (list,))):
      label = [label]
    atoms = ['crystal']
    for x in range(size):
      for y in range(size):
        for z in range(size):
          coords = [[str((x+0.0)/size), str((y+0.0)/size), str((z+0.0)/size)],
                    [str((x+0.5)/size), str((y+0.5)/size), str((z+0.5)/size)]]
          for i in range(len(coords)):
            atoms.append([label[i % len(label)],coords[i][0],coords[i][1],coords[i][2]])
    return atoms, c_atoms, n_atoms    

  @staticmethod
  def fcc(label, size=1):
    c_atoms = 4
    n_atoms = c_atoms * size**3
    if(not isinstance(label, (list,))):
      label = [label]
    atoms = ['crystal']
    for x in range(size):
      for y in range(size):
        for z in range(size):
          coords = [[str((x+0.0)/size), str((y+0.0)/size), str((z+0.0)/size)],
                    [str((x+0.5)/size), str((y+0.5)/size), str((z+0.0)/size)],
                    [str((x+0.5)/size), str((y+0.0)/size), str((z+0.5)/size)],
                    [str((x+0.0)/size), str((y+0.5)/size), str((z+0.5)/size)]]
          for i in range(len(coords)):
            atoms.append([label[i % len(label)],coords[i][0],coords[i][1],coords[i][2]])
    return atoms, c_atoms, n_atoms      

  @staticmethod
  def isolated(label, size=1):   
    c_atoms = 1
    n_atoms = 1
    if(not isinstance(label, (list,))):
      label = [label]
    atoms = ['crystal']
    atoms.append([label[0], "0.5", "0.5", "0.5"])
    return atoms, c_atoms, n_atoms   
    
"""    
    