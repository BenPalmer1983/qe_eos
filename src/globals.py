##########
# GLOBALS


class g: 
  
  args = []
  
  dirs = {
         'wd': 'wd',
         }
  
  sub_dirs = {
         'log': 'log',  
         'output': 'output',   
         'results': 'results',   
         'plots': 'plots',  
         'input': 'input', 
         'templates': 'templates', 
         'relax': 'relax', 
         'eos': 'eos', 
         'ec': 'ec', 
         'data': 'data', 
         }
  
  
  times = {
          'start' : 0.0,
          'end' : 0.0,
          'duration' : 0.0,
          }
            
  inp_raw = {}     
       
  inp = {}
       
       
  data = {
         'size': 1,
         'atoms_in_crystal': 0,
         'atoms_in_crystal_expanded': 0,
         }
       
  relaxed = {}  
  eos = {} 
  ec = {}
       
       
  #d = {
  
  log_fh = None
  
  
