################################################################
#    Processing PWscf input file
#
#
#
#
################################################################



import os
import datetime
import re
import sys
import numpy
import hashlib 
import random
from rand_dist import rand_dist
from pwscf_output import pwscf_output
from atom_config import atom_config

############################
#  pwscf_input
############################

class pwscf_input:

  def __init__(self, file_name=None, file_dir=None):
    self.file_data = []
    self.file_name = None
    self.dir_name = None
    self.reset()
    self.defaults()
    self.rand = rand_dist()
    self.rand.gheat()
    self.rand_seed_set = 0
    if(file_name != None):
      self.load(file_name, file_dir)

  def reset(self):

    # Control
    self.control = {
      "calculation": None,
      "title": None,
      "verbosity": None,
      "restart_mode": None,
      "wf_collect": None,
      "nstep": None,
      "iprint": None,
      "tstress": None,
      "tprnfor": None,
      "dt": None,
      "outdir": None,
      "wfcdir": None,
      "prefix": None,
      "lkpoint_dir": None,
      "max_seconds": None,
      "etot_conv_thr": None,
      "forc_conv_thr": None,
      "disk_io": None,
      "pseudo_dir": None,
      "tefield": None,
      "dipfield": None,
      "lelfield": None,
      "nberrycyc": None,
      "lorbm": None,
      "lberry": None,
      "gdir": None,
      "nppstr": None,
      "lfcpopt": None,
      "gate": None
    }

    # SYSTEM
    self.system = {
      "ibrav": None,
      "celldm": None,
      "A": None,
      "B": None,
      "C": None,
      "cosAB": None,
      "cosAC": None,
      "cosBC": None,
      "nat": None,
      "ntyp": None,
      "nbnd": None,
      "tot_charge": None,
      "starting_charge": None,
      "tot_magnetization": None,
      "starting_magnetization": None,
      "ecutwfc": None,
      "ecutrho": None,
      "ecutfock": None,
      "nr1": None,
      "nr2": None,
      "nr3": None,
      "nr1s": None,
      "nr2s": None,
      "nr3s": None,
      "nosym": None,
      "nosym_evc": None,
      "noinv": None,
      "no_t_rev": None,
      "force_symmorphic": None,
      "use_all_frac": None,
      "occupations": None,
      "one_atom_occupations": None,
      "starting_spin_angle": None,
      "degauss": None,
      "smearing": None,
      "nspin": None,
      "noncolin": None,
      "ecfixed": None,
      "qcutz": None,
      "q2sigma": None,
      "input_dft": None,
      "exx_fraction": None,
      "screening_parameter": None,
      "exxdiv_treatment": None,
      "x_gamma_extrapolation": None,
      "ecutvcut": None,
      "nqx1": None,
      "nqx2": None,
      "nqx3": None,
      "lda_plus_u": None,
      "lda_plus_u_kind": None,
      
      
      "xdm": None,
      "xdm_a1": None,
      "xdm_a2": None,
      "space_group": None,
      "uniqueb": None,
      "origin_choice": None,
      "rhombohedral": None,
      "zgate": None,
      "relaxz": None,
      "block": None,
      "block_1": None,
      "block_2": None,
      "block_height": None
    }
    
    # ELECTRONS
    self.electrons = {
      "electron_maxstep": None,
      "scf_must_converge": None,
      "conv_thr": None,
      "adaptive_thr": None,
      "conv_thr_init": None,
      "conv_thr_multi": None,
      "mixing_mode": None,
      "mixing_beta": None,
      "mixing_ndim": None,
      "mixing_fixed_ns": None,
      "diagonalization": None,
      "ortho_para": None,
      "diago_thr_init": None,
      "diago_cg_maxiter": None,
      "diago_david_ndim": None,
      "diago_full_acc": None,
      "efield": None,
      "efield_cart": None,
      "efield_phase": None,
      "startingpot": None,
      "startingwfc": None,
      "tqr": None
    }

    # IONS
    self.ions = {
      "ion_dynamics": None,
      "ion_positions": None,
      "pot_extrapolation": None,
      "wfc_extrapolation": None,
      "remove_rigid_rot": None,
      "ion_temperature": None,
      "tempw": None,
      "tolp": None,
      "delta_t": None,
      "nraise": None,
      "refold_pos": None,
      "upscale": None,
      "bfgs_ndim": None,
      "trust_radius_max": None,
      "trust_radius_min": None,
      "trust_radius_ini": None,
      "w_1": None,
      "w_2": None
    }

    # CELL
    self.cell = {
      "cell_dynamics": None,
      "press": None,
      "wmass": None,
      "cell_factor": None,
      "press_conv_thr": None,
      "cell_dofree": None
    }

    # Other lists
    self.atomic_species = []
    self.atomic_positions = []
    self.k_points = []
    self.cell_parameters = []

    # File
    self.file = ""


  def defaults(self):
      
    try:
      self.scratch_dir = os.environ['PWSCF_SCRATCH']
    except:
      self.scratch_dir = '/opt/scratch'

    try:
      self.pp_dir = os.environ['PWSCF_PP']
    except:
      self.pp_dir = '/opt/pp'





  #  Load data from file 
  def load(self, file_name, file_dir=None): 
    self.file_name = file_name
    self.dir_name = file_dir
    if(file_dir != None):
      self.file_path = file_dir + "/" + file_name
    else:  
      self.file_path = file_name
    data = self.load_from_file(self.file_path)
    self.load_data(data)
    
 
  # Load from a block of data (text, file etc)
  def load_data(self, data):  
    # Store data into file_data list
    self.file_data.append(data)
    
    # Reset data store
    self.reset()
    
    # Clean
    data = pwscf_input.clean(data)

    # split
    data = data.split("\n")    
    
    # Load keywords
    ###################################
    keywords = []
    # Load Keywords
    for line in data:
      line = line.strip()
      if(len(line)>0):
        # Remove trailing comma
        if(line[-1] == ","):
          line = line[0:-1]
        fields = line.split("=")
        if(len(fields) == 2):
          field_lc = fields[0].lower()
          keyword, id = pwscf_input.process_keyword(field_lc)          
          pwscf_input.add_keyword(keywords, keyword, id, fields[1])
      
    for pair in keywords:
      if(pair[0] in self.control):
        self.control[pair[0]] = pair[1]
      elif(pair[0] in self.system):
        self.system[pair[0]] = pair[1]
      elif(pair[0] in self.electrons):
        self.electrons[pair[0]] = pair[1]
      elif(pair[0] in self.ions):
        self.ions[pair[0]] = pair[1]
      elif(pair[0] in self.cell):
        self.cell[pair[0]] = pair[1]        

    # Load atomic species
    ###################################    
    n_species = 0    
    if(self.system['ntyp'] != None):
      try:
        n_species = int(self.system['ntyp'])
      except:  
        n_species = 0        
    if(n_species > 0):
      counter = 0
      for line in data:
        line = line.strip()
        if(line.upper()[0:14] == "ATOMIC_SPECIES"):
          counter = counter + 1
        elif(counter > 0 and counter <= n_species and line != ""):
          counter = counter + 1
          self.atomic_species.append(pwscf_input.fields(line))

    # Load atomic positions
    ###################################    
    n_atoms = 0    
    if(self.system['nat'] != None):
      try:
        n_atoms = int(self.system['nat'])
      except:  
        n_atoms = 0        
    if(n_atoms > 0):
      counter = 0
      for line in data:
        line = line.strip()
        if(line.upper()[0:16] == "ATOMIC_POSITIONS"):
          fields = pwscf_input.fields(line)
          if(len(fields) == 2):
            self.atomic_positions.append(fields[1])
          counter = counter + 1
        elif(counter > 0 and counter <= n_atoms and line != ""):
          counter = counter + 1
          self.atomic_positions.append(pwscf_input.fields(line))

    # k_points
    ###################################      
    flag = 0
    for line in data:
      line = line.strip()
      if(line.upper()[0:8] == "K_POINTS"):           
        fields = pwscf_input.fields(line)
        k_points_type = fields[1]
        self.k_points.append(k_points_type)
        if(k_points_type.upper() == "AUTOMATIC"):
          flag = 1
      elif(flag > 0):
        flag = flag - 1        
        fields = pwscf_input.fields(line)
        self.k_points.append(fields)
        
    # cell parameters
    ###################################      
    flag = 0
    for line in data:
      line = line.strip()
      if(line.upper()[0:15] == "CELL_PARAMETERS"): 
        fields = pwscf_input.fields(line)
        self.cell_parameters.append(fields[1])

        flag = 3
      elif(flag>0):        
        fields = pwscf_input.fields(line)
        self.cell_parameters.append(fields)


    self.make()



  #  Run as it's own program
  def run(self):
    self.reset()

    option = ""
    file_name = ""

    if(len(sys.argv) > 1 and sys.argv[1] is not None):
      option = sys.argv[1]

    if(len(sys.argv) > 2 and sys.argv[2] is not None):
      file_name = sys.argv[2]

    if(option.lower().strip() == "" or option.lower().strip() == "interactive"):
      self.menu()
      exit()
    elif(option.lower().strip() == "quiet"):
      print("Quiet")
    else:
      return 0






#################################
# READ/LOAD input file
#################################

  def load_from_file(self, file_name):
    # Init variable
    file_data = ""

    # Read it in line by line
    fh = open(file_name, "r")
    for file_row in fh:
      file_data = file_data + file_row.strip() + '\n'

    return file_data




#################################
# MAKE input file
#################################

  def make(self):
  
    now = datetime.datetime.now()
    time_now = str(now.hour) + ":" + str(now.minute) + "   " + str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    file = "! Edited " + time_now + "\n"
    
    # CONTROL
    file += "&CONTROL \n"
    for key in sorted(self.control.keys()):
      file += pwscf_input.make_line(key, self.control[key])
    file += "/ \n"
    
    # SYSTEM
    file += "&SYSTEM \n"
    for key in sorted(self.system.keys()):
      file += pwscf_input.make_line(key, self.system[key]) 
    file += "/ \n"

    # ELECTRONS
    file += "&ELECTRONS \n"
    for key in sorted(self.electrons.keys()):
      value = self.electrons[key]
      if(value != None):
        file += str(key) + " = " + str(value) + ", \n"      
    file += "/ \n"

    # IONS
    file += "&IONS \n"
    for key in sorted(self.ions.keys()):
      value = self.ions[key]
      if(value != None):
        file += str(key) + " = " + str(value) + ", \n"      
    file += "/ \n"

    # CELL
    file += "&CELL \n"
    for key in sorted(self.cell.keys()):
      value = self.cell[key]
      if(value != None):
        file += str(key) + " = " + str(value) + ", \n"      
    file += "/ \n"

    # ATOMIC_SPECIES
    file += "ATOMIC_SPECIES \n"
    for species in self.atomic_species:      
      for field in species:
        file += str(field) + " "
      file += "\n"

    # ATOMIC_POSITIONS
    header = 0
    for position in self.atomic_positions:      
      if(header == 0):
        file += "ATOMIC_POSITIONS "
        file += str(position) + "\n"
        header = 1
      #elif(header == 1):
      #  file += position[1] + "\n"
      #  header = 2
      elif(header == 1):  
        for field in position:
          file += str(field) + "   "
        file += "\n"

    # K_POINTS
    kpoints_type = self.k_points[0]
    kpoints_mesh = ''
    if(len(self.k_points) == 2):
      if(type(self.k_points[1]) == list):
        for k in self.k_points[1]:
          kpoints_mesh += str(k) + ' '
      else:
        kpoints_mesh += self.k_points[1]
    elif(len(self.k_points) == 7):
      for i in range(1,len(self.k_points)):
        kpoints_mesh += self.k_points[i] + ' '
    
    file += "K_POINTS " + kpoints_type
    file += "\n"
    file += kpoints_mesh + " "
    file += "\n"   
        

    # K_POINTS
    file += "CELL_PARAMETERS " + self.cell_parameters[0]
    file += "\n"
    for i in range(1,len(self.cell_parameters)):
      for point in self.cell_parameters[i]:
        file += str(point) + " "
      file += "\n"
      
    # Process
    file = file.strip()
    
    # Store data into file_data list
    self.file_data.append(file)



  def print_out(self):
    self.make()
    print(self.file_data[-1])
    
    


  def print_history(self):
    for file in self.file_data:
      print(file)
      print()
    
    
############################
#  Save, Save/Load Original
############################    
    
  def save(self, file=None, dir=None):
    # Build latest version of file
    self.make()
    
    if(file == None):
      file = self.file_name
    if(dir == None):  
      dir = self.dir_name
      
    self.file_name = file
    self.dir_name = dir
    
    if(dir == None):
      path = file
    else:  
      if (not os.path.exists(dir)):
        os.makedirs(dir)
      path = dir + "/" + file
      
    # Write latest data  
    fh = open(path, "w")
    fh.write(self.file_data[-1])
    fh.close()
    
    
  def save_original(self, file=None, dir=None):
    if(file == None):
      file = self.file_name
    if(dir == None):  
      dir = self.dir_name
      
    self.file_name = file
    self.dir_name = dir
    
    if(dir == None):
      path = file
    else:  
      if (not os.path.exists(dir)):
        os.makedirs(dir)
      path = dir + "/" + file
      
    # Write latest data  
    fh = open(path, "w")
    fh.write(self.file_data[0])
    fh.close()
    
    
  def load_original(self, file=None, dir=None):
    self.load_data(self.file_data[0])
    

############################
#  Set
############################
  
  # Control
  ####################
    
  def set_calculation(self, type=None):
    if(type == None):
      type = "SCF"    
    self.control['calculation'] = '"' + type.lower() + '"'
    
  def set_var(self, var, value):
    for key in sorted(self.control.keys()):
      if(key.upper().strip() == var.upper().strip()):
        self.control['key'] = value
        return True
    return False

  def set_dirs(self, scratch_dir = None, pp_dir = None):
    if(scratch_dir != None):
      self.scratch_dir = scratch_dir
    if(pp_dir != None):
      self.pp_dir = pp_dir
   
    self.control['outdir'] = '"' + self.scratch_dir + '"'
    self.control['pseudo_dir'] = '"' + self.pp_dir + '"'

  def set_prefix(self, pin = None):    
    if(pin == None):
      pin = pwscf_input.rand_string()
    self.control['prefix'] = '"' + pin + '"'

  # System
  ####################
    
  def set_alat(self, alat, variance=0.0, rand_seed=0):
    if(variance != 0.0):
      if(rand_seed == 1 and self.rand_seed_set == 0):
        self.rand_seed_set = 1
        self.rand.randomSeed()
      alat = alat + variance * self.rand.rng()  
      
    self.system['celldm'][0] = str(alat)
    
  def set_degauss(self, degauss):  
    self.system['degauss'] = str(degauss)

  def set_ecutrho(self, ecutrho):  
    self.system['ecutrho'] = str(ecutrho)

  def set_ecutwfc(self, ecutwfc):  
    self.system['ecutwfc'] = str(ecutwfc)

  def set_nosym(self, nosym=False):  
    if(nosym == True or nosym.lower() == ".true."):
      self.system['nosym'] = ".TRUE."
    else:
      self.system['nosym'] = ".FALSE."

  def set_nspin(self, value):
    if(value == 2 or value == "2"):
      self.system['nspin'] = "2"
    elif(value == 4 or value == "4"):
      self.system['nspin'] = "4"
    else:  
      self.system['nspin'] = "1"

  def set_tot_magnetization(self, tot_magnetization):  
    self.system['tot_magnetization'] = str(tot_magnetization)
      
  def set_as_isolated(self, alat=10.0):
    self.set_alat(alat)
    self.set_nosym(True)
    self.set_nspin(2)
    self.set_tot_magnetization(0)
    self.set_cp_identity()
    self.load_config("ISOLATED")


  # Cell Parameters
  ####################

  # Just the 3x3 array
  def set_cell_parameters(self, cell_in):
    type = self.cell_parameters[0]
    self.cell_parameters = [type]
    for row in cell_in:
      new_row = []
      for cell in row:
        new_row.append(str(cell))
      self.cell_parameters.append(new_row) 
      
  # Just the 3x3 array 
  def set_cp_arr(self, cp):
    if(len(cp) == 6):
      cp = pwscf_standard.unvoight(cp)
    self.set_cell_parameters(cp)
    
  def set_cp_strain(self, cp, strain):
    cp = numpy.matmul(strain, cp)
    self.set_cell_parameters(cp)
      
  # Copy entire list [,[,,],[,,],[,,]]    
  def set_cp(self, cp):
    if(isinstance(cp, numpy.ndarray)):
      cp_list = []
      for i in range(3):
        cp_list.append([cp[i,0],cp[i,1], cp[i,2]])
      self.set_cell_parameters(cp_list)
    elif(isinstance(cp, list)):
      self.cell_parameters = cp  
    
  def set_cp_identity(self):
    self.set_cell_parameters([[1.0,0.0,0.0],[0.0,1.0,0.0],[0.0,0.0,1.0]])
    
  def set_cp_zeros(self):
    self.set_cell_parameters([[0.0,0.0,0.0],[0.0,0.0,0.0],[0.0,0.0,0.0]])
    
  
  def set_seed(self, seed=0):
    random.seed(seed)
    self.rand.setSeed(seed)
    self.rand_seed_set = 1


  # K-Points
  ####################
  def set_k_points(self, k_points_type, points_list):
    self.k_points = []
    self.k_points.append(k_points_type)
    self.k_points.append(points_list)  
    
    
  # Atom Positions
  ####################
  def set_atomic_positions(self, atoms, c_type='crystal'):    
    self.system['nat'] = str(len(atoms))
    self.atomic_positions = []
    self.atomic_positions.append(c_type)
    for atom in atoms:
      self.atomic_positions.append([str(atom[0]),str(float(atom[1])),str(float(atom[2])),str(float(atom[3]))])
    
    
  
    
  def set_config(self, s):
  
    if(s['labels'] == None):
      s['labels'] = self.get_atom_labels()      
    s['alat_in'] = float(self.system['celldm'][0])
    
    a = atom_config.make(s)     
    
    self.atomic_positions = []
    self.atomic_positions.append('crystal')
    self.system['nat'] = str(len(a['atoms']))
    for atom in a['atoms']:
      self.atomic_positions.append([str(atom[0]),str(float(atom[1])),str(float(atom[2])),str(float(atom[3]))])
    
    self.system['celldm'][0] = str(float(a['size_x']) * float(self.system['celldm'][0]) * a['alat_change'])
    
    # Make
    self.make()    
    
    return a
    
    
  def nomalise_cell_parameters(self):
    self.system['celldm'][0] = str(float(self.system['celldm'][0]) * float(self.cell_parameters[1][0]))
    d = float(self.cell_parameters[1][0])
    for i in range(1,4):
      for j in range(0,3): 
        self.cell_parameters[i][j] = str(float(self.cell_parameters[i][j]) / d)
        

    
    
############################
#  Load From Output
############################
  
  def load_from_output(self, file_path):
    # Need to add a fail safe, and load atom coords
  
    # Load output file
    output_file = pwscf_output(file_path)
    alat, relaxed_cell = output_file.get_norm_relaxed()
    
    # Set alat and cell parameters
    self.set_alat(alat)
    self.set_cell_parameters(relaxed_cell)
    
 
############################
#  Load Atom Config
############################

  def load_config(self, type="FCC", size=1, alat=None, cp=None): 
    type = type.upper()
    result = {"CrystalAtoms": 0, "TotalAtoms": 0}    
    
    # SC
    if(type == "SC"):
      labels = []
      for row in self.atomic_species:
        labels.append(row[0])
      atoms, c_atoms, n_atoms = pwscf_standard.sc(labels,size) 
      self.atomic_positions = atoms
      self.system['nat'] = str(len(self.atomic_positions) - 1)
    
    # BCC
    if(type == "BCC"):
      labels = []
      for row in self.atomic_species:
        labels.append(row[0])
      atoms, c_atoms, n_atoms = pwscf_standard.bcc(labels,size) 
      self.atomic_positions = atoms
      self.system['nat'] = str(len(self.atomic_positions) - 1)
      
      
    # FCC
    if(type == "FCC"):
      labels = []
      for row in self.atomic_species:
        labels.append(row[0])
      atoms, c_atoms, n_atoms = pwscf_standard.fcc(labels,size) 
      self.atomic_positions = atoms
      self.system['nat'] = str(len(self.atomic_positions) - 1)
    
    # ISOLATED
    if(type == "ISOLATED"):
      labels = []
      for row in self.atomic_species:
        labels.append(row[0])
      atoms, c_atoms, n_atoms = pwscf_standard.isolated(labels)  
      self.atomic_positions = atoms
      self.system['nat'] = str(len(self.atomic_positions) - 1)      

    # ALAT
    if(alat != None):
      self.set_alat(alat)

    # CP
    if(cp != None):
      self.set_cp_arr(cp)
      
      
    # Misc
    if(type == "FCC_VARIED_DOUBLE"):
      labels = []
      for row in self.atomic_species:
        labels.append(row[0])
      atoms, c_atoms, n_atoms = pwscf_standard.fcc_varied_double(labels) 
      self.atomic_positions = atoms
      self.system['nat'] = str(len(self.atomic_positions) - 1)    
    
    # Make
    self.make()
    
    # Return
    return c_atoms, n_atoms
    
    
    
    
  def load_custom_config(self, coords, atoms=None):  
    atom_count = len(coords)
    self.system['nat'] = str(atom_count)   
    
    #for coord in coords:
  
############################
#  Vary Config
############################      
  
  def vary_atom(self, n, dx, dy, dz):
    n = 1 + n % (len(self.atomic_positions) - 1)
    self.atomic_positions[n][1] = str(float(self.atomic_positions[n][1]) + float(dx))
    self.atomic_positions[n][2] = str(float(self.atomic_positions[n][2]) + float(dy))
    self.atomic_positions[n][3] = str(float(self.atomic_positions[n][3]) + float(dz))
  

  def rand_vary(self, amount= 0.01, rand_seed=0):
    if(rand_seed == 1 and self.rand_seed_set == 0):
      self.rand_seed_set = 1
      self.rand.randomSeed()
  
    c = numpy.zeros((3,3))
    for i in range(1,4):
      for j in range(0,3): 
        c[i-1,j] = self.cell_parameters[i][j]
    c_inv = numpy.linalg.inv(c)

    for n in range(1, len(self.atomic_positions)):
      r = numpy.zeros((3))
      r[0] = (amount * self.rand.rng()) * (1.0 / float(self.system['celldm'][0]))
      r[1] = (amount * self.rand.rng()) * (1.0 / float(self.system['celldm'][0]))
      r[2] = (amount * self.rand.rng()) * (1.0 / float(self.system['celldm'][0]))
    
      r = numpy.matmul(c_inv, r)
      self.atomic_positions[n][1] = str(float(self.atomic_positions[n][1]) + r[0])
      self.atomic_positions[n][2] = str(float(self.atomic_positions[n][2]) + r[1])
      self.atomic_positions[n][3] = str(float(self.atomic_positions[n][3]) + r[2])
      
  def rand_vary_positions(self, vmin=0.0, vmax=0.0):
    if(not (vmin == 0.0 and vmax == 0.0)):  
      c = numpy.zeros((3,3))
      for i in range(1,4):
        for j in range(0,3): 
          c[i-1,j] = self.cell_parameters[i][j]
      c_inv = numpy.linalg.inv(c)

      for n in range(1, len(self.atomic_positions)):
        r = numpy.zeros((3))
        r[0] = (vmin + self.rand.rng() * (vmax - vmin)) * (1.0 / float(self.system['celldm'][0]))
        r[1] = (vmin + self.rand.rng() * (vmax - vmin)) * (1.0 / float(self.system['celldm'][0]))
        r[2] = (vmin + self.rand.rng() * (vmax - vmin)) * (1.0 / float(self.system['celldm'][0]))
    
        r = numpy.matmul(c_inv, r)
        self.atomic_positions[n][1] = str(float(self.atomic_positions[n][1]) + r[0])
        self.atomic_positions[n][2] = str(float(self.atomic_positions[n][2]) + r[1])
        self.atomic_positions[n][3] = str(float(self.atomic_positions[n][3]) + r[2])   

  def rand_vary_alat(self, vmin=0.0, vmax=0.0):
    if(not (vmin == 0.0 and vmax == 0.0)):
      alat = self.get_alat()
      f = 1.0 + vmin + random.uniform(0.0,1.0) * (vmax - vmin)
      alat = round(f * float(alat),8)
      self.set_alat(alat)

############################
#  Get
############################

  def get_path(self):
    if(self.file_name == None):
      file = "pwscf.in"
    else:
      file = self.file_name
    if(self.dir_name == None):  
      path = file
    else:
      path = self.dir_name + "/" + file
    return path

  def get_file_name(self):
    return self.file_name


  def get_cp_array(self):
    cp = numpy.zeros((3,3))
    for i in range(3):
      for j in range(3):
        cp[i,j] = float(self.cell_parameters[i+1][j])
    return cp    

  def get_data(self, make=False):
    if(make):
      self.make()
    return self.file_data[-1]
    
  def get_nat(self):  
    return int(self.system['nat'])

  def get_alat(self):
    return self.system['celldm'][0]

  def get_ecutwfc(self):
    return self.system['ecutwfc']
  def get_ecutrho(self):
    return self.system['ecutrho']
  def get_degauss(self):
    return self.system['degauss']
  def get_kpoints(self):
    return str(self.k_points[0]) + ' ' + str(self.k_points[1])


  def get_atomic_species(self):
    return self.atomic_species
    
    
  def get_atom_labels(self):
    l = []
    for li in self.atomic_species:
      l.append(li[0])
    return l
    
  def get_random_atom_label(self):
    l = []
    for li in self.atomic_species:
      l.append(li[0])
    r = random.randint(0, len(l)-1) 
    return l[r]


#################################
# Signature
#################################
    
  def signature(self):
    skip = ['outdir','prefix','wfcdir','pseudo_dir','max_seconds','disk_io']
  
    # CONTROL
    file = "&CONTROL \n"
    for key in sorted(self.control.keys()):
      read = True
      if(key in skip):
        read = False
        
      if(read):
        file += pwscf_input.make_line(key, self.control[key])
    file += "/ \n"    
    # SYSTEM
    file += "&SYSTEM \n"
    for key in sorted(self.system.keys()):
      file += pwscf_input.make_line(key, self.system[key]) 
    file += "/ \n"
    # ELECTRONS
    file += "&ELECTRONS \n"
    for key in sorted(self.electrons.keys()):
      value = self.electrons[key]
      if(value != None):
        file += key + " = " + value + ", \n"      
    file += "/ \n"
    # IONS
    file += "&IONS \n"
    for key in sorted(self.ions.keys()):
      value = self.ions[key]
      if(value != None):
        file += key + " = " + value + ", \n"      
    file += "/ \n"
    # CELL
    file += "&CELL \n"
    for key in sorted(self.cell.keys()):
      value = self.cell[key]
      if(value != None):
        file += key + " = " + value + ", \n"      
    file += "/ \n"
    # ATOMIC_SPECIES
    file += "ATOMIC_SPECIES \n"
    for species in self.atomic_species:      
      for field in species:
        file += str(field) + " "
      file += "\n"
    # ATOMIC_POSITIONS
    header = 0
    for position in self.atomic_positions:      
      if(header == 0):
        file += "ATOMIC_POSITIONS "
        file += position + "\n"
        header = 1
      elif(header == 1):  
        for field in position:
          file += str(field) + "   "
        file += "\n"
    # K_POINTS
    file += "K_POINTS " + self.k_points[0]
    file += "\n"
    for i in range(1,len(self.k_points)):
      for point in self.k_points[i]:
        file += point + " "
      file += "\n"    
    # K_POINTS
    file += "CELL_PARAMETERS " + self.cell_parameters[0]
    file += "\n"
    for i in range(1,len(self.cell_parameters)):
      for point in self.cell_parameters[i]:
        file += point + " "
      file += "\n"
    
    # String being hashed must be converted to utf-8 encoding
    input_string = file.encode('utf-8')
    # Make hash object
    my_hash = hashlib.sha512()
    # Update
    my_hash.update(input_string)
    # Return hash
    return my_hash.hexdigest()

#################################
# Interactive
#################################

  def menu(self):
    while(True):
      choice = self.print_menu().upper()
      print(choice)
      if(choice == "X"):
        exit()
      elif(choice == "1"):
        self.i_load()
      elif(choice == "2"):
        self.i_display()


  def print_menu(self):
    pwscf_input.header("Menu")
    print("1. Load File")
    print("2. Display File")
    print("X. Exit")
    return input("Choice: ")


  def i_load(self):
    pwscf_input.header("Load Input File")
    file_name = input("Enter file name: ")
    self.load(file_name)
    input()


  def i_display(self):
    self.make()
    pwscf_input.header("Display File")
    print(self.file)
    input()



#################################
# Help
#################################

  def help(self):
    print("HELP")

#################################
# Static Methods
#################################

  @staticmethod
  def is_pwscf(file_path): 
    file_size = os.path.getsize(file_path)
    if(file_size > 500000):
      return False

    fh = open(file_path, 'r')
    counter = 0
    for line in fh:
      line = line.strip().lower()
      if(line[0:8] == "&control"):
        counter = counter + 1
      if(line[0:7] == "&system"):
        counter = counter + 1
      if(line[0:10] == "&electrons"):
        counter = counter + 1
      if(line[0:5] == "&ions"):
        counter = counter + 1
      if(line[0:5] == "&cell"):
        counter = counter + 1
      if(line[0:14] == "&atomic_species"):
        counter = counter + 1
      if(line[0:16] == "&atomic_positions"):
        counter = counter + 1
      if(line[0:6] == "outdir"):
        counter = counter + 1
      if(line[0:10] == "pseudo_dir"):
        counter = counter + 1
    if(counter > 5):
      return True
    return False

  @staticmethod
  def remove_spaces(input_string):
    return input_string.replace(" ", "")
 
  @staticmethod
  def fields(input_string):
    input_string = input_string.strip()
    output_string = ""
    last = None
    for character in input_string:
      if(character != " " or (character == " " and last != " ")):
        output_string += character
    return output_string.split(" ")
    
  @staticmethod
  def check_keyword(line, keyword):
    if(line.upper()[0:len(keyword)] == keyword.upper()):
      return True
    return False


  @staticmethod
  def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


  @staticmethod
  def header(sub_title=""):
    pwscf_input.clear_screen()
    print("==========================================================")
    print("                    PWscf Input Editor                    ")
    print("==========================================================")
    print()
    print(sub_title)
    print()
    print()
    print()

  @staticmethod
  def process_keyword(str_in):
    str_in = str_in.lower().strip()
    str_in = pwscf_input.remove_spaces(str_in)
    id = None
    keyword = ""
    flag = 0
    for character in str_in:
      if(character == "("):
        id = ""
        flag = 1
      elif(character == ")"):
        flag = 2
      elif(flag == 0):
        keyword += character
      elif(flag == 1):
        id = id + character
    if(id != None):
      try:
        id = int(id)
      except:
        id = None
    return keyword, id  

  @staticmethod
  def add_keyword(keywords, keyword, id, value):
    if(id == None):
      added = False
      for i in range(len(keywords)):
        if(keywords[i][0] == keyword):
          added = True
          keywords[i][1] = keyword
      if(added == False):
        keywords.append([keyword, value])
    else:   
      n = None
      for i in range(len(keywords)):
        if(keywords[i][0] == keyword):
          n = i
          break
      if(n == None):    
        keywords.append([keyword,[None]])
        n = len(keywords) - 1
        
      while(len(keywords[n][1]) < id):
        keywords[n][1].append(None)

      keywords[n][1][id-1] = value  



  @staticmethod
  def make_line(key, value):
    output = ""
    if(value != None):
       if(isinstance(value, (list,))):
         for i in range(len(value)):
           if(value[i] != None):
             output += str(key) + "(" + str(i+1) + ") = " + str(value[i]) + ", \n"                
       else:
         output += str(key) + " = " + str(value) + ", \n"   
    return output    

  @staticmethod
  def coord_format(float_in):
    pad = "              "
    value = str(round(float_in, 6)).strip()
    return value
    
  @staticmethod
  def label_format(label):  
    pad = "              "
    label = label.strip()
    return label
    
  @staticmethod
  def clean(str_in):  
    str_out = ""
    l = len(str_in)
    for i in range(l):
      # Last, Next, This
      if(i == 0):
        last = None
      else:
        last = str_in[i-1]
      if(i < (l-1)):
        next = str_in[i+1]
      else:  
        next = None
      char = str_in[i]
    
      # Check
      ok = True
      if(last == " " and char == " "):
        ok = False
      elif(last == "\n" and char == "\n"):
        ok = False
      elif(last == "\n" and char == " "):
        ok = False
      elif(char == " " and next == "\n"):
        ok = False
      elif(last == "=" and char == " "):
        ok = False
      elif(char == " " and next == "="):
        ok = False
        
      # Add to string  
      if(ok):
        str_out += char
    return str_out    
    
    
  @staticmethod
  def rand_string(len_in=16):      
    output = ""
    char_set = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOQRSTUVWXYZ"
    for i in range(len_in):
      r = random.randint(0,len(char_set)-1)
      output += char_set[r]
    return output
    
        #data = re.sub(r'\s\s+', ' ', data)
    #data = re.sub(r'\s=\s', '=', data)

class pwscf_standard:

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
    
    
    
  @staticmethod
  def unvoight(cp_in):
    cp_out = [[cp_in[0], cp_in[5], cp_in[4]] , [cp_in[3], cp_in[1], cp_in[3]] , [cp_in[4], cp_in[5], cp_in[2]]]
    return cp_out




  
