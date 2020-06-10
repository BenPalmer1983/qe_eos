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
import hashlib 
from shutil import copyfile


from pwscf_input import pwscf_input
from pwscf_output import pwscf_output
from pwscf_settings import pwscf_settings

############################
#  pwscf_input
############################

class pwscf_exec:

  @staticmethod
  def run():
    print("Running")

    # Get current working directory
    cwd = os.getcwd()  

    # Files list
    files = []

    # Read file list
    files = pwscf_exec.make_file_list(cwd, files)

    # Run
    out = pwscf_exec.execute(files)
   

  @staticmethod
  def make_file_list(path, files):
    for file_name in os.listdir(path):
      full_path = path + "/" + file_name
      if(os.path.isfile(full_path)):
        if(pwscf_input.is_pwscf(full_path)):
          print(full_path)
          files.append(full_path)
      if(os.path.isdir(full_path)):
        files = pwscf_exec.make_file_list(full_path, files)
    return files


  @staticmethod
  def execute(files_in, log=None, set_dirs=True, allow_cache=True):
    files = []
    if type(files_in) is str:
      files.append(files_in)
    elif type(files_in) is list:
      files = files_in
    else:
      return log
      
    # Prepare run list  
    run_list = pwscf_exec.pre_run(files_in, set_dirs)
  
    # Run
    log, list_out, run_list = pwscf_exec.run_pwscf_list(run_list, log, allow_cache, True)

    # Save
    pwscf_exec.save_run_list(run_list)
    
    # Return log
    return log, list_out, run_list

  @staticmethod
  def pre_run(files_in, set_dirs):
    # Create run list
    run_list = []
    
    # Get environment settings
    s = pwscf_settings.load()    
    cache = None
    if('pwscf_cache' in s):
      cache = s['pwscf_cache']
    pwscf_scratch = None
    if('pwscf_scratch' in s):
      pwscf_scratch = s['pwscf_scratch']
    pwscf_pp = None
    if('pwscf_cache' in s):
      pwscf_pp = s['pwscf_pp']
     
    for file_path in files_in:  
      file_name = pwscf_exec.file_name_only(file_path)
      path = pwscf_exec.file_path_only(file_path)
    
      pw_in = pwscf_input()
      pw_in.load(file_path)
      pw_in.set_dirs(pwscf_scratch, pwscf_pp)
      pw_in.save()

      
      sig = pw_in.signature()
      cache_file = None
      
      use_cache = False
      if(cache is not None):
        cache_file_in = cache + "/" + sig + ".in"
        cache_file_out = cache + "/" + sig + ".out"
        
        use_cache = True
        if (not os.path.exists(cache_file_in)):
          use_cache = False
        if (not os.path.exists(cache_file_out)):
          use_cache = False
      
      cmd = 'mpirun -n ' + s['proc_count'] + ' ' + s['pwscf_bin'] + ' -i ' + file_path + ' > ' + path + '/' + file_name + '.out'
      
      run_list.append({
        'file_name': file_name, 
        'path': path, 
        'file_path_in': file_path, 
        'file_path_out': path + '/' + file_name + '.out', 
        'hash': sig,
        'use_cache': use_cache,
        'cache_in': cache_file_in,
        'cache_out': cache_file_out,
        'cmd': cmd,
        'cache_used': False,
        })
      
    # return
    return run_list
    
    
    
  @staticmethod
  def run_pwscf_list(run_list, log, allow_cache, run=True):
    # Get environment settings
    s = pwscf_settings.load()    
    cache = None
    if('pwscf_cache' in s):
      cache = s['pwscf_cache']
      
    list_out = []
    for i in range(len(run_list)):
      run_file = run_list[i]
    
      # Use cache?
      use_cache = run_file['use_cache']
    
      # Recheck for cache      
      if(cache is not None):
        if(os.path.exists(run_file['cache_in']) and os.path.exists(run_file['cache_out'])):
          use_cache = True        
      
      if(use_cache and allow_cache):
        run_list[i]['cache_used'] = True
        copyfile(run_file['cache_out'], run_file['file_path_out'])
        list_out.append({"file": run_file['file_path_out'], "status": "complete",})
        if(log is not None):
          log.add("##START PWSCF##")
          log.add("PWscf Run")
          log.add(run_file['cmd'])
          log.add("Cache used")
          log.add("##END PWSCF##")
          log.add("")
      else:  
      
        # Run
        if(run):
          os.system(run_file['cmd'])
          pwo = pwscf_output(run_file['file_path_out'])
          if(pwo.get_job_done()):
            copyfile(run_file['file_path_in'], run_file['cache_in'])
            copyfile(run_file['file_path_out'], run_file['cache_out'])
            list_out.append({"file": run_file['file_path_out'], "status": "complete",})
          else:
            list_out.append({"file": run_file['file_path_out'], "status": "failed",})          
        
          if(log is not None):
            log.add("##START PWSCF##")
            log.add("PWscf Run")
            log.add(run_file['cmd'])
            if(pwo.get_job_done()):
              log.add("Run successful")
            log.add("##END PWSCF##")
            log.add("")

    return log, list_out, run_list
      
  @staticmethod
  def file_name_only(file_path):
    l1 = file_path.split("/")    
    l2 = l1[-1].split(".")
    file_name = l1[-1][:-(len(l2)+1)]
    return file_name
    
  @staticmethod
  def file_path_only(file_path):
    l1 = file_path.split("/")   
    path = file_path[:-(len(l1[-1])+1)]
    return path

  @staticmethod
  def save_run_list(run_list):  
    # Save Run List
    cwd = os.getcwd() 

    fh = open(cwd + "/run_list.txt", "w")

    for r in run_list:
      field = "File Name:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['file_name'] + "\n")
      field = "Path:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['path'] + "\n")
      field = "File In:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['file_path_in'] + "\n")
      field = "File Out:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['file_path_out'] + "\n")
      field = "Hash:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['hash'] + "\n")

      field = "Use Cache?:"
      while(len(field)<32):
        field = field + " "
      if(r['use_cache']):
        fh.write(field + "True\n")
      else:
        fh.write(field + "False\n")

      field = "Cache Used:"
      while(len(field)<32):
        field = field + " "
      if(r['cache_used']):
        fh.write(field + "True\n")
      else:
        fh.write(field + "False\n")

      field = "Cache In:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['cache_in'] + "\n")

      field = "Cache Out:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['cache_out'] + "\n")

      field = "CMD:"
      while(len(field)<32):
        field = field + " "
      fh.write(field + r['cmd'] + "\n")
      fh.write("\n")
      fh.write("\n")


    fh.close()


      
    
