from load_template import load_template
from pwscf_exec import pwscf_exec
from pwscf_input import pwscf_input
from pwscf_output import pwscf_output
from units import units
from calc_relax import calc_relax
from calc_eos import calc_eos
from calc_ec import calc_ec
from process_results import process_results
from save_results import save_results
from eos_fit import eos_fit
from save_load import save_load
from plot import plot

class qeeos:

  run_list = {'relax': False, 'eos': False, 'ec': False, 'process_results': False, 'save_results': False, 'plot': False,}

  def run():
    print("QE Equation of State")
    
    # LOAD DEFAULTS
    qeeos.load_input_defaults()
    
    # LOAD TEMPLATE
    load_template.run()
    
    # Create Dictionaries
    g.eos = {'complete': False}
    g.ec = {'complete': False}
    g.eos_results = {'complete': False}
    g.ec_results = {'complete': False}
    
    
    # Type of run
    if(len(sys.argv)<3 or (len(sys.argv) == 3 and sys.argv[2].strip().lower() == 'all')):
      qeeos.run_all()
    elif(len(sys.argv) == 3 and sys.argv[2].strip().lower() == 'plot'):
      qeeos.run_plot()
    
    # Save data dictionary
    save_load.save(g.data, g.dirs['data'] + '/' + 'data.dat')  
    
    
  def run_all():
    qeeos.relax()
    qeeos.eos()
    qeeos.ec()
    qeeos.process_results()
    qeeos.save_results()
    qeeos.plot()
    
    
  def run_plot():
    # Try to load needed files
    try:
      g.relaxed = save_load.load(g.dirs['data'] + '/' + 'relax.dat')  
    except:
      pass
    try:
      g.eos = save_load.load(g.dirs['data'] + '/' + 'eos.dat')  
    except:
      pass
    try:
      g.ec = save_load.load(g.dirs['data'] + '/' + 'ec.dat')  
    except:
      pass
      
    # Process results
    qeeos.process_results()
    qeeos.plot()
    
    
    
  def relax():
    if(not qeeos.run_list['relax']):
      qeeos.run_list['relax'] = True
      print("Relax")
      calc_relax.run()
      
  def eos():
    if(not qeeos.run_list['eos']):
      qeeos.run_list['eos'] = True
      print("EoS")
      calc_eos.run()
      
  def ec():
    if(not qeeos.run_list['ec']):
      qeeos.run_list['ec'] = True
      print("EC")
      calc_ec.run()
    
  def process_results():
    if(not qeeos.run_list['process_results']):
      qeeos.run_list['process_results'] = True
      print("PROCESS RESULTS")
      process_results.run()
      
    
  def save_results():  
    if(not qeeos.run_list['save_results']):    
      print("SAVE RESULTS")
      save_results.run()
      
  def plot():
    if(not qeeos.run_list['plot']):     
      print("PLOT")
      plot.run()
    
  def load_input_defaults():
    g.inp = {}
    
    g.inp['pwscf_template'] = {
                              'file': 'input.in',
                              }
    g.inp['settings'] = {
                         'pwscf_run': True,
                         'ecutwfc': 50,
                         'ecutrho': 200,
                         'kpointstype': 'automatic',
                         'kpoints': '5 5 5 1 1 1',
                         'degauss': 0.04,
                        }
    g.inp['config'] = {
                         'structure': None,
                         'size': 1,
                         'alat': 4.00,
                         'alat_units': 'angs',
                        }
    g.inp['ec'] = {
                         'run': True,
                         'points': 6,
                         'strain': 0.005,
                        }
    g.inp['eos'] = {
                         'run': True,
                         'points': 6,
                         'strain': 0.005,
                        }
                        
    for i in g.inp.keys():
      for j in g.inp[i].keys():
        try:
          g.inp[i][j] = g.inp_raw[i][j]
        except:
          pass
        
    
      
      
    
    