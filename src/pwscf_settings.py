#################################
# Load settings from environment
#################################

import os

class pwscf_settings:
 
  @staticmethod
  def load():
    # Default Settings
        
    s = {
    "omp_num_threads":  1,
    "proc_count":  1,
    "pwscf_scratch": '',
    "pwscf_pp": '',
    "pwscf_cache": '',
    "pwscf_bin": '',
    }


    s['omp_num_threads'] = os.environ['OMP_NUM_THREADS']
    s['proc_count'] = os.environ['PROC_COUNT']
    s['pwscf_scratch'] = os.environ['PWSCF_SCRATCH']
    s['pwscf_pp'] = os.environ['PWSCF_PP']
    s['pwscf_cache'] = os.environ['PWSCF_CACHE']
    s['pwscf_bin'] = os.environ['PWSCF_BIN']


    return s
