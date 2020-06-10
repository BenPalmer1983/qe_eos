import matplotlib.pyplot as plt

class plot:


  @staticmethod
  def run(): 
    if(g.eos_results['complete']):
      plot.plot_eos()
    if(g.ec_results['complete']):
      plot.plot_ec()
  
  @staticmethod
  def plot_eos():
  
    plt.clf()
    
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    fig, axs = plt.subplots(1, 1, figsize=(12,9))
    fig.tight_layout(pad=5.0)
    fig.suptitle('Equation of State')    
    
    plt.plot(g.eos_results['data'][:,1], g.eos_results['data'][:,2], color='k',  marker="x", ls='')
    plt.plot(g.eos_results['data_fit'][:,0], g.eos_results['data_fit'][:,1], color='k', ls='solid')
    plt.savefig(g.dirs['plots'] + '/' + 'eos.eps')
    
  @staticmethod
  def plot_ec():
  
    plt.clf()
    
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='x-small')
    plt.rc('ytick', labelsize='x-small')

    fig, axs = plt.subplots(1, 1, figsize=(12,9))
    fig.tight_layout(pad=5.0)
    fig.suptitle('Equation of State')    
    
    plt.plot(g.eos_results['data'][:,1], g.eos_results['data'][:,2], color='k',  marker="x", ls='')
    plt.plot(g.eos_results['data_fit'][:,0], g.eos_results['data_fit'][:,1], color='k', ls='solid')
    plt.savefig(g.dirs['plots'] + '/' + 'eos.eps')
    
    plt.clf()
    
    plt.rc('font', family='serif')
    plt.rc('xtick', labelsize='xx-small')
    plt.rc('ytick', labelsize='xx-small')

    fig, axs = plt.subplots(3, 3, figsize=(12,9))
    fig.tight_layout(pad=5.0)
    fig.suptitle('Elastic Constant Curves')    
    
    for dn in range(9):
      
      xa = g.ec_results['data_' + str(dn)][:,0]
      ya = g.ec_results['data_' + str(dn)][:,2]
      xb = g.ec_results['data_fit_' + str(dn)][:,0]
      yb = g.ec_results['data_fit_' + str(dn)][:,1]
      
      axs[int(numpy.floor(dn/3)), dn % 3].plot(xa[:], ya[:], color='k',  marker="x", ls='')
      axs[int(numpy.floor(dn/3)), dn % 3].plot(xb[:], yb[:], color='k', ls='solid')
      axs[int(numpy.floor(dn/3)), dn % 3].set_title('Distortion D' + str(dn + 1))
      axs[int(numpy.floor(dn/3)), dn % 3].set_xlabel('Strain / Alat')
      axs[int(numpy.floor(dn/3)), dn % 3].set_ylabel('Energy / Ry')
    
    plt.savefig(g.dirs['plots'] + '/' + 'ec.eps')
    
